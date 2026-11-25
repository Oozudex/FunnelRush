import { Glitch, Logo, PawnIcon, SectionTitle, useGame, useMe } from '../ui';

export default function End() {
  const { view, leave } = useGame();
  const { game } = view;
  const { me } = useMe(view);
  const sol = game.solution;
  const winner = game.players.find((p) => p.id === game.winnerId);
  const won = winner?.id === me.id;
  const queries = view.me.queries;

  return (
    <div className="screen no-nav stack">
      <Logo small />
      <div className="center stack" style={{ gap: 6, marginTop: 8 }}>
        {won && (
          <>
            <div className="pix amber">Victory</div>
            <div className="h1"><Glitch text="CASE CLOSED" /></div>
            <p className="mono">You named the killer, detective {me.name}!</p>
          </>
        )}
        {winner && !won && (
          <>
            <div className="pix red">Defeat</div>
            <div className="h1">CASE CLOSED</div>
            <p className="mono">{winner.name} found the killer before you.</p>
          </>
        )}
        {!winner && (
          <>
            <div className="pix red">Defeat · dawn</div>
            <div className="h1 red"><Glitch text="THE KILLER ESCAPED" hard /></div>
            <p className="mono">The police arrived too late. Nobody named the killer.</p>
          </>
        )}
      </div>

      {sol && (
        <div className="panel paper">
          <div style={{ paddingLeft: 14 }}>
            <div className="ev-room">The killer</div>
            <div className="ev-obj" style={{ margin: '4px 0' }}>{sol.name}</div>
            <p className="mono small" style={{ fontWeight: 700 }}>{sol.profile}</p>
            <p className="small">{sol.story}</p>
            <div className="stamp">SOLVED</div>
          </div>
        </div>
      )}

      <SectionTitle>Detectives</SectionTitle>
      <div className="plist">
        {game.players.map((p) => (
          <div key={p.id} className={`pitem ${p.id === game.winnerId ? 'now' : ''}`}>
            <PawnIcon pawn={p.pawn} />
            <div className="grow">
              <b>{p.name}</b>
              <div className="small muted">{p.queries} queries · {p.evidence} cards scanned</div>
            </div>
            {p.id === game.winnerId && <span className="tag amber">Winner</span>}
          </div>
        ))}
      </div>

      <SectionTitle>Your SQL tonight</SectionTitle>
      <div className="h2" style={{ fontSize: 19 }}>
        You wrote <span className="red">{queries.length}</span> SQL quer{queries.length === 1 ? 'y' : 'ies'} tonight!
      </div>
      <div className="stack" style={{ gap: 6 }}>
        {queries.map((q) => (
          <div key={q.at} className="sqlbox">
            {q.sql} <span className="amber">→ {q.names.length} row{q.names.length === 1 ? '' : 's'}</span>
          </div>
        ))}
        {queries.length === 0 && <p className="small muted">No query this time. Next time, ask W.A.T.S.O.N.!</p>}
      </div>

      <button className="btn primary big block" style={{ marginTop: 16 }} onClick={leave}>
        New game
      </button>
    </div>
  );
}
