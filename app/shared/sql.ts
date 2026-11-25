// Turns the sentence blocks into real SQL, and evaluates them on the server.
import type { AttributeDef, Condition, Op } from './types';

export const OP_LABEL: Record<Op, string> = {
  '=': 'is',
  '!=': 'is not',
  between: 'between',
  '>': 'more than',
  '<': 'less than',
};

export function opsFor(attr: AttributeDef): Op[] {
  return attr.type === 'number' ? ['=', 'between', '>', '<'] : ['=', '!='];
}

export function fmtValue(attr: AttributeDef | undefined, v: string | number): string {
  if (typeof v === 'number') return attr?.decimals ? v.toFixed(attr.decimals) : String(v);
  return v;
}

function sqlValue(attr: AttributeDef, v: string | number): string {
  return attr.type === 'number' ? fmtValue(attr, Number(v)) : `'${String(v).replace(/'/g, "''")}'`;
}

export function conditionSql(attr: AttributeDef, c: Condition): string {
  if (c.op === 'between') return `${attr.column} BETWEEN ${sqlValue(attr, c.value)} AND ${sqlValue(attr, c.value2 ?? c.value)}`;
  if (c.op === '!=') return `${attr.column} <> ${sqlValue(attr, c.value)}`;
  return `${attr.column} ${c.op} ${sqlValue(attr, c.value)}`;
}

export function buildSql(table: string, attrs: AttributeDef[], conds: Condition[]): string {
  const where = conds
    .map((c) => {
      const a = attrs.find((x) => x.key === c.attr);
      return a ? conditionSql(a, c) : '';
    })
    .filter(Boolean)
    .join(' AND ');
  return `SELECT name FROM ${table}${where ? ` WHERE ${where}` : ''};`;
}

/** Plain-English version, e.g. "Height between 1.85 and 1.90 m". */
export function describe(attr: AttributeDef | undefined, c: Condition): string {
  if (!attr) return '';
  const unit = attr.unit ? ` ${attr.unit}` : '';
  if (c.op === 'between') return `${attr.label} between ${fmtValue(attr, c.value)} and ${fmtValue(attr, c.value2 ?? c.value)}${unit}`;
  return `${attr.label} ${OP_LABEL[c.op]} ${fmtValue(attr, c.value)}${attr.type === 'number' ? unit : ''}`;
}

export function matches(row: Record<string, string | number>, attr: AttributeDef, c: Condition): boolean {
  const v = row[attr.key];
  if (attr.type === 'number') {
    const n = Number(v);
    const a = Number(c.value);
    const eps = 1e-9;
    switch (c.op) {
      case '=': return Math.abs(n - a) < eps;
      case '!=': return Math.abs(n - a) >= eps;
      case '>': return n > a + eps;
      case '<': return n < a - eps;
      case 'between': {
        const lo = Math.min(a, Number(c.value2 ?? a));
        const hi = Math.max(a, Number(c.value2 ?? a));
        return n >= lo - eps && n <= hi + eps;
      }
    }
  }
  const s = String(v).toLowerCase();
  const t = String(c.value).toLowerCase();
  return c.op === '!=' ? s !== t : s === t;
}
