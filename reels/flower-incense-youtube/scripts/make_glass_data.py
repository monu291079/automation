"""Builds everything the glass-card version of the YouTube video needs:
  remotion/src/data/video.json   absolute timeline (backgrounds, glass cards, chapters)
  build_glass/audio_plan.json    SFX events + chapter times for the music script
  build_glass/voice_parts.json   which voiceover file starts when
  out/youtube_chapters.txt       chapter timestamps for the description
Parts P1..P8 come from scripts/make_timeline.py (text + timings); P8 is cut in two so the
scorecard (P9) and Q&A (P10) can sit between the safety rules and the closing call to action."""
import json, runpy, subprocess, copy, shutil
from pathlib import Path

R = Path(__file__).resolve().parent.parent
g = runpy.run_path(str(R / "scripts/make_timeline.py"))          # also rewrites timeline.json (harmless)
T, S, L, PN, I, BG = g["T"], g["S"], g["L"], g["PN"], g["I"], g["BG"]
P = {p["id"]: copy.deepcopy(p) for p in g["parts"]}
GAP, END = 1.6, 20.0

def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(R / path)]).decode())

INTRO = round(dur("assets/audio/P0.wav") + 0.5, 1)      # cold-open hook (P0) replaces the old silent title card

# ---------------------------------------------------------------- hook (P0): words timed to the voice
import numpy as np, soundfile as sf
def hook_units():
    a, sr = sf.read(str(R / "assets/audio/P0.wav")); h = int(sr * .01); n = len(a) // h
    db = 20 * np.log10(np.array([np.sqrt(np.mean(a[i*h:(i+1)*h] ** 2)) for i in range(n)]) + 1e-9); sm = np.convolve(db, np.ones(3) / 3, mode="same")
    # (speech segment start, end) from the loudness envelope; units spoken in it: (text, syllables, line, style)
    SEG = [((0.16, 1.57), [("MANDIR KE", 3, "A", "n"), ("KACHRE SE 🗑️", 3, "A", "n"), ("KAMAI? 💰", 2, "A", "g")]),
           ((2.62, 3.70), [("SUNNE MEIN", 3, "B", "n"), ("AJEEB", 2, "B", "n"), ("LAGTA HAI", 3, "B", "n")]),
           ((4.02, 6.01), [("LEKIN AAJ", 3, "C", "n"), ("MAIN ISKA", 3, "C", "n"), ("POORA HISAAB", 4, "D", "g"), ("DIKHAUNGA", 3, "D", "g")]),
           ((6.72, 7.99), [("₹5,000 KE", 4, "E", "g"), ("TEST SE", 2, "E", "n")]),
           ((8.24, 9.40), [("90 DIN", 2, "F", "g"), ("KE PLAN", 2, "F", "n"), ("TAK", 1, "F", "n")])]
    out = []
    for (s0, e0), us in SEG:
        tot = sum(u[1] for u in us); cum = 0; b = [s0]
        for u in us[:-1]:
            cum += u[1]; est = s0 + (e0 - s0) * cum / tot; lo, hi = int((est - .08) * 100), int((est + .08) * 100)
            b.append((lo + int(np.argmin(sm[lo:hi]))) / 100)
        b.append(e0)
        for k, u in enumerate(us): out.append(dict(text=u[0], t0=round(b[k], 2), t1=round(b[k + 1], 2), line=u[2], style=u[3]))
    return out
HOOK_UNITS = hook_units()
HOOK_LINES = {"A": dict(top=340, size=124, exit=2.45), "B": dict(top=340, size=124, exit=3.95), "C": dict(top=230, size=130, exit=6.5), "D": dict(top=430, size=150, exit=6.5),
              "E": dict(top=340, size=160, exit=8.15), "F": dict(top=340, size=170, exit=9.4)}
