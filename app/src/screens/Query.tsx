import { useMemo, useState } from 'react';
import type { AttributeDef, Condition, Op, QueryRecord } from '../../shared/types';
import { buildSql, describe, fmtValue, OP_LABEL, opsFor } from '../../shared/sql';
import { buzz, emit } from '../socket';
import { Glitch, SectionTitle, useGame, useMe } from '../ui';

interface Draft { attr?: string; op: Op; value?: string | number; value2?: number }

function complete(d: Draft): d is Required<Pick<Draft, 'attr' | 'value'>> & Draft {
  return !!d.attr && d.value !== undefined && (d.op !== 'between' || d.value2 !== undefined);
}

function SqlPreview({ sql }: { sql: string }) {
  const parts = sql.split(/\b(SELECT|FROM|WHERE|AND|BETWEEN)\b/);
  return (
    <div className="sqlbox" aria-label="SQL">
      💡 {parts.map((p, i) => (['SELECT', 'FROM', 'WHERE', 'AND', 'BETWEEN'].includes(p) ? <b key={i}>{p}</b> : <span key={i}>{p}</span>))}
    </div>
  );
}

function defaultValue(a: AttributeDef): string | number {
  return a.options[Math.floor(a.options.length / 2)];
}

function Block({
  d, idx, attrs, unlocked, onChange, onRemove,
}: {
  d: Draft; idx: number; attrs: AttributeDef[]; unlocked: Set<string>;
  onChange: (d: Draft) => void; onRemove?: () => void;
}) {
  const a = attrs.find((x) => x.key === d.attr);
  return (
    <div className="block">
      <div className="row spread" style={{ marginBottom: 10 }}>
        <span className="kw">{idx === 0 ? 'WHERE' : 'AND'}</span>
        {onRemove && (
          <button className="btn ghost small" onClick={onRemove} aria-label="Remove condition">✕</button>
        )}
      </div>
      {!a ? (
        <div className="attrgrid">
          {attrs.map((x) => {
            const open = unlocked.has(x.key);
            return (
              <button
                key={x.key}
                className={`attr ${open ? '' : 'locked'}`}
                disabled={!open}
                title={open ? x.label : 'Locked: scan evidence about it first'}
                onClick={() => onChange({ attr: x.key, op: '=', value: defaultValue(x) })}
              >
                {open ? '' : '🔒'} {x.label}
              </button>
            );
          })}
        </div>
      ) : (
        <div className="stack" style={{ gap: 8 }}>
          <div className="row" style={{ gap: 8 }}>
            <button className="attr on grow" style={{ minHeight: 52 }} onClick={() => onChange({ op: '=' })}>
              {a.label} ▾
            </button>
            <select
              className="select"
              style={{ width: 'auto', minWidth: 130 }}
              value={d.op}
              aria-label="Operator"
              onChange={(e) => {
                const op = e.target.value as Op;
                const i = a.options.indexOf(d.value as never);
                onChange({ ...d, op, value2: op === 'between' ? (a.options[Math.min(a.options.length - 1, i + 3)] as number) : undefined });
              }}
            >
              {opsFor(a).map((o) => (
                <option key={o} value={o}>{OP_LABEL[o]}</option>
              ))}
            </select>
          </div>
          <div className="row" style={{ gap: 8 }}>
            <select
              className="select grow"
              aria-label="Value"
              value={String(d.value)}
              onChange={(e) => onChange({ ...d, value: a.type === 'number' ? Number(e.target.value) : e.target.value })}
            >
              {a.options.map((o) => (
                <option key={String(o)} value={String(o)}>{fmtValue(a, o)}{a.type === 'number' && a.unit ? ` ${a.unit}` : ''}</option>
              ))}
            </select>
            {d.op === 'between' && (
              <>
                <span className="kw">AND</span>
                <select
                  className="select grow"
                  aria-label="Upper value"
                  value={String(d.value2)}
                  onChange={(e) => onChange({ ...d, value2: Number(e.target.value) })}
                >
                  {a.options.map((o) => (
                    <option key={String(o)} value={String(o)}>{fmtValue(a, o)}</option>
                  ))}
                </select>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export function ResultTable({ rec, crossed, suspects }: { rec: QueryRecord; crossed: string[]; suspects: { id: string; name: string; link: string }[] }) {
  if (rec.names.length === 0)
    return (
      <div className="zero panel alert">
        <div className="h2"><Glitch text="0 SUSPECTS FOUND" hard /></div>
        <p className="mono" style={{ marginTop: 10 }}>Empty result. One of your conditions is false.</p>
        <p className="small muted" style={{ margin: 0 }}>Golden rule: 0 suspects found? One of your clues is fake!</p>
      </div>
    );
  return (
    <div className="panel flat" style={{ padding: 0 }}>
      <table className="result-table">
        <thead>
          <tr><th>#</th><th>name</th><th>link to Victor</th></tr>
        </thead>
        <tbody>
          {rec.names.map((n, i) => {
            const s = suspects.find((x) => x.name === n);
            return (
              <tr key={n} className={s && crossed.includes(s.id) ? 'crossed' : ''}>
                <td className="muted">{i + 1}</td>
                <td style={{ fontWeight: 700 }}>{n}</td>
                <td className="small muted">{s?.link}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <div className="pix muted" style={{ padding: '8px 10px', fontSize: 11 }}>
        {rec.names.length} row{rec.names.length > 1 ? 's' : ''} · private result
      </div>
    </div>
  );
}

export default function Query({ crossed }: { crossed: string[] }) {
  const { view, toast } = useGame();
  const { me, myTurn, current } = useMe(view);
  const { caseInfo, updates } = view.game;
  const attrs = caseInfo.attributes;
  const [drafts, setDrafts] = useState<Draft[]>([{ op: '=' }]);
  const [last, setLast] = useState<QueryRecord | null>(null);
  const [busy, setBusy] = useState(false);

  const unlocked = useMemo(() => {
    const s = new Set<string>();
    view.me.evidence.forEach((e) => e.condition && s.add(e.condition.attr));
    updates.forEach((u) => u.condition && s.add(u.condition.attr));
    return s;
  }, [view.me.evidence, updates]);

  // Quick-fill chips: every distinct clue you hold
  const chips = useMemo(() => {
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

  const ready = drafts.filter(complete);
  const allReady = ready.length === drafts.length && ready.length > 0;
  const sql = buildSql(caseInfo.table, attrs, ready as Condition[]);

  const addChip = (c: Condition) => {
    const nd: Draft = { ...c };
    setDrafts((ds) => {
      const empty = ds.findIndex((d) => !d.attr);
      if (empty >= 0) return ds.map((d, i) => (i === empty ? nd : d));
      if (ds.length < 2) return [...ds, nd];
      return [ds[0], nd];
    });
  };

  const run = async () => {
    setBusy(true);
    try {
      const rec = await emit<QueryRecord>('query:run', ready);
      setLast(rec);
      buzz(rec.names.length ? 50 : [100, 50, 100]);
      setTimeout(() => document.getElementById('q-result')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
    } catch (e) {
      toast((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  let reason = '';
  if (!myTurn) reason = `Wait for your turn (${current?.name ?? '…'} is playing).`;
  else if (me.tokens < 1) reason = 'No token left: recharge in the Server Room, or wait for the next W.A.T.S.O.N. update.';
  else if (unlocked.size === 0) reason = 'Every column is locked 🔒. Scan evidence to unlock them.';
  else if (!allReady) reason = 'Choose a column for each condition.';

  return (
    <div className="stack">
      <div>
        <div className="h2">Police Console</div>
        <p className="small muted">Search W.A.T.S.O.N.'s guest file. 1 query = <b className="red">1 ;</b> token, up to 2 conditions.</p>
      </div>

      {chips.length > 0 && (
        <div>
          <div className="pix muted" style={{ marginBottom: 8 }}>From your clues (tap to use)</div>
          <div className="chips">
            {chips.map(({ c, confirmed, n }) => (
              <button key={JSON.stringify(c)} className={`chip ${confirmed ? 'confirmed' : ''}`} onClick={() => addChip(c)}>
                {describe(attrs.find((a) => a.key === c.attr), c)}
                {confirmed ? ' ✔' : n > 1 ? ` ×${n}` : ''}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="sentence">
        <span className="kw">FIND</span> guests…
      </div>
      {drafts.map((d, i) => (
        <Block
          key={i}
          d={d}
          idx={i}
          attrs={attrs}
          unlocked={unlocked}
          onChange={(nd) => setDrafts((ds) => ds.map((x, j) => (j === i ? nd : x)))}
          onRemove={drafts.length > 1 ? () => setDrafts((ds) => ds.filter((_, j) => j !== i)) : undefined}
        />
      ))}
      {drafts.length < 2 && (
        <button className="btn ghost block" onClick={() => setDrafts((ds) => [...ds, { op: '=' }])}>
          + AND another condition
        </button>
      )}

      <SqlPreview sql={sql} />

      <button className="btn primary big block" disabled={!!reason || busy} onClick={run}>
        {busy ? 'Querying…' : <>Run query · 1 <span style={{ fontSize: 24 }}>;</span></>}
      </button>
      {reason && <p className="small amber center" style={{ margin: 0 }}>{reason}</p>}

      {last && (
        <div id="q-result" className="stack" style={{ scrollMarginTop: 120 }}>
          <SectionTitle>Result</SectionTitle>
          <SqlPreview sql={last.sql} />
          <ResultTable rec={last} crossed={crossed} suspects={caseInfo.suspects} />
        </div>
      )}

      {view.me.queries.length > 0 && (
        <>
          <SectionTitle>Your queries tonight ({view.me.queries.length})</SectionTitle>
          <div className="stack" style={{ gap: 8 }}>
            {[...view.me.queries].reverse().map((q) => (
              <details key={q.at} className="panel flat" style={{ padding: 10 }}>
                <summary style={{ cursor: 'pointer', minHeight: 32 }}>
                  <span className="mono small">{q.sql}</span>{' '}
                  <span className={q.names.length ? 'amber' : 'red'} style={{ fontWeight: 800 }}>
                    → {q.names.length} row{q.names.length === 1 ? '' : 's'}
                  </span>
                </summary>
                <div className="small" style={{ marginTop: 8 }}>
                  {q.names.length ? q.names.join(' · ') : '0 suspects found'}
                  <span className="muted"> (round {q.round})</span>
                </div>
              </details>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
