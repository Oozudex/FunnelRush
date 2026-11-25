import { useState, type ReactNode } from 'react';
import { emit } from '../socket';
import { clockFor, PawnIcon, SectionTitle, Tokens, useGame, useMe } from '../ui';
import { JoinQr } from './Lobby';

interface Confirm { title: string; body: ReactNode; ok: string; danger?: boolean; run: () => Promise<unknown> }

export default function Manor() {
  const { view, toast } = useGame();
  const { game } = view;
  const { me, myTurn, isHost, current } = useMe(view);
  const [confirm, setConfirm] = useState<Confirm | null>(null);
  const [accusing, setAccusing] = useState(false);
  const [showCode, setShowCode] = useState(false);

  const act = (event: string, ...args: unknown[]) => emit(event, ...args).catch((e: Error) => toast(e.message));
  const ordered = game.order.map((id) => game.players.find((p) => p.id === id)!).filter(Boolean);
  const every = game.caseInfo.updateEvery;
  const nextUpdate = Math.ceil(game.round / every) * every;

  return (
    <div className="stack">
      <div>
        <div className="h2">Ravenscroft Manor</div>
        <p className="small muted">Round {game.round} · {clockFor(game.round)} · game {game.code}</p>
      </div>

      {myTurn ? (
        <div className="panel alert stack">
          <div className="pix red">Your turn</div>
          <ol className="rules" style={{ margin: 0, paddingLeft: 18 }}>
            <li><b>Move</b> up to 2 rooms (or stay).</li>
            <li><b>Act</b>: Search (draw + scan), Recharge (Server Room) or Accuse (Library).</li>
            <li>Anytime: <b>Query</b> on your phone for 1 <span className="red">;</span></li>
          </ol>
          <button
            className="btn amber block"
            onClick={() =>
              setConfirm({
                title: 'Recharge',
                body: <>Only in the <b>Server Room</b>. It is your action this turn: refill to {game.caseInfo.maxTokens} tokens.</>,
                ok: "I'm in the Server Room",
                run: () => act('token:recharge'),
              })
            }
          >
            Recharge <Tokens n={game.caseInfo.maxTokens} max={game.caseInfo.maxTokens} />
          </button>
          <button className="btn block" onClick={() => setAccusing(true)}>Accuse (Library only)</button>
          <button className="btn primary big block" onClick={() => act('turn:end')}>End my turn</button>
        </div>
      ) : (
        <div className="panel flat">
          <span className="muted">Waiting for </span><b>{current?.name}</b>
          <span className="muted">. You can still scan the cards you drew and read your clues.</span>
        </div>
      )}

      <SectionTitle>Turn order</SectionTitle>
      <div className="plist">
        {ordered.map((p) => (
          <div key={p.id} className={`pitem ${current?.id === p.id ? 'now' : ''}`}>
            <PawnIcon pawn={p.pawn} />
            <div className="grow">
              <div style={{ fontWeight: 800 }}>
                {p.name} {p.id === me.id && <span className="muted">(you)</span>}
              </div>
              <div className="small muted">{p.queries} queries · {p.evidence} cards scanned</div>
            </div>
            <Tokens n={p.tokens} max={game.caseInfo.maxTokens} />
            <span className={`dot ${p.connected ? '' : 'off'}`} />
          </div>
        ))}
      </div>

      <div className="panel flat small">
        <b className="amber">W.A.T.S.O.N. update</b> at the end of round {nextUpdate}
        {nextUpdate - game.round > 0 ? ` (in ${nextUpdate - game.round + 1} rounds)` : ' (this round)'}: one true trait of the killer for everyone, and +1 <span className="red">;</span> each.
      </div>

      {isHost && (
        <>
          <SectionTitle>Host controls</SectionTitle>
          <div className="stack">
            <button
              className="btn block"
              onClick={() =>
                setConfirm({
                  title: 'End the round now?',
                  body: <>Skips the remaining turns. Round {game.round + 1} starts with {ordered[0]?.name}.{game.round % every === 0 && ' A W.A.T.S.O.N. update will be revealed.'}</>,
                  ok: 'End round',
                  run: () => act('round:end'),
                })
              }
            >
              End round {game.round}
            </button>
            {!myTurn && (
              <button className="btn block" onClick={() => act('turn:end')}>
                Skip {current?.name}'s turn
              </button>
            )}
            <button className="btn ghost block" onClick={() => setShowCode((s) => !s)}>
              {showCode ? 'Hide' : 'Show'} game code & QR (to reconnect)
            </button>
            {showCode && <JoinQr code={game.code} />}
            <button
              className="btn ghost block"
              style={{ color: 'var(--red)' }}
              onClick={() =>
                setConfirm({
                  title: 'Dawn breaks?',
                  body: 'Ends the game for everyone: nobody found the killer, and the solution is revealed.',
                  ok: 'End the game',
                  danger: true,
                  run: () => act('game:abandon'),
                })
              }
            >
              End game (the killer escapes)
            </button>
          </div>
        </>
      )}

      <SectionTitle>Case log</SectionTitle>
      <div className="log">
        {[...game.log].reverse().slice(0, 25).map((e) => (
          <div key={e.id} className={`e ${e.kind}`}>
            <span className="muted">R{e.round}</span> {e.text}
          </div>
        ))}
      </div>

      {confirm && (
        <div className="sheet" onClick={() => setConfirm(null)}>
          <div className="inner stack" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
            <div className="h2">{confirm.title}</div>
            <p>{confirm.body}</p>
            <button
              className={`btn ${confirm.danger ? 'primary' : 'amber'} big block`}
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

      {accusing && <Accuse onClose={() => setAccusing(false)} />}
    </div>
  );
}

function Accuse({ onClose }: { onClose: () => void }) {
  const { view, toast } = useGame();
  const { suspects } = view.game.caseInfo;
  const [inLibrary, setInLibrary] = useState(false);
  const [pick, setPick] = useState('');
  const [busy, setBusy] = useState(false);
  const s = suspects.find((x) => x.id === pick);

  return (
    <div className="sheet" onClick={onClose}>
      <div className="inner stack" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        <div className="pix red">Final accusation</div>
        <div className="h2">Name the killer</div>
        <label className="pitem" style={{ cursor: 'pointer' }}>
          <input type="checkbox" checked={inLibrary} onChange={(e) => setInLibrary(e.target.checked)} style={{ width: 26, height: 26, accentColor: '#E31B3B' }} />
          <span>My pawn is in the <b>Library</b>.</span>
        </label>
        <div className="field">
          <label htmlFor="who">Who is the killer?</label>
          <select id="who" className="select" value={pick} onChange={(e) => setPick(e.target.value)}>
            <option value="">Choose a suspect…</option>
            {suspects.map((x) => (
              <option key={x.id} value={x.id}>{x.name}</option>
            ))}
          </select>
        </div>
        <div className="panel paper">
          <div style={{ paddingLeft: 14 }}>
            <div className="ev-room">Say it out loud, in English:</div>
            <p className="mono" style={{ margin: '6px 0 0', fontWeight: 700 }}>
              “The killer is {s ? s.name : '________'}: __ years old, __ m tall, size __ shoes, ____-handed!”
            </p>
          </div>
        </div>
        <p className="small amber">If you are wrong: back to the Grand Hall and you lose all your tokens. You stay in the game.</p>
        <button
          className="btn primary big block"
          disabled={!inLibrary || !pick || busy}
          onClick={async () => {
            setBusy(true);
            try {
              await emit<boolean>('accuse', pick);
              onClose();
            } catch (e) {
              toast((e as Error).message);
            } finally {
              setBusy(false);
            }
          }}
        >
          I accuse {s ? s.name.split(' ').slice(-1)[0] : '…'}!
        </button>
        <button className="btn ghost block" onClick={onClose}>Cancel</button>
      </div>
    </div>
  );
}
