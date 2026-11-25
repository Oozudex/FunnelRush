// crypto.getRandomValues works on plain http too (randomUUID needs https)
function randomHex(n: number) {
  return Array.from(crypto.getRandomValues(new Uint8Array(n)), (b) => b.toString(16).padStart(2, '0')).join('');
}
const randomUUID = () => randomHex(16);
import { buildSql, describe, matches } from '../../shared/sql';
import type {
  Condition, EvidenceItem, GameState, LogKind, Pawn, PrivateState, PublicPlayer, QueryRecord, ScanResult, View,
} from '../../shared/types';
import { PAWNS } from '../../shared/types';
import { CASES } from './cases';
import { publicCase, type CaseDef } from './cases/types';

const WORDS = ['RAVEN', 'STORM', 'ALIBI', 'MANOR', 'GHOST', 'CIGAR', 'TEACUP', 'MOTIVE', 'SHADOW', 'THUNDER', 'CANDLE', 'BUTLER', 'POISON', 'ATTIC', 'CLOCK'];
export const MAX_PLAYERS = 4;

interface Player {
  id: string;
  secret: string;
  name: string;
  pawn: Pawn | null;
  tokens: number;
  evidence: EvidenceItem[];
  queries: QueryRecord[];
  sockets: Set<string>;
}

export class GameError extends Error {}

export class Game {
  code: string;
  def: CaseDef;
  phase: GameState['phase'] = 'lobby';
  hostId = '';
  players = new Map<string, Player>();
  order: string[] = [];
  firstPlayerId: string | null = null;
  turn = 0;
  round = 1;
  updates: GameState['updates'] = [];
  log: GameState['log'] = [];
  winnerId: string | null = null;
  usedBonus = new Set<string>();
  lastAccusation: GameState['lastAccusation'] = null;
  /** The ONE action of the current turn (rules V2): search, recharge or accuse. */
  action: GameState['action'] = null;
  touched = Date.now();
  logId = 0;

  constructor(code: string, caseId: string) {
    const def = CASES[caseId];
    if (!def) throw new GameError('Unknown case.');
    this.code = code;
    this.def = def;
  }

  // ---------------------------------------------------------------- players
  addPlayer(name: string): Player {
    if (this.phase !== 'lobby') throw new GameError('This game has already started.');
    if (this.players.size >= MAX_PLAYERS) throw new GameError('This game is full (4 detectives max).');
    const clean = cleanName(name);
    if ([...this.players.values()].some((p) => p.name.toLowerCase() === clean.toLowerCase()))
      throw new GameError('A detective already uses this name.');
    const used = new Set([...this.players.values()].map((p) => p.pawn));
    const p: Player = {
      id: randomUUID(),
      secret: randomHex(12),
      name: clean,
      pawn: PAWNS.find((x) => !used.has(x)) ?? null,
      tokens: this.def.startTokens,
      evidence: [],
      queries: [],
      sockets: new Set(),
    };
    this.players.set(p.id, p);
    if (!this.hostId) this.hostId = p.id;
    this.order.push(p.id);
    this.addLog('join', `${p.name} joined the investigation.`);
    return p;
  }

  auth(playerId: string, secret: string): Player {
    const p = this.players.get(playerId);
    if (!p || p.secret !== secret) throw new GameError('Session expired. Join the game again.');
    return p;
  }

  removePlayer(by: string, playerId: string) {
    if (this.phase !== 'lobby') throw new GameError('You can only remove detectives in the waiting room.');
    if (by !== playerId && by !== this.hostId) throw new GameError('Only the host can do this.');
    const p = this.player(playerId);
    this.players.delete(playerId);
    this.order = this.order.filter((id) => id !== playerId);
    if (this.firstPlayerId === playerId) this.firstPlayerId = null;
    if (this.hostId === playerId) this.hostId = this.order[0] ?? '';
    this.addLog('info', `${p.name} left.`);
  }

  pickPawn(playerId: string, pawn: Pawn) {
    if (!PAWNS.includes(pawn)) throw new GameError('Unknown pawn.');
    const taken = [...this.players.values()].find((p) => p.pawn === pawn && p.id !== playerId);
    if (taken) throw new GameError(`${taken.name} already has this pawn.`);
    this.player(playerId).pawn = pawn;
  }

  setFirst(by: string, playerId: string) {
    this.requireHost(by);
    this.player(playerId);
    this.firstPlayerId = playerId;
  }

