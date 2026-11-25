import { useEffect, useRef, useState } from 'react';
import { buzz, persist, store } from '../socket';
import { clockFor, Glitch, Icon, PawnIcon, Tokens, useGame, useMe } from '../ui';
import Scan from './Scan';
import Query from './Query';
import Clues from './Clues';
import Notebook, { type NotebookState } from './Notebook';
import Manor from './Manor';

type Tab = 'scan' | 'query' | 'clues' | 'notebook' | 'manor';
const TABS: { id: Tab; label: string }[] = [
  { id: 'scan', label: 'Scan' },
  { id: 'query', label: 'Query' },
  { id: 'clues', label: 'Clues' },
  { id: 'notebook', label: 'Suspects' },
  { id: 'manor', label: 'Manor' },
];

export default function GameScreen() {
  const { view, toast } = useGame();
  const { game } = view;
  const { me, current, myTurn } = useMe(view);
  const key = `tlq.${game.code}.${me.id}`;
  const [tab, setTabRaw] = useState<Tab>(store(`${key}.tab`, 'scan'));
  const setTab = (t: Tab) => {
    setTabRaw(t);
    persist(`${key}.tab`, t);
    window.scrollTo({ top: 0 });
  };

  // Notebook (private, kept on this phone)
  const [nb, setNb] = useState<NotebookState>(store(`${key}.nb`, { crossed: [], notes: {} }));
  const updateNb = (n: NotebookState) => {
    setNb(n);
    persist(`${key}.nb`, n);
  };

  // W.A.T.S.O.N. update overlay
  const [seenUpdates, setSeenUpdates] = useState<number>(store(`${key}.seenUpd`, 0));
  const showUpdate = game.updates.length > seenUpdates ? game.updates[game.updates.length - 1] : null;
  useEffect(() => {
    if (showUpdate) buzz([80, 60, 80, 60, 200]);
  }, [showUpdate]);
  const closeUpdate = () => {
    setSeenUpdates(game.updates.length);
    persist(`${key}.seenUpd`, game.updates.length);
  };

  // Accusation overlay
  const [seenAcc, setSeenAcc] = useState<number>(store(`${key}.seenAcc`, 0));
  const acc = game.lastAccusation && game.lastAccusation.at > seenAcc && !game.lastAccusation.correct ? game.lastAccusation : null;
  const closeAcc = () => {
    if (!game.lastAccusation) return;
    setSeenAcc(game.lastAccusation.at);
    persist(`${key}.seenAcc`, game.lastAccusation.at);
  };

  // Your turn ping
  const wasMyTurn = useRef(myTurn);
  useEffect(() => {
    if (myTurn && !wasMyTurn.current) {
      buzz([60, 40, 60]);
      toast("It's your turn, detective!", true);
    }
    wasMyTurn.current = myTurn;
  }, [myTurn, toast]);

  const nextUpdate = Math.ceil(game.round / game.caseInfo.updateEvery) * game.caseInfo.updateEvery;
  const accuser = acc && game.players.find((p) => p.id === acc.playerId);

  return (
    <>
      <header className="topbar">
        <div className="row spread">
          <div>
            <div className="pix muted" style={{ fontSize: 10 }}>Round {game.round} · next update R{nextUpdate}</div>
            <div className="clock">{clockFor(game.round)}</div>
          </div>
          <div className="row" style={{ gap: 8 }}>
            <span className="pix muted" style={{ fontSize: 10 }}>Tokens</span>
            <Tokens n={me.tokens} max={game.caseInfo.maxTokens} />
          </div>
        </div>
        <div className={`turnbar ${myTurn ? 'mine' : ''}`}>
          {current && <span className="pawnbg"><PawnIcon pawn={current.pawn} /></span>}
          <span className="grow">{myTurn ? 'Your turn: move, then act' : `${current?.name ?? '…'}'s turn`}</span>
        </div>
      </header>

      <main className="screen">
        {tab === 'scan' && <Scan />}
        {tab === 'query' && <Query crossed={nb.crossed} />}
        {tab === 'clues' && <Clues />}
        {tab === 'notebook' && <Notebook nb={nb} setNb={updateNb} />}
        {tab === 'manor' && <Manor />}
      </main>

      <nav className="nav" aria-label="Police Console">
        {TABS.map((t) => (
          <button key={t.id} className={tab === t.id ? 'on' : ''} onClick={() => setTab(t.id)} aria-current={tab === t.id}>
            {Icon[t.id]}
            {t.label}
            {t.id === 'clues' && view.me.evidence.length > 0 && <span className="badge">{view.me.evidence.length}</span>}
          </button>
        ))}
      </nav>

      {showUpdate && (
        <div className="overlay" role="dialog" aria-modal="true">
          <div className="inner stack center">
            <div className="pix amber">⚡ Lightning strike · end of round {showUpdate.round}</div>
            <div className="h1"><Glitch text="W.A.T.S.O.N. UPDATE" hard /></div>
            <div className="panel alert" style={{ textAlign: 'left' }}>
              <div className="pix muted" style={{ marginBottom: 6 }}>Data restored · confirmed true</div>
              <div className="mono" style={{ fontSize: 18, fontWeight: 700 }}>{showUpdate.text}</div>
            </div>
            <div className="h2">
              <span className="tok">;</span> +1 token for everyone
            </div>
            <p className="small muted">Take 1 Query Token from the reserve (max 3).</p>
            <button className="btn primary big block" onClick={closeUpdate}>Got it</button>
          </div>
        </div>
      )}

      {!showUpdate && acc && (
        <div className="overlay" role="dialog" aria-modal="true">
          <div className="inner stack center">
            <div className="pix muted">Accusation in the Library</div>
            <div className="h1 red"><Glitch text="WRONG!" hard /></div>
            {accuser?.id === me.id ? (
              <>
                <p className="mono">{acc.suspectName} is innocent.</p>
                <div className="panel" style={{ textAlign: 'left' }}>
                  Move your pawn back to the <b>Grand Hall</b> and give back <b>all your tokens</b>. You stay in the game.
                </div>
              </>
            ) : (
              <p className="mono">
                {accuser?.name ?? 'A detective'} accused {acc.suspectName}… and was wrong. Cross that name out!
              </p>
            )}
            <button className="btn primary big block" onClick={closeAcc}>Continue</button>
          </div>
        </div>
      )}
    </>
  );
}
