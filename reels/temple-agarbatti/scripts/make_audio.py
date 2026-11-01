"""Builds the audio for the reel. Everything here is synthesised in code (original,
no third-party samples), so the music and sound effects carry no licensing risk.

Outputs build/music.wav and build/sfx.wav. render.mjs mixes them under the voiceover.
"""
import json
import numpy as np
import soundfile as sf
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TL = json.loads((ROOT / "timeline.json").read_text(encoding="utf-8"))
SR = 44100
DUR = TL["duration"] + 0.6
N = int(SR * DUR)
rng = np.random.default_rng(7)
(ROOT / "build").mkdir(exist_ok=True)


def t_arr(sec):
    return np.arange(int(sec * SR)) / SR


def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e


def lowpass(x, cutoff):
    # one-pole low-pass (cheap, smooth)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def lp_fast(x, cutoff):
    # same filter, vectorised via scipy if present
    try:
        from scipy.signal import lfilter
        a = np.exp(-2 * np.pi * cutoff / SR)
        return lfilter([1 - a], [1, -a], x)
    except ImportError:
        return lowpass(x, cutoff)


def hp_fast(x, cutoff):
    return x - lp_fast(x, cutoff)


def add(buf, sig, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


def note_hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


# ------------------------------------------------------------------ music
BPM = TL.get("audio", {}).get("bpm", 118)
beat = 60 / BPM
bar = beat * 4
music = np.zeros((N, 2))

# A minor: Am - F - C - G (2 bars each)
prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [48, 52, 55]), (55, [55, 59, 62])]


def kick():
    t = t_arr(0.35)
    f = 48 + 90 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(len(t), 0.002, 0.13) * 0.9


def clap():
    t = t_arr(0.25)
    n = rng.standard_normal(len(t))
    n = hp_fast(lp_fast(n, 5000), 900)
    e = env(len(t), 0.001, 0.06)
    return n * e * 0.35


def hat(open_=False):
    t = t_arr(0.18 if open_ else 0.06)
    n = hp_fast(rng.standard_normal(len(t)), 7000)
    return n * env(len(t), 0.001, 0.05 if open_ else 0.015) * 0.18


def saw(freq, sec, detune=0.0):
    t = t_arr(sec)
    ph = (t * freq * (1 + detune)) % 1.0
    return 2 * ph - 1


def pad_chord(notes, sec):
    s = np.zeros(int(sec * SR))
    for m in notes:
        for d in (-0.004, 0.0, 0.005):
            s += saw(note_hz(m + 12), sec, d)
    s = lp_fast(s, 1400) / (len(notes) * 3)
    n = len(s)
    a = np.minimum(1, np.arange(n) / (0.25 * SR))
    r = np.minimum(1, (n - np.arange(n)) / (0.3 * SR))
    return s * a * r * 0.22


def bass(root, sec):
    t = t_arr(sec)
    f = note_hz(root - 12)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return s * env(len(t), 0.01, sec * 0.9) * 0.32


def pluck(m, sec=0.3):
    t = t_arr(sec)
    s = saw(note_hz(m + 24), sec) * 0.5 + np.sin(2 * np.pi * note_hz(m + 24) * t) * 0.5
    return lp_fast(s, 3200) * env(len(t), 0.002, 0.11) * 0.12


