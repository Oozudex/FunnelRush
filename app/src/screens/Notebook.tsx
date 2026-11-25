import { useState } from 'react';
import { useGame } from '../ui';

export interface NotebookState {
  crossed: string[];
  notes: Record<string, string>;
}

export default function Notebook({ nb, setNb }: { nb: NotebookState; setNb: (n: NotebookState) => void }) {
  const { view } = useGame();
  const { suspects } = view.game.caseInfo;
  const [open, setOpen] = useState<string | null>(null);

  const hits = (name: string) => view.me.queries.filter((q) => q.names.includes(name)).length;
  const toggle = (id: string) =>
    setNb({ ...nb, crossed: nb.crossed.includes(id) ? nb.crossed.filter((x) => x !== id) : [...nb.crossed, id] });

  const left = suspects.length - nb.crossed.length;

  return (
    <div className="stack">
      <div>
        <div className="h2">Suspects</div>
        <p className="small muted">
          Your private notebook. Tap <b className="red">✗</b> to cross out a suspect. Tap a name to interrogate them.
        </p>
      </div>
      <div className="row spread pix">
        <span className="muted">Table: {view.game.caseInfo.table}</span>
        <span className={left <= 2 ? 'red' : 'muted'}>{left} / {suspects.length} still suspected</span>
      </div>

      {suspects.map((s) => {
        const out = nb.crossed.includes(s.id);
        const h = hits(s.name);
        const isOpen = open === s.id;
        return (
          <div key={s.id} className={`suspect ${out ? 'out' : ''}`}>
            <div className="srow">
              <button
                className="xbox"
                aria-pressed={out}
                aria-label={out ? `Put ${s.name} back on the list` : `Cross out ${s.name}`}
                onClick={() => toggle(s.id)}
              >
                {out ? '✗' : ''}
              </button>
              <button className="sopen" onClick={() => setOpen(isOpen ? null : s.id)} aria-expanded={isOpen}>
                <div className="sname">{s.name}</div>
                <div className="slink">{s.link}</div>
              </button>
              {h > 0 && <span className="tag amber" title="Times this name appeared in your results">{h}× hit</span>}
            </div>
            {isOpen && (
              <div style={{ paddingBottom: 10 }}>
                <div className="pix muted" style={{ margin: '0 10px 6px' }}>Interrogation</div>
                <div className="quote">“{s.statement}”</div>
                <div className="field" style={{ margin: '0 10px' }}>
                  <label htmlFor={`n-${s.id}`}>My notes</label>
                  <textarea
                    id={`n-${s.id}`}
                    className="input"
                    rows={2}
                    style={{ fontSize: 15, resize: 'vertical' }}
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
  );
}
