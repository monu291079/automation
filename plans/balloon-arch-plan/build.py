import html, re, base64, pathlib
from art import *
from model import *

HERE = pathlib.Path(__file__).parent
B64 = lambda p: "data:image/png;base64," + base64.b64encode((HERE / "assets" / p).read_bytes()).read() if False else "data:image/png;base64," + base64.b64encode((HERE / "assets" / p).read_bytes()).decode()
LOGO, QRY, QRT = B64("logo.png"), B64("qr_youtube.png"), B64("qr_telegram.png")

PAGES = []  # (id, toc_title or None, html)


def page(pid, eyebrow, title, body, toc=None, cont=False, dark=False):
    n = len(PAGES) + 1
    t = f'<h1>{title}{" <small>(aage)</small>" if cont else ""}</h1><div class="rule"></div>'
    PAGES.append((pid, toc, f'''<section class="page{' dark' if dark else ''}" id="{pid}">
<div class="eyebrow">{eyebrow}</div>{t}<div class="body">{body}</div>
<footer><a href="#toc" class="flogo"><img src="{LOGO}"/></a><span>IdeasPulse · ideaspulse.in · Saare numbers udaharan hain, guarantee nahi</span><a class="pn" href="#toc">{n:02d}</a></footer></section>'''))


def callout(title, items, kind="gold"):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<div class="callout {kind}"><b class="ct">{title}</b><ul>{li}</ul></div>'


def para(t):
    return f'<p class="lead">{t}</p>'


def checks(items, bad=False):
    ic = "✕" if bad else "✓"
    return '<ul class="checks">' + "".join(f'<li><i class="{"bad" if bad else "ok"}">{ic}</i><span>{i}</span></li>' for i in items) + "</ul>"


def stat(label, big, sub, accent="#E2BE6A"):
    return f'<div class="stat" style="--ac:{accent}"><div class="sl">{label}</div><div class="sb">{big}</div><div class="ss">{sub}</div></div>'


def table(head, rows, widths=None, hl_last=False):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = ""
    for r in rows:
        tr += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return f'<table class="tb"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def card(inner, cls=""):
    return f'<div class="card {cls}">{inner}</div>'


def flow(steps):
    out = ""
    for i, (ic, t, s) in enumerate(steps):
        out += f'<div class="fl"><div class="fi">{ic}</div><b>{t}</b><span>{s}</span></div>'
        if i < len(steps) - 1:
            out += '<div class="fa">→</div>'
    return f'<div class="flow">{out}</div>'


def timeline(items):
    out = ""
    for h, t, s in items:
        out += f'<div class="tl"><div class="dot"></div><div class="tc"><div class="th">{h}</div><b>{t}</b><span>{s}</span></div></div>'
    return f'<div class="tline">{out}</div>'


def src(t):
    return f'<p class="src">{t}</p>'


# =============================================================== PAGES
# 1 cover
cover_html = f'''<section class="page cover" id="cover">
<div class="cv-top"><span class="pill"><img src="{LOGO}"/>IdeasPulse</span></div>
<div class="cv-hero">{arch_hero(500, 400)}</div>
<div class="cv-text"><div class="eyebrow gold">IDEASPULSE BUSINESS PLAN · HINGLISH</div>
<h1 class="cv-h"><span class="g">Balloon Arch</span> Business Plan</h1>
<p>Ek machine, kuch balloons aur aapki mehnat: <b>birthday, wedding aur baby shower</b> ki decoration se kamai. Poora hisaab, 1 mahine se 12 mahine tak, <b>aasaan Hinglish</b> mein.</p>
<div class="chips"><span class="chip gold">~₹9,000 se lean start</span><span class="chip">Ghar se shuru</span><span class="chip">1-2 log</span><span class="chip">12 mahine ka roadmap</span></div>
<div class="cv-foot">Comment BALLOON karne walon ke liye · ideaspulse.in · Har number ka source page 33 par</div></div></section>'''

# 3 how to use
page("how", "SHURUAAT", "Is plan ko <span class='g'>kaise padhein</span>?", para("Ye plan aise likha hai ki <b>8vi class ka baccha bhi samajh sake</b>. Har page par chhote point, tasveerein aur seedhe numbers hain. Kuch bhi mushkil lage to us page ki tasveer dekho."
) + callout("📌 SABSE ZAROORI 4 BAATEIN", [
    "Pehle <b>1-2 test arch</b> banao, phir paisa lagao.",
    "Pehle <b>customer dhoondo, phir saaman badhao</b>. Order ke bina stock mat bharo.",
    "Machine ki <b>exact price aur demo</b> seller se khud confirm karo (page 15).",
    "Saare numbers <b>udaharan</b> hain, guarantee nahi. Apne sheher ke rate se jodo (source page 33)."]) +
    f'<div class="imgrow">{card(machine(300,250),"flat")}{card(coins(220,170),"flat")}</div><p class="cap">Machine + paisa: iss plan mein dono ka hisaab hai (3D udaharan tasveer).</p>', toc="Is plan ko kaise padhein")

# 4 ek nazar mein
page("glance", "EK NAZAR MEIN", "Poora business <span class='g'>1 page mein</span>", para("Balloon arch business mein aap <b>event par balloons ki sundar arch</b> banakar lagate ho. Customer <b>decoration</b> ka paisa deta hai, sirf machine ka nahi.") +
     '<div class="grid2">' + stat("LEAN SETUP", "₹9,068", "pump, frame, balloons, tools") + stat("SERVICE-READY SETUP", "₹23,164", "2 frame, stock, props, marketing", "#2BB3AA") +
     stat("EK ARCH KA RATE", "₹1,800-10,000+", "design aur jagah ke hisaab se", "#12213A") + stat("EK EVENT KA MUNAFA", "~₹1,200", "₹3,500 ke arch par (page 17)") +
     stat("PAISA WAPAS", "~7 mahine", "base plan: 8 events/mahina tak pahunchne par", "#2BB3AA") + stat("12 MAHINE KA MUNAFA", "~₹79,500", "base plan, aapki mehnat ka paisa nikalne se pehle", "#12213A") + '</div>' +
     src("Setup: page 12-15 · Event ka hisaab: page 17 · Roadmap: page 22-26. Machine (reel wali) ka daam setup mein jodna alag se hai."), toc="Ek nazar mein: poora business")

