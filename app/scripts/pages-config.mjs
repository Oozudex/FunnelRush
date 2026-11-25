// After `npm run build:pages`: point the GitHub Pages copy (../docs) to the Render server.
// Change the URL with: TLQ_SERVER=https://my-app.onrender.com npm run build:pages
import { writeFileSync } from 'node:fs';
const url = process.env.TLQ_SERVER || 'https://the-last-query.onrender.com';
writeFileSync(new URL('../../docs/config.js', import.meta.url),
  `// Game server (Render). Change this line if your Render URL is different.\nwindow.TLQ_SERVER = '${url}';\n`);
writeFileSync(new URL('../../docs/.nojekyll', import.meta.url), '');
console.log(`docs/ ready for GitHub Pages, server = ${url}`);