  setCase(by: string, caseId: string) {
    this.requireHost(by);
    if (this.phase !== 'lobby') throw new GameError('The game has started.');
    const def = CASES[caseId];
    if (!def) throw new GameError('Unknown case.');
    this.def = def;
  }

  start(by: string) {
    this.requireHost(by);
    if (this.phase !== 'lobby') throw new GameError('The game has already started.');
    if ([...this.players.values()].some((p) => !p.pawn)) throw new GameError('Every detective needs a pawn.');
    const ids = [...this.players.keys()];
    const first = this.firstPlayerId && ids.includes(this.firstPlayerId) ? ids.indexOf(this.firstPlayerId) : 0;
    this.order = [...ids.slice(first), ...ids.slice(0, first)];
    this.turn = 0;
    this.round = 1;
    for (const p of this.players.values()) p.tokens = this.def.startTokens;
    this.phase = 'playing';
    this.action = null;
    this.addLog('info', `The investigation begins. ${this.current().name} plays first.`);
  }

  // ---------------------------------------------------------------- turns
  current(): Player {
    return this.player(this.order[this.turn % this.order.length]);
  }

  endTurn(by: string) {
    this.requirePlaying();
    if (by !== this.current().id && by !== this.hostId) throw new GameError('It is not your turn.');
    this.advance();
  }

  private advance() {
    this.action = null;
    this.turn += 1;
    if (this.turn >= this.order.length) this.finishRound();
    else this.addLog('turn', `${this.current().name}'s turn.`);
  }

  endRound(by: string) {
    this.requireHost(by);
    this.requirePlaying();
    this.finishRound();
  }

  private finishRound() {
    const done = this.round;
    this.action = null;
    this.turn = 0;
    this.round += 1;
    if (done % this.def.updateEvery === 0) {
      const idx = done / this.def.updateEvery - 1;
      const u = this.def.updates[idx];
      for (const p of this.players.values()) p.tokens = Math.min(this.def.maxTokens, p.tokens + 1);
      const text = u ? u.text : 'No new data recovered. The storm is too strong.';
      this.updates.push({ round: done, text, condition: u?.condition });
      this.addLog('update', `W.A.T.S.O.N. update: ${text} Everyone gets +1 token.`);
    }
    this.addLog('turn', `Round ${this.round} begins. ${this.current().name}'s turn.`);
  }

  // ---------------------------------------------------------------- actions
  private myTurn(p: Player, what: string) {
    this.requirePlaying();
    if (this.current().id !== p.id) throw new GameError(`Wait for your turn to ${what}. ${this.current().name} is playing.`);
  }

  private takeAction(kind: NonNullable<GameState['action']>) {
    if (this.action) {
      const done = { search: 'searched a room', recharge: 'recharged', accuse: 'accused' }[this.action];
      throw new GameError(`You already ${done} this turn: only ONE action per turn. Tap "End my turn".`);
    }
    this.action = kind;
  }

  scan(playerId: string, raw: string): ScanResult {
    const p = this.player(playerId);
    this.myTurn(p, 'search a room');
    const code = normalizeCode(raw);
    const card = this.def.cards[code];
    if (!card) throw new GameError(`Unknown code "${raw.trim().slice(0, 20)}". Check the code printed under the QR.`);
    const existing = p.evidence.find((e) => e.code === code);
    if (!existing) this.takeAction('search');
    if (card.type === 'bonus') {
      let effect: string | undefined;
      if (card.bonus === 'token') {
        if (this.usedBonus.has(code)) effect = 'This battery has already been used.';
        else if (p.tokens >= this.def.maxTokens) effect = `You already have ${this.def.maxTokens} tokens. Keep this card for later!`;
        else {
          this.usedBonus.add(code);
          p.tokens += 1;
          effect = '+1 Query Token added. Discard the card.';
          this.addLog('recharge', `${p.name} used a Spare Battery.`);
        }
      }
      const item = existing ?? { code, room: card.room, object: card.object, kind: 'bonus' as const, text: card.reveal, at: Date.now() };
      if (!existing) p.evidence.push(item);
      return { item, again: !!existing, effect };
    }
    if (existing) return { item: existing, again: true };
    const item: EvidenceItem = {
      code,
      room: card.room,
      object: card.object,
      kind: card.condition ? 'trait' : 'deadend',
      text: card.reveal,
      condition: card.condition,
      at: Date.now(),
    };
    p.evidence.push(item);
    return { item, again: false };
  }

