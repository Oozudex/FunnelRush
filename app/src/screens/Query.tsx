import { useMemo, useState } from 'react';
import type { AttributeDef, Condition, Op, QueryRecord } from '../../shared/types';
import { buildSql, describe, fmtValue, OP_LABEL, opsFor } from '../../shared/sql';
import { buzz, emit } from '../socket';
import { Glitch, Tokens, useGame, useMe } from '../ui';

const same = (a: Condition, b: Condition) => JSON.stringify(a) === JSON.stringify(b);

function SqlPreview({ sql }: { sql: string }) {
  const parts = sql.split(/\b(SELECT|FROM|WHERE|AND|BETWEEN)\b/);
  return (
    <div className="sqlbox" aria-label="SQL">
      💡 {parts.map((p, i) => (['SELECT', 'FROM', 'WHERE', 'AND', 'BETWEEN'].includes(p) ? <b key={i}>{p}</b> : <span key={i}>{p}</span>))}
    </div>
  );
}

export function ResultTable({ rec, crossed, suspects }: { rec: QueryRecord; crossed: string[]; suspects: { id: string; name: string; link: string }[] }) {
  if (rec.names.length === 0)
    return (
      <div className="zero panel alert">
        <div className="h2"><Glitch text="0 SUSPECTS FOUND" hard /></div>
        <p className="mono" style={{ marginTop: 10 }}>Nobody matches all your conditions.</p>
        <p className="small muted" style={{ margin: 0 }}>Golden rule: one of your clues is fake!</p>
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
        {rec.names.length} suspect{rec.names.length > 1 ? 's' : ''} found · only you see this
      </div>
    </div>
  );
}

/** "Write your own condition": one line, only with the columns your clues unlocked. */
function CustomCondition({ attrs, onAdd }: { attrs: AttributeDef[]; onAdd: (c: Condition) => void }) {
  const [key, setKey] = useState(attrs[0]?.key ?? '');
  const a = attrs.find((x) => x.key === key) ?? attrs[0];
  const [op, setOp] = useState<Op>('=');
  const [value, setValue] = useState<string>('');
  const [value2, setValue2] = useState<string>('');
  if (!a) return <p className="small muted">Scan evidence first: each clue unlocks a column 🔒.</p>;
  const opts = a.options.map(String);
  const v = opts.includes(value) ? value : opts[Math.floor(opts.length / 2)];
  const v2 = opts.includes(value2) ? value2 : opts[Math.min(opts.length - 1, opts.indexOf(v) + 3)];
  const num = (x: string) => (a.type === 'number' ? Number(x) : x);
  const label = (x: string | number) => `${fmtValue(a, x)}${a.type === 'number' && a.unit ? ` ${a.unit}` : ''}`;
  return (
    <div className="stack" style={{ gap: 8 }}>
      <div className="row" style={{ gap: 8 }}>
        <select className="select grow" aria-label="Column" value={a.key} onChange={(e) => { setKey(e.target.value); setOp('='); setValue(''); }}>
          {attrs.map((x) => <option key={x.key} value={x.key}>{x.label}</option>)}
        </select>
        <select className="select" style={{ width: 'auto' }} aria-label="Operator" value={op} onChange={(e) => setOp(e.target.value as Op)}>
          {opsFor(a).map((o) => <option key={o} value={o}>{OP_LABEL[o]}</option>)}
        </select>
      </div>
      <div className="row" style={{ gap: 8 }}>
        <select className="select grow" aria-label="Value" value={v} onChange={(e) => setValue(e.target.value)}>
          {a.options.map((o) => <option key={String(o)} value={String(o)}>{label(o)}</option>)}
        </select>
        {op === 'between' && (
          <>
            <span className="kw">AND</span>
            <select className="select grow" aria-label="Upper value" value={v2} onChange={(e) => setValue2(e.target.value)}>
              {a.options.map((o) => <option key={String(o)} value={String(o)}>{label(o)}</option>)}
            </select>
          </>
        )}
      </div>
      <button
        className="btn block"
        onClick={() => onAdd({ attr: a.key, op, value: num(v), ...(op === 'between' ? { value2: Number(v2) } : {}) })}
      >
        + Add this condition
      </button>
    </div>
  );
}

