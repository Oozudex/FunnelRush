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
  return <img className="logo" src="/logo.svg" alt="The Last Query" style={small ? { maxWidth: 220 } : undefined} />;
}

export function Glitch({ text, hard, className = '' }: { text: string; hard?: boolean; className?: string }) {
  return (
    <span className={`glitch ${hard ? 'hard' : ''} ${className}`} data-text={text}>
      {text}
    </span>
  );
}

export function Tokens({ n, max = 3 }: { n: number; max?: number }) {
  return (
    <span className="tokens" aria-label={`${n} Query Tokens`}>
      {Array.from({ length: max }, (_, i) => (
        <span key={i} className={`tok ${i < n ? '' : 'off'}`}>;</span>
      ))}
    </span>
  );
}

export function PawnIcon({ pawn }: { pawn: Pawn | null }) {
  return <span className={`pawn ${pawn ?? 'none'}`}>{pawn ? pawn.slice(1) : '?'}</span>;
}

export const PAWN_NAME: Record<Pawn, string> = { P1: 'Amber', P2: 'Red', P3: 'Blue', P4: 'Bone' };

/** In-game clock: the crime is at 11:45 PM, round 1 starts at midnight, +15 min per round. */
export function clockFor(round: number): string {
  const mins = (round - 1) * 15;
  const h = Math.floor(mins / 60) % 12;
  const m = mins % 60;
  return `${h === 0 ? 12 : h}:${String(m).padStart(2, '0')} AM`;
}

export function SectionTitle({ children }: { children: ReactNode }) {
  return <div className="section-title pix muted">{children}</div>;
}

const P = { fill: 'none', stroke: 'currentColor', strokeWidth: 2, strokeLinecap: 'square' as const };
export const Icon = {
  scan: (
    <svg viewBox="0 0 24 24" {...P}><path d="M3 8V3h5M16 3h5v5M21 16v5h-5M8 21H3v-5M7 12h10" /></svg>
  ),
  query: (
    <svg viewBox="0 0 24 24" {...P}><path d="M4 6l5 6-5 6M12 18h8" /></svg>
  ),
  clues: (
    <svg viewBox="0 0 24 24" {...P}><path d="M3 10a7 7 0 1 0 14 0a7 7 0 1 0-14 0M15 15l6 6" /></svg>
  ),
  notebook: (
    <svg viewBox="0 0 24 24" {...P}><path d="M5 3h14v18H5zM9 3v18M12 8h4M12 12h4" /></svg>
  ),
  manor: (
    <svg viewBox="0 0 24 24" {...P}><path d="M3 21V10l9-7 9 7v11zM9 21v-6h6v6" /></svg>
  ),
};
