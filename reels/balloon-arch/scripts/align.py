"""Caption timing for the balloon reel. The voice has 6 paragraphs separated by pauses; inside each paragraph the
phrases are placed in proportion to their syllable count and every boundary is snapped to the quietest spot nearby
(that is where one word ends and the next begins). 'gap' marks a spoken ellipsis (a longer, deeper dip is searched)."""
import json, sys
import numpy as np, soundfile as sf
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
a, sr = sf.read(sys.argv[1]); a = a if a.ndim == 1 else a[:, 0]
h = int(sr * .01); n = len(a) // h
db = 20 * np.log10(np.array([np.sqrt(np.mean(a[i*h:(i+1)*h] ** 2)) for i in range(n)]) + 1e-9)
sm = np.convolve(db, np.ones(3) / 3, mode="same")
loud = np.where(db > -38)[0]; START, END = loud[0] / 100, loud[-1] / 100 + 0.04
PARAS = [  # (start, end) of each paragraph, from the pauses found earlier
  (START, 8.71), (8.92, 13.44), (13.70, 18.50), (18.74, 23.29), (23.53, 27.62), (27.84, END)]
# (id, text, syllables, style, gap_after)   style: n normal, g gold, h hidden (spoken, not shown)
CH = [
 [("c1", "YE BHAI VIDESHON MEIN", 6, "n", 0), ("c2", "BALLOON ARCH 🎈", 3, "g", 0), ("c3", "LAKHON KA KAROBAR!", 6, "g", 0), ("c3b", "", 4, "h", 1),
  ("c4", "AUR AB YAHI MACHINE", 6, "n", 0), ("c5", "BHARAT MEIN BHI", 4, "n", 0), ("c6", "KAMAI KA MAUKA 🇮🇳", 5, "g", 0), ("c6b", "", 4, "h", 0)],
 [("c7", "SIRF EK BUTTON DABAIYE", 7, "n", 1), ("c8", "AUR KAI GUBBARE", 5, "n", 0), ("c9", "EK SAATH PHOOLNE", 5, "n", 0), ("c10", "LAGTE HAIN! 🎈", 3, "g", 0)],
 [("c11", "PUMP KO CONNECT KIJIYE", 7, "n", 0), ("c12", "BALLOONS LAGAIYE", 5, "n", 0), ("c13", "AUR TAIYAR KIJIYE", 7, "n", 0), ("c14", "SHAANDAR BALLOON ARCH!", 6, "g", 0)],
 [("c15", "BIRTHDAY • WEDDING • BABY SHOWER", 9, "n", 0), ("c15b", "", 8, "h", 0), ("c16", "₹2,000 SE ₹10,000", 9, "g", 0), ("c17", "YA USSE BHI ZYADA", 6, "g", 0),
  ("c17b", "", 4, "h", 0), ("c18", "DESIGN AUR DECORATION KE HISAAB SE", 12, "n", 0)],
 [("c19", "AB SOCHIYE... 🤔", 4, "n", 1), ("c20", "MAHINE MEIN 10 EVENTS BHI MILE", 12, "n", 0), ("c21", "TO KITNI KAMAI HO SAKTI HAI?", 9, "g", 0)],
 [("c22", "IS BUSINESS KI MACHINE,", 6, "n", 0), ("c23", "INVESTMENT AUR PROFIT", 7, "n", 0), ("c24", "KA POORA HISAAB CHAHIYE?", 8, "n", 0), ("c25", "COMMENT KARO", 4, "n", 0), ("c26", "BALLOON! 🎈", 2, "g", 0)],
]
out = []
for p, ((s, e), chs) in enumerate(zip(PARAS, CH)):
    tot = sum(c[2] for c in chs); cum = 0; b = [s]
    for c in chs[:-1]:
        cum += c[2]; est = s + (e - s) * cum / tot; w = .35 if c[4] else .12
        lo, hi = max(0, int((est - w) * 100)), int((est + w) * 100)
        b.append((lo + int(np.argmin(sm[lo:hi]))) / 100)
    b.append(e)
    for k, c in enumerate(chs):
        out.append(dict(id=c[0], text=c[1], style=c[3], para=p + 1, t0=round(b[k], 2), t1=round(b[k + 1], 2)))
(ROOT / "remotion/src").mkdir(parents=True, exist_ok=True)
(ROOT / "remotion/src/words.json").write_text(json.dumps(dict(start=START, end=END, paras=PARAS, chunks=out), ensure_ascii=False, indent=1))
for c in out: print(f"{c['t0']:5.2f}-{c['t1']:5.2f} P{c['para']} {c['id']:4s} {c['style']} {c['text']}")
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(24, 3.4)); t = np.arange(n) / 100; ax.plot(t, db, lw=.7, color="#218C87"); ax.set_ylim(-70, -4); ax.set_xlim(0, END + .3)
    for c in out:
        ax.axvline(c["t0"], color="#A9812E", lw=1)
        if c["text"]: ax.text(c["t0"] + .02, -6, c["id"], rotation=90, va="top", fontsize=8)
    fig.tight_layout(); fig.savefig(ROOT / "build/sync_check.png", dpi=60)
except ImportError: pass
