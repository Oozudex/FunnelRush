import { useState } from 'react';
import { Bar, Icon, useGame } from '../ui';

export interface NotebookState {
  crossed: string[];
  notes: Record<string, string>;
}

export default function Notebook({ nb, setNb }: { nb: NotebookState; setNb: (n: NotebookState) => void }) {
  const { view } = useGame();
  const { suspects, table } = view.game.caseInfo;
  const [open, setOpen] = useState<string | null>(null);

  const hits = (name: string) => view.me.queries.filter((q) => q.names.includes(name)).length;
  const toggle = (id: string) =>
    setNb({ ...nb, crossed: nb.crossed.includes(id) ? nb.crossed.filter((x) => x !== id) : [...nb.crossed, id] });
  const left = suspects.length - nb.crossed.length;

  return (
    <div className="stack">
      <div>
        <div className="title t2">Suspects</div>
        <p className="small muted" style={{ marginTop: 4 }}>Tap the box to cross a suspect out. Tap a name to read their statement.</p>
      </div>

      <div className="file flush">
        <Bar icon={Icon.suspects} end={<span className={left <= 2 ? '' : ''}>{left} / {suspects.length} left</span>}>Table · {table}</Bar>
        <div>
          {suspects.map((s) => {
            const out = nb.crossed.includes(s.id);
            const h = hits(s.name);
            const isOpen = open === s.id;
            return (
              <div key={s.id} className={`suspect ${out ? 'out' : ''} ${isOpen ? 'open' : ''}`}>
                <div className="srow">
                  <button
                    className="xbox"
                    aria-pressed={out}
                    aria-label={out ? `Put ${s.name} back on the list` : `Cross out ${s.name}`}
                    onClick={() => toggle(s.id)}
                  >
                    <span>{out ? '✗' : ''}</span>
                  </button>
                  <button className="sopen row" style={{ gap: 8 }} onClick={() => setOpen(isOpen ? null : s.id)} aria-expanded={isOpen}>
                    <span className="grow">
                      <span className="sname" style={{ display: 'block' }}>{s.name}</span>
                      <span className="slink">{s.link}</span>
                    </span>
                    {h > 0 && <span className="chip" title="Times this name appeared in your query results">{h}× in results</span>}
                    <span className="chev">{Icon.chevron}</span>
                  </button>
                </div>
                {isOpen && (
                  <div className="more">
                    <div className="quote">“{s.statement}”</div>
                    <div className="field">
                      <label htmlFor={`n-${s.id}`}>My notes</label>
                      <textarea
                        id={`n-${s.id}`}
                        className="input"
                        rows={2}
                        value={nb.notes[s.id] ?? ''}
                        onChange={(e) => setNb({ ...nb, notes: { ...nb.notes, [s.id]: e.target.value } })}
                      />
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
