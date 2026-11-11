"""Single source of truth for cuts and sound-effect times.
Writes remotion/src/timeline.json (picture) and timeline.json (audio script input)."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent.parent
W = json.loads((R / "remotion/src/words.json").read_text())
C = {c["id"]: c for c in W["chunks"]}
VOICE_END = W["paras"][-1][1] + 0.05
END_CARD = 4.0
DURATION = round(VOICE_END + END_CARD, 2)

# picture cuts: ref clip (timelapse / slow) or the creator talking head
CUTS = [
  dict(clip="b_fast", t0=0.00, t1=2.00, speed="4.8x"), dict(clip="e_fast", t0=2.00, t1=3.55, speed="2.1x"),
  dict(clip="d_fast", t0=3.55, t1=5.26, speed="3.3x"), dict(clip="c_fast", t0=5.26, t1=6.55, speed="3.2x"),
  dict(clip="creator", t0=6.55, t1=8.92), dict(clip="a_slow", t0=8.92, t1=13.70),
  dict(clip="b_slow", t0=13.70, t1=18.74), dict(clip="c_slow", t0=18.74, t1=21.20), dict(clip="creator", t0=21.20, t1=VOICE_END)]
json.dump(dict(duration=DURATION, voice_end=VOICE_END, cuts=CUTS), open(R / "remotion/src/timeline.json", "w"), indent=1)

sfx = [dict(t=c["t0"] - 0.05, type="whoosh") for c in CUTS[1:]]
sfx += [dict(t=0.08, type="impact"), dict(t=0.1, type="shimmer"), dict(t=1.6, type="riser"), dict(t=C["c3"]["t0"], type="impact"), dict(t=C["c6"]["t0"], type="impact"),
        dict(t=C["c14"]["t0"], type="impact"), dict(t=C["c16"]["t0"], type="impact"), dict(t=C["c26"]["t0"], type="impact"), dict(t=C["c21"]["t0"] - 0.55, type="riser"), dict(t=VOICE_END - 1.8, type="riser")]
sfx += [dict(t=C["c11"]["t0"], type="pop"), dict(t=C["c12"]["t0"], type="pop"), dict(t=C["c13"]["t0"], type="pop"), dict(t=C["c15"]["t0"], type="pop"), dict(t=C["c15"]["t0"] + .26, type="pop"), dict(t=C["c15"]["t0"] + .52, type="pop")]
sfx += [dict(t=C["c7"]["t1"] - 0.22, type="click"), dict(t=C["c9"]["t0"], type="pop"), dict(t=C["c9"]["t0"] + .14, type="pop"), dict(t=C["c9"]["t0"] + .28, type="pop"), dict(t=C["c9"]["t0"] + .42, type="pop"), dict(t=C["c9"]["t0"] + .56, type="pop")]
sfx += [dict(t=C["c22"]["t1"] - 0.1, type="pop"), dict(t=C["c23"]["t0"] + 0.55, type="pop"), dict(t=C["c23"]["t1"] - 0.1, type="pop"), dict(t=C["c20"]["t0"], type="pop"), dict(t=C["c21"]["t0"], type="shimmer")]
sfx += [dict(t=C["c25"]["t0"] + 0.35, type="typing"), dict(t=VOICE_END - 0.06, type="click"), dict(t=VOICE_END, type="whoosh"), dict(t=VOICE_END + 0.45, type="shimmer")]
sfx.sort(key=lambda e: e["t"])
json.dump(dict(fps=30, duration=DURATION, sfx=sfx, audio=dict(bpm=126, voice_gain_db=0, music_gain_db=-17, sfx_gain_db=-9, target_lufs=-14)), open(R / "timeline.json", "w"), indent=1)
print("duration", DURATION, "cuts", len(CUTS), "sfx", len(sfx))
