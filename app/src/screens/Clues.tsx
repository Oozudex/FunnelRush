import type { Condition, EvidenceItem } from '../../shared/types';
import { describe } from '../../shared/sql';
import { SectionTitle, useGame } from '../ui';
import { EvidenceCard } from './Scan';

export default function Clues() {
  const { view } = useGame();
  const { caseInfo, updates } = view.game;
  const ev = view.me.evidence;
  const traits = ev.filter((e) => e.kind === 'trait');
  const groups = new Map<string, { c: Condition; items: EvidenceItem[] }>();
  for (const e of traits) {
    const k = JSON.stringify(e.condition);
    const g = groups.get(k) ?? { c: e.condition!, items: [] };
    g.items.push(e);
    groups.set(k, g);
  }
  const sorted = [...groups.values()].sort((a, b) => b.items.length - a.items.length);
  const confirmed = new Set(updates.map((u) => JSON.stringify(u.condition)));
  const deadends = ev.filter((e) => e.kind === 'deadend');
  const bonus = ev.filter((e) => e.kind === 'bonus');

  return (
    <div className="stack">
      <div>
        <div className="h2">My clues</div>
        <p className="small muted">Private. Some clues are fake, planted by the killer.</p>
      </div>

      <div className="panel alert">
        <div className="pix red" style={{ marginBottom: 6 }}>Golden rules</div>
        <p className="mono" style={{ margin: '0 0 6px' }}>“Find the same clue twice, and it's probably true.”</p>
        <p className="mono" style={{ margin: 0 }}>“0 suspects found? One of your clues is fake!”</p>
      </div>

      {updates.length > 0 && (
        <>
          <SectionTitle>W.A.T.S.O.N. updates · confirmed</SectionTitle>
          {updates.map((u) => (
            <div key={u.round} className="pitem" style={{ borderColor: 'var(--amber)' }}>
              <span className="tag amber">R{u.round}</span>
              <span className="grow mono small">{u.text}</span>
              <span className="amber">✔</span>
            </div>
          ))}
        </>
      )}

      <SectionTitle>Traits of the killer ({sorted.length})</SectionTitle>
      {sorted.length === 0 && <p className="small muted">No clue yet. Search a room and scan the card.</p>}
      {sorted.map(({ c, items }) => {
        const attr = caseInfo.attributes.find((a) => a.key === c.attr);
        const isConfirmed = confirmed.has(JSON.stringify(c));
        return (
          <div key={JSON.stringify(c)} className={`panel ${items.length > 1 || isConfirmed ? 'alert' : 'flat'}`} style={{ padding: 12 }}>
            <div className="row spread">
              <div className="mono" style={{ fontWeight: 700, fontSize: 17 }}>{describe(attr, c)}</div>
              <span className={`tag ${items.length > 1 ? 'red' : 'muted'}`}>seen ×{items.length}</span>
            </div>
            <div className="small muted" style={{ marginTop: 4 }}>
              {items.map((i) => `${i.object} (${i.room}, ${i.code})`).join(' · ')}
            </div>
            {isConfirmed && <div className="small amber" style={{ marginTop: 4 }}>✔ Confirmed by W.A.T.S.O.N.</div>}
          </div>
        );
      })}

      {deadends.length > 0 && (
        <>
          <SectionTitle>Dead ends ({deadends.length})</SectionTitle>
          {deadends.map((e) => (
            <details key={e.code} className="pitem" style={{ display: 'block' }}>
              <summary style={{ cursor: 'pointer' }}>
                <span className="mono small muted">{e.code}</span> <b>{e.object}</b>
              </summary>
              <div style={{ marginTop: 10 }}><EvidenceCard item={e} /></div>
            </details>
          ))}
        </>
      )}

      {bonus.length > 0 && (
        <>
          <SectionTitle>Bonus cards</SectionTitle>
          {bonus.map((e) => (
            <div key={e.code} className="pitem">
              <span className="tag amber">{e.code}</span>
              <span className="grow"><b>{e.object}</b> <span className="small muted">{e.text}</span></span>
            </div>
          ))}
        </>
      )}
    </div>
  );
}