# 5 kya hai
page("what", "SAMJHO", "Balloon arch business <span class='g'>kya hai</span>?", para("Birthday, shaadi, baby shower, shop opening: har jagah log <b>sundar photo-spot</b> chahte hain. Aap wahan jaakar balloons ki arch lagate ho. Isi kaam ke paise milte hain.") +
     flow([(tile3d("📞"), "Booking", "customer ne bola"), (tile3d("🎈", "#2BB3AA"), "Balloon phulao", "pump / machine se"), (tile3d("🏗️", "#4C8DFF"), "Arch banao", "frame par lagao"), (tile3d("💰", "#E2BE6A"), "Paisa lo", "advance + baaki")]) +
     card("<b class='h3'>Aasaan bhasha mein</b><p>Aap <b>ek dukaan nahi</b>, ek <b>service</b> chalate ho. Saaman (balloons, frame) <b>aap laate ho</b>, event par lagate ho, aur kaam ke paise lete ho. Dukaan ya bada godown ki zaroorat nahi, ghar ka ek kona kaafi hai.</p>") +
     card("<b class='h3'>Kyun pasand hai ye business?</b>" + checks(["<b>Chhota setup</b>: ₹9,000 se shuru ho sakta hai", "<b>Ghar se</b> kaam, kiraya nahi", "Har <b>birthday/shaadi</b> par demand", "<b>Skill</b> seekh kar hi aati hai: practice se"])), toc="Balloon arch business kya hai")

# 6 machine
page("machine", "SAMJHO", "Reel wali machine <span class='g'>kya karti hai</span>?", f'<div class="hero3d">{machine(360,290)}</div>' +
     para("Machine ek baar mein <b>kai balloons ek saath phulati hai</b>. Isse <b>time bachta hai</b>, kyunki muh ya hath-pump se phulane mein bahut time jaata hai.") +
     '<div class="grid2">' + card("<b class='h3 ok2'>✓ Machine karti hai</b>" + checks(["Balloons <b>jaldi phulati</b> hai", "Thakaan kam, <b>kaam tez</b>"])) + card("<b class='h3 bad2'>✕ Machine nahi karti</b>" + checks(["Arch <b>khud nahi banati</b>", "Design, rang, <b>fitting aap karoge</b>"], True)) + '</div>' +
     callout("⚠️ DHYAAN DO", ["Aam <b>₹666-900 ki dual-nozzle pump</b> aur reel wali <b>multi-balloon machine</b> alag cheezein ho sakti hain.", "Khareedne se pehle <b>demo video, warranty, voltage, balloon size, daam</b> seller se pucho."], "red"), toc="Machine kya karti hai (aur kya nahi)")

# 7 customers
page("cust", "BAZAAR", "Customer <span class='g'>kaun</span> hain?", para("Ye log arch ke paise dete hain. Inse <b>pehle 3 kisam</b> pakdo, phir badhao.") +
     '<div class="grid2">' + "".join(card(f'<div class="ct3">{tile3d(ic,col,54)}</div><b class="h3">{t}</b><span class="sm">{d}</span>') for ic, col, t, d in [
         ("🎂", "#FF8FB8", "Birthday", "Ghar ya hall ki arch, name balloon"), ("🍼", "#4C8DFF", "Baby shower / naming", "Pastel arch, welcome board"), ("💍", "#E2BE6A", "Shaadi, haldi, mehendi", "Entry arch, photo corner"),
         ("🏪", "#2BB3AA", "Dukaan opening", "Brand-color arch, pillar"), ("🎓", "#9B6BFF", "School / office", "Stage aur gate decoration"), ("🛍️", "#FF6B5A", "DIY customer", "Taiyar balloon garland kit")]) + '</div>' +
     callout("🧭 KAHAN MILENGE?", ["WhatsApp status, Instagram reel, local <b>Facebook groups</b>", "<b>Cake shop, photographer, banquet hall, event planner</b> se tie-up", "Khush customer se <b>review aur referral</b>"], "teal"), toc="Customer kaun hain?")

# 8 packages
page("pack", "BAZAAR", "Kya <span class='g'>bechoge</span>? 5 package", para("Customer ko <b>photo + balloon ginti + kya-kya shamil hai</b> likh kar quote do. Neeche <b>test rate</b> hain, apne shehar ke hisaab se badlo.") +
     table(["Package", "Isme kya", "Test rate"], [["🎈 <b>Starter arch</b>", "1 simple arch, 2-3 rang, local jagah", "<b>₹1,800-2,800</b>"], ["🎂 <b>Birthday corner</b>", "Arch + chhota backdrop + floor bunch", "<b>₹2,800-4,500</b>"], ["📸 <b>Theme photo corner</b>", "Arch + ring/frame + name foil + styling", "<b>₹4,500-7,500</b>"],
                                            ["💍 <b>Wedding entry arch</b>", "Badi arch, ghani balloons, setup", "<b>₹5,000-10,000+</b>"], ["🏪 <b>Shop opening</b>", "Entry arch ya 2 pillar, brand rang", "<b>₹3,500-7,000</b>"]]) +
     callout("📌 BHAV KAISE TAY KARO", ["<b>Balloon + saaman ka kharcha</b> + aana-jaana + helper", "+ <b>aapka time</b> + muanfa", "Sirf bachhe-jaisi sasti arch ka bhav, badi arch ko mat do."]) +
     src("Rates: BalloonDekor, Funtook, mytribe listings par dikhe ₹1,499 se ₹11,499 ke range se liye. Mathura ke exact quote nahi hain, test rate hain."), toc="Packages aur bechne ke rate")

