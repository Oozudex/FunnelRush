import React, { useMemo, useState } from 'react';
import type { AttributeDef, Condition, QueryRecord } from '../../shared/types';
import { describe, fmtValue } from '../../shared/sql';
import { buzz, emit } from '../socket';
import { Bar, Icon, Sheet, Tokens, useGame, useMe } from '../ui';

export function ResultTable({ rec, crossed, suspects }: { rec: QueryRecord; crossed: string[]; suspects: { id: string; name: string; link: string }[] }) {
  if (rec.names.length === 0)
    return (
      <div className="file center stack tight">
        <div style={{ padding: '6px 0' }}><span className="stamp big">0 suspects</span></div>
        <p className="typed">Nobody matches all your conditions.</p>
        <p className="small red"><b>Golden rule: one of your clues is fake!</b></p>
      </div>
    );
  return (
    <div className="file flush">
      <Bar icon={Icon.suspects} end={<span>{rec.names.length} found</span>}>Result · only you see it</Bar>
      <table className="result">
        <thead>
          <tr><th>name</th><th>link to Victor</th></tr>
        </thead>
        <tbody>
          {rec.names.map((n) => {
            const s = suspects.find((x) => x.name === n);
            return (
              <tr key={n} className={s && crossed.includes(s.id) ? 'crossed' : ''}>
                <td style={{ fontWeight: 800 }}>{n}</td>
                <td className="small muted">{s?.link}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ======================================================================= SQL composer
// The player writes the query block by block. Only blocks that are valid SQL at this
// point can be tapped, so nobody gets stuck, but every choice is the player's.

type Kw = 'SELECT' | 'FROM' | 'WHERE' | 'AND' | 'BETWEEN';
type SqlOp = '=' | '<>' | '>' | '<';
type Tok =
  | { k: 'kw'; v: Kw }
  | { k: 'field'; v: 'name' }
  | { k: 'table'; v: string }
  | { k: 'col'; v: string }
  | { k: 'op'; v: SqlOp }
  | { k: 'val'; v: string | number; label: string };

type State = 'SELECT' | 'FIELD' | 'FROM' | 'TABLE' | 'WHERE' | 'COL' | 'OP' | 'VAL' | 'BAND' | 'VAL2' | 'NEXT';

const OP_OF: Record<SqlOp, Condition['op']> = { '=': '=', '<>': '!=', '>': '>', '<': '<' };
const OP_WORD: Record<SqlOp, string> = { '=': 'is', '<>': 'is not', '>': 'more than', '<': 'less than' };
const MAX_CONDS = 2;

function analyse(toks: Tok[]) {
  let state: State = 'SELECT';
  const conds: Condition[] = [];
  let cur: Partial<Condition> = {};
  for (const t of toks) {
    switch (state) {
      case 'SELECT': state = 'FIELD'; break;
      case 'FIELD': state = 'FROM'; break;
      case 'FROM': state = 'TABLE'; break;
      case 'TABLE': state = 'WHERE'; break;
      case 'WHERE': state = 'COL'; break;
      case 'COL': cur = { attr: String(t.v) }; state = 'OP'; break;
      case 'OP':
        cur.op = t.k === 'kw' ? 'between' : OP_OF[t.v as SqlOp];
        state = 'VAL';
        break;
      case 'VAL':
        cur.value = t.v as string | number;
        if (cur.op === 'between') state = 'BAND';
        else {
          conds.push(cur as Condition);
          state = 'NEXT';
        }
        break;
      case 'BAND': state = 'VAL2'; break;
      case 'VAL2':
        cur.value2 = Number(t.v);
        conds.push(cur as Condition);
        state = 'NEXT';
        break;
      case 'NEXT': state = 'COL'; break;
    }
  }
  return { state, conds, curAttr: state === 'OP' || state === 'VAL' || state === 'VAL2' || state === 'BAND' ? cur.attr : undefined };
}

const HINT: Record<State, string> = {
  SELECT: 'Start your query with SELECT ("show me…").',
  FIELD: 'Which column do you want to see? The name of the guests.',
  FROM: 'FROM: in which table do you look?',
  TABLE: 'W.A.T.S.O.N. keeps the guest file in the table guests.',
  WHERE: 'WHERE: now say who you are looking for.',
  COL: 'Pick a column to filter. Your clues unlocked some of them.',
  OP: 'How do you compare? = is, <> is not, > more than, < less than.',
  VAL: 'Pick the value.',
  BAND: 'BETWEEN needs two values: value AND value.',
  VAL2: 'Pick the second value.',
  NEXT: 'Ready! Run it, or add AND for a second condition (max 2).',
};

function tokText(t: Tok, attrs: AttributeDef[]) {
  if (t.k === 'col') return attrs.find((a) => a.key === t.v)?.column ?? String(t.v);
  if (t.k === 'val') return t.label;
  return String(t.v);
}

export default function PoliceConsole({ crossed, onClose }: { crossed: string[]; onClose: () => void }) {
  const { view, toast } = useGame();
  const { me } = useMe(view);
  const { caseInfo, updates } = view.game;
  const attrs = caseInfo.attributes;
  const [toks, setToks] = useState<Tok[]>([]);
  const [last, setLast] = useState<QueryRecord | null>(null);
  const [busy, setBusy] = useState(false);

  // clues = reminder only, never filled in automatically
  const clues = useMemo(() => {
    const m = new Map<string, { c: Condition; confirmed: boolean; n: number }>();
    for (const u of updates) if (u.condition) m.set(JSON.stringify(u.condition), { c: u.condition, confirmed: true, n: 0 });
    for (const e of view.me.evidence) {
      if (!e.condition) continue;
      const k = JSON.stringify(e.condition);
      const prev = m.get(k);
      m.set(k, { c: e.condition, confirmed: prev?.confirmed ?? false, n: (prev?.n ?? 0) + 1 });
    }
    return [...m.values()];
  }, [view.me.evidence, updates]);
  const unlocked = new Set(clues.map((c) => c.c.attr));

  const { state, conds, curAttr } = analyse(toks);
  const curA = attrs.find((a) => a.key === curAttr);
  const complete = state === 'NEXT';
  const add = (t: Tok) => {
    setLast(null);
    setToks((l) => [...l, t]);
    buzz(10);
  };

  // which blocks can be tapped now
  const kwOk = (k: Kw) =>
    (k === 'SELECT' && state === 'SELECT') ||
    (k === 'FROM' && state === 'FROM') ||
    (k === 'WHERE' && state === 'WHERE') ||
    (k === 'BETWEEN' && state === 'OP' && curA?.type === 'number') ||
    (k === 'AND' && (state === 'BAND' || (state === 'NEXT' && conds.length < MAX_CONDS)));

  const run = async () => {
    setBusy(true);
    try {
      const rec = await emit<QueryRecord>('query:run', conds);
      setLast(rec);
      buzz(rec.names.length ? 50 : [100, 50, 100]);
      setTimeout(() => document.getElementById('q-result')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
    } catch (e) {
      toast((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const valueOptions = curA && (state === 'VAL' || state === 'VAL2') ? curA.options : [];
  const hint = state === 'NEXT' && conds.length >= MAX_CONDS ? 'Ready! Run your query (2 conditions max).' : HINT[state];

  // the contextual blocks: only what makes sense at this point of the sentence
  let palette: React.ReactNode = null;
  let paletteLabel = '';
  if (state === 'FIELD') {
    paletteLabel = 'Column to show';
    palette = <button className="blk" onClick={() => add({ k: 'field', v: 'name' })}>name</button>;
  } else if (state === 'TABLE') {
    paletteLabel = 'Table';
    palette = <button className="blk" onClick={() => add({ k: 'table', v: caseInfo.table })}>{caseInfo.table}</button>;
  } else if (state === 'COL') {
    paletteLabel = 'Columns';
    palette = attrs.map((a) => {
      const open = unlocked.has(a.key);
      return (
        <button
          key={a.key}
          className={`blk ${open ? '' : 'locked'}`}
          disabled={!open}
          title={open ? a.label : 'Locked: find a clue about it first'}
          onClick={() => add({ k: 'col', v: a.key })}
        >
          {a.column}
          <small>{open ? a.label : 'locked'}</small>
        </button>
      );
    });
  } else if (state === 'OP') {
    paletteLabel = 'Compare';
    palette = (['=', '<>', '>', '<'] as SqlOp[])
      .filter((o) => !(curA?.type === 'enum' && (o === '>' || o === '<')))
      .map((o) => (
        <button key={o} className="blk" onClick={() => add({ k: 'op', v: o })}>
          {o}
          <small>{OP_WORD[o]}</small>
        </button>
      ));
  } else if (state === 'VAL' || state === 'VAL2') {
    paletteLabel = `Values · ${curA?.label ?? ''}${curA?.unit ? ` (${curA.unit})` : ''}`;
    palette = valueOptions.map((v) => (
      <button key={String(v)} className="blk" onClick={() => add({ k: 'val', v, label: curA?.type === 'number' ? fmtValue(curA, v) : `'${v}'` })}>
        {curA?.type === 'number' ? fmtValue(curA, v) : `'${v}'`}
      </button>
    ));
  }

  return (
    <Sheet title="Police Console" icon={Icon.console} onClose={onClose} full>
      <div className="stack">
        <div className="row spread">
          <span className="small muted">1 query = 1 token</span>
          <Tokens n={me.tokens} max={caseInfo.maxTokens} />
        </div>

        {/* reminder of the clues: the player copies them into the query */}
        <div className="stack tight">
          <div className="label">My clues</div>
          {clues.length === 0 ? (
            <p className="small red">No clue yet: search a room first.</p>
          ) : (
            <div className="clue-chips">
              {clues.map(({ c, confirmed, n }) => (
                <span key={JSON.stringify(c)} className={`clue-chip ${confirmed ? 'ok' : ''}`}>
                  {describe(attrs.find((a) => a.key === c.attr), c)}
                  {confirmed ? ' ✓' : n > 1 ? ` ×${n}` : ''}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* the query being written */}
        <div>
          <div className="sql" aria-live="polite">
            <span className="prompt">&gt;</span>
            {toks.map((t, i) => (
              <span key={i} className={t.k === 'kw' ? 'kw' : t.k === 'col' ? 'col' : t.k === 'table' ? 'table' : t.k === 'val' ? 'val' : ''}>
                {tokText(t, attrs)}
              </span>
            ))}
            {complete ? <span className="kw">;</span> : <span className="caret" />}
          </div>
          <div className="row" style={{ gap: 0, justifyContent: 'flex-end' }}>
            <button className="btn ghost small" disabled={!toks.length} onClick={() => { setLast(null); setToks((l) => l.slice(0, -1)); }}>Undo</button>
            <button className="btn ghost small" disabled={!toks.length} onClick={() => { setLast(null); setToks([]); }}>Clear</button>
          </div>
        </div>

        <p className="hint"><b>NEXT</b><span>{hint}</span></p>

        <div className="stack tight">
          <div className="label">Keywords</div>
          <div className="blocks">
            {(['SELECT', 'FROM', 'WHERE', 'AND', 'BETWEEN'] as Kw[]).map((k) => (
              <button key={k} className="blk kw" disabled={!kwOk(k)} onClick={() => add({ k: 'kw', v: k })}>{k}</button>
            ))}
          </div>
        </div>
        {palette && (
          <div className="stack tight">
            <div className="label">{paletteLabel}</div>
            <div className="blocks">{palette}</div>
          </div>
        )}

        {complete && (
          <div className="note small">
            <span className="label">In English</span>
            <p style={{ marginTop: 4 }}>
              Find the guests whose <b>{conds.map((c) => describe(attrs.find((a) => a.key === c.attr), c).toLowerCase()).join(' and ')}</b>.
            </p>
          </div>
        )}
        <button className="btn red big block" disabled={!complete || busy || me.tokens < 1} onClick={run}>
          {busy ? 'Running…' : <>Run the query <span className="tok">;</span></>}
        </button>
        {me.tokens < 1 && <p className="small red center">No token left: recharge in the Server Room or wait for the next W.A.T.S.O.N. update.</p>}

        {last && (
          <div id="q-result" className="stack" style={{ scrollMarginTop: 70 }}>
            <div className="sql small">{last.sql}</div>
            <ResultTable rec={last} crossed={crossed} suspects={caseInfo.suspects} />
            <p className="small muted">Cross out the others in the Suspects tab.</p>
          </div>
        )}

        {view.me.queries.length > 0 && (
          <details className="file flush disclosure">
            <summary>
              <span className="grow">My previous queries ({view.me.queries.length})</span>
              <span className="chev">{Icon.chevron}</span>
            </summary>
            <div className="in stack tight">
              {[...view.me.queries].reverse().map((q) => (
                <div key={q.at} className="small">
                  <div className="mono">{q.sql}</div>
                  <div className={q.names.length ? 'muted' : 'red'}>→ {q.names.length ? q.names.join(' · ') : '0 suspects found'}</div>
                </div>
              ))}
            </div>
          </details>
        )}

        <button className="btn block" onClick={onClose}>Back to my turn</button>
      </div>
    </Sheet>
  );
}
