# IdeasPulse Reel: 3D Resin Printing Business

A 9:16 Instagram Reel (1080 × 1920, 30 fps, 44.9 s, H.264 + AAC, mixed to -14 LUFS).

- **Final video:** `out/ideaspulse_resin_reel.mp4`
- **Light preview (540p):** `out/preview_540p.mp4`

This project is separate from the IdeasPulse website. It does not touch the site's database, payments, login, APIs or deployment.

## What's in it

| Time | Scene | Visuals |
|---|---|---|
| 0.0–1.7 | Hook | **Real footage**: print rising out of the resin vat, speed-ramped, headline visible from frame 1 |
| 1.7–2.9 | Hook | Cut to the Photon Mono 4 (the linked machine) with the price chip |
| 2.9–6.5 | Creator + footage | Talking head, quick cutaway to the finished print in hand |
| 6.5–12.5 | Machine demo | **Fast timeline**: Step 1 resin pour → Step 2 print start → layer-by-layer timelapse → Step 3 print ready |
| 12.5–15.4 | What you can sell | Gaming figures → custom gifts (real print close-up) → home decor (lit lantern) |
| 15.4–23.6 | Creator + concept | "Sochiye…", Photo ➜ 3D miniature (marked as a concept illustration), real print cutaway, custom orders |
| 23.6–26.4 | Home business | **4-step fast montage**: print setup → layer by layer → finishing → online becho |
| 26.4–31.7 | Reality check | Kit photo, cost rows, "PEHLE NIKALEIN POORA COST!", plus a note that earnings are not guaranteed |
| 31.7–36.6 | Creator | Chhote star se shuru → apna brand |
| 36.6–41.2 | Plan | Live footage card + checklist: machine cost, investment, profit calculation |
| 41.2–44.9 | CTA | Creator in a gold frame, a typed "PLAN" comment, Follow @ideaspulse.in |

## Sources used

- `assets/source/creator_part1.mov` and `creator_part2.mov`: your talking-head clips. Their audio matches `voiceover.mp3` exactly (clip 2 starts at 22.172 s). The two clips are joined in the pause at 23.50 s.
- `assets/source/voiceover.mp3`: the master audio.
- `assets/source/demo_resin_printing.mp4`: the real resin-printing demo (pour, print, lift, finished print). Its sound is not used. Which shots are used and how fast they play is set in the `"broll"` list in `timeline.json` (`in`/`out` = seconds in this clip).
- A second clip (a TikTok repost of another creator's Photon Mono 4 Ultra unboxing) was **not used**: it carries another creator's watermark, and it shows a different model.
- `assets/images/raw_*`: the Anycubic Photon Mono 4 listing images you supplied. Specs shown on screen (7" 10K, 9024×5120, 153×87×165 mm) come only from these images.
- Music and sound effects are synthesized in code by `scripts/make_audio.py`. They are original and need no licence.
- Fonts: Anton and Poppins (Google Fonts, SIL Open Font License).
- No IdeasPulse logo file was supplied, so the ending shows only the text "IdeasPulse.in". To add the real logo, put it in `assets/images/` and ask for it to be added to the CTA scene.

## Editing from an iPhone

**Option A: ask Claude Code (easiest).** Open a Claude Code session on this repo from the Claude app and say what to change, e.g. "change the hook text to …" or "make captions bigger". It edits, re-renders and commits.

**Option B: edit the text yourself, GitHub renders it.**
1. In the GitHub app or on github.com, open `reels/resin-printer/timeline.json` and tap the pencil to edit.
2. Change any on-screen text in `"text"` or `"captions"`, or nudge a timing (seconds on the voiceover). Keep the quotes and commas.
3. Commit. The **Render resin printer reel** action starts automatically (Actions tab). After ~10 minutes, download the MP4 from that run's **Artifacts** section.
   You can also start it by hand: Actions → Render resin printer reel → Run workflow.

Useful fields in `timeline.json`:
- `broll[]`: real-footage shots. Change `in`/`out` to pick a different moment, and `title2`, `hud` or `label` to change their text.
- `text.hook_line1`, `text.hook_line2`: the opening headline
- `text.price_chip`, `text.price_note`: the price badge and its disclaimer
- `captions[]`: subtitles on the talking-head shots. `hl` = the words shown in gold.
- `text.cta_comment`, `text.cta_follow`, `handle`: the call to action
- `sfx[]`: sound-effect hits (impact, whoosh, pop, tick, shimmer, riser, typing, click)
- `audio.music_gain_db`: music level under the voice (more negative = quieter)

## Rendering on a computer

Needs Node 18+, Python 3 with `numpy scipy soundfile pillow`, ffmpeg, and Playwright Chromium.

```bash
cd reels/resin-printer
npm install && npx playwright install chromium
node render.mjs                      # full render -> out/ideaspulse_resin_reel.mp4 (~3-4 min)
node render.mjs --stills 1.5,8,30    # quick PNG stills at given seconds -> out/stills/
```

Pipeline: `scripts/build_base.sh` (joins the creator clips into 30 fps frames) → `scripts/prep_images.py` (crops and cut-outs) → `composition.html` drawn frame by frame in headless Chromium → `scripts/make_audio.py` (music + SFX) → ffmpeg mix (music ducks under the voice) and H.264 encode.
