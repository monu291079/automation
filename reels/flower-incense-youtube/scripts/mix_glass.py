"""Audio for the glass-card video: places every voiceover part at its start time, builds the
original music + SFX (scripts/make_music.py), ducks the music under the voice, loudness-normalises
to -14 LUFS and muxes onto the silent Remotion render.
  python3 scripts/mix_glass.py           -> out/ideaspulse_flower_incense_glass.mp4 (+ _720p_mobile.mp4)"""
import json, os, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
B = R / "build_glass"
plan = json.loads((B / "audio_plan.json").read_text()); parts = json.loads((B / "voice_parts.json").read_text())
DUR = plan["duration"]
def run(*a, **kw): subprocess.run(list(map(str, a)), check=True, cwd=R, **kw)

run("python3", "scripts/make_music.py", env={**os.environ, "BUILD_DIR": str(B)})
vin = [x for p in parts for x in ("-i", p["file"])]
vf = ";".join(f"[{k}:a]aresample=48000,pan=mono|c0=c0,adelay={round(p['start'] * 1000)}[v{k}]" for k, p in enumerate(parts))
vf += ";" + "".join(f"[v{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0:duration=longest,apad,atrim=0:{DUR:.3f}[vo]"
run("ffmpeg", "-loglevel", "error", "-y", *vin, "-filter_complex", vf, "-map", "[vo]", B / "voiceover_full.wav")
mix = ";".join([
  "[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=150:makeup=3dB,asplit=2[vo][key]",
  "[2:a]aresample=48000,volume=-19dB[mus]", "[mus][key]sidechaincompress=threshold=0.025:ratio=5:attack=20:release=450[duck]",
  "[3:a]aresample=48000,volume=-12dB[sfx]", "[vo][duck][sfx]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=11[aout]"])
silent = R / "remotion/out/full_silent.mp4"
out = R / "out/ideaspulse_flower_incense_glass.mp4"
run("ffmpeg", "-loglevel", "error", "-y", "-i", silent, "-i", B / "voiceover_full.wav", "-i", B / "music.wav", "-i", B / "sfx.wav",
    "-filter_complex", mix, "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{DUR:.3f}", out)
run("ffmpeg", "-loglevel", "error", "-y", "-i", out, "-vf", "scale=1280:720", "-c:v", "libx264", "-preset", "medium", "-crf", "25", "-maxrate", "1500k", "-bufsize", "3000k",
    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out).replace(".mp4", "_720p_mobile.mp4"))
print("done", out)
