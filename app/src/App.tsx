import { useCallback, useEffect, useRef, useState } from 'react';
import type { Session, View } from '../shared/types';
import { leave as netLeave, loadSession, resume, saveSession, setHandlers, wake } from './socket';
import type { NetStatus } from './net/room';
import { GameCtx } from './ui';
import Home from './screens/Home';
import Lobby from './screens/Lobby';
import GameScreen from './screens/Game';
import End from './screens/End';

export default function App() {
  const [view, setView] = useState<View | null>(null);
  const [status, setStatus] = useState<NetStatus>('connecting');
  const [resuming, setResuming] = useState(!!loadSession());
  const [toastMsg, setToast] = useState<{ msg: string; ok?: boolean; id: number } | null>(null);
  const timer = useRef<number>();

  const toast = useCallback((msg: string, ok?: boolean) => {
    setToast({ msg, ok, id: Date.now() });
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => setToast(null), 3600);
  }, []);

  useEffect(() => {
    setHandlers({
      view: setView,
      status: setStatus,
      closed: (reason) => {
        saveSession(null);
        setView(null);
        toast(reason);
      },
    });
    tryResume();
  }, [toast]); // eslint-disable-line react-hooks/exhaustive-deps

  const [resumeError, setResumeError] = useState('');
  function tryResume() {
    const s = loadSession();
    if (!s) return setResuming(false);
    setResuming(true);
    setResumeError('');
    resume(s)
      .then(() => setResuming(false))
      .catch((e: Error) => {
        if (e.message.startsWith('No answer') || e.message.startsWith('No connection') || e.message.startsWith('Cannot reach')) {
          setResumeError(e.message); // keep the seat: the host may just be away
          return;
        }
        saveSession(null);
        setView(null);
        setResuming(false);
        toast(e.message);
      });
  }
  const forget = () => {
    saveSession(null);
    setResumeError('');
    setResuming(false);
  };

  useEffect(() => {
    const onVis = () => document.visibilityState === 'visible' && wake();
    document.addEventListener('visibilitychange', onVis);
    window.addEventListener('online', onVis);
    return () => {
      document.removeEventListener('visibilitychange', onVis);
      window.removeEventListener('online', onVis);
    };
  }, []);

  const onSession = (s: Session) => {
    saveSession(s);
    const url = new URL(window.location.href);
    if (url.searchParams.has('join')) {
      url.searchParams.delete('join');
      window.history.replaceState(null, '', url.toString());
    }
  };

  const leave = useCallback(() => {
    netLeave();
    saveSession(null);
    setView(null);
  }, []);

  let body;
  if (!view) body = resuming ? <Loading error={resumeError} retry={tryResume} forget={forget} /> : <Home onSession={onSession} toast={toast} />;
  else {
    const ctx = { view, toast, leave };
    body = (
      <GameCtx.Provider value={ctx}>
        {view.game.phase === 'lobby' && <Lobby />}
        {view.game.phase === 'playing' && <GameScreen />}
        {view.game.phase === 'over' && <End />}
      </GameCtx.Provider>
    );
  }

  return (
    <>
      {body}
      {view && status !== 'online' && view.game.phase !== 'over' && (
        <div className="toast" style={{ top: 12, bottom: 'auto' }} role="status">
          {status === 'host-away' ? "Waiting for the host's phone… (the host must keep the app open)" : 'Connection lost. Reconnecting…'}
        </div>
      )}
      {toastMsg && (
        <div key={toastMsg.id} className={`toast ${toastMsg.ok ? 'ok' : ''}`} role="status" onClick={() => setToast(null)}>
          {toastMsg.msg}
        </div>
      )}
    </>
  );
}

function Loading({ error, retry, forget }: { error: string; retry: () => void; forget: () => void }) {
  return (
    <div className="screen no-nav center stack" style={{ paddingTop: '26vh' }}>
      <div className="h2"><span className="glitch hard" data-text="RECONNECTING…">RECONNECTING…</span></div>
      {error && (
        <>
          <p className="amber">{error}</p>
          <button className="btn primary big block" onClick={retry}>Try again</button>
          <button className="btn ghost block" onClick={forget}>Leave this game</button>
        </>
      )}
    </div>
  );
}
