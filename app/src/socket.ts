import { io } from 'socket.io-client';
import type { Ack, Session } from '../shared/types';

export const socket = io({ autoConnect: true, transports: ['websocket', 'polling'] });

/** Emit with acknowledgement. Rejects with the server's English error message. */
export function emit<T = unknown>(event: string, ...args: unknown[]): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('No answer from the server. Check your connection.')), 8000);
    socket.emit(event, ...args, (res: Ack<T>) => {
      clearTimeout(timer);
      if (res?.ok) resolve(res.data as T);
      else reject(new Error(res?.error || 'Something went wrong.'));
    });
  });
}

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
