import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import basicSsl from '@vitejs/plugin-basic-ssl';

// HTTPS=1 npm run dev -> self-signed HTTPS, needed for the camera on phones over Wi-Fi.
const https = process.env.HTTPS === '1';
const target = 'http://localhost:3001';

export default defineConfig({
  plugins: [react(), ...(https ? [basicSsl()] : [])],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': target,
      '/socket.io': { target, ws: true },
    },
  },
});
