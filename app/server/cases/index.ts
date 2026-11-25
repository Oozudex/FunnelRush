import { foxglove } from './foxglove';
import type { CaseDef } from './types';

/** Register new cases here. */
export const CASES: Record<string, CaseDef> = {
  [foxglove.id]: foxglove,
};

export const DEFAULT_CASE = foxglove.id;
