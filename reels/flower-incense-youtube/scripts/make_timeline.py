"""Writes timeline.json: every background shot and on-screen graphic, timed in seconds
from the start of its voiceover part (P1..P8). render.mjs turns these into absolute times.
Edit the text/timings here or directly in timeline.json."""
import json
from pathlib import Path

def T(t0, t1, title, kicker=None, sub=None, sub_at=None, pos="center", size=120, subcls=None):
    return dict(type="title", t0=t0, t1=t1, at=t0, title=title, kicker=kicker, sub=sub, sub_at=sub_at, pos=pos, size=size, subcls=subcls)
def S(t0, t1, text, color="gold", top=430, size=84, rot=-4):
    return dict(type="stamp", t0=t0, t1=t1, at=t0, text=text, color=color, top=top, size=size, rot=rot)
def L(t0, t1, chips, arrows=False):
    return dict(type="lower", t0=t0, t1=t1, at=t0, arrows=arrows, chips=[dict(at=a, text=x, hl=h) for a, x, h in chips])
def PN(t0, t1, title, items, kicker=None, style="list", pos="left", w=None, top=None, badge=None, dots=None, footer=None):
    return dict(type="panel", t0=t0, t1=t1, at=t0, title=title, kicker=kicker, style=style, pos=pos, w=w, top=top, badge=badge, dots=dots, footer=footer,
                items=[dict(zip(("at", "text", "icon", "val", "warn", "total"), it)) if isinstance(it, tuple) else it for it in items])
def I(at, text, icon=None, val=None, warn=None, total=None):
    d = dict(at=at, text=text)
    for k, v in (("icon", icon), ("val", val), ("warn", warn), ("total", total)):
        if v is not None: d[k] = v
    return d
def STEP(n, t0, t1, title, items, pos="left"):
    return PN(t0, t1, title, items, kicker=f"STEP {n} / 8", badge=None, dots=[n, 8], pos=pos, w=960, top=150)
def BG(t, src, frm=None, to=None, inn=None):
    d = dict(t=t, src=src)
    if frm: d["from"] = frm
    if to: d["to"] = to
    if inn: d["in"] = inn
    return d

parts = []

# ---------------- P1 Hook + intro
parts.append(dict(id="P1", file="assets/audio/P1.wav", chapter="PHOOL SE BUSINESS", short="HOOK + INTRO",
 bg=[BG(0, "img:img_temple_sunrise", [.45, .6, 1.25], [.5, .5, 1.0]), BG(4.9, "clip:w01_temple_waste"), BG(9.9, "clip:w01b_flowers_dumped"),
     BG(14.5, "clip:w02_sorting"), BG(16.0, "clip:w03_drying"), BG(17.6, "clip:w04_grinding"), BG(19.1, "img:img_puja_cone", [.45, .55, 1.25], [.45, .5, 1.05]),
     BG(23.9, "img:img_cones_sticks"), BG(32.8, "img:img_workshop", [.5, .5, 1.0], [.4, .6, 1.15]), BG(41.0, "img:img_packs_money"), BG(48.2, "clip:w07_burning")],
 ov=[T(0.2, 4.8, "MANDIR KE PHOOL KAHAN JAATE HAIN?", kicker="KABHI SOCHA HAI? 🤔", size=104),
     S(5.0, 9.8, "KACHRE MEIN! 🗑️", color="red", top=420, size=110),
     L(10.0, 14.4, [(10.1, "SUBAH: KHUSHBOO 🌸", False), (12.0, "SHAAM: BAS EK DHER", True)], arrows=True),
     L(14.5, 19.0, [(14.7, "SAAF KARO", False), (16.1, "SUKHAO ☀️", False), (17.7, "PEESO", True)], arrows=True),
     T(19.2, 23.8, "PHOOLON SE DHOOP + AGARBATTI", kicker="AAJ KA BUSINESS IDEA 💡", sub="🌸 ➜ 🪔", sub_at=21.5),
     L(24.0, 28.3, [(24.2, "🎙️ MANISH • IDEASPULSE.IN", True)]),
     L(28.5, 32.7, [(28.6, "ITNA AASAAN — 8TH CLASS KA BACHCHA BHI SAMJHE ✅", False)]),
     PN(32.9, 40.9, "IS VIDEO MEIN 👇", [I(33.1, "Phool kahan se aayenge?", "🌸"), I(34.6, "Cheezein kaise banengi?", "🛠️"), I(35.7, "Kitna kharcha hoga?", "💰"),
        I(37.1, "Kitni kamai ho sakti hai?", "📈"), I(38.6, "Kin galtiyon se bachna hai?", "⚠️")], pos="right"),
     PN(41.1, 48.0, "SAAF BAAT 🙏", [I(42.0, "Raaton-raat ameer bano scheme", "❌", warn=True), I(44.6, "Chhota, samajhdaari wala shuruaati plan", "✅")], pos="right"),
     L(48.3, 57.8, [(49.4, "1 • CHHOTA TEST", False), (52.9, "2 • GRAHAK KI RAAY", False), (55.0, "3 • PHIR BADA KADAM 🚀", True)], arrows=True)]))

