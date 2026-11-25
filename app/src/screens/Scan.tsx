import { useEffect, useRef, useState } from 'react';
import jsQR from 'jsqr';
import type { EvidenceItem, ScanResult } from '../../shared/types';
import { describe } from '../../shared/sql';
import { buzz, emit } from '../socket';
import { Bar, Icon, roomIcon, useGame } from '../ui';

export function EvidenceCard({ item, note }: { item: EvidenceItem; note?: string }) {
  const { view } = useGame();
  const attr = item.condition && view.game.caseInfo.attributes.find((a) => a.key === item.condition!.attr);
  const bonus = item.kind === 'bonus';
  return (
    <div className="file margin evcard">
      <Bar icon={bonus ? Icon.bolt : Icon.clues} color={bonus ? 'amber' : 'blue'} end={<span className="code">{item.code}</span>}>
        {bonus ? 'Bonus' : 'Evidence'}
      </Bar>
      <div className="obj">{item.object}</div>
      <div className="where label">{roomIcon(item.room)} Found in the {item.room}</div>
      <p className="text">{item.text}</p>
      {item.kind === 'trait' && attr && (
        <>
          <span className="stamp">Clue: {describe(attr, item.condition!)}</span>
          <p className="foot">Use the column <b>{attr.column}</b> in the Police Console.</p>
        </>
      )}
      {item.kind === 'deadend' && <span className="stamp grey">Dead end</span>}
      {note && <p className="foot"><b>{note}</b></p>}
    </div>
  );
}

function Camera({ onCode }: { onCode: (code: string) => void }) {
  const video = useRef<HTMLVideoElement>(null);
  const [on, setOn] = useState(false);
  const [err, setErr] = useState('');
  const stream = useRef<MediaStream | null>(null);
  const raf = useRef(0);
  const last = useRef({ code: '', at: 0 });

  const stop = () => {
    cancelAnimationFrame(raf.current);
    stream.current?.getTracks().forEach((t) => t.stop());
    stream.current = null;
    setOn(false);
  };
  useEffect(() => stop, []);

  const start = async () => {
    setErr('');
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
      setErr('The camera needs a secure (https) page. Type the backup code below instead.');
      return;
    }
    try {
      const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
      stream.current = s;
      setOn(true);
      const v = video.current!;
      v.srcObject = s;
      v.setAttribute('playsinline', 'true');
      await v.play();
      const canvas = document.createElement('canvas');
      const g = canvas.getContext('2d', { willReadFrequently: true })!;
      let frame = 0;
      const tick = () => {
        raf.current = requestAnimationFrame(tick);
        if (++frame % 3 || v.readyState < 2) return;
        const w = 360;
        const h = Math.round((v.videoHeight / v.videoWidth) * w) || w;
        canvas.width = w;
        canvas.height = h;
        g.drawImage(v, 0, 0, w, h);
        const res = jsQR(g.getImageData(0, 0, w, h).data, w, h, { inversionAttempts: 'dontInvert' });
        if (res?.data) {
          const now = Date.now();
          if (res.data === last.current.code && now - last.current.at < 4000) return;
          last.current = { code: res.data, at: now };
          buzz(60);
          stop();
          onCode(res.data);
        }
      };
      tick();
    } catch {
      stop();
      setErr('Camera blocked. Allow the camera in your browser, or type the backup code below.');
    }
  };

  return (
    <div className="stack">
      <div className="cam">
        <video ref={video} muted playsInline style={{ display: on ? 'block' : 'none' }} />
        {on ? (
          <>
            <div className="frame"><i /><i /><i /><i /></div>
            <div className="laser" />
          </>
        ) : (
          <button className="btn big" onClick={start} style={{ boxShadow: 'none', borderColor: 'var(--sheet)' }}>
            {Icon.scan} Open the camera
          </button>
        )}
      </div>
      {on && <button className="btn ghost block" onClick={stop}>Stop camera</button>}
      {err && <p className="small red">{err}</p>}
    </div>
  );
}

/** Camera + backup code. Used by the "Search the room" action of the Play screen. */
export function ScanPanel({ onResult }: { onResult: (r: ScanResult) => void }) {
  const { toast } = useGame();
  const [code, setCode] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (raw: string) => {
    if (!raw.trim() || busy) return;
    setBusy(true);
    try {
      const r = await emit<ScanResult>('card:scan', raw);
      setCode('');
      buzz(r.item.kind === 'trait' ? [40, 30, 120] : 40);
      onResult(r);
    } catch (e) {
      toast((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="stack">
      <p className="small">
        Draw the top card of your room's deck and scan its QR code. Only you see what it reveals.
      </p>
      <Camera onCode={submit} />
      <form
        onSubmit={(e) => {
          e.preventDefault();
          submit(code);
        }}
      >
        <div className="field">
          <label htmlFor="bk">No camera? Type the code under the QR</label>
          <div className="row">
            <input
              id="bk"
              className="input code grow"
              placeholder="LIB-01"
              value={code}
              maxLength={10}
              autoCapitalize="characters"
              autoComplete="off"
              onChange={(e) => setCode(e.target.value.toUpperCase())}
            />
            <button className="btn primary flat" style={{ minWidth: 80 }} disabled={busy || code.trim().length < 3}>
              {busy ? '…' : 'OK'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