/** Police Console: tick 1 or 2 of your clues, run, read the private result. */
export default function PoliceConsole({ crossed, onClose }: { crossed: string[]; onClose: () => void }) {
  const { view, toast } = useGame();
  const { me } = useMe(view);
  const { caseInfo, updates } = view.game;
  const attrs = caseInfo.attributes;
  const [picked, setPicked] = useState<Condition[]>([]);
  const [last, setLast] = useState<QueryRecord | null>(null);
  const [busy, setBusy] = useState(false);

  const clues = useMemo(() => {
    const m = new Map<string, { c: Condition; confirmed: boolean; n: number }>();
    for (const u of updates) if (u.condition) m.set(JSON.stringify(u.condition), { c: u.condition, confirmed: true, n: 0 });
    for (const e of view.me.evidence) {
      if (!e.condition) continue;
      const k = JSON.stringify(e.condition);
      const prev = m.get(k);
      m.set(k, { c: e.condition, confirmed: prev?.confirmed ?? false, n: (prev?.n ?? 0) + 1 });
    }
    return [...m.values()].sort((x, y) => Number(y.confirmed) - Number(x.confirmed) || y.n - x.n);
  }, [view.me.evidence, updates]);

  const unlockedAttrs = attrs.filter((a) => clues.some((c) => c.c.attr === a.key));

  const toggle = (c: Condition) => {
    setLast(null);
    setPicked((p) => {
      if (p.some((x) => same(x, c))) return p.filter((x) => !same(x, c));
      if (p.length >= 2) {
        toast('2 conditions max per query. Untick one first.');
        return p;
      }
      return [...p, c];
    });
  };

  const run = async () => {
    setBusy(true);
    try {
      const rec = await emit<QueryRecord>('query:run', picked);
      setLast(rec);
      buzz(rec.names.length ? 50 : [100, 50, 100]);
      setTimeout(() => document.getElementById('q-result')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
    } catch (e) {
      toast((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const sentence = picked.map((c) => describe(attrs.find((a) => a.key === c.attr), c).toLowerCase()).join(' AND ');

  return (
    <div className="sheet full" role="dialog" aria-modal="true" aria-label="Police Console">
      <div className="inner stack">
        <div className="row spread">
          <div>
            <div className="h2">Police Console</div>
            <div className="small muted">Search W.A.T.S.O.N.'s guest file</div>
          </div>
          <button className="btn ghost small" onClick={onClose} aria-label="Close">✕ Close</button>
        </div>
        <div className="row spread panel flat" style={{ padding: '8px 12px' }}>
          <span className="small">1 search = 1 token</span>
          <Tokens n={me.tokens} max={caseInfo.maxTokens} />
        </div>

        <div className="step-title"><span className="num">1</span> Tick 1 or 2 of your clues</div>
        {clues.length === 0 && <p className="small amber">No clue yet. Search a room and scan a card first.</p>}
        <div className="stack" style={{ gap: 8 }}>
          {clues.map(({ c, confirmed, n }) => {
            const on = picked.some((x) => same(x, c));
            return (
              <button key={JSON.stringify(c)} className={`tick ${on ? 'on' : ''}`} onClick={() => toggle(c)} aria-pressed={on}>
                <span className="box">{on ? '✓' : ''}</span>
                <span className="grow">
                  <span className="mono" style={{ fontWeight: 700 }}>{describe(attrs.find((a) => a.key === c.attr), c)}</span>
                  <span className="small muted" style={{ display: 'block' }}>
                    {confirmed ? '✔ confirmed by W.A.T.S.O.N.' : n > 1 ? `seen ×${n}: probably true` : 'seen once'}
                  </span>
                </span>
              </button>
            );
          })}
          {picked.filter((p) => !clues.some((c) => same(c.c, p))).map((c) => (
            <button key={JSON.stringify(c)} className="tick on" onClick={() => toggle(c)} aria-pressed>
              <span className="box">✓</span>
              <span className="grow mono" style={{ fontWeight: 700 }}>{describe(attrs.find((a) => a.key === c.attr), c)}</span>
            </button>
          ))}
        </div>

        {clues.length > 0 && (
          <details className="panel flat" style={{ padding: 12 }}>
            <summary style={{ cursor: 'pointer', fontWeight: 800 }}>Or write your own condition</summary>
            <div style={{ marginTop: 10 }}>
              <CustomCondition attrs={unlockedAttrs} onAdd={(c) => (picked.some((x) => same(x, c)) ? null : toggle(c))} />
            </div>
          </details>
        )}

        <div className="step-title"><span className="num">2</span> Search</div>
        <div className="panel flat" style={{ padding: 12 }}>
          <p style={{ margin: '0 0 8px' }}>
            {picked.length ? <>Find the guests whose <b>{sentence}</b>.</> : <span className="muted">Tick a clue above.</span>}
          </p>
          <SqlPreview sql={buildSql(caseInfo.table, attrs, picked)} />
        </div>
        <button className="btn primary big block" disabled={!picked.length || busy || me.tokens < 1} onClick={run}>
          {busy ? 'Searching…' : <>Search · 1 <span style={{ fontSize: 24 }}>;</span></>}
        </button>
        {me.tokens < 1 && <p className="small amber center" style={{ margin: 0 }}>No token left: recharge in the Server Room or wait for the next W.A.T.S.O.N. update.</p>}

        {last && (
          <div id="q-result" className="stack" style={{ scrollMarginTop: 20 }}>
            <div className="step-title"><span className="num">3</span> Result</div>
            <ResultTable rec={last} crossed={crossed} suspects={caseInfo.suspects} />
            <p className="small muted" style={{ margin: 0 }}>Cross out the others in the Suspects tab.</p>
          </div>
        )}

        {view.me.queries.length > 0 && (
          <details className="panel flat" style={{ padding: 12 }}>
            <summary style={{ cursor: 'pointer', fontWeight: 800 }}>My previous searches ({view.me.queries.length})</summary>
            <div className="stack" style={{ gap: 8, marginTop: 10 }}>
              {[...view.me.queries].reverse().map((q) => (
                <div key={q.at} className="small">
                  <div className="mono">{q.sql}</div>
                  <div className={q.names.length ? 'amber' : 'red'}>→ {q.names.length ? q.names.join(' · ') : '0 suspects found'}</div>
                </div>
              ))}
            </div>
          </details>
        )}

        <button className="btn ghost block" onClick={onClose}>Back to my turn</button>
      </div>
    </div>
  );
}
