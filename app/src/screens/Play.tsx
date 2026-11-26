import { useEffect, useState, type ReactNode } from 'react';
import type { ScanResult } from '../../shared/types';
import { emit } from '../socket';
import { Bar, Icon, PawnIcon, RoomIcon, useGame, useMe } from '../ui';
import { EvidenceCard, ScanPanel } from './Scan';
import PoliceConsole from './Query';

type Panel = null | 'search' | 'recharge' | 'accuse';

function Step({ n, title, sub, state, children }: { n: string; title: string; sub?: ReactNode; state?: 'done' | 'info'; children?: ReactNode }) {
  return (
    <div className={`step ${state === 'done' ? 'done' : state === 'info' ? 'muted-step' : ''}`}>
      <span className="n">{state === 'done' ? <span style={{ width: 18, height: 18, display: 'block' }}>{Icon.check}</span> : n}</span>
      <div className="head">
        <div className="t">{title}</div>
        {sub && <div className="small muted">{sub}</div>}
      </div>
      {children && <div className="body">{children}</div>}
    </div>
  );
}

function RoomTile({ room, icon, title, sub, main, onClick }: { room: string; icon: ReactNode; title: string; sub: string; main?: boolean; onClick: () => void }) {
  return (
    <button className={`room ${main ? 'main' : ''}`} onClick={onClick}>
      <Bar icon={icon}>{room}</Bar>
      <span className="in">
        <span>
          <span className="t" style={{ display: 'block' }}>{title}</span>
          <span className="s">{sub}</span>
        </span>
        {Icon.arrow}
      </span>
    </button>
  );
}

