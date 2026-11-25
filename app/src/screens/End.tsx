import { Bar, Icon, Logo, PawnIcon, useGame, useMe } from '../ui';

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

      <div className="file center stack" style={{ padding: '24px 16px' }}>
        <div><span className="stamp big">{winner ? 'Case closed' : 'Escaped'}</span></div>
        <p className="title t3" style={{ marginTop: 6 }}>
          {won ? 'Victory!' : winner ? 'Defeat' : 'Defeat · dawn'}
        </p>
        <p className="typed" style={{ fontSize: 17 }}>
          {won
            ? `You named the killer, detective ${me.name}!`
            : winner
              ? `${winner.name} found the killer before you.`
              : 'The police arrived too late. Nobody named the killer.'}
        </p>
      </div>

      {sol && (
        <div className="file margin">
          <Bar icon={Icon.scale} color="red">The killer</Bar>
          <div className="title t2">{sol.name}</div>
          <p className="mono small" style={{ fontWeight: 700, marginTop: 8 }}>{sol.profile}</p>
          <p className="typed" style={{ marginTop: 10 }}>{sol.story}</p>
          <div style={{ marginTop: 14 }}><span className="stamp">Solved</span></div>
        </div>
      )}

      <div className="file flush">
        <Bar icon={Icon.suspects}>Detectives</Bar>
        <div className="list">
          {game.players.map((p) => (
            <div key={p.id} className={`item ${p.id === game.winnerId ? 'now' : ''}`}>
              <PawnIcon pawn={p.pawn} />
              <div className="grow">
                <div className="name">{p.name}</div>
                <div className="small muted">{p.queries} queries · {p.evidence} cards scanned</div>
              </div>
              {p.id === game.winnerId && <span className="chip red">Winner</span>}
            </div>
          ))}
        </div>
      </div>

      <div className="file stack tight">
        <Bar icon={Icon.console}>Your SQL tonight</Bar>
        <p className="title t3">
          You wrote <span className="red">{queries.length}</span> SQL quer{queries.length === 1 ? 'y' : 'ies'}!
        </p>
        {queries.map((q) => (
          <div key={q.at} className="sql small">
            <span>{q.sql}</span>
            <span className="kw">→ {q.names.length} row{q.names.length === 1 ? '' : 's'}</span>
          </div>
        ))}
        {queries.length === 0 && <p className="small muted">No query this time. Next time, ask W.A.T.S.O.N.!</p>}
      </div>

      <button className="btn primary big block" onClick={leave}>New game</button>
    </div>
  );
}
