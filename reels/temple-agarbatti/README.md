# IdeasPulse Reel: Temple Flower Agarbatti & Dhoop

9:16 Instagram Reel, 1080 × 1920, 30 fps, 66 s (62.5 s voiceover + a 3.5 s QR end card), H.264 + AAC at -14 LUFS.
On-screen text is Roman Hinglish + English (Anton / Poppins). Music and sound effects are synthesized by `scripts/make_audio.py`, so they're original and free to use.

- **Final video:** `out/ideaspulse_temple_agarbatti_reel.mp4`
- **Light preview:** `out/preview_540p.mp4`

## Scenes

| Time | What's on screen |
|---|---|
| 0.0–4.3 | Hook: temple flower pile (speed-ramped). "KYA AAP JAANTE HAIN? / MANDIR KE PHOOL 🌸 / KACHRE MEIN?! 😱" |
| 4.3–7.6 | Creator: INHI SE LAKHON KA BUSINESS! 💰 |
| 7.6–13.3 | Footage: collecting flowers → incense smoke. "INHI PHOOLON SE / AGARBATTI + DHOOP 🪔" |
| 13.3–22.7 | Creator (Mathura • Vrindavan, pooja) → flower pile "KAMAI KA ZARIYA 💸" |
| 22.7–36.8 | Fast 7-step process, real footage + step labels: sampark → collect → sukhao → powder → binder + fragrance → agarbatti / dhoop cone → packaging |
| 36.8–42.3 | Creator → USP card "TEMPLE FLOWER AGARBATTI" (product art from the plan poster) |
| 42.3–47.5 | KAHAN BECHEIN?: Pooja shops → Mandir ke paas → Online |
| 47.5–52.3 | Creator: kitna kharcha? kitna munafa? |
| 52.3–56.9 | Plan poster + checklist, "COMMENT 'PHOOL' 👇 · Plan seedha DM mein", "FOLLOW IDEASPULSE" |
| 56.9–62.6 | Closing line over incense smoke: "KAL TAK BEKAAR PHOOL... / AAJ ROZGAAR + KHUSHBOO 🌸" |
| 62.6–66.0 | End card: logo, YouTube + Telegram QR codes (both verified to scan), comment PHOOL, ideaspulse.in |

## Sources (`assets/source/`)
- `voiceover.mp3`: master audio. `creator_main.mp4` matches it from 0 s; `creator_part2.mp4` starts at 47.45 s (set in `timeline.json` → `takes`).
- `broll_c1…c6`: temple waste, hand-making, collecting, drying/grinding, smoke, market.
- `assets/images/`: logo, QR codes, plan poster.

## Editing
All text and timings live in `timeline.json` (`broll[]`, `captions[]`, `text.*`, `sfx[]`). Re-render with `node render.mjs`, or quick stills with `node render.mjs --stills 1,30,60`. From an iPhone, ask Claude Code in a session on this repo.
