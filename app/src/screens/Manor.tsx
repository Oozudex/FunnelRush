import { useState, type ReactNode } from 'react';
import { emit } from '../socket';
import { clockFor, PawnIcon, SectionTitle, Tokens, useGame, useMe } from '../ui';
import { JoinQr } from './Lobby';

interface Confirm { title: string; body: ReactNode; ok: string; run: () => Promise<unknown> }

/** "Game" tab: who plays, next W.A.T.S.O.N. update, how to play, host controls, log. */
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

  return (
    <div className="stack">
      <div>
        <div className="h2">The game</div>
        <p className="small muted">Round {game.round} · {clockFor(game.round)} · code {game.code}</p>
      </div>

      <SectionTitle>Turn order</SectionTitle>
      <div className="plist">
        {ordered.map((p) => (
          <div key={p.id} className={`pitem ${current?.id === p.id ? 'now' : ''}`}>
            <PawnIcon pawn={p.pawn} />
            <div className="grow">
              <div style={{ fontWeight: 800 }}>
                {p.name} {p.id === me.id && <span className="muted">(you)</span>}
              </div>
              <div className="small muted">{current?.id === p.id ? 'Playing now' : `${p.evidence} cards · ${p.queries} searches`}</div>
            </div>
            <Tokens n={p.tokens} max={game.caseInfo.maxTokens} />
            <span className={`dot ${p.connected ? '' : 'off'}`} title={p.connected ? 'online' : 'offline'} />
          </div>
        ))}
      </div>

      <div className="panel flat small">
        <b className="amber">⚡ Next W.A.T.S.O.N. update</b>{' '}
        {roundsLeft === 0 ? 'at the end of this round' : `in ${roundsLeft + 1} rounds`}: one true trait of the killer for everyone, and +1 <span className="red">;</span> each.
      </div>

      <SectionTitle>How to play</SectionTitle>
      <div className="panel flat small">
        <ol className="rules" style={{ margin: 0, paddingLeft: 18 }}>
          <li><b>Move</b> up to 2 rooms.</li>
          <li><b>One action</b>: search the room (scan up to {game.scansPerTurn} cards), recharge (Server Room) or accuse (Library).</li>
          <li><b>Query</b> W.A.T.S.O.N. with your clues: 1 token each.</li>
          <li>A clue found twice is probably true. 0 suspects found? One clue is fake!</li>
        </ol>
      </div>

      {isHost && (
        <details className="panel flat" style={{ padding: 12 }}>
          <summary style={{ cursor: 'pointer', fontWeight: 800 }}>Host controls</summary>
          <div className="stack" style={{ marginTop: 12 }}>
            {!myTurn && (
              <button className="btn block" onClick={() => setConfirm({ title: `Skip ${current?.name}'s turn?`, body: 'Use it if this player has left or their phone is off.', ok: 'Skip turn', run: () => act('turn:end') })}>
                Skip {current?.name}'s turn
              </button>
            )}
            <button
              className="btn block"
              onClick={() =>
                setConfirm({
                  title: 'End the round now?',
                  body: <>The remaining turns are skipped. Round {game.round + 1} starts with {ordered[0]?.name}.{game.round % every === 0 && ' A W.A.T.S.O.N. update will be revealed.'}</>,
                  ok: 'End round',
                  run: () => act('round:end'),
                })
              }
            >
              End round {game.round}
            </button>
            <button className="btn ghost block" onClick={() => setShowCode((s) => !s)}>
              {showCode ? 'Hide' : 'Show'} the game QR code
            </button>
            {showCode && <JoinQr code={game.code} />}
            <button
              className="btn ghost block"
              style={{ color: 'var(--red)' }}
              onClick={() => setConfirm({ title: 'Dawn breaks?', body: 'Ends the game for everyone: nobody found the killer, and the solution is revealed.', ok: 'End the game', run: () => act('game:abandon') })}
            >
              End the game (the killer escapes)
            </button>
            <p className="small muted" style={{ margin: 0 }}>Your phone runs the game: keep this app open.</p>
          </div>
        </details>
      )}

      <details className="panel flat" style={{ padding: 12 }}>
        <summary style={{ cursor: 'pointer', fontWeight: 800 }}>Case log</summary>
        <div className="log" style={{ marginTop: 10 }}>
          {[...game.log].reverse().slice(0, 25).map((e) => (
            <div key={e.id} className={`e ${e.kind}`}>
              <span className="muted">R{e.round}</span> {e.text}
            </div>
          ))}
        </div>
      </details>

      {confirm && (
        <div className="sheet" onClick={() => setConfirm(null)}>
          <div className="inner stack" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
            <div className="h2">{confirm.title}</div>
            <p>{confirm.body}</p>
            <button
              className="btn primary big block"
              onClick={async () => {
                await confirm.run();
                setConfirm(null);
              }}
            >
              {confirm.ok}
            </button>
            <button className="btn ghost block" onClick={() => setConfirm(null)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}
