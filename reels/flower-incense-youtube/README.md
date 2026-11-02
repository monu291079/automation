# IdeasPulse YouTube: Mandir ke Phoolon se Agarbatti + Dhoop (faceless, 16:9)

1920 × 1080, 30 fps, ~11:00, voiceover P1–P8 + original synthesized music/SFX (copyright-free), -14 LUFS.

- Final video: `out/ideaspulse_flower_incense_youtube.mp4` (720p phone copy: `_720p_mobile.mp4`)
- Thumbnail: `out/thumbnail_1280x720.jpg`
- Title, description, chapters, tags: `out/youtube_upload_text.md` (chapters also in `out/youtube_chapters.txt`)

## How it is built
- `scripts/make_timeline.py` → `timeline.json`: every background shot and on-screen graphic, timed from the start of each voiceover part (all text Hinglish).
- `composition.html`: IdeasPulse theme (navy #12213A, gold #A9812E, cream #FAF9F5, teal #218C87; Anton + Poppins). Graphic types: title, stamp, lower chips, panels (list / check / cross / money / numbered / bar chart), counter, 30-day timeline, comparison, price cards, chapter cards, intro, end screen.
- `render.mjs`: lays parts end to end (3.5 s intro, 1.6 s chapter card between parts, 20 s end screen), renders frames in Chromium, mixes voice + music (ducked) + SFX, encodes MP4s, writes YouTube chapters.
- `scripts/make_music.py`: soft devotional lo-fi (drone, pad, bells, light beat) + chapter stings + SFX.
- `scripts/build_base.sh`: clip frames. AI clips are reframed with a slight zoom; vertical clips get a blurred 16:9 background.

## Assets
- `assets/audio/P1–P8.wav`: voiceover parts (script: `voiceover_script.md`)
- `assets/images/img_*.jpg`: 5 still images; `assets/clips/w*.mp4`: AI b-roll; `r_*`: clips reused from the agarbatti reel.

## Editing
Change text or timings in `scripts/make_timeline.py`, run `python3 scripts/make_timeline.py`, then `node render.mjs`. Quick check: `node render.mjs --stills 30,200,400`.
