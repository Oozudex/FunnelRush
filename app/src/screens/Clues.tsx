import type { Condition, EvidenceItem } from '../../shared/types';
import { describe } from '../../shared/sql';
import { Bar, Icon, Label, useGame } from '../ui';
import { EvidenceCard } from './Scan';

export default function Clues() {
  const { view } = useGame();
  const { caseInfo, updates } = view.game;
  const ev = view.me.evidence;
  const groups = new Map<string, { c: Condition; items: EvidenceItem[] }>();
  for (const e of ev.filter((x) => x.kind === 'trait')) {
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
        <div className="title t2">My clues</div>
        <p className="small muted" style={{ marginTop: 4 }}>Private. Some clues are fake, planted by the killer.</p>
      </div>

      <div className="note typed">
        <p>“Find the same clue twice, and it's probably true.”</p>
        <p style={{ marginTop: 4 }}>“0 suspects found? One of your clues is fake!”</p>
      </div>

      {updates.length > 0 && (
        <div className="file flush">
          <Bar icon={Icon.bolt} color="amber">W.A.T.S.O.N. · confirmed true</Bar>
          <div className="list">
            {updates.map((u) => (
              <div key={u.round} className="item">
                <span className="chip ink">R{u.round}</span>
                <span className="grow mono small" style={{ fontWeight: 700 }}>{u.text}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="file flush">
        <Bar icon={Icon.clues} color="blue" end={<span>{sorted.length}</span>}>Traits of the killer</Bar>
        {sorted.length === 0 ? (
          <p className="small muted" style={{ padding: 14 }}>No clue yet. Search a room and scan a card.</p>
        ) : (
          <div className="list">
            {sorted.map(({ c, items }) => {
              const attr = caseInfo.attributes.find((a) => a.key === c.attr);
              const isConfirmed = confirmed.has(JSON.stringify(c));
              const strong = items.length > 1 || isConfirmed;
              return (
                <div key={JSON.stringify(c)} className="item" style={{ alignItems: 'flex-start' }}>
                  <div className="grow">
                    <div className="mono" style={{ fontWeight: 700, fontSize: 16 }}>{describe(attr, c)}</div>
                    <div className="small muted" style={{ marginTop: 2 }}>
                      {items.map((i) => `${i.object} (${i.code})`).join(' · ')}
                    </div>
                    {isConfirmed && <div className="small" style={{ color: 'var(--green)', fontWeight: 700, marginTop: 2 }}>✓ Confirmed by W.A.T.S.O.N.</div>}
                  </div>
                  <span className={`chip ${strong ? 'red' : ''}`}>seen ×{items.length}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {deadends.length > 0 && (
        <div className="stack tight">
          <Label>Dead ends ({deadends.length})</Label>
          {deadends.map((e) => (
            <details key={e.code} className="file flush disclosure">
              <summary>
                <span className="mono small faint">{e.code}</span>
                <span className="grow">{e.object}</span>
                <span className="chev">{Icon.chevron}</span>
              </summary>
              <div className="in"><EvidenceCard item={e} /></div>
            </details>
          ))}
        </div>
      )}

      {bonus.length > 0 && (
        <div className="file flush">
          <Bar icon={Icon.bolt} color="amber">Bonus cards</Bar>
          <div className="list">
            {bonus.map((e) => (
              <div key={e.code} className="item">
                <div className="grow">
                  <div className="name">{e.object}</div>
                  <div className="small muted">{e.text}</div>
                </div>
                <span className="chip">{e.code}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