# 9 process 1
page("proc1", "PROCESS", "Poora business <span class='g'>step by step</span>", para("Booking se paise tak: har event par <b>yehi 10 step</b> chalte hain.") +
     timeline([("Step 1-2", "Call aaya → sawaal pucho", "Kab, kahan, kitne log, kaun sa event, budget"), ("Step 3", "Photo + quote bhejo", "Design ki photo, balloon ginti, kya shamil hai, rate"),
               ("Step 4", "Advance lo (30-50%)", "UPI par. Date lock. Cancel policy likho."), ("Step 5", "Saaman ginti karo", "Balloon + 10% extra, frame, tape, tools, extension")]) +
     callout("✍️ BOOKING FORM MEIN YE LIKHO", ["Date, time, <b>pata</b>, event ka naam", "Rang, <b>package</b>, balloon ginti, frame/backdrop", "Setup aur teardown time, <b>budget aur advance</b>"], "teal"), toc="Poora business process (1/2)")
page("proc2", "PROCESS", "Poora business <span class='g'>step by step</span>", timeline([("Step 6", "Ek din pehle: taiyari", "Saaman gaadi mein rakho, balloons ka test, frame check, phone charge"), ("Step 7", "Event din: pahunch kar jagah dekho", "Hawa, power point, floor, permission. Phir frame lagao"),
                                                                             ("Step 8", "Balloons phulao aur arch banao", "Machine/pump se phulao, strip par lagao, rang ke hisaab se"), ("Step 9", "Photo + video lo, customer ko dikhao", "Aapka portfolio isi se banega. Photo permission lo"),
                                                                             ("Step 10", "Baaki paisa lo, review maango", "Kharcha likho (job sheet page 34), Google/WhatsApp review lo")]) +
     callout("⏱️ EVENT-DIN KA TIME (udaharan)", ["Pahunchna <b>2 ghante pehle</b>", "Arch banane mein <b>45-90 min</b> (practice se kam hoga)", "Customer ke aane se <b>30 min pehle taiyar</b>"]), cont=True, toc=None)
PAGES[-1] = (PAGES[-1][0], None, PAGES[-1][2])

# 11 set cost levels
page("setup", "PAISA · SET COST", "Shuruaat ka kharcha: <span class='g'>3 level</span>", para("Ye <b>ek baar ka kharcha</b> hai (machine ke bina). Aap apne budget ke hisaab se level chuno.") +
     '<div class="grid3">' + card(f'<div class="lv">LEVEL 1</div><b class="h3">Lean start</b><div class="big">₹{LEAN:,}</div><span class="sm">1 pump, 1 frame, 1,000 balloons, tools. Pehle test ke liye.</span>', "lvl") +
     card(f'<div class="lv">LEVEL 2 ⭐</div><b class="h3">Service-ready</b><div class="big">₹{SETUP:,}</div><span class="sm">2 frame, stock, props, marketing. Serious start.</span>', "lvl hot") +
     card('<div class="lv">LEVEL 3</div><b class="h3">Expanded</b><div class="big">₹50k-1L+</div><span class="sm">Kai frame, premium props, lights, team. Demand dikhne ke baad.</span>', "lvl") + '</div>' +
     f'<div class="hero3d" style="margin-top:6px">{coins(250,150)}</div>' +
     callout("📌 SAMJHO", ["Sabse bada kharcha: <b>frames</b> (₹1,669 se ₹4,399) aur <b>balloon stock</b>", "<b>Machine alag se</b> add hogi (page 15)", "Level 1 se test karo, bookings aayen to Level 2"]), toc="Shuruaat ka kharcha: 3 level")

# 12 itemised donut
parts = [("Frames", 6068, "#E2BE6A"), ("Balloon stock", 2800, "#2BB3AA"), ("DIY kits", 1996, "#12213A"), ("Pump x2", 1600, "#4C8DFF"), ("Props + backdrop", 2500, "#FF8FB8"), ("Baaki (tools, bag, foil, brand, marketing, buffer)", 8200, "#9B6BFF")]
page("donut", "PAISA · SET COST", f"₹{SETUP:,} <span class='g'>kahan lagega</span>?", para("Ye <b>service-ready</b> setup ka hisaab hai. Har cheez ka daam online listing se liya hai (Nov 2026).") +
     card(f'<div class="dn">{donut(parts, 290, "₹23,164", "KUL BUDGET")}</div>' + '<ul class="lg">' + "".join(f'<li><i style="background:{c}"></i><span>{l}</span><b>{inr(v)}</b></li>' for l, v, c in parts) + '</ul>'), toc="₹23,164 kahan lagega (chart)")

# 13 item table
page("items", "PAISA · SET COST", "Har cheez ka <span class='g'>hisaab</span>", table(["Cheez", "Kitna", "Daam", "Kul"], [[i, q, p, f"<b>{inr(t)}</b>"] for i, q, p, t, n in SETUP_ITEMS] + [["<b>KUL (machine ke bina)</b>", "", "", f"<b>{inr(SETUP)}</b>"]]) +
     src("Daam source: Kiwiparty / TradeIndia (pump), HASTHIP / CRAze (frame), Party Supplies India (kit), Party Wholesale Hub (balloon). 'Allowance' wale daam apne andaze hain, local dukaan se quote lo. Poora link page 33 par."), toc="Har cheez ka hisaab (table)")

# 14 lean
page("lean", "PAISA · SET COST", f"Sabse sasta start: <span class='g'>₹{LEAN:,}</span>", para("Abhi tak yakin nahi? <b>Chhote se shuru</b> karo. 2-3 event karke dekho, phir badhao.") +
     card(f'<ul class="lg">' + "".join(f'<li><i style="background:#E2BE6A"></i><span>{l}</span><b>{inr(v)}</b></li>' for l, v in LEAN_ITEMS) + f'<li class="tot"><span>KUL</span><b>{inr(LEAN)}</b></li></ul>') +
     callout("🎯 LEAN START KA MAUKA", ["Pehle <b>5 bar practice</b> (ghar par, ya doston ke liye)", "<b>3 sample photo/video</b> banao", "Phir <b>3-5 paid event</b>: tab Level 2"], "teal"), toc="Sabse sasta start (₹9,068)")

