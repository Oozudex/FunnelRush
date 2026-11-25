import { useState } from 'react';
import type { Condition, EvidenceItem } from '../../shared/types';
import { describe } from '../../shared/sql';
import { emit } from '../socket';
import { Bar, Icon, Label, useGame, useMe } from '../ui';
import { EvidenceCard } from './Scan';

export default function Clues() {
  const { view, toast } = useGame();
  const { myTurn } = useMe(view);
  const [busy, setBusy] = useState('');
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

  // two clues that disagree on the same trait: one of them is planted (the app never says which)
  const byAttr = new Map<string, Set<string>>();
  for (const g of sorted) byAttr.set(g.c.attr, (byAttr.get(g.c.attr) ?? new Set()).add(JSON.stringify(g.c)));
  for (const u of updates) if (u.condition) byAttr.set(u.condition.attr, (byAttr.get(u.condition.attr) ?? new Set()).add(JSON.stringify(u.condition)));
  const conflicts = [...byAttr.entries()].filter(([, s]) => s.size > 1).map(([k]) => caseInfo.attributes.find((a) => a.key === k)?.label ?? k);

  const play = async (code: string) => {
    setBusy(code);
    try {
      toast(await emit<string>('bonus:play', code));
    } catch (e) {
      toast((e as Error).message);
    } finally {
      setBusy('');
    }
  };

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

      {conflicts.length > 0 && (
        <div className="note" style={{ borderColor: 'var(--red)' }}>
          <p className="small red"><b>These clues disagree: {conflicts.join(', ')}.</b></p>
          <p className="small" style={{ marginTop: 4 }}>The killer can only have one. One of them is <b>planted</b>: trust the one you saw twice.</p>
        </div>
      )}

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
          <p className="small muted" style={{ padding: '10px 14px 0' }}>Keep them face up. Play one on your turn (it is not your action), then discard it.</p>
          <div className="list">
            {bonus.map((e) => (
              <div key={e.code} className="item">
                <div className="grow">
                  <div className="name" style={e.used ? { textDecoration: 'line-through', opacity: 0.6 } : undefined}>{e.object}</div>
                  <div className="small muted">{e.text}</div>
                </div>
                {e.used ? (
                  <span className="chip">played</span>
                ) : (
                  <button className="btn primary small" disabled={!myTurn || busy === e.code} onClick={() => play(e.code)}>
                    {myTurn ? 'Play it' : 'On your turn'}
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
