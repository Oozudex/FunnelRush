import { useState } from 'react';
import type { Session } from '../../shared/types';
import { createGame, joinGame, persist, store } from '../socket';
import { Bar, Icon, Logo } from '../ui';

export default function Home({ onSession, toast }: { onSession: (s: Session) => void; toast: (m: string) => void }) {
  const initialCode = new URLSearchParams(window.location.search).get('join') ?? '';
  const [mode, setMode] = useState<'menu' | 'create' | 'join'>(initialCode ? 'join' : 'menu');
  const [name, setName] = useState<string>(store('tlq.name', ''));
  const [code, setCode] = useState(initialCode.toUpperCase());
  const [busy, setBusy] = useState(false);

  const go = async () => {
    setBusy(true);
    persist('tlq.name', name.trim());
    try {
      const s = mode === 'create' ? await createGame(name) : await joinGame(code, name);
      onSession(s);
    } catch (e) {
      toast((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="screen no-nav stack" style={{ gap: 22 }}>
      <div style={{ paddingTop: 20 }}>
        <Logo />
      </div>

      {mode === 'menu' && (
        <>
          <div className="file margin">
            <Bar icon={Icon.console}>Police Console</Bar>
            <p className="typed" style={{ fontSize: 17 }}>
              Ravenscroft Manor, 11:45 PM. Sir Victor is dead. The storm has cut the bridge. The killer is still in the house.
            </p>
          </div>
          <div className="stack">
            <button className="btn primary big block" onClick={() => setMode('create')}>Create a game</button>
            <button className="btn big block" onClick={() => setMode('join')}>Join a game</button>
          </div>
          <p className="small muted center">One phone per detective. The host creates the game, the others scan its QR code.</p>
        </>
      )}

      {mode !== 'menu' && (
        <form
          className="file stack"
          onSubmit={(e) => {
            e.preventDefault();
            if (!busy) go();
          }}
        >
          <Bar icon={mode === 'create' ? Icon.console : Icon.scan}>{mode === 'create' ? 'New investigation' : 'Join the investigation'}</Bar>
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
              autoFocus={mode === 'create' || !!code}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <button className="btn primary big block" disabled={busy || name.trim().length < 2 || (mode === 'join' && code.trim().length < 4)}>
            {busy ? (mode === 'create' ? 'Opening the line…' : 'Calling the host…') : mode === 'create' ? 'Create the game' : 'Join'}
          </button>
          <button type="button" className="btn ghost block" onClick={() => setMode('menu')}>Back</button>
        </form>
      )}
    </div>
  );
}
