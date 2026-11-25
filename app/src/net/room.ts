/**
 * The host's phone runs the game (src/engine). Guests send actions and receive their own view.
 * Topics: <ROOT><code>/up (guests -> host), /all (host -> everyone),
 *         /to/<device> (host -> one phone), /host (retained: this code is taken).
 */
import type { Ack, Pawn, Session, View, Condition } from '../../shared/types';
import { CASES, DEFAULT_CASE } from '../engine/cases';
import { Game, GameError, newGameCode, normalizeGameCode } from '../engine/game';
import { link, rid, ROOT, safe, type Link } from './link';

const PING = 4000;
const TIMEOUT = 13000;
const REPLY_TIMEOUT = 12000;

export type NetStatus = 'connecting' | 'online' | 'offline' | 'host-away';

export interface Handlers {
  view: (v: View) => void;
  status: (s: NetStatus) => void;
  closed: (reason: string) => void;
}

const base = (code: string) => `${ROOT}${code.toLowerCase()}/`;
const hostKey = (code: string) => `tlq.host.${code}`;

/** In-game actions, same for the host's own taps and for guests' messages. */
function dispatch(g: Game, me: string, event: string, args: any[]): unknown {
  switch (event) {
    case 'lobby:pawn': return g.pickPawn(me, args[0] as Pawn);
    case 'lobby:first': return g.setFirst(me, String(args[0]));
    case 'lobby:case': return g.setCase(me, String(args[0]));
    case 'lobby:kick': return g.removePlayer(me, String(args[0]));
    case 'game:start': return g.start(me);
    case 'card:scan': return g.scan(me, String(args[0] ?? ''));
    case 'query:run': return g.query(me, args[0] as Condition[]);
    case 'turn:end': return g.endTurn(me);
    case 'round:end': return g.endRound(me);
    case 'token:recharge': return g.recharge(me);
    case 'accuse': return g.accuse(me, String(args[0]));
    case 'game:abandon': return g.abandon(me);
    default: throw new GameError('Unknown action.');
  }
}

function errMsg(e: unknown) {
  if (e instanceof GameError) return e.message;
  console.error(e);
  return 'Something went wrong.';
}

// =================================================================== host
export class HostRoom {
  game: Game;
  myId = '';
  private L: Link | null = null;
  private devs = new Map<string, { pid: string | null; seen: number }>();
  private timer: number | undefined;
  private dead = false;
  private wasUp = false;
  /** Answers already sent, by request id: a resent request is answered again, never run twice. */
  private answered = new Map<string, Ack>();

  constructor(game: Game, private h: Handlers) {
    this.game = game;
  }

  /** Claims the code on the brokers. Resolves false if another host already uses it. */
  open(fresh: boolean): Promise<boolean> {
    const b = base(this.game.code);
    const me = rid();
    return new Promise((resolve) => {
      let decided = false;
      let taken = false;
      let pending = false;
      this.L = link(
        [`${b}up`, `${b}host`],
        (topic, m, retained) => {
          if (topic === `${b}host`) {
            if (fresh && !decided && retained && m.me !== me && Date.now() - (m.at || 0) < 12 * 3600e3) taken = true;
            return;
          }
          this.onUp(m);
        },
        () => {
          if (this.dead || !this.L) return;
          const up = this.L.connected();
          if (up && !decided && !pending) {
            pending = true;
            setTimeout(() => {
              decided = true;
              if (taken) {
                this.close(false);
                return resolve(false);
              }
              this.L!.pub(`${b}host`, { me, at: Date.now() }, { retain: true });
              this.h.status('online');
              resolve(true);
            }, fresh ? 1500 : 0);
          } else if (decided && up !== this.wasUp) this.h.status(up ? 'online' : 'offline');
          this.wasUp = up;
        },
      );
      this.h.status('connecting');
      this.timer = window.setInterval(() => this.tick(), PING);
    });
  }

  private tick() {
    if (this.dead || !this.L) return;
    if (!this.L.connected()) return this.L.wake();
    this.L.pub(`${base(this.game.code)}all`, { t: 'ping' }, { qos: 0 });
    if (this.refreshPresence()) this.push();
  }