HOOK_CHIPS = [dict(at=5.1, text="🧮 POORA HISAAB"), dict(at=7.0, text="₹5,000 TEST"), dict(at=8.5, text="90 DIN PLAN")]
HOOK_BG = [(0.0, "clip:w01b_flowers_dumped", 0.3), (2.6, "clip:w01_temple_waste", 1.0), (4.0, "img:img_packs_money", 0), (6.7, "img:img_workshop", 0), (8.2, "clip:x03_two_cones_burn", 1.0)]

# ---------------------------------------------------------------- new clips in the existing parts
def setbg(pid, t, src=None, inn=None, insert=False):
    bgs = P[pid]["bg"]
    if insert:
        bgs.append(BG(t, src, inn=inn)); bgs.sort(key=lambda b: b["t"]); return
    for b in bgs:
        if abs(b["t"] - t) < 1e-6: b["src"] = src; return
    raise KeyError((pid, t))
setbg("P3", 5.6, "clip:x01_clean_flowers")
setbg("P3", 51.0, "clip:x09_binder_mix", insert=True)
setbg("P3", 84.0, "clip:x06_label_pack", insert=True)
setbg("P4", 40.4, "clip:x06_label_pack", insert=True)
setbg("P5", 46.8, "clip:x05_margin_calc")
setbg("P6", 13.2, "clip:x07_rickshaw")
setbg("P2", 61.4, "clip:w11_gift_box")

# ---------------------------------------------------------------- P8 -> P8a + P8b
CUT = 62.45
A = R / "assets/audio"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(A / "P8.wav"), "-t", str(CUT), str(A / "P8a.wav")], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(A / "P8.wav"), "-ss", str(CUT), str(A / "P8b.wav")], check=True)
p8 = P["P8"]
def shift(o, d):
    o = copy.deepcopy(o)
    for k in ("t0", "t1", "at", "sub_at"):
        if o.get(k) is not None: o[k] -= d
    for k in ("items", "chips", "blocks", "cards"):
        for it in o.get(k, []) or []:
            it["at"] -= d
            if "valAt" in it: it["valAt"] -= d
    for c in o.get("cols", []) or []:
        for r in c["rows"]: r["at"] -= d
    return o
p8a = dict(p8, id="P8a", file="assets/audio/P8a.wav", chapter="SURAKSHA + KAANOON", short="SURAKSHA + KAANOON")
p8a["bg"] = [b for b in p8["bg"] if b["t"] < CUT]
p8a["ov"] = [dict(o, t1=min(o["t1"], CUT - 0.15)) for o in p8["ov"] if o["t0"] < CUT - 0.1]
later = [b for b in p8["bg"] if b["t"] >= CUT]
p8b_bg = [dict(later[0], t=0)] + [dict(b, t=b["t"] - CUT) for b in later[1:]]
p8b = dict(p8, id="P8b", file="assets/audio/P8b.wav", chapter="AAKHRI SANDESH", short="AAKHRI SANDESH", bg=p8b_bg, ov=[shift(o, CUT) for o in p8["ov"] if o["t0"] >= CUT - 0.1])

