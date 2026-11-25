import { useEffect, useRef, useState } from 'react';
import { buzz, persist, store } from '../socket';
import { Bar, clockFor, Icon, PawnIcon, Sheet, Tokens, useGame, useMe } from '../ui';
import Play from './Play';
import Clues from './Clues';
import Notebook, { type NotebookState } from './Notebook';
import Manor from './Manor';

type Tab = 'turn' | 'clues' | 'suspects';
const TABS: { id: Tab; label: string }[] = [
  { id: 'turn', label: 'Turn' },
  { id: 'clues', label: 'Clues' },
  { id: 'suspects', label: 'Suspects' },
];

export default function GameScreen() {
  const { view, toast } = useGame();
  const { game } = view;
  const { me, current, myTurn } = useMe(view);
  const key = `tlq.${game.code}.${me.id}`;
  const saved = store<string>(`${key}.tab`, 'turn');
  const [tab, setTabRaw] = useState<Tab>(TABS.some((t) => t.id === saved) ? (saved as Tab) : 'turn');
  const [menu, setMenu] = useState(false);
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

  // Wrong accusation overlay
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
      setTab('turn');
      setMenu(false);
      toast("It's your turn, detective!", true);
    }
    wasMyTurn.current = myTurn;
  }, [myTurn, toast]); // eslint-disable-line react-hooks/exhaustive-deps

  const accuser = acc && game.players.find((p) => p.id === acc.playerId);

  return (
    <>
      <header className="topbar">
        <div className="row spread">
          <div>
            <div className="meta muted">Round {game.round}</div>
            <div className="clock">{clockFor(game.round)}</div>
          </div>
          <div className="row" style={{ gap: 6 }}>
            <Tokens n={me.tokens} max={game.caseInfo.maxTokens} />
            <button className="iconbtn" onClick={() => setMenu(true)} aria-label="Game info and settings">{Icon.menu}</button>
          </div>
        </div>
        <div className={`turnstrip ${myTurn ? 'mine' : ''}`}>
          <Bar icon={current ? <PawnIcon pawn={current.pawn} /> : null}>
            {myTurn ? 'Your turn' : `${current?.name ?? '…'} is playing`}
          </Bar>
        </div>
      </header>

      <main className="screen">
        {tab === 'turn' && <Play crossed={nb.crossed} goTo={setTab} />}
        {tab === 'clues' && <Clues />}
        {tab === 'suspects' && <Notebook nb={nb} setNb={updateNb} />}
      </main>

      <nav className="nav" aria-label="Police Console">
        {TABS.map((t) => (
          <button key={t.id} className={tab === t.id ? 'on' : ''} onClick={() => setTab(t.id)} aria-current={tab === t.id ? 'page' : undefined}>
            {Icon[t.id]}
            {t.label}
            {t.id === 'clues' && view.me.evidence.length > 0 && <span className="badge">{view.me.evidence.length}</span>}
          </button>
        ))}
      </nav>

      {menu && (
        <Sheet title="The game" icon={Icon.info} onClose={() => setMenu(false)}>
          <Manor />
        </Sheet>
      )}

      {showUpdate && (
        <div className="overlay" role="dialog" aria-modal="true">
          <div className="file stack">
            <Bar icon={Icon.bolt} color="amber" end={<span>Round {showUpdate.round}</span>}>W.A.T.S.O.N. update</Bar>
            <div><span className="stamp">Data restored</span></div>
            <p className="small muted">Lightning strike! One true trait of the killer:</p>
            <p className="title t2">{showUpdate.text}</p>
            <div className="row note">
              <span className="tok">;</span>
              <span className="small"><b>+1 Query Token for everyone</b> (max 3). Take one from the reserve.</span>
            </div>
            <button className="btn primary big block" onClick={closeUpdate}>Got it</button>
          </div>
        </div>
      )}

      {!showUpdate && acc && (
        <div className="overlay" role="dialog" aria-modal="true">
          <div className="file stack">
            <Bar icon={Icon.scale} color="red">Accusation · Library</Bar>
            <div className="center" style={{ padding: '6px 0' }}><span className="stamp big">Wrong!</span></div>
            {accuser?.id === me.id ? (
              <>
                <p className="typed center" style={{ fontSize: 18 }}>{acc.suspectName} is innocent.</p>
                <div className="note small">Move your pawn back to the <b>Grand Hall</b> and give back <b>all your tokens</b>. You stay in the game.</div>
              </>
            ) : (
              <p className="typed center" style={{ fontSize: 17 }}>
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