  /** Mirrors who is online into game.players[].sockets. Returns true if something changed. */
  private refreshPresence(): boolean {
    const now = Date.now();
    let changed = false;
    for (const p of this.game.players.values()) {
      const online = new Set<string>();
      if (p.id === this.myId) online.add('host');
      this.devs.forEach((d, dev) => d.pid === p.id && now - d.seen <= TIMEOUT && online.add(dev));
      if (online.size !== p.sockets.size || [...online].some((x) => !p.sockets.has(x))) {
        p.sockets = online;
        changed = true;
      }
    }
    return changed;
  }

  private onUp(m: any) {
    const dev = m.dev && safe(m.dev);
    if (!dev) return;
    const d = this.devs.get(dev) ?? { pid: null, seen: 0 };
    const wasAway = Date.now() - d.seen > TIMEOUT;
    d.seen = Date.now();
    this.devs.set(dev, d);
    if (m.t === 'hello' && d.pid) this.sendView(dev, d.pid);
    if (m.t === 'req') {
      const id = String(m.id);
      let res = this.answered.get(id);
      if (!res) {
        res = this.handleGuest(dev, String(m.event), Array.isArray(m.args) ? m.args : []);
        this.answered.set(id, res);
        if (this.answered.size > 200) this.answered.delete(this.answered.keys().next().value!);
      }
      this.L?.pub(`${base(this.game.code)}to/${dev}`, { t: 'ack', id: m.id, res });
    }
    if (wasAway && this.refreshPresence()) this.push();
  }

  private handleGuest(dev: string, event: string, args: any[]): Ack {
    const g = this.game;
    const d = this.devs.get(dev)!;
    try {
      let data: unknown;
      if (event === 'game:join') {
        const p = g.addPlayer(args[0]?.name);
        d.pid = p.id;
        data = { code: g.code, playerId: p.id, secret: p.secret } satisfies Session;
      } else if (event === 'game:resume') {
        const p = g.auth(String(args[0]?.playerId), String(args[0]?.secret));
        d.pid = p.id;
        data = true;
      } else if (event === 'game:leave') {
        if (d.pid && g.phase === 'lobby') g.removePlayer(d.pid, d.pid);
        d.pid = null;
        data = true;
      } else {
        if (!d.pid || !g.players.has(d.pid)) throw new GameError('You are not in this game any more.');
        data = dispatch(g, d.pid, event, args);
      }
      this.refreshPresence();
      this.changed();
      return { ok: true, data };
    } catch (e) {
      return { ok: false, error: errMsg(e) };
    }
  }

  /** The host's own taps. */
  local(event: string, args: any[]): unknown {
    if (event === 'game:leave') {
      this.close(true);
      return true;
    }
    const before = new Set(this.game.players.keys());
    const out = dispatch(this.game, this.myId, event, args);
    // someone kicked: tell their phone
    for (const id of before) {
      if (this.game.players.has(id)) continue;
      this.devs.forEach((d, dev) => {
        if (d.pid !== id) return;
        d.pid = null;
        this.L?.pub(`${base(this.game.code)}to/${dev}`, { t: 'closed', reason: 'The host removed you from the game.' });
      });
    }
    this.changed();
    return out;
  }

  changed() {
    this.game.touched = Date.now();
    try {
      localStorage.setItem(hostKey(this.game.code), JSON.stringify(this.game));
    } catch {
      /* storage full or blocked: the game still runs */
    }
    this.push();
  }

  private push() {
    if (this.dead) return;
    if (this.game.players.has(this.myId)) this.h.view(this.game.view(this.myId));
    this.devs.forEach((d, dev) => d.pid && this.sendView(dev, d.pid));
  }

  private sendView(dev: string, pid: string) {
    if (!this.game.players.has(pid)) return;
    this.L?.pub(`${base(this.game.code)}to/${dev}`, { t: 'view', view: this.game.view(pid) });
  }

  wake() {
    this.L?.wake();
  }

  close(announce: boolean) {
    if (announce) {
      this.L?.pub(`${base(this.game.code)}all`, { t: 'closed', reason: 'The host closed the game.' });
      this.L?.pub(`${base(this.game.code)}host`, {}, { retain: true });
      try {
        localStorage.removeItem(hostKey(this.game.code));
      } catch {
        /* ignore */
      }
    }
    this.dead = true;
    clearInterval(this.timer);
    const L = this.L;
    this.L = null;
    // let the last messages leave before closing the sockets
    setTimeout(() => L?.close(), announce ? 800 : 0);
  }
}

