# Pushkar Complete Travel Guide 2026 (How Is Travellers Life)

Two A5 PDFs (Hindi + English), 27 pages each, with a linked table of contents, QR + tap-to-open Google Maps for every place, own trip photos and labelled AI illustrations.

- `data.py` — all content as (Hindi, English) pairs. Edit here, then rebuild.
- `build.py` — builds `guide_hi.html` / `guide_en.html`.
- `style.css` — design.
- `render.mjs` — renders both PDFs into `out/` and prints any page overflow.
- `assets/img/ai_*.jpg` — AI illustrations generated in Figma; other images are from the Nov 2026 trip.

Rebuild: `python3 build.py && node render.mjs`