# ---------------------------------------------------------------- P9 scorecard
def row(at, text, icon, tick): return dict(at=at, text=text, icon=icon, val="✅", valAt=tick)
p9 = dict(id="P9", file="assets/audio/P9.mp3", chapter="GO / NO-GO SCORECARD", short="GO / NO-GO",
 bg=[BG(0, "img:img_workshop"), BG(10.6, "clip:x01_clean_flowers"), BG(19.2, "clip:x03_two_cones_burn"), BG(27.25, "clip:x04_buy_pouches"),
     BG(35.35, "clip:x05_margin_calc"), BG(45.4, "clip:x06_label_pack"), BG(53.9, "img:img_puja_cone")],
 ov=[T(0.2, 4.6, "AAKHRI JAANCH ✅", kicker="SHURU KARNE SE PEHLE", sub="Khud se 5 sawaal", sub_at=2.8, size=130),
     T(5.8, 9.5, "GO / NO-GO SCORECARD", kicker="MAIN ISE KEHTA HOON", size=112),
     PN(9.8, 53.2, "5 SAWAAL — 5 JAWAAB", [
        row(10.6, "KACCHA MAAL: saaf phool, niyamit, ijazat ke saath?", "1️⃣", 17.0),
        row(19.2, "PRODUCTION: har batch mein ek jaisa sookhna + jalna?", "2️⃣", 25.0),
        row(27.25, "GRAHAK: sample lene wale paise dekar dobara order dete hain?", "3️⃣", 33.3),
        row(35.35, "KAMAI KA HISAAB: dukaandaar margin + delivery ke baad bhi paisa bachta hai?", "4️⃣", 43.2),
        row(45.4, "NIYAM: label, suraksha, standards ki jaanch poori hai?", "5️⃣", 52.1)],
        style="num", pos="left", w=1130, top=110, kicker="GO / NO-GO"),
     S(53.9, 57.0, "PAANCHON HAAN = GO ✅", color="teal", top=440, size=96),
     S(57.3, 62.3, "KAHIN NAHI? ROKO → THEEK KARO 🔧", color="red", top=440, size=80)])
for o in p9["ov"]:
    if o["type"] == "panel":
        for it in o["items"]: it.setdefault("valAt", None)

# ---------------------------------------------------------------- P10 Q&A + sources
QA = [
 (3.45, 6.1, "KYA MANDIR KE PHOOL MUFT MILENGE?", "ZAROORI NAHI", "Ijazat • collection ka samjhauta • dhulai-chhantai ka kharch"),
 (12.4, 14.8, "KYA HAR TARAH KE PHOOL CHALENGE?", "NAHI", "Pehle alag-alag phoolon ka chhota trial + gandagi/milawat ki jaanch"),
 (19.5, 23.2, "KYA SIRF PHOOL PEESKAR AGARBATTI BAN JAYEGI?", "AAMTAUR PAR NAHI", "Binder / filler aur sahi formulation ki zaroorat hoti hai"),
 (28.7, 31.4, "KYA ₹5,000 MEIN FACTORY LAG JAYEGI?", "NAHI", "Ye sirf haath se banaya jaane wala chhota test hai"),
 (38.2, 40.4, "SHURUAAT DHOOP CONE SE KYUN?", "HAATH SE MOULDING AASAAN", "Shuruaati pilot mein ye apekshakrit saral ho sakta hai"),
 (43.5, 46.6, "KYA HAR BATCH KI KHUSHBOO EK JAISI?", "NAHI — FARQ AA SAKTA HAI", "Phoolon ki kism aur mausam se. Isliye batch control zaroori"),
 (52.4, 54.9, "KITNA PROFIT HOGA?", "PATA NAHI — BINA ASLI DATA", "Asli bikri, barbaadi aur roz ke fixed kharch jaane bina bharosemand profit nahi"),
]
qa_items = [dict(q_at=q, a_at=a, q=qq, a=aa, sub=ss, t1=(QA[i + 1][0] if i + 1 < len(QA) else 61.0) - 0.15, n=i + 1) for i, (q, a, qq, aa, ss) in enumerate(QA)]
p10 = dict(id="P10", file="assets/audio/P10.mp3", chapter="SAWAAL-JAWAAB + SOURCES", short="SAWAAL-JAWAAB",
 bg=[BG(0, "img:img_cones_sticks"), BG(3.45, "clip:x01_clean_flowers"), BG(12.4, "clip:x08_flower_types"), BG(19.5, "clip:x09_binder_mix"), BG(28.7, "clip:w06_mould"),
     BG(38.2, "clip:x03_two_cones_burn"), BG(43.5, "clip:x02_cones_rack"), BG(52.4, "clip:x05_margin_calc"), BG(61.1, "img:img_temple_sunrise"), BG(72.3, "img:img_puja_cone")],
 ov=[T(0.2, 3.3, "SAWAAL-JAWAAB 🙋", kicker="AB KUCH SAWAAL JO SABKE MAN MEIN AATE HAIN", size=120),
     dict(type="qa", t0=3.4, t1=61.0, at=3.4, items=qa_items),
     PN(61.1, 72.2, "SOURCES — YE PLAN KIN PAR TIKA HAI", [I(62.0, "NITI for States — mandir ke phool se agarbatti case study", "🏛️"),
        I(65.3, "ThePrint — mandir ke phoolon ki recycling report", "📰"), I(67.6, "PIB — BIS IS 19412:2025 ghoshna", "📜"),
        I(70.0, "Saare links video ke description mein", "🔗")], style="list", pos="center", w=1500, top=190, kicker="GAHRAI JAANKARI"),
     PN(72.3, 76.5, "KHARIDNE SE PEHLE", [I(72.9, "Supplier se quotation lein", "🧾"), I(74.2, "Niyam aur standards khud jaanchein", "✅")], style="check", pos="center", w=1100, top=330)])

