import { useState } from 'react';
import type { Session } from '../../shared/types';
import { emit, persist, store } from '../socket';
import { Logo } from '../ui';

export default function Home({ onSession, toast, connected }: { onSession: (s: Session) => void; toast: (m: string) => void; connected: boolean }) {
  const initialCode = new URLSearchParams(window.location.search).get('join') ?? '';
  const [mode, setMode] = useState<'menu' | 'create' | 'join'>(initialCode ? 'join' : 'menu');
  const [name, setName] = useState<string>(store('tlq.name', ''));
  const [code, setCode] = useState(initialCode.toUpperCase());
  const [busy, setBusy] = useState(false);

  const go = async () => {
    setBusy(true);
    persist('tlq.name', name.trim());
    try {
      const s =
        mode === 'create'
          ? await emit<Session>('game:create', { name })
          : await emit<Session>('game:join', { code, name });
      onSession(s);
    } catch (e) {
      toast((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="screen no-nav">
      <div style={{ marginTop: 18 }}>
        <Logo />
      </div>
      <p className="home-tag pix">Police Console · W.A.T.S.O.N. terminal</p>
      {!connected && (
        <p className="small amber center" role="status">
          Waking up the W.A.T.S.O.N. server… (up to 1 minute the first time)
        </p>
      )}

      {mode === 'menu' && (
        <div className="stack">
          <div className="panel flat small">
            <p className="mono" style={{ margin: 0 }}>
              <span className="red">&gt;</span> Ravenscroft Manor, 11:45 PM. Sir Victor is dead. The storm has cut the bridge.
              The killer is still in the house.
            </p>
          </div>
          <button className="btn primary big block" onClick={() => setMode('create')}>
            Create a game
          </button>
          <button className="btn big block" onClick={() => setMode('join')}>
            Join a game
          </button>
          <p className="small muted center" style={{ marginTop: 8 }}>
            One phone per detective. The host creates the game, the others scan the QR code or type the game code.
          </p>
        </div>
      )}

      {mode !== 'menu' && (
        <form
          className="stack"
          onSubmit={(e) => {
            e.preventDefault();
            if (!busy) go();
          }}
        >
          <div className="h2">{mode === 'create' ? 'New investigation' : 'Join the investigation'}</div>
          {mode === 'join' && (
            <div className="field">
              <label htmlFor="code">Game code</label>
              <input
                id="code"
                className="input code"
                placeholder="RAVEN-42"
                value={code}
                autoCapitalize="characters"
                autoComplete="off"
                maxLength={12}
                onChange={(e) => setCode(e.target.value.toUpperCase())}
              />
            </div>
          )}
          <div className="field">
            <label htmlFor="name">Your detective name</label>
            <input
              id="name"
              className="input"
              placeholder="e.g. Sherlock"
              value={name}
              maxLength={18}
              autoComplete="nickname"
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <button className="btn primary big block" disabled={busy || name.trim().length < 2 || (mode === 'join' && code.trim().length < 4)}>
            {busy ? 'Connecting…' : mode === 'create' ? 'Create & get a code' : 'Join'}
          </button>
          <button type="button" className="btn ghost block" onClick={() => setMode('menu')}>
            Back
          </button>
        </form>
      )}
    </div>
  );
}
