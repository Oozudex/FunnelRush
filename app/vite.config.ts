import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import basicSsl from '@vitejs/plugin-basic-ssl';
import { networkInterfaces } from 'node:os';

// HTTPS=1 npm run dev -> self-signed HTTPS, needed for the camera on phones over Wi-Fi.
const https = process.env.HTTPS === '1';
const ips = Object.values(networkInterfaces()).flat().filter((i) => i && i.family === 'IPv4' && !i.internal).map((i) => i!.address);
const lan = ips.find((i) => i.startsWith('192.168.')) ?? ips[0] ?? '';

export default defineConfig({
  base: './',
  plugins: [react(), ...(https ? [basicSsl()] : [])],
  define: { __LAN_IP__: JSON.stringify(lan) },
  server: { host: true, port: 5173 },
});