# ---------------- P2 Business + products
parts.append(dict(id="P2", file="assets/audio/P2.wav", chapter="BUSINESS KYA HAI + PRODUCTS", short="BUSINESS + PRODUCTS",
 bg=[BG(0, "img:img_temple_sunrise", [.55, .75, 1.3], [.5, .7, 1.12]), BG(5.1, "clip:r_collect_vertical"), BG(9.8, "clip:w02_sorting", inn=3),
     BG(12.2, "clip:w03_drying", inn=2), BG(13.6, "clip:w05_sieving"), BG(14.7, "clip:w06_mould"), BG(18.0, "clip:w01b_flowers_dumped"),
     BG(26.1, "clip:w09_flower_market"), BG(31.0, "clip:w03_drying", inn=5), BG(36.7, "img:img_cones_sticks"),
     BG(42.3, "img:img_puja_cone", [.45, .5, 1.3], [.45, .45, 1.1]), BG(49.0, "img:img_cones_sticks", [.8, .65, 1.5], [.75, .65, 1.3]),
     BG(57.0, "clip:r_smoke_vertical"), BG(61.4, "clip:w11_gift_box"), BG(66.8, "img:img_cones_sticks", [.4, .55, 1.3], [.5, .5, 1.05])],
 ov=[T(0.2, 5.0, "YE BUSINESS HAI KYA? 🤔", size=130),
     PN(5.2, 17.8, "BAHUT SEEDHI BAAT", [I(5.4, "Ijazat lekar saaf phool ikattha karo", "📝"), I(9.9, "Chhaanto", "🧹"), I(11.3, "Sukhao", "☀️"),
        I(12.6, "Peeso", "⚙️"), I(14.8, "Dhoop cone / agarbatti banao", "🔺")], pos="left", kicker="BUSINESS MODEL"),
     S(18.0, 21.4, "BADI GALATFAHMI ⚠️", color="red"),
     PN(21.5, 36.6, "MYTH: 'MANDIR KE PHOOL FREE!'", [I(21.7, "Free milenge — zaroori nahi", "❌", warn=True), I(26.2, "Pehle ijazat leni hogi", "📝"),
        I(28.2, "Laane-le jaane ka kharcha", "🚚"), I(31.0, "Chhantai mein mehnat", "🧤"), I(33.6, "Sookhne ke baad wazan bahut kam", "⚖️")],
        pos="right", kicker="SACH KYA HAI ✅"),
     L(36.8, 41.4, [(36.9, "SAB SHURU SE HISAAB MEIN JODO 🧮", True)]),
     T(41.5, 42.2, "PRODUCTS 🛍️", size=130),
     T(42.3, 48.9, "DHOOP CONE ⭐", kicker="PRODUCT #1", sub="Roz ki pooja • Pehle yahi banao", pos="top", size=130),
     T(49.0, 56.9, "AGARBATTI", kicker="PRODUCT #2", sub="Baans ki dandi + mixture chipkana = extra kaam", pos="top", size=130, subcls="p-gold"),
     T(57.0, 61.3, "DHOOP CUP", kicker="PRODUCT #3", sub="Ghar ya mandir ke liye", pos="top", size=130),
     T(61.4, 66.6, "FESTIVAL GIFT PACK 🎁", kicker="PRODUCT #4", sub="Tyohar mein return gift", pos="top", size=130),
     S(66.8, 71.2, "PEHLE EK CHEEZ ACHHE SE ✅", color="teal", size=76)]))

