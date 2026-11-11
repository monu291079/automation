# Balloon Arch reel (IdeasPulse.in, 9:16, 37.8 s)
Pipeline: `scripts/prep_clips.sh` (timelapse clips from reference footage) -> `align.py` (phrase timing from voiceover) -> `make_data.py` -> `make_audio.py` (original synthesized music + SFX) -> `npx remotion render src/index.ts Balloon build/silent.mp4` (in `remotion/`) -> `scripts/mix.sh`.
Footage/voice sources and outputs are gitignored (third-party reference footage is not redistributed).
Rule: picture never zooms/shakes; only glass widgets, captions and balloons move.
