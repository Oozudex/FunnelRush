/**
 * Multi-phone link through free public MQTT brokers (WebSocket over TLS).
 * No server of our own: GitHub Pages only serves the files, the brokers relay the messages.
 * Every message goes to 2 brokers at once and is de-duplicated, so the game keeps
 * working if one of them is down.
 */
import mqtt, { type MqttClient } from 'mqtt';

const BROKERS = ['wss://broker.hivemq.com:8884/mqtt', 'wss://broker.emqx.io:8084/mqtt'];
export const ROOT = 'thelastquery/v1/';

export const rid = () => Math.random().toString(36).slice(2, 10);
export const safe = (s: string) => String(s).replace(/[^a-zA-Z0-9_-]/g, '');

export interface Link {
  connected(): boolean;
  pub(topic: string, msg: object, opts?: { retain?: boolean; qos?: 0 | 1 }): void;
  wake(): void;
  close(): void;
}

export function link(
  topics: string[],
  onMsg: (topic: string, msg: any, retained: boolean) => void,
  onConn: () => void,
): Link {
  const seen = new Map<string, number>();
  const clients: MqttClient[] = [];
  let dead = false;
  for (const url of BROKERS) {
    let c: MqttClient;
    try {
      c = mqtt.connect(url, { clientId: `tlq_${rid()}`, clean: true, keepalive: 30, reconnectPeriod: 2500, connectTimeout: 8000 });
    } catch {
      continue;
    }
    clients.push(c);
    c.on('connect', () => {
      c.subscribe(topics, { qos: 0 });
      onConn();
    });
    c.on('close', () => !dead && onConn());
    c.on('offline', () => !dead && onConn());
    c.on('error', () => {
      /* mqtt.js reconnects by itself */
    });
    c.on('message', (topic, buf, packet) => {
      let m: any;
      try {
        m = JSON.parse(buf.toString());
      } catch {
        return;
      }
      if (!m || !m._k || seen.has(m._k)) return;
      seen.set(m._k, Date.now());
      if (seen.size > 500) {
        const old = Date.now() - 60_000;
        seen.forEach((t, k) => t < old && seen.delete(k));
      }
      onMsg(topic, m, !!packet?.retain);
    });
  }
  return {
    connected: () => clients.some((c) => c.connected),
    pub(topic, msg, opts) {
      const body = JSON.stringify({ _k: rid() + rid(), ...msg });
      for (const c of clients) {
        if (!c.connected) continue;
        try {
          c.publish(topic, body, { qos: opts?.qos ?? 1, retain: !!opts?.retain });
        } catch {
          /* ignore */
        }
      }
    },
    wake() {
      for (const c of clients) {
        if (!c.connected && !c.reconnecting) {
          try {
            c.reconnect();
          } catch {
            /* ignore */
          }
        }
      }
    },
    close() {
      dead = true;
      for (const c of clients) {
        try {
          c.end(true);
        } catch {
          /* ignore */
        }
      }
    },
  };
}
