# IdeasPulse Reel: Butter Candle Business

9:16 Instagram Reel, 1080 × 1920, 30 fps, 45.0 s, H.264 + AAC at -14 LUFS.

- **Final video:** `out/ideaspulse_butter_candle_reel.mp4`
- **Light preview:** `out/preview_540p.mp4`

On-screen text mixes Hindi (Devanagari, Khand font) with English words (Anton / Poppins).

## Scenes

| Time | Scene | What's on screen |
|---|---|---|
| 0.0–2.4 | Hook | Real footage of a butter candle being lit and dipped. "इस दिवाली / खाने वाली CANDLE! 😱" is visible from the first frame, plus "सिर्फ ₹5,000 से शुरू*". |
| 2.4–5.6 | Creator (take A) | ऐसा UNIQUE BUSINESS → जिसे देखकर लोग पूछेंगे… |
| 5.6–10.3 | Footage | Bread dipped into the melted candle, then "जी हाँ, ये है BUTTER CANDLE" |
| 10.3–12.8 | Creator (take B) | जो जलती भी है 🔥 / और खाई भी जाती है 😋 |
| 12.8–18.2 | Fast montage | अमेरिका में VIRAL FOOD TREND: mixing → herbs → wick → moulding |
| 18.2–22.4 | Creator (take C) | CHICAGO के RESTAURANTS में भी / खास अंदाज़ में SERVE |
| 22.4–27.0 | Flavours | Garlic / Chilli / Rosemary chips over the jars from the plan poster |
| 27.0–32.4 | Where to sell | Footage: DIWALI PARTIES → CAFES → PREMIUM HAMPERS |
| 32.4–34.4 | Creator (take A) | घर से ही शुरुआत 🏠 |
| 34.4–36.9 | Budget | The plan PDF's ₹5,000 budget page scrolls in, with the TOTAL row highlighted |
| 36.9–39.8 | Plan PDF | 5 PDF pages flip in like a book, then "COMMENT 'BUTTER' 👇 · Plan सीधा DM में" |
| 39.8–45.0 | Community | Logo reveal, YouTube + Telegram QR codes (held still so they can be scanned), Instagram comment line, ideaspulse.in |

## Source files (`assets/source/`)

- `voiceover.mp3`: master audio. `creator_takeA/B/C.mp4` are three lip-synced takes; the reel cuts between them.
- `broll_b1/b2/b3.mp4`: the recipe clips you supplied. Only hands and food shots are used. These look like other creators' videos, so make sure you have the right to use them.
- `Butter_Candle_Plan.pdf`: its pages are rendered to `assets/pdf_pages/`.
- `assets/images/`: logo, QR codes (both checked to decode: `youtube.com/@ideaspuls`, `t.me/ideaspulse`), and the jars cropped from the plan poster.

Music and sound effects are synthesized by `scripts/make_audio.py` (original, no licence needed).

## Editing

All text and timings live in `timeline.json`:
- `captions[]`: subtitles on creator shots. `hl` = the word shown in gold.
- `broll[]`: footage shots (`clip`, `in`/`out` seconds, zoom, `title1`/`title2`/`hud`/`label` text).
- `text.*`: flavours, budget, PDF pages shown (`pdf_pages`), comment keyword, ending text.

From an iPhone: open a Claude Code session on this repo and ask for the change. Or edit `timeline.json` on GitHub; the **Render butter candle reel** action re-renders it and attaches the MP4 under the run's Artifacts.

Rendering on a computer: Node 18+, Python 3 (`numpy scipy soundfile pillow zxing-cpp`), ffmpeg, poppler-utils (`pdftoppm`), and Playwright Chromium:

```bash
cd reels/butter-candle
npm install && npx playwright install chromium
node render.mjs                     # full render (~4 min)
node render.mjs --stills 1,20,41    # quick PNG stills
```
