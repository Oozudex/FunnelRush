// After `npm run build:pages`: GitHub Pages must not run Jekyll on ../docs.
import { writeFileSync } from 'node:fs';
writeFileSync(new URL('../../docs/.nojekyll', import.meta.url), '');
console.log('docs/ ready for GitHub Pages');
