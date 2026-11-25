import { useState, type ReactNode } from 'react';
import { emit } from '../socket';
import { Bar, clockFor, Icon, Label, PawnIcon, Tokens, useGame, useMe } from '../ui';
import { JoinQr } from './Lobby';

interface Confirm { title: string; body: ReactNode; ok: string; run: () => Promise<unknown> }

/** Menu sheet: turn order, next W.A.T.S.O.N. update, rules, host controls, log. */
export default function Manor() {
  const { view, toast } = useGame();
  const { game } = view;
  const { me, myTurn, isHost, current } = useMe(view);
  const [confirm, setConfirm] = useState<Confirm | null>(null);
  const [showCode, setShowCode] = useState(false);

  const act = (event: string, ...args: unknown[]) => emit(event, ...args).catch((e: Error) => toast(e.message));
  const ordered = game.order.map((id) => game.players.find((p) => p.id === id)!).filter(Boolean);
  const every = game.caseInfo.updateEvery;
  const nextUpdate = Math.ceil(game.round / every) * every;
  const roundsLeft = nextUpdate - game.round;

  if (confirm)
    return (
      <div className="file stack">
        <Bar icon={Icon.info} color="red">Are you sure?</Bar>
        <p className="title t3">{confirm.title}</p>
        <p>{confirm.body}</p>
        <button
          className="btn red big block"
          onClick={async () => {
            await confirm.run();
            setConfirm(null);
          }}
        >
          {confirm.ok}
        </button>
        <button className="btn block" onClick={() => setConfirm(null)}>Cancel</button>
      </div>
    );

  return (
    <div className="stack">
      <div className="row spread">
        <span className="label">Round {game.round} · {clockFor(game.round)}</span>
        <span className="label">Code {game.code}</span>
      </div>

      <div className="file flush">
        <Bar icon={Icon.suspects}>Turn order</Bar>
        <div className="list">
          {ordered.map((p) => (
            <div key={p.id} className={`item ${current?.id === p.id ? 'now' : ''}`}>
              <PawnIcon pawn={p.pawn} />
              <div className="grow">
                <div className="name">{p.name}{p.id === me.id && <span className="muted"> (you)</span>}</div>
                <div className="small muted">{current?.id === p.id ? 'Playing now' : `${p.evidence} cards · ${p.queries} queries`}</div>
              </div>
              <Tokens n={p.tokens} max={game.caseInfo.maxTokens} />
              <span className={`dot ${p.connected ? '' : 'off'}`} title={p.connected ? 'online' : 'offline'} />
            </div>
          ))}
        </div>
      </div>

      <div className="note row" style={{ alignItems: 'flex-start' }}>
        <span style={{ width: 22, flex: 'none', color: '#9a6311' }}>{Icon.bolt}</span>
        <p className="small">
          <b>Next W.A.T.S.O.N. update {roundsLeft === 0 ? 'at the end of this round' : `in ${roundsLeft + 1} rounds`}.</b> One true trait of the killer for everyone, and +1 token each.
        </p>
      </div>

      <div className="file margin">
        <Label>How to play</Label>
        <ol className="small" style={{ margin: '8px 0 0', paddingLeft: 18, display: 'grid', gap: 6 }}>
          <li><b>Move</b> up to 2 rooms. <b>Once</b> on the way, search: draw and scan <b>1 card</b>.</li>
          <li><b>Or, instead of searching:</b> recharge (Server Room) or accuse (Library).</li>
          <li><b>Anytime on your turn:</b> ONE query for 1 token. Bonus cards: play them on your turn.</li>
          <li>A clue found twice is probably true. 0 suspects found? One clue is fake!</li>
        </ol>
      </div>

      {isHost && (
        <div className="file stack tight">
          <Bar icon={Icon.console} color="red">Host controls</Bar>
          {!myTurn && current && (
            <button className="btn block" onClick={() => setConfirm({ title: `Skip ${current.name}'s turn?`, body: 'Use it if this player has left or their phone is off.', ok: 'Skip turn', run: () => act('turn:end') })}>
              Skip {current.name}'s turn
            </button>
          )}
          <button
            className="btn block"
            onClick={() =>
              setConfirm({
                title: `End round ${game.round} now?`,
                body: <>The remaining turns are skipped. Round {game.round + 1} starts with {ordered[0]?.name}.{game.round % every === 0 && ' A W.A.T.S.O.N. update will be revealed.'}</>,
                ok: 'End the round',
                run: () => act('round:end'),
              })
            }
          >
            End round {game.round}
          </button>
          <button className="btn block" onClick={() => setShowCode((s) => !s)}>{showCode ? 'Hide' : 'Show'} the join QR code</button>
          {showCode && <JoinQr code={game.code} />}
          <button
            className="btn ghost block"
            style={{ color: 'var(--red)' }}
            onClick={() => setConfirm({ title: 'Dawn breaks?', body: 'Ends the game for everyone: nobody found the killer, and the solution is revealed.', ok: 'End the game', run: () => act('game:abandon') })}
          >
            End the game (the killer escapes)
          </button>
          <p className="small muted center">Your phone runs the game: keep this app open.</p>
        </div>
      )}

      <details className="file flush disclosure">
        <summary>
          <span className="grow">Case log</span>
          <span className="chev">{Icon.chevron}</span>
        </summary>
        <div className="in log">
          {[...game.log].reverse().slice(0, 25).map((e) => (
            <div key={e.id} className={`e ${e.kind}`}>
              <span className="faint">R{e.round}</span> {e.text}
            </div>
          ))}
        </div>
      </details>

    </div>
  );
}
