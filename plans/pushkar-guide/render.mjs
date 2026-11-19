import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const dir = new URL(".", import.meta.url).pathname;
const b = await chromium.launch();
for (const lang of ["hi", "en"]) {
  const p = await b.newPage({ viewport: { width: 560, height: 794 } });
  await p.goto("file://" + dir + `guide_${lang}.html`);
  await p.waitForTimeout(900);
  const over = await p.evaluate(() => [...document.querySelectorAll(".page")].map((pg, i) => {
    const f = pg.querySelector("footer"); const limit = f ? f.getBoundingClientRect().top - 2 : pg.getBoundingClientRect().bottom;
    let max = 0; pg.querySelectorAll(".body > *, .pad > *").forEach(el => { max = Math.max(max, el.getBoundingClientRect().bottom); });
    return [i + 1, Math.round(max - limit)];
  }).filter(x => x[1] > 0));
  console.log(lang, "OVERFLOW", JSON.stringify(over));
  const name = lang === "hi" ? "Pushkar_Travel_Guide_2026_Hindi_HowIsTravellersLife.pdf" : "Pushkar_Travel_Guide_2026_English_HowIsTravellersLife.pdf";
  await p.pdf({ path: dir + "out/" + name, width: "148mm", height: "210mm", printBackground: true, outline: true, tagged: true });
  await p.close();
}
await b.close();
