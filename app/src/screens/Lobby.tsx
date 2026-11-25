import { useEffect, useState } from 'react';
import QRCode from 'qrcode';
import { PAWNS } from '../../shared/types';
import { emit } from '../socket';
import { Bar, Icon, Label, Logo, PAWN_NAME, PawnIcon, useGame, useMe } from '../ui';

declare const __LAN_IP__: string;

/** URL other phones open. In local dev (localhost) we swap in the computer's Wi-Fi IP so phones can reach it. */
export function useJoinUrl(code: string) {
  const { hostname, protocol, port, pathname, origin } = window.location;
  const local = ['localhost', '127.0.0.1', '::1'].includes(hostname) && __LAN_IP__;
  const host = local ? `${protocol}//${__LAN_IP__}${port ? `:${port}` : ''}` : origin;
  return `${host}${pathname}?join=${code}`;
}

export function JoinQr({ code }: { code: string }) {
  const url = useJoinUrl(code);
  const [src, setSrc] = useState('');
  useEffect(() => {
    QRCode.toDataURL(url, { margin: 1, width: 480, color: { dark: '#17171A', light: '#F5EFE1' } }).then(setSrc);
  }, [url]);
  return (
    <div className="stack tight center">
      <div className="qrbox">{src && <img src={src} alt={`QR code to join ${code}`} />}</div>
      <div className="gamecode" aria-label="Game code">{code}</div>
      <p className="small muted">Scan it with the phone camera, or tap “Join a game” and type the code.</p>
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
    <div className="screen no-nav stack">
      <Logo small />

      <div className="file">
        <Bar icon={Icon.scan} end={<span>{game.players.length}/4</span>}>Join the case</Bar>
        <JoinQr code={game.code} />
      </div>

      <div className="file flush">
        <Bar icon={Icon.suspects}>Detectives</Bar>
        <div className="list">
          {ordered.map((p, i) => (
            <div className={`item ${p.id === me.id ? 'now' : ''}`} key={p.id}>
              <PawnIcon pawn={p.pawn} />
              <div className="grow">
                <div className="name">{p.name}{p.id === me.id && <span className="muted"> (you)</span>}</div>
                <div className="small muted">{i === 0 ? 'Plays first' : `Plays ${['', '2nd', '3rd', '4th'][i]}`}</div>
              </div>
              {p.isHost && <span className="chip red">Host</span>}
              <span className={`dot ${p.connected ? '' : 'off'}`} title={p.connected ? 'online' : 'offline'} />
              {isHost && p.id !== me.id && (
                <button className="iconbtn" aria-label={`Remove ${p.name}`} onClick={() => act('lobby:kick', p.id)}>{Icon.close}</button>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="stack tight">
        <Label>Pick your pawn</Label>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8 }}>
          {PAWNS.map((pw) => {
            const owner = game.players.find((p) => p.pawn === pw);
            const mine = me.pawn === pw;
            return (
              <button
                key={pw}
                className={`btn flat ${mine ? 'primary' : ''}`}
                style={{ flexDirection: 'column', gap: 6, padding: '10px 4px', minHeight: 84 }}
                disabled={!!owner && owner.id !== me.id}
                onClick={() => act('lobby:pawn', pw)}
                aria-pressed={mine}
              >
                <PawnIcon pawn={pw} />
                <span className="small">{owner ? (owner.id === me.id ? 'You' : owner.name.slice(0, 7)) : PAWN_NAME[pw]}</span>
              </button>
            );
          })}
        </div>
      </div>

      {isHost ? (
        <div className="file stack">
          <Bar icon={Icon.turn} color="red">Before you start</Bar>
          <ol className="small" style={{ margin: 0, paddingLeft: 20, display: 'grid', gap: 4 }}>
            <li>Shuffle the 7 room decks, face down on their rooms.</li>
            <li>All pawns in the <b>Grand Hall</b>.</li>
            <li>Every detective takes <b>3 Query Tokens</b>.</li>
          </ol>
          <div className="field">
            <label htmlFor="first">Who plays first? (the youngest)</label>
            <select id="first" className="select" value={game.order[0]} onChange={(e) => act('lobby:first', e.target.value)}>
              {game.players.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <button
            className="btn red big block"
            disabled={busy}
            onClick={async () => {
              setBusy(true);
              await act('game:start');
              setBusy(false);
            }}
          >
            Start the investigation
          </button>
          <p className="small muted center">
            {game.players.length < 2 ? '2 to 4 detectives. You can still start alone to test. ' : ''}
            Your phone runs the game: keep the app open.
          </p>
        </div>
      ) : (
        <div className="file center stack tight">
          <div><span className="stamp">Waiting for the host</span></div>
          <p className="small muted">The game starts when the host is ready.</p>
        </div>
      )}

      <div className="file margin">
        <Label className="red">{game.caseInfo.tagline}</Label>
        <div className="title t3" style={{ margin: '6px 0 10px' }}>{game.caseInfo.title}</div>
        <div className="stack tight typed">
          {game.caseInfo.intro.map((t, i) => <p key={i}>{t}</p>)}
        </div>
      </div>

      <button className="btn ghost block" onClick={leave}>Leave the game</button>
    </div>
  );
}
