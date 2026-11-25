import type { AttributeDef, Condition, PublicCase } from '../../../shared/types';

export type CardType = 'clue' | 'deadend' | 'planted' | 'bonus';
export type BonusEffect = 'token' | 'move' | 'peek';

export interface CardDef {
  room: string;
  object: string;
  type: CardType;
  /** What the scan reveals, in English. */
  reveal: string;
  /** For clue and planted cards: the trait it points to (unlocks that query block). */
  condition?: Condition;
  bonus?: BonusEffect;
}

export interface SuspectDef {
  id: string;
  name: string;
  link: string;
  statement: string;
  traits: Record<string, string | number>;
}

/**
 * One playable case. To add a case: copy foxglove.ts, change the data,
 * and register it in cases/index.ts. Card codes are the ones printed on
 * the physical cards (QR = "TLQ:<code>"), so the same 40 cards are reused.
 */
export interface CaseDef {
  id: string;
  title: string;
  tagline: string;
  intro: string[];
  table: string;
  attributes: AttributeDef[];
  suspects: SuspectDef[];
  cards: Record<string, CardDef>;
  killerId: string;
  /** Revealed to everyone at the end of rounds updateEvery, 2*updateEvery, ... */
  updates: { text: string; condition: Condition }[];
  updateEvery: number;
  startTokens: number;
  maxTokens: number;
  solutionStory: string;
}

export function publicCase(c: CaseDef): PublicCase {
  return {
    id: c.id,
    title: c.title,
    tagline: c.tagline,
    intro: c.intro,
    table: c.table,
    attributes: c.attributes,
    suspects: c.suspects.map(({ id, name, link, statement }) => ({ id, name, link, statement })),
    updateEvery: c.updateEvery,
    maxTokens: c.maxTokens,
    startTokens: c.startTokens,
  };
}
