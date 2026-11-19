# Pushkar Complete Travel Guide 2026 (How Is Travellers Life)

One A5 PDF (55 pages): a home page with links to the Hindi guide (pages 2–28) and the English guide (pages 29–55), with a linked table of contents, QR + tap-to-open Google Maps for every place, own trip photos and labelled AI illustrations.

- `data.py` — all content as (Hindi, English) pairs. Edit here, then rebuild.
- `build.py` — builds `guide.html` (home page + Hindi + English).
- `style.css` — design.
- `render.mjs` — renders the combined PDF into `out/` and prints any page overflow.
- `assets/img/ai_*.jpg` — AI illustrations generated in Figma; other images are from the Nov 2026 trip.

Rebuild: `python3 build.py && node render.mjs`