# ---------------- P3 8 steps
parts.append(dict(id="P3", file="assets/audio/P3.wav", chapter="BANANE KE 8 STEPS", short="8 STEPS PROCESS",
 bg=[BG(0, "img:img_workshop", [.5, .5, 1.05], [.5, .55, 1.2]), BG(5.6, "clip:r_collect_vertical"), BG(12.3, "clip:w09_flower_market", inn=4),
     BG(16.8, "clip:w02_sorting"), BG(25.9, "clip:w03_drying"), BG(36.5, "clip:w04_grinding"), BG(41.8, "clip:w05_sieving"),
     BG(46.4, "clip:w12_mixing_mask"), BG(61.7, "clip:w06_mould"), BG(70.5, "clip:w07_burning"), BG(79.6, "clip:w08_packing")],
 ov=[T(0.2, 5.4, "8 STEPS MEIN BANAO 👇", kicker="AB AATA HAI ASLI MAZA 😎", size=130),
     STEP(1, 5.7, 16.7, "IJAZAT + PHOOL IKATTHA", [I(7.5, "Likhkar ya saaf shabdon mein ijazat lo", "📝"), I(12.5, "Kab • kis dibbe mein • kaun le jayega — tay karo", "📦")]),
     STEP(2, 16.9, 25.8, "CHHANTAI", [I(17.6, "Plastic • dhaaga • foil • mitti alag", "❌"), I(19.6, "Khaane ka kachra • sade phool alag", "❌"),
        I(21.6, "Ek gandi cheez = poora batch kharab!", "⚠️", warn=True)]),
     STEP(3, 26.0, 36.4, "SAFAI + SUKHANA ☀️", [I(31.6, "Dhoop ya dryer mein poori tarah sukhao", "☀️"), I(34.6, "Zara bhi nami = fafoond + badbu", "⚠️", warn=True)]),
     STEP(4, 36.6, 46.3, "PEESNA + CHHAANNA", [I(41.9, "Sookhe phool peeso, phir chhaano", "⚙️"), I(43.8, "Saaf, sookhe dibbe mein • label lagao", "🏷️")]),
     STEP(5, 46.5, 61.6, "MIXTURE KA CHHOTA TRIAL 🧪", [I(47.6, "Powder + chipkane wala padarth", "🧪"), I(51.0, "Koi ek FIXED formula nahi", "⚠️", warn=True),
        I(57.2, "Har phool alag — jaankaar se salah zaroor lo", "🧑‍🔬")]),
     STEP(6, 61.8, 70.4, "AAKAAR + SUKHANA", [I(62.6, "Mould se cone banao", "🔺"), I(66.3, "Ek jaisa aakaar • daraar nahi • poora sookha", "✅")]),
     STEP(7, 70.6, 79.5, "JALAKAR JAANCH 🔥", [I(71.0, "Kitni der jalta hai?", "⏱️"), I(72.6, "Dhuaan kitna?", "💨"), I(74.0, "Raakh kaisi?", "⚪"),
        I(75.3, "Khushboo kaisi?", "🌸"), I(77.0, "Ye jaanch bahut zaroori!", "✅")]),
     STEP(8, 79.7, 87.4, "PACKING 📦", [I(80.6, "Nami se bachane wala pack", "🛡️"), I(82.6, "Wazan • batch no. • taareekh", "🏷️"), I(84.8, "Banane wale ka naam", "✍️")])]))

