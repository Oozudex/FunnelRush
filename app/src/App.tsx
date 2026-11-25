import { useCallback, useEffect, useRef, useState } from 'react';
import type { Session, View } from '../shared/types';
import { emit, loadSession, saveSession, socket } from './socket';
import { GameCtx } from './ui';
import Home from './screens/Home';
import Lobby from './screens/Lobby';
import GameScreen from './screens/Game';
import End from './screens/End';

export default function App() {
  const [view, setView] = useState<View | null>(null);
  const [connected, setConnected] = useState(socket.connected);
  const [resuming, setResuming] = useState(!!loadSession());
  const [toastMsg, setToast] = useState<{ msg: string; ok?: boolean; id: number } | null>(null);
  const timer = useRef<number>();

  const toast = useCallback((msg: string, ok?: boolean) => {
    setToast({ msg, ok, id: Date.now() });
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => setToast(null), 3200);
  }, []);

  useEffect(() => {
    const onView = (v: View) => setView(v);
    const resume = () => {
      setConnected(true);
      const s = loadSession();
      if (!s) return setResuming(false);
      emit('game:resume', s)
        .catch((e: Error) => {
          saveSession(null);
          setView(null);
          toast(e.message);
        })
        .finally(() => setResuming(false));
    };
    const onDown = () => setConnected(false);
    socket.on('view', onView);
    socket.on('connect', resume);
    socket.on('disconnect', onDown);
    if (socket.connected) resume();
    return () => {
      socket.off('view', onView);
      socket.off('connect', resume);
      socket.off('disconnect', onDown);
    };
  }, [toast]);

  const onSession = (s: Session) => {
    saveSession(s);
    const url = new URL(window.location.href);
    if (url.searchParams.has('join')) {
      url.searchParams.delete('join');
      window.history.replaceState(null, '', url.toString());
    }
  };

  const leave = useCallback(() => {
    emit('game:leave').catch(() => {});
    saveSession(null);
    setView(null);
  }, []);

  let body;
  if (!view) body = resuming ? <Loading /> : <Home onSession={onSession} toast={toast} connected={connected} />;
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
      {!connected && view && (
        <div className="toast" style={{ top: 12, bottom: 'auto' }}>
          Connection lost. Reconnecting…
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

function Loading() {
  return (
    <div className="screen no-nav center" style={{ paddingTop: '30vh' }}>
      <div className="h2"><span className="glitch hard" data-text="RECONNECTING…">RECONNECTING…</span></div>
    </div>
  );
}