# ---------------------------------------------------------------- chapter teasers (open loop to the next chapter)
TEASE = {"P1": "", "P2": "Pehle samjho: business hai kya, kya bechein?", "P3": "8 steps — ek-ek karke, ijazat se packing tak",
         "P4": "Kitne paise lagenge? Seedha hisaab", "P5": "Ek pack par kitni bachat? Aur pehla batch", "P6": "Phool kahan se, bechna kahan, pehle 90 din",
         "P7": "1 saal mein kitna? Machine kab lein?", "P8a": "Suraksha + kaanoon — yahan galti mat karna", "P9": "Kya aap taiyaar hain? Go / No-Go jaanch",
         "P10": "Aapke sawaal, saaf jawaab + sources", "P8b": "Aakhri sandesh aur aapka agla kadam"}
ORDER = [P["P1"], P["P2"], P["P3"], P["P4"], P["P5"], P["P6"], P["P7"], p8a, p9, p10, p8b]

# ---------------------------------------------------------------- absolute timeline
def absolute(o, d):
    o = copy.deepcopy(o)
    for k in ("t0", "t1", "at", "sub_at"):
        if o.get(k) is not None: o[k] += d
    for k in ("items", "chips", "blocks", "cards"):
        for it in o.get(k, []) or []:
            if "at" in it: it["at"] += d
            for kk in ("valAt", "q_at", "a_at", "t1"):
                if it.get(kk) is not None: it[kk] += d
    for c in o.get("cols", []) or []:
        for r in c["rows"]: r["at"] += d
    return o

cur = INTRO; parts, chapters, bgs, ovs, voice, sfx = [], [], [], [], [], []
voice.append(dict(file="assets/audio/P0.wav", start=0.0))
for i, (t0, src, inn) in enumerate(HOOK_BG):
    kind, name = src.split(":", 1)
    bgs.append(dict(t0=t0, t1=HOOK_BG[i + 1][0] if i + 1 < len(HOOK_BG) else INTRO, kind=kind, name=name, inn=inn))
    if i: sfx.append(dict(t=t0 - 0.06, type="whoosh"))