# ---------------- P4 Budget
parts.append(dict(id="P4", file="assets/audio/P4.wav", chapter="₹5,000 STARTING BUDGET", short="₹5,000 BUDGET",
 bg=[BG(0, "img:img_packs_money", [.5, .6, 1.2], [.5, .5, 1.0]), BG(9.9, "img:img_workshop", [.3, .5, 1.3], [.7, .5, 1.3]),
     BG(47.9, "img:img_packs_money", [.75, .7, 1.4], [.7, .7, 1.2]), BG(52.2, "img:img_workshop"), BG(63.2, "clip:w07_burning")],
 ov=[T(0.2, 4.3, "KITNE PAISE CHAHIYE? 💰", kicker="SABSE ZAROORI SAWAAL", size=130),
     dict(type="stat", t0=4.5, t1=14.3, at=4.6, kicker="SIRF", value=5000, sub="⚠️ Factory nahi — ghar se chhota TEST", sub_at=7.8),
     PN(14.5, 52.0, "₹5,000 BUDGET BREAKDOWN", [I(18.6, "Dibbe + dastane + mask", val=500), I(21.6, "Sukhane ki tray + stand", val=900),
        I(23.8, "Taraazu + chhalni", val=600), I(27.8, "Peesne-milane ke auzaar", val=700), I(30.2, "Cone ke saanche", val=500),
        I(32.6, "Trial saamaan (binder + test khushboo)", val=700), I(40.6, "Pouch + label", val=500), I(43.6, "Aana-jaana + achanak kharch", val=600),
        I(48.0, "TOTAL", val=5000, total=True)], style="bars", pos="center", w=1300, top=110, kicker="KHARCHA KAHAN HOGA?"),
     PN(52.3, 63.0, "IS BUDGET MEIN SHAMIL NAHI", [I(53.0, "Dukaan ka kiraya"), I(53.9, "Mazdoori"), I(54.8, "Badi machine"), I(55.8, "Lab test"),
        I(57.2, "Registration"), I(58.6, "Bada stock")], style="cross", pos="right", kicker="DHYAN DO ⚠️"),
     PN(63.3, 68.6, "₹5,000 SIRF YE JAANNE KE LIYE", [I(63.6, "Product sach mein banta hai?"), I(66.0, "Log use pasand karte hain?")], style="check", pos="right")]))

