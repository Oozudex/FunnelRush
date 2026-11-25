/**
 * App-side network API. No server: the host's phone runs the game (HostRoom),
 * the other phones talk to it through public MQTT brokers (GuestRoom).
 */
import type { Session } from '../shared/types';
import { GuestRoom, HostRoom, loadHostedGame, makeGame, normalizeGameCode, type Handlers } from './net/room';

let room: HostRoom | GuestRoom | null = null;
let roomKey = '';
let handlers: Handlers = { view: () => {}, status: () => {}, closed: () => {} };

export function setHandlers(h: Handlers) {
  handlers = h;
}

/** One id per tab: 2 tabs = 2 phones. */
function deviceId(): string {
  try {
    let d = sessionStorage.getItem('tlq.dev');
    if (!d) {
      d = Math.random().toString(36).slice(2, 12);
      sessionStorage.setItem('tlq.dev', d);
    }
    return d;
  } catch {
    return Math.random().toString(36).slice(2, 12);
  }
}

function withTimeout<T>(p: Promise<T>, ms: number, msg: string): Promise<T> {
  return Promise.race([p, new Promise<T>((_, rej) => setTimeout(() => rej(new Error(msg)), ms))]);
}

const NO_NET = 'Cannot reach the relay servers. Check your internet connection.';

export async function createGame(name: string): Promise<Session> {
  const tried = new Set<string>();
  for (let i = 0; i < 4; i++) {
    const { game, playerId, secret } = makeGame(name, tried);
    tried.add(game.code);
    const r = new HostRoom(game, handlers);
    r.myId = playerId;
    let ok: boolean;
    try {
      ok = await withTimeout(r.open(true), 15000, NO_NET);
    } catch (e) {
      r.close(false);
      throw e;
    }
    if (!ok) continue; // code already used by another game: try another one
    room?.close(false);
    room = r;
    roomKey = `${game.code}:${playerId}`;
    r.changed();
    return { code: game.code, playerId, secret, host: true };
  }
  throw new Error('Could not create a game. Try again.');
}

export async function joinGame(rawCode: string, name: string): Promise<Session> {
  const code = normalizeGameCode(rawCode);
  if (!/^[A-Z]+-\d{2}$/.test(code)) throw new Error('A game code looks like RAVEN-42.');
  const g = new GuestRoom(code, deviceId(), handlers);
  try {
    const s = await g.request<Session>('game:join', [{ code, name }]);
    room?.close(false);
    room = g;
    roomKey = `${code}:${s.playerId}`;
    return { ...s, host: false };
  } catch (e) {
    g.close();
    const msg = (e as Error).message;
    throw new Error(msg.startsWith('No answer') ? `No game found with the code ${code}. Check the code, and that the host's app is open.` : msg);
  }
}

/** After a reload: the host restores its saved game, a guest asks the host again. */
let inflight: { key: string; p: Promise<void> } | null = null;

export function resume(s: Session): Promise<void> {
  const key = `${s.code}:${s.playerId}`;
  // React StrictMode runs effects twice: share the same attempt
  if (inflight?.key === key) return inflight.p;
  if (room && roomKey === key) return Promise.resolve();
  const p = doResume(s, key).finally(() => {
    if (inflight?.p === p) inflight = null;
  });
  inflight = { key, p };
  return p;
}

async function doResume(s: Session, key: string): Promise<void> {
  roomKey = key;
  if (s.host) {
    const game = loadHostedGame(s.code);
    if (!game) throw new Error('This game is not on this phone any more.');
    game.auth(s.playerId, s.secret);
    const r = new HostRoom(game, handlers);
    r.myId = s.playerId;
    room = r;
    r.changed(); // show the game right away, even before the relays answer
    await withTimeout(r.open(false), 15000, NO_NET).catch(() => {});
    return;
  }
  const g = new GuestRoom(s.code, deviceId(), handlers);
  room = g;
  try {
    await g.request('game:resume', [s]);
  } catch (e) {
    g.close();
    room = null;
    roomKey = '';
    throw e;
  }
}

/** Every in-game action. */
export function emit<T = unknown>(event: string, ...args: unknown[]): Promise<T> {
  if (room instanceof HostRoom) {
    try {
      return Promise.resolve(room.local(event, args) as T);
    } catch (e) {
      return Promise.reject(new Error((e as Error).message || 'Something went wrong.'));
    }
  }
  if (room instanceof GuestRoom) return room.request<T>(event, args);
  return Promise.reject(new Error('You are not in a game.'));
}

export function leave() {
  const r = room;
  room = null;
  roomKey = '';
  if (r instanceof HostRoom) r.local('game:leave', []);
  else if (r instanceof GuestRoom) {
    r.request('game:leave', []).catch(() => {}).finally(() => r.close());
  }
}

export function wake() {
  room?.wake();
}

// ------------------------------------------------------------------ session & storage
const KEY = 'tlq.session';

/**
 * The session lives in sessionStorage (one per tab, so 2 tabs = 2 detectives) and in
 * localStorage (so a phone that closed its tab can come back). A tab opened from a
 * join link never picks up the localStorage session.
 */
export function loadSession(): Session | null {
  const parse = (raw: string | null) => {
    const s = JSON.parse(raw || 'null');
    return s && s.code && s.playerId && s.secret ? (s as Session) : null;
  };
  try {
    const tab = parse(sessionStorage.getItem(KEY));
    if (tab) return tab;
    if (new URLSearchParams(window.location.search).has('join')) return null;
    return parse(localStorage.getItem(KEY));
  } catch {
    return null;
  }
}

export function saveSession(s: Session | null) {
  try {
    if (s) {
      sessionStorage.setItem(KEY, JSON.stringify(s));
      localStorage.setItem(KEY, JSON.stringify(s));
    } else {
      sessionStorage.removeItem(KEY);
      localStorage.removeItem(KEY);
    }
  } catch {
    /* private mode: the session just won't survive a reload */
  }
}

export function store<T>(key: string, fallback: T): T {
  try {
    const v = localStorage.getItem(key);
    return v ? (JSON.parse(v) as T) : fallback;
  } catch {
    return fallback;
  }
}

export function persist(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* ignore */
  }
}

export function buzz(pattern: number | number[] = 40) {
  try {
    navigator.vibrate?.(pattern);
  } catch {
    /* ignore */
  }
}
