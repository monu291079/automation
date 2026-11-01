// Renders each <section class="slide"> of carousel.html to a 1080x1350 JPG.
//   node carousel/render_carousel.mjs   -> out/carousel/slide-01.jpg ...
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, '..', 'out', 'carousel');
fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1400 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(HERE, 'carousel.html')).href);
await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => null))); window.fitAll(); });
const slides = await page.$$('section.slide');
for (let i = 0; i < slides.length; i++) {
  await slides[i].screenshot({ path: path.join(OUT, `slide-${String(i + 1).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 95 });
}
await browser.close();
console.log(`${slides.length} slides -> ${OUT}`);