# 15 machine decision
page("mach2", "PAISA · SET COST", "Reel wali <span class='g'>machine ka daam</span>", para("Reel wali multi-balloon machine ka <b>pakka daam hum yahan nahi likh rahe</b>, kyunki alag-alag seller alag daam batate hain. Isliye ye <b>setup mein alag se add</b> hoga.") +
     f'<div class="grid2">{card(machine(200,170),"flat")}<div>' + callout("🧾 SELLER SE PUCHO", ["Exact <b>model aur daam</b>", "<b>Demo video</b> (live)", "Warranty + <b>service</b>", "Kaun-se balloon size chalte hain", "Voltage, shipping, GST bill"], "red") + '</div></div>' +
     card("<b class='h3'>Paise ka formula</b><p><b>Kul start paisa = Setup (₹9,068 ya ₹23,164) + Machine ka daam</b><br>Aur <b>wapas aane ke events = Kul start paisa ÷ ek event ka munafa (₹1,200)</b></p>") +
     callout("💡 SAMJHDARI", ["<b>3 seller</b> se quote lo, sabse sasta nahi, <b>sabse bharosemand</b> chuno", "Pehle Level 1 se bookings test karo, machine baad mein bhi aa sakti hai"]), toc="Reel wali machine ka daam")

# 16 running expenses
page("running", "PAISA · MONTHLY KHARCHA", "Har mahine ka <span class='g'>chalu kharcha</span>", para("Ye <b>running (chalne ka) kharcha</b> hai: event ho ya na ho, ye lagega.") +
     card("<b class='h3'>Fixed: har mahine</b><ul class='lg'>" + "".join(f"<li><i style='background:#E2BE6A'></i><span>{l}</span><b>{inr(v)}</b></li>" for l, v in FIXED) + f"<li class='tot'><span>Kul fixed (shuru ke mahine)</span><b>{inr(FIXED_M1)}</b></li></ul>") +
     card("<b class='h3'>Variable: har event par</b><ul class='lg'>" + "".join(f"<li><i style='background:#2BB3AA'></i><span>{l}</span><b>{inr(v)}</b></li>" for l, v in EVENT) + f"<li class='tot'><span>Kul (₹3,500 ke arch par)</span><b>{inr(EVENT_COST)}</b></li></ul>") +
     callout("📌 YAAD RAKHO", ["<b>Aapki apni mehnat/salary</b> in kharchon mein nahi hai", "Marketing aur helper badhne par <b>fixed ₹3,000-3,500</b> tak ja sakta hai (roadmap mein shamil)"]), toc="Har mahine ka chalu kharcha")

# 17 event math
bars = bars3d([(3500, 2300, 1200), (2500, 1800, 700), (4000, 2500, 1500)], 470, 220, labels=["₹3,500 arch", "₹2,500 arch", "₹4,000 arch"], fmt=lambda v: f"{v/1000:.1f}k")
page("event", "HISAAB", "Ek event ka <span class='g'>hisaab</span>", para("₹3,500 ka ek arch bechne par <b>kitna bachta hai</b>? Pehle kharcha ghata kar dekho.") +
     f'<div class="eq"><div><small>Customer deta hai</small><b>₹3,500</b></div><span>−</span><div><small>Kharcha</small><b>₹2,300</b></div><span>=</span><div class="hl"><small>Munafa (1 event)</small><b>₹1,200</b></div></div>' +
     card(f'<b class="h3">3D chart: alag-alag rate par</b>{bars}') + callout("📌 SAMJHO", ["Munafa <b>34%</b> hai. Aapki mehnat iske <b>upar</b> alag hai.", "Rate <b>₹1,800 par bahut kam</b> bachta hai: kam rate se bacho", "Jitna <b>sundar design</b>, utna bada ticket"], "gold"), toc="Ek event ka hisaab (kamai - kharcha)")

# 18 breakeven
page("be", "HISAAB", "Paisa <span class='g'>kab wapas</span> aayega?", para("<b>Break-even</b> matlab: shuruaati kharcha wapas nikalna. Formula: <b>Setup ÷ ek event ka munafa</b>.") +
     table(["Munafa / event", "Lean (₹9,068)", "Service-ready (₹23,164)"], [["₹700", "13 events", "34 events"], ["₹1,000", "10 events", "24 events"], ["<b>₹1,200 (base)</b>", "<b>8 events</b>", "<b>20 events</b>"], ["₹1,500", "7 events", "16 events"], ["₹2,000", "5 events", "12 events"]]) +
     card(f'<b class="h3">Base roadmap mein</b><p>Fixed kharche bhi jodne par <b>Level 2 ka paisa ~7 mahine</b> mein wapas aata hai (page 24). Low bookings mein <b>12 mahine mein bhi poora nahi</b> hota (page 26): isliye pehle Level 1.</p>') +
     callout("⚠️ SACH", ["Ye sirf <b>shuruaati kharcha wapas</b> hone ka hisaab hai. Bookings aayengi ya nahi, wo aapki marketing par hai."], "red"), toc="Paisa kab wapas aayega")