ovs.append(dict(type="hook", t0=0.0, t1=INTRO, at=0.0, units=HOOK_UNITS, lines=HOOK_LINES, chips=HOOK_CHIPS, brand_at=round(HOOK_UNITS[-1]["t1"] + 0.06, 2), part=0))
sfx += [dict(t=0.12, type="impact"), dict(t=3.3, type="riser"), dict(t=4.02, type="impact"), dict(t=6.72, type="impact"), dict(t=round(HOOK_UNITS[-1]["t1"] + 0.06, 2), type="shimmer")]
sfx += [dict(t=u["t0"], type="pop") for u in HOOK_UNITS] + [dict(t=c["at"], type="whoosh") for c in HOOK_CHIPS]
for k, p in enumerate(ORDER):
    if k > 0:
        chapters.append(dict(n=k + 1, title=p["chapter"], tease=TEASE[p["id"]], t0=cur, t1=cur + GAP))
        sfx += [dict(t=cur - 0.45, type="riser"), dict(t=cur + 0.2, type="impact")]
        cur += GAP
    d = dur(p["file"]); start, end = cur, cur + dur(p["file"])
    parts.append(dict(n=k + 1, id=p["id"], short=p["short"], chapter=p["chapter"], start=start, end=end, gapAfter=GAP if k < len(ORDER) - 1 else 0))
    voice.append(dict(file=p["file"], start=start))
    nxt_gap = GAP if k < len(ORDER) - 1 else 0
    for i, b in enumerate(p["bg"]):
        t0 = start + b["t"]; t1 = start + p["bg"][i + 1]["t"] if i + 1 < len(p["bg"]) else end + nxt_gap
        kind, name = b["src"].split(":", 1)
        bgs.append(dict(t0=t0, t1=t1, kind=kind, name=name, inn=b.get("in") or 0))
        if i > 0: sfx.append(dict(t=t0 - 0.06, type="whoosh"))
    for o in p["ov"]:
        a = absolute(o, start); a["part"] = k + 1; ovs.append(a)
        if a["type"] in ("title", "stamp", "stat"): sfx.append(dict(t=a["at"], type="impact"))
        for key in ("items", "chips", "blocks", "cards"):
            for it in a.get(key, []) or []:
                if a["type"] == "qa":
                    sfx += [dict(t=it["q_at"], type="whoosh"), dict(t=it["a_at"], type="impact")]
                else:
                    sfx.append(dict(t=it["at"], type="shimmer" if it.get("total") else "pop"))
                    if it.get("valAt"): sfx.append(dict(t=it["valAt"], type="pop"))
        for c in a.get("cols", []) or []:
            for r in c["rows"]: sfx.append(dict(t=r["at"], type="shimmer" if r.get("total") else "tick"))
    cur = end
end_t0 = cur; total = cur + END
sfx += [dict(t=end_t0, type="whoosh"), dict(t=end_t0 + 0.6, type="shimmer")]
sfx.sort(key=lambda e: e["t"])

clips = {}
for f in sorted((R / "remotion/public/clips").glob("*.mp4")):
    clips[f.stem] = dur(str(f.relative_to(R)))
video = dict(fps=30, total=total, intro=dict(t0=0, t1=INTRO, kicker="IDEASPULSE BUSINESS PLAN", title="MANDIR KE PHOOLON SE AGARBATTI + DHOOP", sub="Poora plan • ₹5,000 test • 8 steps"),
             end=dict(t0=end_t0, t1=total), chapters=chapters, parts=parts, bg=bgs, ov=ovs, clipdur=clips)
(R / "remotion/src/data").mkdir(parents=True, exist_ok=True)
(R / "remotion/src/data/video.json").write_text(json.dumps(video, ensure_ascii=False))
(R / "build_glass").mkdir(exist_ok=True)
(R / "build_glass/audio_plan.json").write_text(json.dumps(dict(duration=total, sfx=sfx, chapters=[INTRO] + [c["t0"] for c in chapters])))
(R / "build_glass/voice_parts.json").write_text(json.dumps(voice))

mm = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"
lines = ["0:00 Intro", f"{mm(INTRO)} 01. {ORDER[0]['chapter']}"] + [f"{mm(c['t0'])} {c['n']:02d}. {c['title']}" for c in chapters] + [f"{mm(end_t0)} Community + End"]
(R / "out").mkdir(exist_ok=True); (R / "out/youtube_chapters.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines)); print("total", round(total, 1), "s =", round(total * 30), "frames; overlays", len(ovs), "bg", len(bgs), "sfx", len(sfx))