  unlockedAttrs(p: Player): Set<string> {
    const s = new Set<string>();
    p.evidence.forEach((e) => e.condition && s.add(e.condition.attr));
    this.updates.forEach((u) => u.condition && s.add(u.condition.attr));
    return s;
  }

  query(playerId: string, conds: Condition[]): QueryRecord {
    this.requirePlaying();
    const p = this.player(playerId);
    this.myTurn(p, 'run a query');
    if (p.tokens < 1) throw new GameError('No Query Token left. Recharge in the Server Room.');
    if (!Array.isArray(conds) || conds.length < 1 || conds.length > 2) throw new GameError('Use 1 or 2 conditions.');
    const unlocked = this.unlockedAttrs(p);
    const attrs = this.def.attributes;
    for (const c of conds) {
      const a = attrs.find((x) => x.key === c?.attr);
      if (!a) throw new GameError('Unknown column.');
      if (!unlocked.has(a.key)) throw new GameError(`"${a.label}" is locked. Find evidence about it first.`);
      const okOps = a.type === 'number' ? ['=', 'between', '>', '<'] : ['=', '!='];
      if (!okOps.includes(c.op)) throw new GameError('Invalid operator.');
      if (!a.options.map(String).includes(String(c.value))) throw new GameError(`Invalid value for ${a.label}.`);
      if (c.op === 'between' && !a.options.map(String).includes(String(c.value2))) throw new GameError(`Invalid value for ${a.label}.`);
    }
    const rows = this.def.suspects.filter((s) =>
      conds.every((c) => matches(s.traits, attrs.find((a) => a.key === c.attr)!, c)),
    );
    p.tokens -= 1;
    const rec: QueryRecord = {
      conditions: conds.map((c) => ({ attr: c.attr, op: c.op, value: c.value, ...(c.op === 'between' ? { value2: c.value2 } : {}) })),
      sql: buildSql(this.def.table, attrs, conds),
      names: rows.map((r) => r.name),
      at: Date.now(),
      round: this.round,
    };
    p.queries.push(rec);
    return rec;
  }

  recharge(playerId: string) {
    const p = this.player(playerId);
    this.myTurn(p, 'recharge');
    this.takeAction('recharge');
    p.tokens = this.def.maxTokens;
    this.addLog('recharge', `${p.name} recharged in the Server Room.`);
  }

  accuse(playerId: string, suspectId: string): boolean {
    const p = this.player(playerId);
    this.myTurn(p, 'accuse');
    const s = this.def.suspects.find((x) => x.id === suspectId);
    if (!s) throw new GameError('Unknown suspect.');
    this.takeAction('accuse');
    const correct = s.id === this.def.killerId;
    this.lastAccusation = { playerId: p.id, suspectName: s.name, correct, at: Date.now() };
    if (correct) {
      this.winnerId = p.id;
      this.phase = 'over';
      this.addLog('accuse-right', `${p.name} accused ${s.name}. CASE CLOSED!`);
    } else {
      p.tokens = 0;
      this.addLog('accuse-wrong', `${p.name} accused ${s.name}. WRONG! Back to the Grand Hall, all tokens lost.`);
      this.advance();
    }
    return correct;
  }

  abandon(by: string) {
    this.requireHost(by);
    if (this.phase !== 'playing') throw new GameError('The game is not running.');
    this.phase = 'over';
    this.winnerId = null;
    this.addLog('end', 'Dawn breaks. The police arrive... and the killer has escaped.');
  }

  // ---------------------------------------------------------------- views
  publicState(): GameState {
    const killer = this.def.suspects.find((s) => s.id === this.def.killerId)!;
    const t = killer.traits;
    return {
      code: this.code,
      caseInfo: publicCase(this.def),
      phase: this.phase,
      hostId: this.hostId,
      players: [...this.players.values()].map<PublicPlayer>((p) => ({
        id: p.id,
        name: p.name,
        pawn: p.pawn,
        connected: p.sockets.size > 0,
        tokens: p.tokens,
        queries: p.queries.length,
        evidence: p.evidence.filter((e) => e.kind !== 'bonus').length,
        isHost: p.id === this.hostId,
      })),
      order: this.phase === 'lobby' ? this.lobbyOrder() : this.order,
      turn: this.turn,
      round: this.round,
      updates: this.updates,
      log: this.log.slice(-40),
      winnerId: this.winnerId,
      lastAccusation: this.lastAccusation,
      action: this.action,
      solution:
        this.phase === 'over'
          ? {
              suspectId: killer.id,
              name: killer.name,
              profile: `${t.age} years old, ${Number(t.height).toFixed(2)} m tall, size ${t.shoe} shoes, ${t.hand}-handed, ${t.hair} hair, smells of ${t.smell}.`,
              story: this.def.solutionStory,
            }
          : null,
    };
  }