# 19 roadmap overview
page("road", "ROADMAP", "<span class='g'>1 / 6 / 12 mahine</span> ka raasta", para("Aap kahan pahunchoge, ek nazar mein. Neeche base plan hai.") +
     timeline([("MAHINA 1", "Seekho + portfolio", "2 events · kamai ₹5,000 · kharcha ₹5,600 · <b>profit -₹600</b>"), ("MAHINA 6", "Pakke customers", "7 events · kamai ₹24,500 · kharcha ₹19,100 · <b>profit +₹5,400</b>"), ("MAHINA 7", "Setup ka paisa wapas ✅", "8 events · kamai ₹32,000 · <b>cumulative +₹336</b>"), ("MAHINA 12", "Stable business", "10 events · kamai ₹40,000 · profit ₹11,500 · <b>saal ka profit ~₹79,500</b>")]) +
     callout("📌 ROADMAP KYA BATATA HAI", ["Pehle 3 mahine <b>seekhne ke</b>, profit kam", "Mahina 4 se <b>naam banta hai</b>, repeat customers", "Mahina 7 se <b>setup ka paisa wapas</b> aur munafa shuru"], "teal"), toc="1 / 6 / 12 mahine ka roadmap")

# 20 month 1 week by week
page("m1a", "ROADMAP · 1 MAHINA", "Pehle <span class='g'>30 din</span>", timeline([("HAFTA 1", "Seekho + saaman lo", "3 seller se pump/frame ke quote · practice: 2 arch shape · Udyam registration (free)"), ("HAFTA 2", "Portfolio banao", "3 rang-design, mock setup, din ki roshni mein photo + timelapse video")]) +
     timeline([("HAFTA 3", "Pehle customer dhoondo", "WhatsApp status par rate card · 10 cake shop/photographer/hall se milo · intro offer"), ("HAFTA 4", "Pehle paid event", "Advance lo, time par pahucho, photo/review lo, har kharcha likho")]) +
     card("<b class='h3'>Mahina 1 ka hisaab (base)</b><ul class='lg'><li><span>Events</span><b>2 × ₹2,500</b></li><li><span>Kamai (revenue)</span><b>₹5,000</b></li><li><span>Event kharcha</span><b>₹3,600</b></li><li><span>Fixed kharcha</span><b>₹2,000</b></li><li class='tot'><span>Profit</span><b>-₹600</b></li></ul>"), toc="Pehle 30 din: hafte-hafte ka plan")
page("m1b", "ROADMAP · 1 MAHINA", "Pehle <span class='g'>30 din</span>: roz ka kaam", checks(["<b>Din 1-3:</b> 3 seller ko call, daam/demo/warranty likho", "<b>Din 4-7:</b> saaman order, Udyam registration (free portal)", "<b>Din 8-10:</b> 2 arch practice, balloon ginti aur time likho", "<b>Din 11-14:</b> 3 design ke photo + video, Instagram page banao", "<b>Din 15-18:</b> 10 jagah milo: cake shop, photographer, banquet", "<b>Din 19-21:</b> intro offer: pehle 3 customer ko chhoot", "<b>Din 22-26:</b> pehle 2 booking: advance + confirm", "<b>Din 27-30:</b> event, photo, review, hisaab check"]) +
     callout("🎯 MAHINA 1 KA TARGET", ["<b>3 asli photo</b> + <b>2 paid event</b> + <b>1 review</b>", "Profit ki chinta nahi, <b>seekhna aur saboot</b> banana hai"], "teal"), cont=True, toc=None)

# 22 six month table
r6 = BASEROWS[:6]
page("m6", "ROADMAP · 6 MAHINE", "6 mahine: <span class='g'>kamai vs kharcha vs profit</span>", table(["Mahina", "Events", "Kamai", "Kharcha", "Profit", "Jama (setup ke baad)"], [[f"<b>M{i+1}</b>", r["ev"], inr(r["rev"]), inr(r["exp"]), f"<b>{inr(r['profit'])}</b>", inr(r["cum"])] for i, r in enumerate(r6)] +
                                                                                           [["<b>Kul</b>", f"<b>{tot(BASEROWS,0,6,'ev')}</b>", f"<b>{inr(tot(BASEROWS,0,6,'rev'))}</b>", f"<b>{inr(tot(BASEROWS,0,6,'exp'))}</b>", f"<b>{inr(tot(BASEROWS,0,6,'profit'))}</b>", ""]]) +
     card(f'<b class="h3">3D chart</b>{bars3d([(r["rev"], r["exp"], max(r["profit"],0)) for r in r6], 470, 210, labels=[f"M{i+1}" for i in range(6)])}') +
     src(f"'Jama' = ab tak ka profit − ₹{SETUP:,} setup. Minus ka matlab setup ka paisa abhi wapas nahi aaya."), toc="6 mahine: kamai vs kharcha vs profit")

page("m6b", "ROADMAP · 6 MAHINE", "6 mahine mein <span class='g'>kya karna hai</span>", timeline([("MAHINA 2-3", "Naam banao", "10 asli photo, 5 review, 3 vendor tie-up (cake shop/photographer)"), ("MAHINA 4", "Rate badhao", "₹3,000 → ₹3,500: design behtar, 2-3 palette ready"), ("MAHINA 5-6", "Repeat customer", "Birthday/anniversary reminder, referral discount, helper fixed karo")]) +
     f'<div class="hero3d">{line_chart([r["cum"] for r in r6], 480, 190)}</div><p class="cap">Setup ke baad ka jama paisa (6 mahine): laal line = setup wapas.</p>' +
     callout("📌 6 MAHINE KE BAAD", ["Saal bhar mein <b>₹89,000 kamai</b>, <b>₹15,000 profit</b> (base)", "Setup abhi <b>poora wapas nahi</b>. Mahina 7 tak ruko, sabr rakho"], "gold"), cont=True, toc=None)

