import { useEffect, useRef, useState } from 'react';
import jsQR from 'jsqr';
import type { EvidenceItem, ScanResult } from '../../shared/types';
import { describe } from '../../shared/sql';
import { buzz, emit } from '../socket';
import { SectionTitle, useGame } from '../ui';

export function EvidenceCard({ item, note }: { item: EvidenceItem; note?: string }) {
  const { view } = useGame();
  const attr = item.condition && view.game.caseInfo.attributes.find((a) => a.key === item.condition!.attr);
  const label = item.kind === 'bonus' ? 'BONUS' : 'EVIDENCE';
  return (
    <div className="panel paper">
      <div className={`ev-head ${item.kind}`}>
        <span className="pix">{label}</span>
        <span className="mono" style={{ fontWeight: 700 }}>{item.code}</span>
      </div>
      <div style={{ paddingLeft: 14 }}>
        <div className="ev-obj">{item.object}</div>
        <div className="ev-room">Found in the {item.room}</div>
        <p className="ev-text">{item.text}</p>
        {item.kind === 'trait' && attr && (
          <>
            <div className="stamp">CLUE: {describe(attr, item.condition!).toUpperCase()}</div>
            <p className="small" style={{ marginTop: 10 }}>
              🔓 <b>{attr.label}</b> is unlocked in the Police Console.
            </p>
          </>
        )}
        {item.kind === 'deadend' && <div className="stamp" style={{ color: '#6b665c', borderColor: '#6b665c' }}>DEAD END</div>}
        {note && <p className="small" style={{ marginTop: 10, fontWeight: 700 }}>{note}</p>}
      </div>
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
          <div className="center" style={{ padding: 20 }}>
            <div className="pix muted" style={{ marginBottom: 12 }}>QR scanner</div>
            <button className="btn primary big" onClick={start}>Open camera</button>
          </div>
        )}
      </div>
      {on && <button className="btn ghost block" onClick={stop}>Stop camera</button>}
      {err && <p className="small amber">{err}</p>}
    </div>
  );
}

export default function Scan() {
  const { view, toast } = useGame();
  const [code, setCode] = useState('');
  const [result, setResult] = useState<ScanResult | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async (raw: string) => {
    if (!raw.trim() || busy) return;
    setBusy(true);
    try {
      const r = await emit<ScanResult>('card:scan', raw);
      setResult(r);
      setCode('');
      buzz(r.item.kind === 'trait' ? [40, 30, 120] : 40);
      setTimeout(() => document.getElementById('scan-result')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
    } catch (e) {
      toast((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const count = view.me.evidence.filter((e) => e.kind !== 'bonus').length;

  return (
    <div className="stack">
      <div>
        <div className="h2">Scan evidence</div>
        <p className="small muted">Search a room on the board, then scan the card you drew. Only you see what it reveals.</p>
      </div>

      <Camera onCode={submit} />

      <form
        className="stack"
        onSubmit={(e) => {
          e.preventDefault();
          submit(code);
        }}
      >
        <div className="field">
          <label htmlFor="bk">No camera? Type the backup code</label>
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
            <button className="btn primary" style={{ minWidth: 92 }} disabled={busy || code.trim().length < 3}>
              Scan
            </button>
          </div>
        </div>
      </form>

      {result && (
        <div id="scan-result" className="stack" style={{ scrollMarginTop: 120 }}>
          <SectionTitle>{result.again ? 'Already in your clues' : 'New evidence'}</SectionTitle>
          <EvidenceCard item={result.item} note={result.effect} />
          {result.item.kind !== 'bonus' && <p className="small muted center">Keep the card face down in front of you.</p>}
        </div>
      )}

      <p className="small muted center" style={{ marginTop: 8 }}>
        {count} evidence card{count === 1 ? '' : 's'} scanned. Bonus cards don't need scanning (Spare Battery codes add your token here).
      </p>
    </div>
  );
}
