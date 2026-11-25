import express from 'express';
import { createServer } from 'node:http';
import { networkInterfaces } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { existsSync, readFileSync, writeFileSync, renameSync } from 'node:fs';
import { Server, type Socket } from 'socket.io';
import type { Ack, Condition, Pawn, Session } from '../shared/types';
import { CASES, DEFAULT_CASE } from './cases';
import { Game, GameError, newGameCode, normalizeGameCode } from './game';

const PORT = Number(process.env.PORT) || 3001;
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DIST = join(ROOT, 'dist');

const app = express();
const http = createServer(app);
const io = new Server(http, { cors: { origin: true } });
const games = new Map<string, Game>();

// Games are kept in memory and saved to a JSON file, so a restart doesn't kill a running game.
const SAVE = process.env.SAVE_FILE || join(ROOT, '.games.json');
try {
  if (existsSync(SAVE)) {
    for (const d of JSON.parse(readFileSync(SAVE, 'utf8'))) {
      try { games.set(d.code, Game.fromJSON(d)); } catch { /* case removed: skip */ }
    }
    console.log(`Restored ${games.size} game(s) from ${SAVE}`);
  }
} catch (e) {
  console.warn('Could not read saved games:', (e as Error).message);
}
let saveTimer: NodeJS.Timeout | undefined;
function scheduleSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try {
      writeFileSync(`${SAVE}.tmp`, JSON.stringify([...games.values()]));
      renameSync(`${SAVE}.tmp`, SAVE);
    } catch (e) {
      console.warn('Could not save games:', (e as Error).message);
    }
  }, 300);
}

app.get('/api/info', (_req, res) => {
  const ips = Object.values(networkInterfaces())
    .flat()
    .filter((i) => i && i.family === 'IPv4' && !i.internal)
    .map((i) => i!.address);
  res.json({ lanIps: ips, cases: Object.values(CASES).map((c) => ({ id: c.id, title: c.title })) });
});
app.get('/api/health', (_req, res) => res.json({ ok: true, games: games.size }));

if (existsSync(DIST)) {
  app.use(express.static(DIST));
  app.get('*', (_req, res) => res.sendFile(join(DIST, 'index.html')));
}

// ------------------------------------------------------------------ sockets
interface Bound { code: string; playerId: string }
const bound = new Map<string, Bound>();

function broadcast(game: Game) {
  game.touched = Date.now();
  scheduleSave();
  for (const p of game.players.values()) {
    const v = game.view(p.id);
    for (const sid of p.sockets) io.to(sid).emit('view', v);
  }
}

function bind(socket: Socket, game: Game, playerId: string) {
  const prev = bound.get(socket.id);
  if (prev) games.get(prev.code)?.players.get(prev.playerId)?.sockets.delete(socket.id);
  bound.set(socket.id, { code: game.code, playerId });
  game.player(playerId).sockets.add(socket.id);
}

function ctx(socket: Socket) {
  const b = bound.get(socket.id);
  if (!b) throw new GameError('You are not in a game.');
  const game = games.get(b.code);
  if (!game) throw new GameError('This game does not exist any more.');
  return { game, me: b.playerId };
}

type Handler = (...args: any[]) => unknown;
function on(socket: Socket, event: string, fn: Handler) {
  socket.on(event, (...args: unknown[]) => {
    const cb = typeof args[args.length - 1] === 'function' ? (args.pop() as (a: Ack) => void) : () => {};
    try {
      cb({ ok: true, data: fn(...args) });
    } catch (e) {
      const msg = e instanceof GameError ? e.message : 'Something went wrong.';
      if (!(e instanceof GameError)) console.error(e);
      cb({ ok: false, error: msg });
    }
  });
}

io.on('connection', (socket) => {
  on(socket, 'game:create', (p: { name: string; caseId?: string }) => {
    const code = newGameCode((c) => games.has(c));
    const game = new Game(code, p?.caseId && CASES[p.caseId] ? p.caseId : DEFAULT_CASE);
    const pl = game.addPlayer(p?.name);
    games.set(code, game);
    bind(socket, game, pl.id);
    broadcast(game);
    return { code, playerId: pl.id, secret: pl.secret } satisfies Session;
  });

  on(socket, 'game:join', (p: { code: string; name: string }) => {
    const code = normalizeGameCode(p?.code);
    const game = games.get(code);
    if (!game) throw new GameError(`No game with the code ${code || '...'}. Check the code with the host.`);
    const pl = game.addPlayer(p?.name);
    bind(socket, game, pl.id);
    broadcast(game);
    return { code, playerId: pl.id, secret: pl.secret } satisfies Session;
  });

  on(socket, 'game:resume', (s: Session) => {
    const game = games.get(normalizeGameCode(s?.code));
    if (!game) throw new GameError('This game does not exist any more.');
    game.auth(s.playerId, s.secret);
    bind(socket, game, s.playerId);
    broadcast(game);
    return true;
  });

  on(socket, 'game:leave', () => {
    const { game, me } = ctx(socket);
    if (game.phase === 'lobby') game.removePlayer(me, me);
    else game.player(me).sockets.delete(socket.id);
    bound.delete(socket.id);
    if (game.players.size === 0) {
      games.delete(game.code);
      scheduleSave();
    } else broadcast(game);
    return true;
  });

  const act = (event: string, fn: (game: Game, me: string, ...a: any[]) => unknown) =>
    on(socket, event, (...a: unknown[]) => {
      const { game, me } = ctx(socket);
      const out = fn(game, me, ...a);
      broadcast(game);
      return out;
    });

  act('lobby:pawn', (g, me, pawn: Pawn) => g.pickPawn(me, pawn));
  act('lobby:first', (g, me, id: string) => g.setFirst(me, id));
  act('lobby:case', (g, me, id: string) => g.setCase(me, id));
  act('lobby:kick', (g, me, id: string) => g.removePlayer(me, id));
  act('game:start', (g, me) => g.start(me));
  act('card:scan', (g, me, code: string) => g.scan(me, code));
  act('query:run', (g, me, conds: Condition[]) => g.query(me, conds));
  act('turn:end', (g, me) => g.endTurn(me));
  act('round:end', (g, me) => g.endRound(me));
  act('token:recharge', (g, me) => g.recharge(me));
  act('accuse', (g, me, id: string) => g.accuse(me, id));
  act('game:abandon', (g, me) => g.abandon(me));

  socket.on('disconnect', () => {
    const b = bound.get(socket.id);
    bound.delete(socket.id);
    const game = b && games.get(b.code);
    if (game) {
      game.players.get(b.playerId)?.sockets.delete(socket.id);
      broadcast(game);
    }
  });
});

// Forget games nobody touched for 8 hours.
setInterval(() => {
  const limit = Date.now() - 8 * 3600_000;
  for (const [code, g] of games) if (g.touched < limit) games.delete(code);
}, 600_000).unref();

http.listen(PORT, () => {
  console.log(`The Last Query server on http://localhost:${PORT}${existsSync(DIST) ? ' (serving dist/)' : ''}`);
});