# 24 twelve month
page("m12", "ROADMAP · 12 MAHINE", "12 mahine: <span class='g'>kamai vs kharcha vs profit</span>", table(["Mahina", "Events", "Kamai", "Kharcha", "Profit", "Jama"], [[f"<b>M{i+1}</b>", r["ev"], inr(r["rev"]), inr(r["exp"]), f"<b>{inr(r['profit'])}</b>", inr(r["cum"])] for i, r in enumerate(BASEROWS)] +
                                                                                              [["<b>Kul</b>", f"<b>{tot(BASEROWS,0,12,'ev')}</b>", f"<b>{inr(tot(BASEROWS,0,12,'rev'))}</b>", f"<b>{inr(tot(BASEROWS,0,12,'exp'))}</b>", f"<b>{inr(tot(BASEROWS,0,12,'profit'))}</b>", f"<b>{inr(BASEROWS[-1]['cum'])}</b>"]]), toc="12 mahine: kamai vs kharcha vs profit")
page("m12b", "ROADMAP · 12 MAHINE", "12 mahine ka <span class='g'>3D chart</span>", card(f'<b class="h3">Har mahine: kamai, kharcha, profit (base)</b>{bars3d([(r["rev"], r["exp"], max(r["profit"],0)) for r in BASEROWS], 480, 230, labels=[str(i+1) for i in range(12)])}') +
     card(f'<b class="h3">Jama paisa (setup ke baad)</b>{line_chart([r["cum"] for r in BASEROWS], 480, 170)}') +
     callout("📌 12 MAHINE KA NATIJA (base)", [f"Kamai <b>{inr(tot(BASEROWS,0,12,'rev'))}</b>, kharcha <b>{inr(tot(BASEROWS,0,12,'exp'))}</b>, profit <b>{inr(tot(BASEROWS,0,12,'profit'))}</b>", f"Setup ({inr(SETUP)}) nikaal kar <b>{inr(BASEROWS[-1]['cum'])}</b> bacha", "Aapki apni mehnat/salary iske <b>upar</b> alag hai"], "teal"), cont=True, toc=None)

# 26 3 scenarios
page("scen", "ROADMAP · 12 MAHINE", "Kam, <span class='g'>base</span> aur busy: 3 scenario", para("Bookings kam-zyada ho sakti hain. Isliye <b>3 tarah ke saal</b> dikhaye hain (rate aur kharcha same).") +
     table(["", "Kam (half)", "<b>Base</b>", "Busy (1.5x)"], [["Events / saal", tot(LOW, 0, 12, "ev"), f"<b>{tot(BASEROWS,0,12,'ev')}</b>", tot(BUSY, 0, 12, "ev")], ["Kamai", inr(tot(LOW, 0, 12, "rev")), f"<b>{inr(tot(BASEROWS,0,12,'rev'))}</b>", inr(tot(BUSY, 0, 12, "rev"))], ["Kharcha", inr(tot(LOW, 0, 12, "exp")), f"<b>{inr(tot(BASEROWS,0,12,'exp'))}</b>", inr(tot(BUSY, 0, 12, "exp"))],
                                         ["Profit", inr(tot(LOW, 0, 12, "profit")), f"<b>{inr(tot(BASEROWS,0,12,'profit'))}</b>", inr(tot(BUSY, 0, 12, "profit"))], [f"Setup ({inr(SETUP)}) ke baad", inr(LOW[-1]["cum"]), f"<b>{inr(BASEROWS[-1]['cum'])}</b>", inr(BUSY[-1]["cum"])], ["Paisa wapas", "12 mahine mein nahi", "<b>Mahina 7</b>", "Mahina 6"]]) +
     card(f'<b class="h3">Saal ka profit: 3D tulna</b>{bars3d([(tot(s,0,12,"rev"), tot(s,0,12,"exp"), max(tot(s,0,12,"profit"),0)) for s in (LOW, BASEROWS, BUSY)], 470, 200, labels=["Kam", "Base", "Busy"], fmt=lambda v: f"{v/1000:.0f}k")}') +
     callout("⚠️ KAM WALA SAAL SIKHATA HAI", ["Bookings aadhi hui to <b>12 mahine mein bhi setup wapas nahi</b> aata", "Isliye <b>pehle Level 1</b>, bookings dikhne par hi Level 2"], "red"), toc="Kam / base / busy: 3 scenario")

# 27 seasonality
months = [("Jan", "Naya saal party"), ("Feb", "Valentine, shaadi"), ("Mar", "Holi, exam ke baad"), ("Apr", "Garmi, birthday"), ("May", "Shaadi + summer"), ("Jun", "Kam: offer do"), ("Jul", "Kam: tie-up banao"), ("Aug", "Rakhi, Independence"), ("Sep", "Ganesh, festival"), ("Oct", "Navratri, Diwali"), ("Nov", "Shaadi season"), ("Dec", "Christmas, New Year")]
page("season", "ROADMAP · SAAL BHAR", "Saal bhar ke <span class='g'>mauke</span>", para("Har mahine bookings barabar nahi hoti. <b>Shaadi aur tyohaar</b> par demand zyada ho sakti hai, baaki mahine <b>birthday aur family event</b> chalte hain. Neeche andaza hai, apne shehar ka calendar banao.") +
     '<div class="grid3">' + "".join(card(f'<b class="h3">{m}</b><span class="sm">{t}</span>', "mini") for m, t in months) + '</div>' +
     callout("📌 TIP", ["Tyohaar se <b>2-3 hafte pehle</b> offer post karo", "Kam mahine mein <b>tie-up aur practice</b> karo"], "teal"), toc="Saal bhar ke mauke (calendar)")

# 28 marketing
page("mkt", "GROW", "Customer <span class='g'>kaise laaye</span>?", para("Mehenge ad ki zaroorat nahi. <b>Asli photo aur video</b> sabse bada hathiyar hai.") +
     checks(["<b>WhatsApp Status:</b> 10 second ka before/after arch video + shuruaati rate", "<b>Instagram Reels:</b> balloon phulte hue, arch banti hui, final reveal. Asli time dikhao", "<b>Tie-up:</b> cake shop, photographer, planner, banquet, kids store", "<b>3 rang option:</b> pastel pink-white, blue-white-gold, black-gold", "<b>Review:</b> har khush customer se Google/WhatsApp review lo", "<b>Local group:</b> Facebook/WhatsApp group mein asli kaam daalo", "<b>Referral:</b> naye customer laane par chhoot"]) +
     callout("🚫 JHOOTHA DAAWA MAT KARO", ["'1 minute mein arch' ya 'lakhon ki kamai' tab hi likho jab <b>asli demo aur bill</b> ho"], "red"), toc="Customer kaise laayein")

