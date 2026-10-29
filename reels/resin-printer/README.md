# IdeasPulse Reel: 3D Resin Printing Business

A 9:16 Instagram Reel (1080 × 1920, 30 fps, 44.9 s, H.264 + AAC, mixed to -14 LUFS).

- **Final video:** `out/ideaspulse_resin_reel.mp4`
- **Light preview (540p):** `out/preview_540p.mp4`

This project is separate from the IdeasPulse website. It does not touch the site's database, payments, login, APIs or deployment.

## What's in it

| Time | Scene | Visuals |
|---|---|---|
| 0.0–2.9 | Hook | Figurine builds up layer by layer, camera pulls back to the printer, "3D MACHINE SE / CUSTOM BUSINESS! 😱" |
| 2.9–6.5 | Creator | Talking head with kinetic captions |
| 6.5–12.5 | Machine reveal | Printer orbit with labels for the LCD, build plate and resin vat; build volume (153 × 87 × 165 mm); 10K detail zoom |
| 12.5–15.4 | What you can sell | Gaming figures → custom gifts → collectibles |
| 15.4–23.6 | Creator + concept | "Sochiye…", then Photo ➜ 3D miniature (marked as a concept illustration), then custom orders |
| 23.6–26.4 | Home business | Ghar se shuru? Steps: design → print → wash & cure → pack → online order |
| 26.4–31.7 | Reality check | Kit photo, cost rows, "PEHLE NIKALEIN POORA COST!", plus a note that earnings are not guaranteed |
| 31.7–36.6 | Creator | Chhote star se shuru → apna brand |
| 36.6–41.2 | Plan | Business plan checklist: machine cost, investment, profit calculation |
| 41.2–44.9 | CTA | Creator in a gold frame, a typed "PLAN" comment, Follow @ideaspulse.in |

## Sources used

- `assets/source/creator_part1.mov` and `creator_part2.mov`: your talking-head clips. Their audio matches `voiceover.mp3` exactly (clip 2 starts at 22.172 s). The two clips are joined in the pause at 23.50 s.
- `assets/source/voiceover.mp3`: the master audio.
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