start = 0.0
t = start
bar_i = 0
K, C = kick(), clap()
while t < DUR:
    root, chord = prog[(bar_i // 2) % 4]
    intro = t < 2.9            # hook: sparser, lets impacts land
    for b in range(4):
        bt = t + b * beat
        add(music[:, 0], K, bt); add(music[:, 1], K, bt)
        if b in (1, 3) and not intro:
            c = C
            add(music[:, 0], c, bt); add(music[:, 1], c * 0.9, bt)
        for e8 in range(2):
            h = hat(open_=(e8 == 1 and b == 3))
            pan = 0.6 if e8 else 0.4
            add(music[:, 0], h * (1 - pan) * 2, bt + e8 * beat / 2)
            add(music[:, 1], h * pan * 2, bt + e8 * beat / 2)
        # bass on 8ths with rests
        for e8 in (0, 1):
            if not (b == 3 and e8 == 1):
                bs = bass(root, beat / 2 * 0.9)
                add(music[:, 0], bs, bt + e8 * beat / 2); add(music[:, 1], bs, bt + e8 * beat / 2)
    pc = pad_chord(chord, bar)
    add(music[:, 0], pc, t); add(music[:, 1], pc * 0.95, t)
    if not intro:
        arp = chord + [chord[1] + 12]
        for k in range(8):
            p = pluck(arp[(k * 3) % 4])
            pan = 0.3 + 0.4 * (k % 2)
            add(music[:, 0], p * (1 - pan) * 2, t + k * beat / 2)
            add(music[:, 1], p * pan * 2, t + k * beat / 2)
    t += bar
    bar_i += 1

# fade out last 0.8s
fo = int(0.8 * SR)
music[-fo:] *= np.linspace(1, 0, fo)[:, None]
music /= np.max(np.abs(music)) + 1e-9
music *= 0.8
sf.write(ROOT / "build" / "music.wav", music.astype(np.float32), SR)

# ------------------------------------------------------------------ sfx
sfx = np.zeros((N, 2))


def s_impact():
    t = t_arr(1.2)
    f = 38 + 70 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.45)
    n = lp_fast(rng.standard_normal(len(t)), 2500) * env(len(t), 0.001, 0.08) * 0.6
    s = np.tanh((boom + n) * 1.6) * 0.9
    return np.stack([s, s], 1)


def s_whoosh(sec=0.45):
    t = t_arr(sec)
    n = rng.standard_normal(len(t))
    # sweep a band by mixing two lowpasses with moving cutoff (approx via segments)
    out = np.zeros_like(n)
    seg = 512
    for i in range(0, len(n), seg):
        x = i / len(n)
        c = 400 + 5200 * np.sin(np.pi * x) ** 2
        out[i:i + seg] = hp_fast(lp_fast(n[i:i + seg], c), c * 0.35)
    shape = np.sin(np.pi * np.linspace(0, 1, len(t))) ** 1.5
    s = out * shape * 0.9
    pan = np.linspace(0.2, 0.8, len(t))
    return np.stack([s * (1 - pan) * 1.6, s * pan * 1.6], 1)


def s_pop():
    t = t_arr(0.18)
    f = 900 * np.exp(-t * 12) + 500
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.001, 0.05) * 0.7
    return np.stack([s, s], 1)


def s_tick():
    t = t_arr(0.08)
    s = np.sin(2 * np.pi * 2400 * t) * env(len(t), 0.0005, 0.012) * 0.5
    return np.stack([s, s], 1)


def s_shimmer():
    t = t_arr(1.4)
    s = np.zeros_like(t)
    for k, m in enumerate([81, 84, 88, 91, 93, 96]):
        d = k * 0.06
        tt = np.clip(t - d, 0, None)
        s += np.sin(2 * np.pi * note_hz(m) * tt) * (t > d) * np.exp(-tt * 3.0) * 0.12
    l = s; r = np.roll(s, int(0.012 * SR))
    return np.stack([l, r], 1)


def s_riser(sec=0.6):
    t = t_arr(sec)
    f = 200 + 1800 * (t / sec) ** 2
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15
    n = hp_fast(rng.standard_normal(len(t)), 3000) * 0.2
    s = (s + n) * (t / sec) ** 2
    return np.stack([s, s], 1)


def s_typing():
    out = np.zeros((int(0.8 * SR), 2))
    for k in range(4):
        c = s_tick()[:, 0] * 0.8
        c = c * (0.7 + 0.3 * rng.random())
        i = int((k * 0.17 + rng.random() * 0.03) * SR)
        out[i:i + len(c), 0] += c
        out[i:i + len(c), 1] += c
    return out


def s_click():
    a = s_tick() * 1.2
    b = s_pop() * 0.6
    out = np.zeros((max(len(a), len(b)), 2))
    out[: len(a)] += a
    out[: len(b)] += b
    return out


MAKE = {"impact": s_impact, "whoosh": s_whoosh, "pop": s_pop, "tick": s_tick,
        "shimmer": s_shimmer, "riser": s_riser, "typing": s_typing, "click": s_click}
for ev in TL["sfx"]:
    s = MAKE[ev["type"]]()
    i = int(ev["t"] * SR)
    j = min(N, i + len(s))
    sfx[i:j] += s[: j - i]
sfx /= max(1.0, np.max(np.abs(sfx)) / 0.95)
sf.write(ROOT / "build" / "sfx.wav", sfx.astype(np.float32), SR)
print("audio ok", DUR)
