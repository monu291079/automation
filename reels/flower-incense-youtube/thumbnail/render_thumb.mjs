import { chromium } from 'playwright';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(pathToFileURL(path.join(HERE, 'thumbnail.html')).href);
await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => null))); });
await p.screenshot({ path: path.join(HERE, '..', 'out', 'thumbnail_1280x720.jpg'), type: 'jpeg', quality: 92 });
await b.close();