# 29 safety
page("safety", "SAVDHAANI", "Safety <span class='g'>aur quality</span>", checks(["Zyada arch mein <b>hawa bhare</b> balloon (helium zaroori nahi)", "Pump ke <b>hawa ke ched khule</b> rakho, geele haath se mat chalao", "Frame ka <b>bhaar wala base</b> lagao, outdoor mein hawa dekho", "Balloon ko <b>aag, garam light, nukili cheez</b> se door rakho", "Phate balloon ke tukde <b>utha lo</b> (bachhon ke liye khatra)", "Kamzor deewar par <b>bina permission</b> kuch mat chipkao", "Spare: balloon, glue dots, tape, extension, scissor saath rakho", "Likhit <b>scope, time, advance, cancel policy</b>"]), toc="Safety aur quality")

# 30 registration
page("reg", "SAVDHAANI", "Registration <span class='g'>checklist</span>", checks(["Shuru mein <b>sole proprietor</b> ke taur par, <b>PAN + bank account</b> alag rakho", "<b>Udyam registration</b> sarkari portal par <b>free</b> hai. Paid duplicate site se bacho", "<b>GST:</b> services ke liye aam limit <b>₹20 lakh</b> saalana turnover (CBIC). Apne CA se confirm karo", "<b>Shop / trade license:</b> nagar nigam se pucho", "<b>Bill/receipt</b> do, advance aur kharcha likho"]) +
     callout("📌 YAAD RAKHO", ["Rules badalte hain. <b>Apne CA ya sarkari portal</b> se confirm karo", "Hum yahan tax advice nahi de rahe"], "gold") + src("Source: udyamregistration.gov.in aur CBIC GST FAQ (page 33)."), toc="Registration checklist")

# 31 mistakes
page("mist", "SAVDHAANI", "Galtiyan <span class='g'>mat karna</span>", card("<b class='h3'>Ye galti mat karo</b>" + checks(["Bina order ke <b>bahut saara stock</b> khareedna", "Sasti arch <b>₹1,800 se kam</b> mein bechna", "Safety ya frame ka <b>base check</b> na karna", "Event ka <b>time ya jagah</b> ka andaza na lena", "<b>Advance ke bina</b> date pakki karna"], True)) +
     card("<b class='h3'>Sahi tareeka</b>" + checks(["Har job ka <b>kharcha-kamai likho</b> (job sheet)", "<b>5-10% extra balloon</b> rakho", "<b>Pehle photo mockup</b> dikhao", "Advance lo, <b>cancel policy likho</b>", "Chhota shuru karo, seekho, phir badhao"])), toc="Galtiyan aur sahi tareeka")

# 32 risks
page("risk", "SAVDHAANI", "Risk aur <span class='g'>bachav</span>", table(["Risk", "Kya ho sakta hai", "Bachav"], [["Kam bookings", "Paisa der se wapas", "Level 1 se test, tie-up banao"], ["Balloon fatna", "Arch kharab dikhti hai", "5-10% extra, sample test, garmi se bacho"], ["Galat rate", "Munafa khatam", "Har job ka kharcha likho"], ["Hawa / kamzor frame", "Safety aur nuksaan", "Weight base, indoor pehle, site check"], ["Last minute cancel", "Stock aur time barbaad", "Advance aur likhit policy"], ["Jhootha daawa", "Customer ka bharosa tootna", "Asli demo aur photo hi dikhao"]]), toc="Risk aur bachav")

# 33 sources
SRC = [
    ("Kiwiparty · Electric Balloon Pump, ₹666", "https://www.kiwiparty.in/products/electric-balloon-pump-73003", "Pump ka retail daam"),
    ("TradeIndia · balloon pump listings", "https://www.tradeindia.com/manufacturers/balloon-pump.html", "Pump ₹800-900"),
    ("HASTHIP · 8x6 ft arch kit ₹1,556 / 9 ft ₹1,669", "https://hasthip.com/products/hasthip%C2%AE-balloon-arc-stand-for-decoration-9ft-height-adjustable-balloon-arch-stand-balloon-arch-frame-with-base-complete-accessories-set-for-wedding-baby-shower-birthday-party-supplies-decorations", "Frame ka daam"),
    ("CRAze · 10 ft arch stand ₹4,399", "https://thecraze.in/products/10ft-balloon-arch-stand-kit-for-tables-balloon-garland-decoration", "Majboot frame"),
    ("Party Supplies India · DIY kit ₹499", "https://www.partysuppliesindia.com/products/balloon-garland-arch-diy-kit", "Strip, glue dots, tape"),
    ("Party Wholesale Hub · 100 latex ₹280", "https://partywholesale.in/products/12-standard-latex-balloons-white", "Balloon ka daam"),
    ("BalloonDekor · city-wise decor pricing", "https://balloondekor.com/blog/birthday-decoration-cost-india-city-guide", "₹1,499 se ₹11,499 rate range"),
    ("Funtook · balloon decoration prices", "https://funtook.in/balloon-decoration", "Package rate"),
    ("mytribe / Xclusive Event · NCR pricing", "https://mytribe.in/xclusive_event_/event-decoration", "200 balloon / ring arch rate"),
    ("Hindustan Times · celebration booking trends (20 May 2026)", "https://www.hindustantimes.com/genesis/indias-celebration-market-is-going-last-minute-as-quick-commerce-reshapes-birthdays-baby-showers-101779254576401-amp.html", "Platform ka reported data"),
    ("CBIC GST sectoral FAQ", "https://cbic-gst.gov.in/hindi/sectoral-faq.html", "₹20 lakh services limit"),
    ("Udyam Registration portal", "https://udyamregistration.gov.in/Important.aspx", "Free MSME registration")]