# ---------------- P5 Per-pack + batch
parts.append(dict(id="P5", file="assets/audio/P5.wav", chapter="EK PACK KA HISAAB", short="PACK KA HISAAB",
 bg=[BG(0, "img:img_packs_money", [.55, .55, 1.0], [.5, .5, 1.15]), BG(6.4, "clip:w08_packing"), BG(26.3, "img:img_packs_money", [.4, .65, 1.5], [.45, .65, 1.3]),
     BG(46.8, "clip:w08_packing", inn=5), BG(65.4, "img:img_packs_money")],
 ov=[T(0.2, 6.2, "EK PACK KA HISAAB 🧮", kicker="AB AATE HAIN HISAAB PAR", sub="20g TEST PACK", sub_at=3.5, size=130),
     PN(6.5, 26.1, "KHARCHA: 20g PACK", [I(7.2, "Phool powder + chhantai nuksaan", val="₹4"), I(11.6, "Chipkane wala padarth", val="₹4"),
        I(17.0, "Khushboo + baaki saamaan", val="₹2"), I(19.2, "Mazdoori + sukhana + bijli", val="₹3"), I(21.8, "Pouch + label", val="₹2"),
        I(24.4, "SEEDHA KHARCHA", val="₹16", total=True)], style="money", pos="left", kicker="EK PACK"),
     PN(26.4, 34.2, "AGAR ₹39 MEIN BECHEIN", [I(26.6, "Daam", "💰", val="₹39"), I(28.4, "Kharcha", "➖", val="−₹16"),
        I(31.0, "BACHAT / PACK 🎉", "🟰", val="₹23", total=True)], style="money", pos="right"),
     S(34.3, 35.7, "RUKO! ✋", color="red", size=120),
     PN(35.8, 46.6, "ABHI GHATANA BAAKI", [I(36.5, "Kiraya"), I(37.2, "Prachaar"), I(38.0, "Delivery"), I(38.9, "Wapas aaya maal"),
        I(41.0, "Aapki apni tankhwah"), I(42.6, "Tax"), I(43.6, "Machine ki ghisaai")], style="cross", pos="right", kicker="₹23 POORI BACHAT NAHI"),
     PN(46.9, 65.2, "PEHLA BATCH: 100 PACK", [I(48.6, "Bikri: 100 × ₹39", "📦", val="₹3,900"), I(52.6, "Kharcha: 100 × ₹16", "➖", val="−₹1,600"),
        I(58.4, "Bechna + local delivery test", "🚚", val="−₹500"), I(62.0, "ANUMANIT BACHAT", "🟰", val="≈ ₹1,800", total=True)],
        style="money", pos="center", w=1150, top=170, footer="*Sirf chhota anumaan"),
     S(65.5, 70.6, "GUARANTEED PROFIT NAHI ⚠️", color="red", size=80),
     L(70.8, 76.9, [(71.0, "NA BIKA YA WAPAS AAYA MAAL = ALAG NUKSAAN", False)])]))

# ---------------- P6 Sources, selling, 30/90 days
parts.append(dict(id="P6", file="assets/audio/P6.wav", chapter="PHOOL KAHAN SE • BECHNA KAHAN", short="SOURCE + SELLING + 90 DIN",
 bg=[BG(0, "clip:w09_flower_market"), BG(4.2, "img:img_temple_sunrise"), BG(9.1, "clip:w09_flower_market", inn=5), BG(13.2, "clip:r_collect_vertical"),
     BG(17.3, "img:img_cones_sticks", [.8, .65, 1.4], [.7, .6, 1.2]), BG(23.2, "clip:r_shop_vertical"), BG(32.4, "clip:w07_burning"),
     BG(36.9, "clip:w11_gift_box"), BG(41.6, "img:img_packs_money"), BG(48.1, "img:img_workshop"), BG(69.6, "clip:w08_packing"),
     BG(74.2, "clip:r_shop_vertical"), BG(81.0, "img:img_puja_cone", [.45, .5, 1.0], [.45, .45, 1.15])],
 ov=[PN(0.2, 23.0, "PHOOL KAHAN SE? 🌸", [I(4.3, "Mandir / dharmik sthal — ijazat, samay, dibbe tay", "🛕"), I(9.2, "Phool mandi / florist — roz ke bache phool", "💐"),
        I(13.3, "Event decorator — karyakram ke baad", "🎉"), I(17.4, "Baaki kachcha maal: baans dandi + manzoor khushboo (sahi bill)", "🎋")],
        pos="left", w=900, kicker="4 RAASTE"),
     PN(23.3, 47.9, "KAHAN BECHEIN? 🛒", [I(26.6, "Pooja dukaan — sample pack + unki raay", "🏪"), I(32.5, "WhatsApp + Instagram — demo + apni kahani", "📱"),
        I(37.0, "Tyohar gift box + corporate gifting", "🎁"), I(39.6, "Online marketplace", "🌐"),
        I(42.0, "Pehle packing, fees, toot-phoot ka hisaab", "⚠️", warn=True)], pos="right", w=900, kicker="4 CHANNELS"),
     dict(type="timeline", t0=48.2, t1=80.8, at=48.2, title="PEHLE 30 DIN ⏳", blocks=[
        dict(at=50.6, day="DIN 1–5", text="Ijazat + 2-3 phool srot tay"), dict(at=53.6, day="6–10", text="Chhantai, sukhana, peesna"),
        dict(at=58.6, day="11–15", text="Chhote cone ke trial"), dict(at=63.4, day="16–20", text="Jalakar + nami jaanch"),
        dict(at=69.7, day="21–25", text="Packing, label, daam test"), dict(at=74.3, day="26–30", text="Raay + pehla asli order 🎉")]),
     PN(81.1, 101.4, "90 DIN — 3 SAWAAL", [I(84.6, "Mahina 1: Har baar theek sookhta + jalta hai?", "1️⃣"), I(89.0, "Mahina 2: Grahak dobara khareedta hai?", "2️⃣"),
        I(93.4, "Mahina 3: Munafa + quality dono tik rahe?", "3️⃣"), I(97.8, "Jawab HAAN? Tab aage badho 🚀", "✅", total=True)], pos="right", w=920)]))