// =================================================================== guest
export class GuestRoom {
  private L: Link;
  private waiting = new Map<string, (a: Ack) => void>();
  private timer: number;
  private seen = 0;
  private open = false;
  private helloAt = 0;
  private fails = 0;
  private dead = false;

  constructor(public code: string, public dev: string, private h: Handlers) {
    const b = base(code);
    this.L = link(
      [`${b}all`, `${b}to/${safe(dev)}`],
      (_topic, m) => {
        if (this.dead) return;
        this.seen = Date.now();
        this.fails = 0;
        if (!this.open) {
          this.open = true;
          this.h.status('online');
        }
        if (m.t === 'ack') this.waiting.get(m.id)?.(m.res);
        else if (m.t === 'view') this.h.view(m.view);
        else if (m.t === 'closed') {
          this.close();
          this.h.closed(m.reason || 'The game is over.');
        }
      },
      () => {
        if (this.dead) return;
        if (this.L.connected()) this.hello();
        else if (this.open) {
          this.open = false;
          this.h.status('offline');
        }
      },
    );
    this.h.status('connecting');
    this.timer = window.setInterval(() => this.tick(), PING);
  }

  connected() {
    return this.L.connected();
  }

  private hello() {
    if (!this.L.connected()) return;
    this.helloAt = Date.now();
    this.L.pub(`${base(this.code)}up`, { dev: this.dev, t: 'hello' });
  }

  private tick() {
    if (this.dead) return;
    if (!this.L.connected()) return this.L.wake();
    this.L.pub(`${base(this.code)}up`, { dev: this.dev, t: 'ping' }, { qos: 0 });
    const now = Date.now();
    if (this.open && now - this.seen > TIMEOUT) {
      this.open = false;
      this.h.status('host-away');
      this.hello();
    } else if (!this.open && now - this.helloAt > 9000) {
      this.fails += 1;
      this.h.status(this.fails > 1 ? 'host-away' : 'connecting');
      this.hello();
    }
  }

  /** Waits for the brokers, then sends the request and waits for the host's answer. */
  async request<T>(event: string, args: unknown[]): Promise<T> {
    const t0 = Date.now();
    while (!this.L.connected()) {
      if (Date.now() - t0 > 10000) throw new Error('No connection. Check your internet and try again.');
      await new Promise((r) => setTimeout(r, 200));
    }
    const id = rid() + rid();
    const send = () => this.L.pub(`${base(this.code)}up`, { dev: this.dev, t: 'req', id, event, args });
    const res = await new Promise<Ack>((resolve) => {
      // public relays can drop a message: resend every 3 s (the host answers a repeat without running it twice)
      const retry = setInterval(send, 3000);
      const timer = setTimeout(() => {
        clearInterval(retry);
        this.waiting.delete(id);
        resolve({ ok: false, error: "No answer from the host's phone. Is the host's app open?" });
      }, REPLY_TIMEOUT);
      this.waiting.set(id, (a) => {
        clearInterval(retry);
        clearTimeout(timer);
        this.waiting.delete(id);
        resolve(a);
      });
      send();
    });
    if (!res?.ok) throw new Error(res?.error || 'Something went wrong.');
    return res.data as T;
  }

  wake() {
    this.L.wake();
    this.hello();
  }

  close() {
    this.dead = true;
    clearInterval(this.timer);
    this.L.close();
  }
}

// =================================================================== helpers used by the app
export function loadHostedGame(code: string): Game | null {
  try {
    const raw = localStorage.getItem(hostKey(code));
    return raw ? Game.fromJSON(JSON.parse(raw)) : null;
  } catch {
    return null;
  }
}

export function makeGame(name: string, takenCodes: Set<string>): { game: Game; playerId: string; secret: string } {
  const code = newGameCode((c) => takenCodes.has(c));
  const game = new Game(code, DEFAULT_CASE);
  const p = game.addPlayer(name);
  return { game, playerId: p.id, secret: p.secret };
}

export { normalizeGameCode, CASES };
