import { useEffect, useState } from 'react';
import QRCode from 'qrcode';
import { PAWNS } from '../../shared/types';
import { emit } from '../socket';
import { Logo, PAWN_NAME, PawnIcon, SectionTitle, useGame, useMe } from '../ui';

/** URL other phones open. On localhost we swap in the computer's Wi-Fi IP so phones can reach it. */
export function useJoinUrl(code: string) {
  const base = `${window.location.origin}${window.location.pathname}`;
  const [url, setUrl] = useState(`${base}?join=${code}`);
  useEffect(() => {
    const { hostname, protocol, port } = window.location;
    if (!['localhost', '127.0.0.1', '::1'].includes(hostname)) return;
    fetch('/api/info')
      .then((r) => r.json())
      .then((info: { lanIps: string[] }) => {
        const ip = info.lanIps.find((i) => i.startsWith('192.168.')) ?? info.lanIps[0];
        if (ip) setUrl(`${protocol}//${ip}${port ? `:${port}` : ''}${window.location.pathname}?join=${code}`);
      })
      .catch(() => {});
  }, [code]);
  return url;
}

export function JoinQr({ code }: { code: string }) {
  const url = useJoinUrl(code);
  const [src, setSrc] = useState('');
  useEffect(() => {
    QRCode.toDataURL(url, { margin: 1, width: 480, color: { dark: '#0B0B0C', light: '#F4F0E6' } }).then(setSrc);
  }, [url]);
  return (
    <div className="stack center">
      <div className="gamecode" aria-label="Game code">{code}</div>
      <div className="qrbox">{src && <img src={src} alt={`QR code to join ${code}`} />}</div>
      <p className="small muted" style={{ wordBreak: 'break-all' }}>
        Scan with the phone camera, or go to <span className="mono">{url.replace(/\/?\?join=.*/, '')}</span> and type the code.
      </p>
    </div>
  );
}

export default function Lobby() {
  const { view, toast, leave } = useGame();
  const { game } = view;
  const { me, isHost } = useMe(view);
  const [busy, setBusy] = useState(false);

  const act = (event: string, ...args: unknown[]) => emit(event, ...args).catch((e: Error) => toast(e.message));
  const ordered = game.order.map((id) => game.players.find((p) => p.id === id)!).filter(Boolean);

  return (
    <div className="screen no-nav">
      <Logo small />
      <div className="center pix muted" style={{ margin: '6px 0 16px' }}>Waiting room</div>

      <JoinQr code={game.code} />

      <SectionTitle>Detectives ({game.players.length}/4)</SectionTitle>
      <div className="plist">
        {ordered.map((p, i) => (
          <div className={`pitem ${p.id === me.id ? 'now' : ''}`} key={p.id}>
            <PawnIcon pawn={p.pawn} />
            <div className="grow">
              <div style={{ fontWeight: 800 }}>
                {p.name} {p.id === me.id && <span className="muted">(you)</span>}
              </div>
              <div className="small muted">{i === 0 ? 'Plays first' : `Plays ${['', '2nd', '3rd', '4th'][i]}`}</div>
            </div>
            {p.isHost && <span className="tag red">Host</span>}
            <span className={`dot ${p.connected ? '' : 'off'}`} title={p.connected ? 'online' : 'offline'} />
            {isHost && p.id !== me.id && (
              <button className="btn ghost small" aria-label={`Remove ${p.name}`} onClick={() => act('lobby:kick', p.id)}>
                ✕
              </button>
            )}
          </div>
        ))}
      </div>

      <SectionTitle>Choose your pawn</SectionTitle>
      <div className="pawn-pick">
        {PAWNS.map((pw) => {
          const owner = game.players.find((p) => p.pawn === pw);
          return (
            <button
              key={pw}
              className={me.pawn === pw ? 'on' : ''}
              disabled={!!owner && owner.id !== me.id}
              onClick={() => act('lobby:pawn', pw)}
            >
              <PawnIcon pawn={pw} />
              {owner ? (owner.id === me.id ? 'You' : owner.name.slice(0, 8)) : PAWN_NAME[pw]}
            </button>
          );
        })}
      </div>

      <SectionTitle>Case file</SectionTitle>
      <div className="panel paper">
        <div style={{ paddingLeft: 14 }}>
          <div className="ev-room">{game.caseInfo.tagline}</div>
          <div className="ev-obj" style={{ margin: '4px 0 8px' }}>{game.caseInfo.title}</div>
          {game.caseInfo.intro.map((t, i) => (
            <p key={i} className="small">{t}</p>
          ))}
        </div>
      </div>

      {isHost ? (
        <div className="stack" style={{ marginTop: 18 }}>
          <div className="field">
            <label htmlFor="first">Who starts? (the youngest player)</label>
            <select id="first" className="select" value={game.order[0]} onChange={(e) => act('lobby:first', e.target.value)}>
              {game.players.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <div className="panel flat small">
            <div className="pix muted" style={{ marginBottom: 6 }}>Before you start</div>
            <ol className="rules" style={{ margin: 0, paddingLeft: 18 }}>
              <li>Shuffle the 7 room decks, face down on their rooms.</li>
              <li>All pawns in the <b>Grand Hall</b>.</li>
              <li>Every detective takes <b className="red">3 ;</b> Query Tokens.</li>
            </ol>
          </div>
          {game.players.length < 2 && <p className="small amber center">2–4 detectives recommended. You can still start alone to test.</p>}
          <button
            className="btn primary big block"
            disabled={busy}
            onClick={async () => {
              setBusy(true);
              await act('game:start');
              setBusy(false);
            }}
          >
            Start the investigation
          </button>
        </div>
      ) : (
        <div className="panel flat center" style={{ marginTop: 18 }}>
          <span className="glitch" data-text="WAITING FOR THE HOST…">WAITING FOR THE HOST…</span>
        </div>
      )}

      <button className="btn ghost block" style={{ marginTop: 14 }} onClick={leave}>
        Leave the game
      </button>
    </div>
  );
}