page("src", "SOURCES", "Ye numbers <span class='g'>kahan se aaye</span>?", para("Daam online listing se (Nov 2026) liye hain. Listing ka daam badalta rehta hai: <b>khareedne se pehle khud confirm karo</b>.") +
     '<div class="srcs">' + "".join(f'<div class="sr"><a href="{u}">{t}</a><span>{d}</span></div>' for t, u, d in SRC) + '</div>' +
     src("'Allowance' wale daam (tools, bag, props, branding, marketing) aur roadmap ke events/ticket <b>IdeasPulse ke udaharan assumption</b> hain, kisi listing se nahi. Roadmap guarantee nahi, ek model hai. Machine (reel wali) ka daam source mein nahi, seller se lo."), toc="Ye numbers kahan se aaye (sources)")

# 34 final + job sheet
page("final", "AAGE KYA KAREIN", "Final salaah <span class='g'>+ job sheet</span>", callout("✅ SEEDHI SALAAH", ["Pehle <b>local service</b> ki tarah shuru karo", "<b>Neat arch</b> banana seekho, <b>3-5 paid event</b> karo", "Phir hi bada frame, machine, props mein paisa lagao"], "teal") +
     card("<b class='h3'>📋 Har event ka JOB SHEET (copy mein banao)</b>" + table(["Date", "Customer", "Package", "Rate", "Balloon", "Kharcha", "Munafa", "Review"], [["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""]])) +
     callout("📌 HAR MAHINE ke ant mein", ["Kitne event? <b>Kul kamai? Kul kharcha? Profit?</b>", "Agle mahine ka <b>target</b> likho"], "gold"), toc="Final salaah + job sheet")

# 35 CTA (dark)
page("cta", "AAGE KYA?", "Judo <span class='g'>IdeasPulse</span> ke saath", f'''<p class="lead dk">Machine, investment aur profit ka <b>poora hisaab</b> chahiye? Comment mein ye shabd likho:</p>
<div class="keyw"><span>Comment karo</span><b>BALLOON</b></div>
<div class="qrs"><div class="qr"><img src="{QRY}"/><span>▶ YouTube @ideaspuls</span></div><div class="qr"><img src="{QRT}"/><span>✈ Telegram @ideaspulse</span></div></div>
<p class="lead dk">🌐 Aur business plans: <b class="g">ideaspulse.in</b></p>
<p class="disc">Disclaimer: Is plan ke saare kharch, daam, bikri aur munafe ke aankde <b>udaharan hain, guarantee nahi</b>. Rate badalte rehte hain. Khareedne se pehle supplier se khud confirm karein. Tyohaar/season ka asar alag hota hai. Tasveerein 3D udaharan hain. © ideaspulse.in · Share aur resell allowed nahi.</p>''', toc="Judo IdeasPulse ke saath (Comment BALLOON)", dark=True)

# ----- TOC page (inserted as page 2)
def build_toc():
    n_total = len(PAGES) + 2
    rows = ""
    # page numbers: PAGES list index + 2 (cover=1, toc=2); sections before toc insertion shift
    for idx, (pid, t, _) in enumerate(PAGES):
        if t:
            rows += f'<a class="trow" href="#{pid}"><span class="tn">{idx+3:02d}</span><span class="tt">{t}</span><span class="td"></span></a>'
    body = para("Ye plan aise likha hai ki <b>8vi class ka baccha bhi samajh sake</b>. Kisi bhi line par <b>tap/click</b> karo: seedha us page par pahunch jaoge.") + f'<div class="toc">{rows}</div>'
    return f'''<section class="page" id="toc"><div class="eyebrow">SHURUAAT</div><h1>Is plan mein <span class="g">kya hai</span>?</h1><div class="rule"></div><div class="body">{body}</div>
<footer><a href="#cover" class="flogo"><img src="{LOGO}"/></a><span>IdeasPulse · ideaspulse.in · Saare numbers udaharan hain, guarantee nahi</span><a class="pn" href="#cover">02</a></footer></section>'''


DECO = {"how": 1, "cta": 2, "glance": 2, "what": 3, "cust": 4, "pack": 5, "proc1": 6, "proc2": 7, "lean": 1, "event": 2, "be": 3, "road": 4, "m1a": 5, "m1b": 6, "season": 7, "mkt": 1, "safety": 2, "reg": 3, "mist": 4, "risk": 5, "final": 6, "m6b": 3, "mach2": 4, "items": 0, "running": 0, "scen": 0}


def page_numbers_fix():
    # the page() footer numbers assumed cover+toc offset missing; recompute
    out = []
    for idx, (pid, t, h) in enumerate(PAGES):
        h = re.sub(r'<a class="pn" href="#toc">\d+</a>', f'<a class="pn" href="#toc">{idx+3:02d}</a>', h)
        if DECO.get(pid):
            h = h.replace("</div>\n<footer>", f'<div class="deco">{cluster(DECO[pid])}</div></div>\n<footer>', 1)
        out.append(h)
    return out


CSS = (HERE / "style.css").read_text()
FONT = "".join(f"@font-face{{font-family:'Poppins';font-weight:{w};src:url(data:font/ttf;base64,{base64.b64encode((HERE/'assets'/f'Poppins-{n}.ttf').read_bytes()).decode()})}}" for n, w in (("Bold", 700), ("ExtraBold", 800), ("Black", 900)))
doc = f"<!doctype html><html lang='hi'><head><meta charset='utf-8'><title>Balloon Arch Business Plan · IdeasPulse</title><style>{FONT}{CSS}</style></head><body>" + cover_html + build_toc() + "".join(page_numbers_fix()) + "</body></html>"
(HERE / "plan.html").write_text(doc)
print("pages", len(PAGES) + 2)