export default function Play({ crossed, goTo }: { crossed: string[]; goTo: (t: 'clues' | 'suspects') => void }) {
  const { view, toast } = useGame();
  const { game } = view;
  const { me, myTurn, current } = useMe(view);
  const [panel, setPanel] = useState<Panel>(null);
  const [scans, setScans] = useState<ScanResult[]>([]);
  const [consoleOpen, setConsoleOpen] = useState(false);
  const [busy, setBusy] = useState(false);

  // new turn: start clean
  const turnKey = `${game.round}:${game.turn}`;
  useEffect(() => {
    setPanel(null);
    setScans([]);
    setConsoleOpen(false);
  }, [turnKey]);

  // ------------------------------------------------------------ not my turn
  if (!myTurn) {
    return (
      <div className="stack">
        <div className="file center stack" style={{ padding: '28px 16px' }}>
          <div style={{ display: 'flex', justifyContent: 'center' }}>{current && <PawnIcon pawn={current.pawn} />}</div>
          <div className="title t2">{current?.name ?? '…'} is playing</div>
          <p className="typed muted">Wait for your turn. Your phone will buzz.</p>
        </div>
        <div className="label center" style={{ marginTop: 6 }}>Meanwhile</div>
        <button className="btn big block" onClick={() => goTo('clues')}>{Icon.clues} Read my clues</button>
        <button className="btn big block" onClick={() => goTo('suspects')}>{Icon.suspects} Cross out suspects</button>
      </div>
    );
  }

  // ------------------------------------------------------------ my turn
  const done = game.action;
  const max = game.scansPerTurn;
  const canScanMore = done === 'search' && game.scans < max;
  const searched = done === 'search' && !canScanMore;
  const other = done === 'recharge' || done === 'accuse';
  const otherText = done === 'recharge' ? `Take Query Tokens from the reserve, up to ${game.caseInfo.maxTokens} in front of you.` : done === 'accuse' ? 'You accused.' : '';
  const cards = max === 1 ? '1 card' : `up to ${max} cards`;

  const endTurn = async () => {
    setBusy(true);
    await emit('turn:end').catch((e: Error) => toast(e.message));
    setBusy(false);
  };

  const panelBox = (
    <>
        {canScanMore && panel !== 'search' && (
          <button className="btn primary block" onClick={() => setPanel('search')}>{Icon.scan} Scan the next card</button>
        )}

        {panel !== null && (!done || (panel === 'search' && canScanMore)) && (
          <div className="file stack">
            <Bar
              icon={panel === 'search' ? Icon.scan : panel === 'recharge' ? RoomIcon['Server Room'] : RoomIcon.Library}
              color={panel === 'accuse' ? 'red' : undefined}
            >
              {panel === 'search' ? 'Search the room' : panel === 'recharge' ? 'Server Room · recharge' : 'Library · accuse'}
            </Bar>
            {panel === 'search' && (
              <ScanPanel
                onResult={(r) => {
                  setScans((l) => [r, ...l.filter((x) => x.item.code !== r.item.code)]);
                  setPanel(null);
                }}
              />
            )}
            {panel === 'recharge' && (
              <>
                <p>Is your pawn in the <b>Server Room</b>? Take Query Tokens from the reserve until you have <b>{game.caseInfo.maxTokens}</b> in front of you.</p>
                <button
                  className="btn primary big block"
                  disabled={busy}
                  onClick={async () => {
                    setBusy(true);
                    await emit('token:recharge').then(() => setPanel(null)).catch((e: Error) => toast(e.message));
                    setBusy(false);
                  }}
                >
                  Recharge <span className="tok">;</span>
                </button>
              </>
            )}
            {panel === 'accuse' && <Accuse onDone={() => setPanel(null)} />}
            {!done && <button className="btn ghost block" onClick={() => setPanel(null)}>Back</button>}
          </div>
        )}

    </>
  );

  return (
    <div className="stack" style={{ gap: 22 }}>
      <div className="title t2">Your turn, {me.name}</div>

      <Step
        n="1"
        title="Move and search"
        sub={
          searched
            ? 'Card drawn. You can finish your move (up to 2 rooms in all).'
            : other
              ? 'No search this turn: you used your action.'
              : <>Move up to 2 rooms. <b>Once</b> on the way (before, halfway or at the end), draw <b>{cards}</b> in the room you are in.</>
        }
        state={searched ? 'done' : other ? 'info' : undefined}
      >
        {!done && panel === null && (
          <div className="rooms">
            <RoomTile room="Any room with a deck" icon={Icon.scan} title="Search the room" sub={`Draw ${cards} and scan it`} main onClick={() => setPanel('search')} />
          </div>
        )}
        {(panel === 'search' || canScanMore) && panelBox}
        {scans.map((sc) => (
          <EvidenceCard key={sc.item.code} item={sc.item} note={sc.effect ?? (sc.again ? 'You had already scanned this card.' : undefined)} />
        ))}
        {scans.length > 0 && <p className="small muted center">Keep your cards face down in front of you.</p>}
      </Step>

      <Step n="2" title="Or, instead of searching" sub={other ? otherText : searched ? 'You searched this turn.' : 'Only in these two rooms.'} state={other ? 'done' : searched ? 'info' : undefined}>
        {!done && panel === null && (
          <div className="rooms">
            <RoomTile room="Server Room" icon={RoomIcon['Server Room']} title="Recharge" sub={`Take tokens from the reserve, up to ${game.caseInfo.maxTokens}`} onClick={() => setPanel('recharge')} />
            <RoomTile room="Library" icon={RoomIcon.Library} title="Accuse the killer" sub="Name the killer and win" onClick={() => setPanel('accuse')} />
          </div>
        )}
        {(panel === 'recharge' || panel === 'accuse') && panelBox}
      </Step>

      <Step
        n="3"
        title="Query W.A.T.S.O.N."
        sub={game.queried ? 'Query done for this turn.' : 'Optional. Anytime on your turn: ONE query. Scan one of your Query Tokens to run it.'}
        state={game.queried ? 'done' : undefined}
      >
        <button className="btn block" onClick={() => setConsoleOpen(true)} >
          {Icon.console} {game.queried ? 'See my query' : 'Open the Police Console'}
        </button>
      </Step>

      <button className="btn primary big block" disabled={busy} onClick={endTurn}>
        End my turn {Icon.move}
      </button>

      {consoleOpen && <PoliceConsole crossed={crossed} onClose={() => setConsoleOpen(false)} />}
    </div>
  );
}

function Accuse({ onDone }: { onDone: () => void }) {
  const { view, toast } = useGame();
  const { suspects } = view.game.caseInfo;
  const [pick, setPick] = useState('');
  const [busy, setBusy] = useState(false);
  const s = suspects.find((x) => x.id === pick);

  return (
    <>
      <p>Your pawn must be in the <b>Library</b>.</p>
      <div className="field">
        <label htmlFor="who">Who is the killer?</label>
        <select id="who" className="select" value={pick} onChange={(e) => setPick(e.target.value)}>
          <option value="">Choose a suspect…</option>
          {suspects.map((x) => (
            <option key={x.id} value={x.id}>{x.name}</option>
          ))}
        </select>
      </div>
      <div className="note">
        <div className="label">Say it out loud, in English</div>
        <p className="typed" style={{ marginTop: 6, fontSize: 17 }}>
          “The killer is {s ? s.name : '________'}: __ years old, __ m tall, size __ shoes, ____-handed!”
        </p>
      </div>
      <p className="small red">Wrong? Back to the Grand Hall, and all your Query Tokens go back to the reserve.</p>
      <button
        className="btn red big block"
        disabled={!pick || busy}
        onClick={async () => {
          setBusy(true);
          try {
            await emit<boolean>('accuse', pick);
            onDone();
          } catch (e) {
            toast((e as Error).message);
          } finally {
            setBusy(false);
          }
        }}
      >
        {s ? `I accuse ${s.name.split(' ').slice(-1)[0]}!` : 'I accuse…'}
      </button>
    </>
  );
}
