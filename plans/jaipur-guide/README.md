# Jaipur Complete Travel Guide 2026 (How Is Travellers Life)

A5 PDF lead magnet for the "Comment JAIPUR" reels. Hinglish, 35 pages, QR + tap-to-open Google Maps for every place.

- `data.py` — all place data (tickets, timings, tips, distances). Edit here, then rebuild.
- `build.py` — builds `guide.html` from data + assets.
- `style.css` — design.
- `render.mjs` — renders `out/*.pdf` with Playwright and prints any page overflow.

Rebuild: `python3 build.py && node render.mjs`
