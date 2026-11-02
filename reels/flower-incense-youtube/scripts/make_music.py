"""Original background music + sound effects for the long YouTube video, synthesised in
code (no samples, no licences needed). Soft devotional lo-fi: drone, pad, bass, bells,
gentle beat. Reads build/audio_plan.json written by render.mjs."""
import json
import numpy as np
import soundfile as sf
from pathlib import Path
from scipy.signal import lfilter

ROOT = Path(__file__).resolve().parent.parent
PLAN = json.loads((ROOT / "build" / "audio_plan.json").read_text())
SR = 44100
DUR = PLAN["duration"] + 0.5
N = int(SR * DUR)
rng = np.random.default_rng(11)

def lp(x, c): a = np.exp(-2 * np.pi * c / SR); return lfilter([1 - a], [1, -a], x)
def hp(x, c): return x - lp(x, c)
def ta(sec): return np.arange(int(sec * SR)) / SR
def env(n, a=.005, r=.2): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(buf, sig, at, gain=1.0, pan=.5):
    i = int(at * SR)
    if i >= len(buf) or i < 0: return
    j = min(len(buf), i + len(sig)); s = sig[: j - i] * gain
    if s.ndim == 1: buf[i:j, 0] += s * (1 - pan) * 2 ** .5; buf[i:j, 1] += s * pan * 2 ** .5
    else: buf[i:j] += s

# ---------------------------------------------------------------- music (D major, 84 bpm)
BPM = 84; beat = 60 / BPM; bar = beat * 4
prog = [(50, [62, 66, 69]), (47, [59, 62, 66]), (43, [55, 59, 62]), (45, [57, 61, 64])]   # D  Bm  G  A
pent = [74, 76, 78, 81, 83, 86]                                                          # D major pentatonic
mus = np.zeros((N, 2))

# drone (tanpura-like): D + A with slow beating, whole track
t = np.arange(N) / SR
dr = np.zeros(N)
for m, g in ((38, .5), (45, .35), (50, .25), (57, .12)):
    f = hz(m); dr += g * (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.003 * t) + .2 * np.sin(2 * np.pi * f * 3.01 * t))
dr *= (.75 + .25 * np.sin(2 * np.pi * t / 7.0))
dr = lp(dr, 1200) * .16
mus[:, 0] += dr; mus[:, 1] += np.roll(dr, int(.011 * SR))

def pad(notes, sec):
    s = np.zeros(int(sec * SR)); tt = ta(sec)
    for m in notes:
        for d in (-.003, 0, .004):
            ph = (tt * hz(m) * (1 + d)) % 1.0; s += (2 * ph - 1)
    s = lp(s, 900) / (len(notes) * 3); n = len(s)
    return s * np.minimum(1, np.arange(n) / (.6 * SR)) * np.minimum(1, (n - np.arange(n)) / (.6 * SR)) * .2

def bell(m, sec=2.6):
    tt = ta(sec); f = hz(m)
    s = sum(a * np.sin(2 * np.pi * f * r * tt) * np.exp(-tt * d) for a, r, d in ((1, 1, 1.4), (.5, 2.76, 2.5), (.3, 5.4, 4), (.2, 8.9, 6)))
    return s * env(len(tt), .002, 2.0) * .09

def kick():
    tt = ta(.3); f = 45 + 70 * np.exp(-tt * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), .002, .12) * .55
def shaker():
    tt = ta(.09); return hp(rng.standard_normal(len(tt)), 6000) * env(len(tt), .004, .025) * .07
def bassn(m, sec):
    tt = ta(sec); f = hz(m - 12); return (np.sin(2 * np.pi * f * tt) + .2 * np.sin(4 * np.pi * f * tt)) * env(len(tt), .02, sec * .8) * .22

K = kick(); bi = 0; tb = 0.0
while tb < DUR:
    root, ch = prog[(bi // 2) % 4]
    add(mus, pad(ch, bar * 1.02), tb)
    for b in range(4):
        bt = tb + b * beat
        if b in (0, 2): add(mus, K, bt)
        for e in range(2): add(mus, shaker(), bt + e * beat / 2, pan=.35 + .3 * e)
        if b in (0, 2): add(mus, bassn(root, beat * 1.8), bt)
    if bi % 2 == 0: add(mus, bell(pent[(bi // 2) % len(pent)]), tb + .02, pan=.6)
    # light pentatonic motif every other bar
    if bi % 4 in (1, 3):
        for k in range(3):
            add(mus, bell(pent[(bi * 3 + k * 2) % len(pent)] - 12, 1.2) * .7, tb + k * beat * 1.33, pan=.3 + .2 * k)
    tb += bar; bi += 1

# chapter stings: big bell + swell at each chapter card
for c in PLAN["chapters"]:
    add(mus, bell(74, 3.5) * 3, c + .1, pan=.5); add(mus, bell(81, 3.0) * 2, c + .35, pan=.65)
fo = int(2.5 * SR); mus[-fo:] *= np.linspace(1, 0, fo)[:, None]
mus /= np.max(np.abs(mus)) + 1e-9; mus *= .85
(ROOT / "build").mkdir(exist_ok=True)
sf.write(ROOT / "build" / "music.wav", mus.astype(np.float32), SR)

# ---------------------------------------------------------------- sound effects
sfx = np.zeros((N, 2))
def s_impact():
    tt = ta(1.0); f = 40 + 60 * np.exp(-tt * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), .002, .4); n = lp(rng.standard_normal(len(tt)), 2200) * env(len(tt), .001, .06) * .5
    return np.tanh((boom + n) * 1.5) * .8
def s_whoosh(sec=.5):
    tt = ta(sec); n = rng.standard_normal(len(tt)); out = np.zeros_like(n)
    for i in range(0, len(n), 512):
        x = i / len(n); c = 400 + 4800 * np.sin(np.pi * x) ** 2; out[i:i + 512] = hp(lp(n[i:i + 512], c), c * .35)
    return out * np.sin(np.pi * np.linspace(0, 1, len(tt))) ** 1.5 * .8
def s_pop():
    tt = ta(.16); f = 850 * np.exp(-tt * 12) + 480; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), .001, .045) * .55
def s_tick():
    tt = ta(.07); return np.sin(2 * np.pi * 2300 * tt) * env(len(tt), .0005, .012) * .45
def s_shimmer():
    tt = ta(1.3); s = np.zeros_like(tt)
    for k, m in enumerate([81, 85, 88, 93, 97]):
        d = k * .06; t2 = np.clip(tt - d, 0, None); s += np.sin(2 * np.pi * hz(m) * t2) * (tt > d) * np.exp(-t2 * 3) * .11
    return s
def s_riser(sec=.6):
    tt = ta(sec); f = 220 + 1600 * (tt / sec) ** 2
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * .12 + hp(rng.standard_normal(len(tt)), 3000) * .15) * (tt / sec) ** 2
MAKE = {"impact": s_impact, "whoosh": s_whoosh, "pop": s_pop, "tick": s_tick, "shimmer": s_shimmer, "riser": s_riser}
GAIN = {"impact": .8, "whoosh": .7, "pop": .5, "tick": .5, "shimmer": .7, "riser": .8}
for e in PLAN["sfx"]:
    add(sfx, MAKE[e["type"]](), e["t"], GAIN[e["type"]], pan=.5)
sfx /= max(1.0, np.max(np.abs(sfx)) / .95)
sf.write(ROOT / "build" / "sfx.wav", sfx.astype(np.float32), SR)
print("music + sfx", round(DUR, 1), "s")
