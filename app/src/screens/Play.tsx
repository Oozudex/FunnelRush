import { useEffect, useState } from 'react';
import type { ScanResult } from '../../shared/types';
import { emit } from '../socket';
import { Glitch, PawnIcon, Tokens, useGame, useMe } from '../ui';
import { EvidenceCard, ScanPanel } from './Scan';
import PoliceConsole from './Query';

type Panel = null | 'search' | 'recharge' | 'accuse';

export default function Play({ crossed, goTo }: { crossed: string[]; goTo: (t: 'clues' | 'notebook') => void }) {
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
        <div className="panel center stack" style={{ padding: '26px 16px' }}>
          <div style={{ display: 'flex', justifyContent: 'center' }}>{current && <PawnIcon pawn={current.pawn} />}</div>
          <div className="h2">{current?.name ?? '…'} is playing</div>
          <p className="muted" style={{ margin: 0 }}>Wait for your turn. Your phone will buzz.</p>
        </div>
        <div className="pix muted center" style={{ marginTop: 8 }}>Meanwhile</div>
        <button className="btn big block" onClick={() => goTo('clues')}>🔎 Read my clues</button>
        <button className="btn big block" onClick={() => goTo('notebook')}>✗ Cross out suspects</button>
        <div className="row spread panel flat" style={{ padding: '8px 12px' }}>
          <span className="small">My Query Tokens</span>
          <Tokens n={me.tokens} max={game.caseInfo.maxTokens} />
        </div>
      </div>
    );
  }

  // ------------------------------------------------------------ my turn
  const done = game.action;
  const max = game.scansPerTurn;
  const canScanMore = done === 'search' && game.scans < max;
  const doneText = done === 'search'
    ? game.scans >= max ? `You scanned ${max} cards.` : `Card ${game.scans} of ${max} scanned. You can scan one more card.`
    : done === 'recharge' ? 'You recharged your tokens.' : done === 'accuse' ? 'You accused.' : '';

  const endTurn = async () => {
    setBusy(true);
    await emit('turn:end').catch((e: Error) => toast(e.message));
    setBusy(false);
  };

  return (
    <div className="stack">
      <div className="h2">Your turn, {me.name}</div>

      {/* ① MOVE */}
      <div className="step">
        <div className="step-title"><span className="num">1</span> Move your pawn</div>
        <p className="small" style={{ margin: 0 }}>Up to 2 rooms on the board, or stay where you are.</p>
      </div>

      {/* ② ACT */}
      <div className={`step ${done && !canScanMore ? 'ok' : 'now'}`}>
        <div className="step-title"><span className="num">2</span> Do ONE action {done && !canScanMore && <span className="tag" style={{ marginLeft: 'auto', color: '#3ac06b' }}>✓ done</span>}</div>
        {done ? (
          <>
            <p className="small" style={{ margin: 0 }}>{doneText}</p>
            {canScanMore && panel !== 'search' && (
              <button className="btn primary block action" style={{ marginTop: 10 }} onClick={() => setPanel('search')}>
                <span>🔎 Scan a 2nd card</span><small>Draw the next card of the same room</small>
              </button>
            )}
          </>
        ) : panel === null ? (
          <div className="stack" style={{ gap: 10 }}>
            <button className="btn primary big block action" onClick={() => setPanel('search')}>
              <span>🔎 Search the room</span><small>Draw up to {max} cards and scan them</small>
            </button>
            <button className="btn big block action" onClick={() => setPanel('recharge')}>
              <span>⚡ Recharge</span><small>Only in the Server Room</small>
            </button>
            <button className="btn big block action" onClick={() => setPanel('accuse')}>
              <span>⚖ Accuse the killer</span><small>Only in the Library</small>
            </button>
          </div>
        ) : (
          <button className="btn ghost small" onClick={() => setPanel(null)}>← Choose another action</button>
        )}

        {(!done || canScanMore) && panel === 'search' && (
          <div style={{ marginTop: 12 }}>
            <ScanPanel onResult={(r) => { setScans((l) => [r, ...l.filter((x) => x.item.code !== r.item.code)]); setPanel(null); }} />
          </div>
        )}
        {!done && panel === 'recharge' && (
          <div className="stack" style={{ marginTop: 12 }}>
            <p style={{ margin: 0 }}>Is your pawn in the <b>Server Room</b>? Your tokens go back to {game.caseInfo.maxTokens}.</p>
            <button
              className="btn amber big block"
              disabled={busy}
              onClick={async () => {
                setBusy(true);
                await emit('token:recharge').then(() => setPanel(null)).catch((e: Error) => toast(e.message));
                setBusy(false);
              }}
            >
              Yes, recharge <Tokens n={game.caseInfo.maxTokens} max={game.caseInfo.maxTokens} />
            </button>
          </div>
        )}
        {!done && panel === 'accuse' && <Accuse onDone={() => setPanel(null)} />}
      </div>

      {scans.length > 0 && (
        <div className="stack">
          {scans.map((sc) => (
            <EvidenceCard key={sc.item.code} item={sc.item} note={sc.effect ?? (sc.again ? 'You had already scanned this card.' : undefined)} />
          ))}
          <p className="small muted center" style={{ margin: 0 }}>Keep your cards face down in front of you.</p>
        </div>
      )}

      {/* ③ QUERY */}
      <div className="step">
        <div className="step-title"><span className="num">3</span> Query W.A.T.S.O.N. <span className="muted small" style={{ marginLeft: 6 }}>(optional)</span></div>
        <p className="small" style={{ margin: '0 0 10px' }}>Use your clues to find who matches. 1 search = 1 token.</p>
        <button className="btn block" onClick={() => setConsoleOpen(true)} disabled={me.tokens < 1}>
          Open the Police Console <Tokens n={me.tokens} max={game.caseInfo.maxTokens} />
        </button>
        {me.tokens < 1 && <p className="small amber" style={{ margin: '8px 0 0' }}>No token: recharge in the Server Room.</p>}
      </div>

      {/* ④ END */}
      <button className="btn primary big block" style={{ marginTop: 6 }} disabled={busy} onClick={endTurn}>
        End my turn ➜
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
    <div className="stack" style={{ marginTop: 12 }}>
      <p style={{ margin: 0 }}>Your pawn must be in the <b>Library</b>.</p>
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
      <p className="small amber" style={{ margin: 0 }}>Wrong? Back to the Grand Hall and you lose all your tokens.</p>
      <button
        className="btn primary big block"
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
        {s ? <Glitch text={`I accuse ${s.name.split(' ').slice(-1)[0]}!`} /> : 'I accuse…'}
      </button>
    </div>
  );
}