# ---------------- P7 1-year estimate + machines
parts.append(dict(id="P7", file="assets/audio/P7.wav", chapter="1 SAAL KI KAMAI + MACHINE", short="1 SAAL + MACHINE",
 bg=[BG(0, "img:img_packs_money", [.6, .6, 1.25], [.5, .55, 1.05]), BG(6.8, "clip:w08_packing"), BG(26.0, "clip:w11_gift_box"),
     BG(49.0, "img:img_workshop"), BG(53.6, "img:img_workshop", [.55, .45, 1.3], [.45, .5, 1.15]), BG(70.4, "clip:w06_mould")],
 ov=[T(0.2, 6.6, "1 SAAL MEIN KITNI KAMAI? 📈", sub="Sirf anumaan — GUARANTEE NAHI", sub_at=4.0, subcls="p-red", size=120),
     dict(type="compare", t0=6.9, t1=48.8, at=6.9, footer="*Anumaan — asli nateeja demand, daam, barbaadi aur bechne ke tareeke par", cols=[
        dict(kicker="RAASTA 1", title="DHEERE BADHNA 🐢", rows=[I(8.6, "Packs / saal", val="4,500"), I(11.0, "Bikri", val="₹1,75,500"),
            I(14.6, "Seedha kharcha", val="−₹72,000"), I(17.6, "Bachat", val="₹1,03,500"), I(20.6, "Fixed kharcha", val="−₹48,000"),
            I(23.4, "ANUMANIT", val="≈ ₹55,500", total=True)]),
        dict(kicker="RAASTA 2", title="TEZI SE BADHNA 🚀", rows=[I(28.6, "Packs / saal", val="11,150"), I(32.0, "Bikri", val="₹4,34,850"),
            I(36.0, "Seedha kharcha", val="−₹1,78,400"), I(39.6, "Bachat", val="₹2,56,450"), I(43.0, "Fixed kharcha", val="−₹1,20,000"),
            I(46.0, "ANUMANIT", val="≈ ₹1,36,450", total=True)])]),
     L(49.1, 53.4, [(49.2, "DEMAND", False), (50.2, "DAAM", False), (51.0, "BARBAADI", False), (51.9, "BECHNE KA TAREEKA", True)]),
     T(53.7, 59.0, "MACHINE KAB LEIN? 🤔", size=130),
     S(59.2, 61.0, "JALDI BILKUL NAHI! ✋", color="red", size=100),
     dict(type="cards", t0=61.1, t1=70.2, at=61.1, title="ONLINE LISTING EXAMPLES", footer="*Sirf listing ke udaharan — daam badalte rehte hain", cards=[
        dict(at=61.4, icon="🪔", label="Agarbatti machine", val="~₹65,000"), dict(at=64.0, icon="☀️", label="Dryer", val="~₹10,000"),
        dict(at=65.6, icon="⚙️", label="Mixer", val="~₹22,000"), dict(at=67.4, icon="🔺", label="Dry dhoop cone machine", val="~₹35,000")]),
     PN(70.5, 77.7, "MACHINE TAB LO JAB…", [I(71.6, "Baar-baar order aa rahe hon"), I(75.8, "Haath se banana sach mein rukawat ban jaye")], style="check", pos="right")]))

