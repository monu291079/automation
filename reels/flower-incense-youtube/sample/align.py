"""Word timing for the 15 s kinetic-typography sample.
Speech segments come from the loudness envelope of the voiceover; inside a segment the words are
placed in proportion to their syllable count and each boundary is snapped to the quietest spot
(+-80 ms), which is where one word ends and the next begins."""
import json, sys
import numpy as np, soundfile as sf
from pathlib import Path
SRC = Path(sys.argv[1]); OUT = Path(__file__).parent / "words.json"
a, sr = sf.read(SRC); a = a[: sr * 16]
h = int(sr * .01); n = len(a) // h
db = 20 * np.log10(np.array([np.sqrt(np.mean(a[i*h:(i+1)*h] ** 2)) for i in range(n)]) + 1e-9)
sm = np.convolve(db, np.ones(3) / 3, mode="same")
# (segment start, end) from the envelope, then the units spoken in it: (text, syllables, line, style)
SEG = [
 ((0.14, 3.66), [("KYA", 1, "A", "n"), ("AAPNE", 3, "A", "n"), ("KABHI", 2, "A", "n"), ("SOCHA HAI", 3, "A", "n"),
                 ("MANDIR MEIN", 3, "B", "n"), ("CHADHE", 2, "B", "n"), ("PHOOL", 1, "B", "g"),
                 ("AGLE DIN", 4, "C", "n"), ("KAHAN", 2, "C", "n"), ("JAATE HAIN?", 3, "C", "g")]),
 ((4.86, 5.61), [("ZYAADATAR...", 1, "D", "s")]),
 ((5.91, 6.39), [("KACHRE MEIN", 1, "E", "r")]),
 ((7.44, 9.52), [("SUBAH", 2, "F", "n"), ("SUNDAR", 2, "F", "n"), ("KHUSHBOODAAR", 4, "F", "g"), ("PHOOL", 1, "F", "g")]),
 ((9.94, 10.75), [("AUR", 1, "G", "n"), ("SHAAM", 2, "G", "d"), ("TAK?", 1, "G", "d")]),
 ((11.11, 11.40), [("BAS", 1, "H", "s")]),
 ((11.62, 12.09), [("EK", 1, "H", "s")]),
 ((13.14, 13.98), [("DHER.", 1, "H", "r")]),
]
units = []
for (s, e), us in SEG:
    tot = sum(u[1] for u in us); cum = 0; b = [s]
    for u in us[:-1]:
        cum += u[1]; est = s + (e - s) * cum / tot
        lo, hi = int((est - .08) * 100), int((est + .08) * 100)
        b.append((lo + int(np.argmin(sm[lo:hi]))) / 100)
    b.append(e)
    for k, u in enumerate(us):
        units.append(dict(text=u[0], t0=round(b[k], 2), t1=round(b[k + 1], 2), line=u[2], style=u[3]))
OUT.write_text(json.dumps(units, ensure_ascii=False, indent=1))
for u in units: print(f"{u['t0']:5.2f}-{u['t1']:5.2f} {u['line']} {u['style']} {u['text']}")
# picture to check the sync by eye
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(22, 4)); t = np.arange(n) / 100
    ax.plot(t, db, lw=.8, color="#218C87"); ax.set_ylim(-70, -5); ax.set_xlim(0, 15)
    for u in units:
        ax.axvline(u["t0"], color="#A9812E", lw=1); ax.text(u["t0"] + .01, -9, u["text"], rotation=90, va="top", fontsize=8)
    fig.tight_layout(); fig.savefig(Path(__file__).parent / "sync_check.png", dpi=70)
except ImportError:
    print("matplotlib missing")
