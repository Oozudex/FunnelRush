// Types shared by the server and the phone client.

export type Op = '=' | '!=' | 'between' | '>' | '<';

export interface AttributeDef {
  key: string;            // e.g. "shoe"
  label: string;          // e.g. "Shoe size"
  column: string;         // SQL column name
  type: 'number' | 'enum';
  unit?: string;          // "m", "years"
  decimals?: number;      // 2 for height
  options: (string | number)[]; // values offered in the dropdowns
}

export interface Condition {
  attr: string;
  op: Op;
  value: string | number;
  value2?: number;        // upper bound for BETWEEN
}

export interface PublicSuspect {
  id: string;
  name: string;
  link: string;           // link to the victim
  statement: string;      // what they say when interrogated (flavour, English practice)
}

export interface PublicCase {
  id: string;
  title: string;
  tagline: string;
  intro: string[];
  table: string;
  attributes: AttributeDef[];
  suspects: PublicSuspect[];
  updateEvery: number;    // W.A.T.S.O.N. update every N rounds
  maxTokens: number;
  startTokens: number;
}

export type Pawn = 'P1' | 'P2' | 'P3' | 'P4';
export const PAWNS: Pawn[] = ['P1', 'P2', 'P3', 'P4'];

export interface PublicPlayer {
  id: string;
  name: string;
  pawn: Pawn | null;
  connected: boolean;
  tokens: number;
  queries: number;
  evidence: number;
  isHost: boolean;
}

export type LogKind = 'info' | 'join' | 'turn' | 'update' | 'accuse-wrong' | 'accuse-right' | 'recharge' | 'end';

export interface LogEntry {
  id: number;
  at: number;
  round: number;
  kind: LogKind;
  text: string;
}

export interface WatsonUpdate {
  round: number;
  text: string;
  condition?: Condition;
}

export interface Solution {
  suspectId: string;
  name: string;
  profile: string;
  story: string;
}

export type Phase = 'lobby' | 'playing' | 'over';

export interface GameState {
  code: string;
  caseInfo: PublicCase;
  phase: Phase;
  hostId: string;
  players: PublicPlayer[];
  order: string[];        // player ids in turn order
  turn: number;           // index in order
  round: number;
  updates: WatsonUpdate[];
  log: LogEntry[];
  winnerId: string | null;
  solution: Solution | null;
  lastAccusation: { playerId: string; suspectName: string; correct: boolean; at: number } | null;
  action: 'search' | 'recharge' | 'accuse' | null;  // the ONE action already done this turn
  scans: number;          // cards scanned this turn
  scansPerTurn: number;   // max cards per Search action
}

export interface EvidenceItem {
  code: string;
  room: string;
  object: string;
  kind: 'trait' | 'deadend' | 'bonus';  // never says if a trait is true or planted
  text: string;
  condition?: Condition;
  at: number;
}

export interface QueryRecord {
  conditions: Condition[];
  sql: string;
  names: string[];
  at: number;
  round: number;
}

export interface PrivateState {
  playerId: string;
  evidence: EvidenceItem[];
  queries: QueryRecord[];
}

export interface View {
  game: GameState;
  me: PrivateState;
}

export interface Ack<T = unknown> {
  ok: boolean;
  error?: string;
  data?: T;
}

export interface Session {
  code: string;
  playerId: string;
  secret: string;
  host?: boolean;   // this phone runs the game
}

export interface ScanResult {
  item: EvidenceItem;
  again: boolean;     // already in your evidence
  effect?: string;    // bonus effect message
}