# ---------------- P8 Safety + law + CTA
parts.append(dict(id="P8", file="assets/audio/P8.wav", chapter="SURAKSHA + KAANOON", short="SURAKSHA + KAANOON",
 bg=[BG(0, "img:img_workshop", [.85, .7, 1.6], [.8, .7, 1.35]), BG(5.2, "clip:w02_sorting"), BG(14.5, "clip:w07_burning"), BG(27.4, "img:img_cones_sticks"),
     BG(37.4, "img:img_packs_money"), BG(44.0, "clip:w12_mixing_mask"), BG(51.2, "img:img_temple_sunrise"), BG(56.4, "clip:r_smoke_vertical"),
     BG(62.8, "img:img_temple_sunrise", [.5, .5, 1.15], [.5, .5, 1.0]), BG(68.5, "img:img_puja_cone"), BG(73.1, "clip:w11_gift_box"),
     BG(78.3, "img:img_puja_cone", [.45, .5, 1.25], [.45, .5, 1.05])],
 ov=[T(0.2, 5.0, "SURAKSHA + KAANOON ⚖️", sub="Yahan laaparwaahi mat karna", sub_at=2.6, subcls="p-red", size=130),
     PN(5.2, 56.2, "7 ZAROORI NIYAM", [I(5.4, "Nami, fafoond, baahri cheez ya badbu? Use mat karo"), I(10.4, "Har batch: jalne ka samay, dhuaan, raakh, khushboo likho"),
        I(14.6, "Bina jaanch 'chemical-free / non-toxic / dhuaan-rahit' ya sehat ke daave NAHI"),
        I(26.0, "Agarbatti BIS standard IS 19412:2025 samjho • roke gaye padarth se bacho"),
        I(37.5, "Registration, GST, packing ghoshnaayein, local anumati check"), I(44.0, "Mask, dastane, hawa • powder ki dhool saans mein nahi"),
        I(51.3, "Mandir ka naam/logo bina likhit ijazat NAHI")], style="num", pos="center", w=1640, top=110),
     PN(56.4, 62.6, "GRAHAK KO LIKHKAR BATAO", [I(56.6, "Jalti cheez akeli na chhodein", "🔥"), I(59.4, "Bachchon + pets se door rakhein", "👶")], pos="right"),
     L(62.9, 69.0, [(63.0, "CHHOTA SHURU", False), (64.5, "HISAAB SAAF", False), (66.0, "QUALITY PAR SAMJHAUTA NAHI", True)]),
     T(69.1, 75.8, "KAL KA KACHRA ➜ AAJ BUSINESS KI KHUSHBOO 🌸", kicker="YAAD RAKHIYE", size=96),
     T(75.9, 83.8, "COMMENT 'FLOWER' 👇", kicker="POORA PLAN + GUIDE + TEMPLATE? 📘", sub="🌐 ideaspulse.in", sub_at=79.4, size=150)]))

tl = dict(
    _help="All on-screen text and timings. Times are seconds from the start of each voiceover part. Regenerate with scripts/make_timeline.py or edit here, then: node render.mjs",
    fps=30, intro=3.5, gap=1.6, end_screen=20.0,
    intro_card=dict(kicker="IDEASPULSE BUSINESS PLAN", title="MANDIR KE PHOOLON SE AGARBATTI + DHOOP", sub="Poora plan • ₹5,000 se test • 8 steps"),
    end_card=dict(title="SUBSCRIBE KARO 🔔", sub="Har hafte naye business ideas + plans"),
    parts=parts,
    sfx_rules=dict(bg_cut="whoosh", title="impact", stamp="impact", item="pop", chapter="riser"))
Path(__file__).resolve().parent.parent.joinpath("timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
print("parts", len(parts), "overlays", sum(len(p["ov"]) for p in parts), "bg", sum(len(p["bg"]) for p in parts))