  private lobbyOrder() {
    const ids = [...this.players.keys()];
    const f = this.firstPlayerId ? ids.indexOf(this.firstPlayerId) : 0;
    return f > 0 ? [...ids.slice(f), ...ids.slice(0, f)] : ids;
  }

  view(playerId: string): View {
    const p = this.player(playerId);
    const me: PrivateState = { playerId: p.id, evidence: p.evidence, queries: p.queries };
    return { game: this.publicState(), me };
  }

  describeCondition(c: Condition) {
    return describe(this.def.attributes.find((a) => a.key === c.attr), c);
  }

  // ---------------------------------------------------------------- save / restore (survives a server restart)
  toJSON() {
    return {
      code: this.code, caseId: this.def.id, phase: this.phase, hostId: this.hostId,
      players: [...this.players.values()].map(({ sockets, ...p }) => p),
      order: this.order, firstPlayerId: this.firstPlayerId, turn: this.turn, round: this.round,
      updates: this.updates, log: this.log, winnerId: this.winnerId, usedBonus: [...this.usedBonus],
      lastAccusation: this.lastAccusation, action: this.action, touched: this.touched, logId: this.logId,
    };
  }

  static fromJSON(d: ReturnType<Game['toJSON']>): Game {
    const g = new Game(d.code, d.caseId);
    Object.assign(g, {
      phase: d.phase, hostId: d.hostId, order: d.order, firstPlayerId: d.firstPlayerId, turn: d.turn, round: d.round,
      updates: d.updates, log: d.log, winnerId: d.winnerId, usedBonus: new Set(d.usedBonus),
      lastAccusation: d.lastAccusation, action: d.action ?? null, touched: d.touched, logId: d.logId,
    });
    for (const p of d.players) g.players.set(p.id, { ...p, sockets: new Set() });
    return g;
  }

  // ---------------------------------------------------------------- helpers
  player(id: string): Player {
    const p = this.players.get(id);
    if (!p) throw new GameError('Unknown detective.');
    return p;
  }

  private requireHost(by: string) {
    if (by !== this.hostId) throw new GameError('Only the host can do this.');
  }

  private requirePlaying() {
    if (this.phase !== 'playing') throw new GameError(this.phase === 'lobby' ? 'The game has not started yet.' : 'The case is closed.');
  }

  addLog(kind: LogKind, text: string) {
    this.log.push({ id: ++this.logId, at: Date.now(), round: this.round, kind, text });
    if (this.log.length > 200) this.log.shift();
  }
}

export function cleanName(name: unknown): string {
  const n = String(name ?? '').replace(/\s+/g, ' ').trim().slice(0, 18);
  if (n.length < 2) throw new GameError('Type a name (2 letters or more).');
  return n;
}

/** "tlq:lib-01", "LIB01", " lib 01 " -> "LIB-01" */
export function normalizeCode(raw: string): string {
  let s = String(raw ?? '').trim().toUpperCase();
  if (s.startsWith('TLQ:')) s = s.slice(4);
  s = s.replace(/[^A-Z0-9]/g, '');
  const m = s.match(/^([A-Z]{3})(\d{1,2})$/);
  return m ? `${m[1]}-${m[2].padStart(2, '0')}` : s;
}

export function normalizeGameCode(raw: string): string {
  const s = String(raw ?? '').trim().toUpperCase().replace(/[^A-Z0-9]/g, '');
  const m = s.match(/^([A-Z]+)(\d{2})$/);
  return m ? `${m[1]}-${m[2]}` : s;
}

export function newGameCode(taken: (c: string) => boolean): string {
  for (let i = 0; i < 500; i++) {
    const c = `${WORDS[Math.floor(Math.random() * WORDS.length)]}-${String(Math.floor(Math.random() * 90) + 10)}`;
    if (!taken(c)) return c;
  }
  throw new GameError('Too many games running. Try again.');
}
