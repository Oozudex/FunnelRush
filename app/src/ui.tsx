import { createContext, useContext, type ReactNode } from 'react';
import type { Pawn, View } from '../shared/types';

export interface Ctx {
  view: View;
  toast: (msg: string, ok?: boolean) => void;
  leave: () => void;
}
export const GameCtx = createContext<Ctx | null>(null);
export function useGame(): Ctx {
  const c = useContext(GameCtx);
  if (!c) throw new Error('GameCtx missing');
  return c;
}

export function useMe(view: View) {
  const me = view.game.players.find((p) => p.id === view.me.playerId)!;
  const current = view.game.phase === 'playing' ? view.game.players.find((p) => p.id === view.game.order[view.game.turn]) : undefined;
  return { me, current, myTurn: !!current && current.id === me?.id, isHost: view.game.hostId === view.me.playerId };
}

export function Logo({ small }: { small?: boolean }) {
  return (
    <img
      className="logo"
      src={`${import.meta.env.BASE_URL}logo-light.svg`}
      alt="The Last Query"
      style={small ? { maxWidth: 200 } : undefined}
    />
  );
}

export function Tokens({ n, max = 3 }: { n: number; max?: number }) {
  return (
    <span className="tokens" aria-label={`${n} of ${max} Query Tokens`}>
      {Array.from({ length: max }, (_, i) => (
        <span key={i} className={`tok ${i < n ? '' : 'off'}`} aria-hidden>;</span>
      ))}
    </span>
  );
}

export function PawnIcon({ pawn }: { pawn: Pawn | null }) {
  return <span className={`pawn ${pawn ?? 'none'}`}>{pawn ?? '?'}</span>;
}

export const PAWN_NAME: Record<Pawn, string> = { P1: 'Amber', P2: 'Red', P3: 'Blue', P4: 'Bone' };

/** In-game clock: the crime is at 11:45 PM, round 1 starts at midnight, +15 min per round. */
export function clockFor(round: number): string {
  const mins = (round - 1) * 15;
  const h = Math.floor(mins / 60) % 12;
  const m = mins % 60;
  return `${h === 0 ? 12 : h}:${String(m).padStart(2, '0')} AM`;
}

/** Black header bar of the cards and the board rooms. */
export function Bar({ icon, color, children, end }: { icon?: ReactNode; color?: 'blue' | 'amber' | 'red' | 'grey'; children: ReactNode; end?: ReactNode }) {
  return (
    <div className="bar">
      <span className={`sq ${color ?? ''}`}>{icon}</span>
      <span className="grow">{children}</span>
      {end}
    </div>
  );
}

export function Label({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <div className={`label ${className}`}>{children}</div>;
}

export function Sheet({ title, icon, onClose, full, children }: { title: string; icon?: ReactNode; onClose: () => void; full?: boolean; children: ReactNode }) {
  return (
    <div className={`sheet ${full ? 'full' : ''}`} onClick={onClose}>
      <div className="panel" role="dialog" aria-modal="true" aria-label={title} onClick={(e) => e.stopPropagation()}>
        <div className="sheet-head">
          <div className="bar">
            <span className="sq">{icon}</span>
            <span className="grow">{title}</span>
            <button className="iconbtn" onClick={onClose} aria-label="Close">{Icon.close}</button>
          </div>
        </div>
        {children}
      </div>
    </div>
  );
}

const P = { fill: 'none', stroke: 'currentColor', strokeWidth: 2, strokeLinecap: 'square' as const, strokeLinejoin: 'miter' as const };
const svg = (d: string) => (
  <svg viewBox="0 0 24 24" {...P} aria-hidden>
    <path d={d} />
  </svg>
);

export const Icon = {
  turn: svg('M7 4l12 8-12 8z'),
  clues: svg('M3 10a7 7 0 1 0 14 0a7 7 0 1 0-14 0M15 15l6 6'),
  suspects: svg('M5 3h14v18H5zM9 3v18M12 8h4M12 12h4'),
  menu: svg('M4 7h16M4 12h16M4 17h16'),
  close: svg('M6 6l12 12M18 6L6 18'),
  scan: svg('M3 8V3h5M16 3h5v5M21 16v5h-5M8 21H3v-5M7 12h10'),
  console: svg('M4 6l5 6-5 6M12 18h8'),
  bolt: svg('M13 2L5 14h6l-1 8 8-12h-6z'),
  scale: svg('M12 3v18M7 21h10M4 7h16M4 7l-2 7h6zM20 7l-2 7h6z'),
  move: svg('M5 12h14M13 6l6 6-6 6'),
  chevron: svg('M6 9l6 6 6-6'),
  arrow: svg('M9 6l6 6-6 6'),
  check: svg('M4 12l5 5L20 6'),
  lock: svg('M6 11h12v10H6zM9 11V7a3 3 0 0 1 6 0v4'),
  info: svg('M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M12 11v6M12 7v1'),
  back: svg('M15 6l-6 6 6 6'),
  undo: svg('M9 7L4 12l5 5M4 12h11a5 5 0 0 1 0 10h-2'),
  stamp: svg('M9 3h6v6l3 4H6l3-4zM4 17h16v4H4z'),
};

/** Room icons, same set as the board V3. */
export const RoomIcon: Record<string, ReactNode> = {
  Observatory: svg('M4 15l12-7 2 4-12 7zM10 16l-3 6M12 15l3 7'),
  Library: svg('M3 5h7a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H3zM21 5h-7a2 2 0 0 0-2 2v13a2 2 0 0 1 2-2h7z'),
  Chapel: svg('M12 3v3M9 10h6v11H9zM12 6a2 2 0 0 1 0 4'),
  'Music Room': svg('M9 18V5l11-2v13M9 18a3 3 0 1 1-6 0a3 3 0 1 1 6 0M20 16a3 3 0 1 1-6 0a3 3 0 1 1 6 0'),
  'Grand Hall': svg('M5 21V5h14v16M9 21v-8h6v8'),
  Kitchen: svg('M4 9h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM17 11h2a2 2 0 0 1 0 4h-2M8 3v3M12 3v3'),
  Greenhouse: svg('M5 19C5 10 11 5 20 4c-1 9-6 15-15 15zM5 19l8-8'),
  'Wine Cellar': svg('M10 2h4v5l2 3v12H8V10l2-3z'),
  'Server Room': svg('M4 4h16v5H4zM4 9h16v5H4zM4 14h16v6H4zM7 6.5h1M7 11.5h1M7 17h1'),
};
export const roomIcon = (room: string) => RoomIcon[room] ?? Icon.clues;
