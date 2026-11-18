import base64, io, pathlib, urllib.parse, html
import segno
from data import *

HERE = pathlib.Path(__file__).parent
A = HERE / 'assets'
def b64(p, mime):
    return f'data:{mime};base64,' + base64.b64encode(p.read_bytes()).decode()
IMG = {p.stem: b64(p, 'image/jpeg') for p in (A / 'img').glob('*.jpg')}
FONT = lambda n: b64(A / 'fonts' / n, 'font/ttf')
E = html.escape

def maps_url(k):
    return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote_plus(MAPQ[k])

def qr(url, dark='#2A1A12'):
    q = segno.make(url, error='m')
    buf = io.BytesIO(); q.save(buf, kind='svg', scale=4, border=1, dark=dark, light=None, xmldecl=False, svgns=True)
    return 'data:image/svg+xml;base64,' + base64.b64encode(buf.getvalue()).decode()

G = {r[0]: r for r in GLANCE}
def cdot(c): return f'<span class="cdot" style="background:{CLUSTERS[c][1]}"></span>'
def ctag(c): return f'<span class="ctag" style="--c:{CLUSTERS[c][1]}">{CLUSTERS[c][0]}</span>'

PAGES = []
def page(body, cls='', sec='', bg=None, footer=True):
    st = f' style="background-image:url({bg})"' if bg else ''
    PAGES.append(dict(body=body, cls=cls, sec=sec, st=st, footer=footer))

def facts(k):
    _, n, hi, c, tk, tm, need, best, must = G[k]
    return f'''<div class="facts">
      <div><b>Ticket</b><span>{E(tk)}</span></div><div><b>Timing</b><span>{E(tm)}</span></div>
      <div><b>Time lagega</b><span>{E(need)}</span></div><div><b>Best time</b><span>{E(best)}</span></div></div>'''

def qrbox(k, small=False):
    return f'<a class="qr{" sm" if small else ""}" href="{maps_url(k)}"><img src="{qr(maps_url(k))}"><span>Scan / tap<br>Maps</span></a>'

def see_row(k):
    if k not in EXTRA: return ''
    s, near = EXTRA[k]
    return '<div class="see"><b>Kya dekhein</b>' + ''.join(f'<span>{E(x)}</span>' for x in s) + f'</div><div class="near"><b>📍 Paas me:</b> {E(near)}</div>'

def card(k, img=None, compact=False):
    _, n, hi, c, *_r = G[k]; P = PLACES[k]; must = G[k][8]
    pos = {'nah_jalview': 'center 52%;height:95mm', 'patrika': 'center 45%;height:60mm'}.get(img, 'center 35%')
    im = f'<div class="cimg" style="background-image:url({IMG[img]});background-position:{pos}"></div>' if img else ''
    return f'''<section class="card{" compact" if compact else ""}">{im}
      <div class="chead"><div><h3>{E(n)}{' <i class="star">★ MUST SEE</i>' if must else ''}</h3><div class="hi">{hi}</div></div>{ctag(c)}</div>
      <p class="intro">{E(P["intro"])}</p>{facts(k)}{see_row(k)}
      <div class="reach"><div><b>🚗 Car</b> {E(P["car"])}</div><div><b>🚌 Public</b> {E(P["public"])}</div></div>
      <div class="tipqr"><div class="tip"><b>Pro tip:</b> {E(P["tip"])}</div>{qrbox(k, True)}</div></section>'''

def big_place(k, hero, side_imgs, sec):
    _, n, hi, c, *_r = G[k]; P = PLACES[k]
    see = ''.join(f'<li>{E(s)}</li>' for s in P['see'])
    sides = ''.join(f'<div class="sideimg" style="background-image:url({IMG[s]})"></div>' for s in side_imgs)
    page(f'''<div class="hero" style="background-image:url({IMG[hero]})"><div class="herotxt">{ctag(c)}<h2>{E(n)}</h2><div class="hi big">{hi}</div></div></div>
      <div class="body pad"><p class="intro lg">{E(P["intro"])}</p>{facts(k)}
      <div class="two"><div><h4>Kya dekhein</h4><ul class="ticks">{see}</ul></div><div class="sides">{sides}</div></div>
      <div class="reach"><div><b>🚗 Car</b> {E(P["car"])}</div><div><b>🚌 Public</b> {E(P["public"])}</div></div>
      <div class="tipqr"><div class="tip"><b>Pro tip:</b> {E(P["tip"])}</div>{qrbox(k)}</div></div>''', 'nopad', sec)

# ---------------- 1 cover ----------------
page(f'''<div class="cover" style="background-image:url({IMG["amer_pavilion"]})">
  <div class="cv-top"><span class="brand">HOW IS TRAVELLERS LIFE</span><span class="ed">EDITION 2026</span></div>
  <div class="cv-mid"><div class="hi cvhi">जयपुर</div><h1>JAIPUR</h1><div class="cvsub">Complete Travel Guide</div>
  <div class="cvpills"><span>24 jagahein</span><span>Tickets & Timings</span><span>QR Maps</span><span>1–3 din plan</span></div></div>
  <div class="cv-bot"><b>Humne khud ghoom ke banaya</b> · Amer & Nahargarh ki photos humari Nov 2026 trip ki hain<br>Hinglish edition · Last checked: November 2026</div></div>''', 'nopad cv', footer=False)

# ---------------- 2 welcome + contents ----------------
toc = [('Jaipur ek nazar me (cheat sheet)', 'Cheat sheet'), ('Paise bachao: tickets 2026', 'Money'), ('Jaipur ka map: 5 clusters', 'Map'), ('Amer & North', 'Amer & North'),
       ('Nahargarh & Hills', 'Nahargarh & Hills'), ('Walled City (Pink City)', 'Walled City'), ('Central & South Jaipur', 'Central & South'), ('Hills & East + Safari', 'Hills & East'),
       ('Day trips', 'Day trips'), ('Doori aur time (route planner)', 'Route planner'), ('Jaipur kaise pahunchein + kahan rukein', 'Reach & stay'), ('Shehar me ghoomna', 'Getting around'),
       ('1, 2, 3 din ke plan', 'Itinerary'), ('Kya khayein', 'Food'), ('Kya kharidein', 'Shopping'), ('Scams se bachav + helplines', 'Safety'),
       ('Mausam, tyohaar & packing', 'Season'), ('Budget', 'Budget'), ('Sources', 'Sources')]
tocl = ''.join(f'<li><span>{E(t)}</span><i></i><b>@@{t}@@</b></li>' for t, p in toc)
page(f'''<div class="body">
  <div class="eyebrow">Namaste! 🙏</div><h2>Is guide ko kaise use karein</h2>
  <p>Ye guide un sab ke liye hai jinhone reel par <b>"JAIPUR"</b> comment kiya. Isme har jagah ka ticket, timing, kitna time lagega, best time, car aur public transport ka raasta — sab ek jagah hai.</p>
  <div class="howto">
    <div><b>📍 QR scan kariye</b>Har jagah ke saath QR hai — scan (ya PDF me tap) karte hi Google Maps khul jaayega.</div>
    <div><b>🎨 Rang = area</b>Har jagah ka rang uska cluster batata hai. Ek rang ki jagahein ek din me ghoomiye.</div>
    <div><b>★ Must see</b>Time kam hai? Sirf star wali jagahein kariye.</div>
  </div>
  <h4 class="mt">Is guide me</h4><ol class="toc">{tocl}</ol></div>''', sec='Welcome')

# ---------------- 3-4 cheat sheet ----------------
def glance_rows(rows):
    out = ''
    for (k, n, hi, c, tk, tm, need, best, must) in rows:
        out += f'<tr><td>{cdot(c)}<a href="{maps_url(k)}">{E(n)}</a>{" <i class=star>★</i>" if must else ""}</td><td>{E(tk)}</td><td>{E(tm)}</td><td>{E(need)}</td><td>{E(best)}</td></tr>'
    return out
legend = ''.join(f'<span>{cdot(c)}{n}</span>' for c, (n, _) in CLUSTERS.items())
for i, rows in enumerate((GLANCE[:12], GLANCE[12:])):
    page(f'''<div class="body"><div class="eyebrow">Screenshot le lijiye 📸</div><h2>Jaipur ek nazar me {i + 1}/2</h2>
      <div class="legend">{legend}</div>
      <table class="gl"><thead><tr><th>Jagah</th><th>Ticket*</th><th>Timing</th><th>Time</th><th>Best time</th></tr></thead><tbody>{glance_rows(rows)}</tbody></table>
      <p class="note">*Ticket = Indian adult, 2026 rates. Foreigner, camera aur guide charges alag. Jagah ke naam par tap karte hi Maps khulega.</p></div>''', sec='Cheat sheet')

# ---------------- 5 money ----------------
page(f'''<div class="body"><div class="eyebrow">Paise bachao 💰</div><h2>Tickets 2026: kya badla</h2>
  <p><b>1 January 2026</b> se Rajasthan sarkar ne lagbhag 10 saal baad monuments ki fees badhayi. Amer Fort ab <b>₹200</b> (pehle ₹100) aur Hawa Mahal, Jantar Mantar, Albert Hall, Nahargarh <b>₹100</b> (pehle ₹50) ke aas-paas hain.</p>
  <div class="callout"><div class="cbig">COMPOSITE<br>TICKET</div><div><b>Ek ticket, 7 jagahein, 2 din valid.</b> Amer Fort, Hawa Mahal, Jantar Mantar, Albert Hall, Nahargarh, Sisodia Rani Garden aur Vidyadhar Garden.
  <br><br>2026 se pehle iska rate <b>₹300</b> (Indian) tha — naye rate counter ya online par check kariye. 3 se zyada jagahein dekh rahe hain to ye almost hamesha sasta padta hai.</div></div>
  <h4>5 aur money tips</h4><ul class="ticks">
  <li><b>Students:</b> valid student ID par bahut kam ticket — ID saath rakhiye.</li>
  <li><b>Online ticket</b> le lijiye — Amer jaise spots par counter ki line bachti hai.</li>
  <li><b>Cab:</b> poore din ke liye 8 hr/80 km package lijiye; har jagah alag auto mehnga padta hai.</li>
  <li><b>Guide:</b> sirf sarkari ID card wale guide; rate pehle tay kariye.</li>
  <li><b>Free jagahein:</b> Jal Mahal view, Patrika Gate, Birla Mandir, Moti Dungri, Galtaji, Govind Dev Ji.</li></ul>
  <p class="note">Rates badal sakte hain — ye guide Nov 2026 tak ki jaankari par bani hai.</p></div>''', sec='Money')

# ---------------- 6 map ----------------
MAPSVG = '''<svg viewBox="0 0 500 560" class="map" xmlns="http://www.w3.org/2000/svg" font-family="Poppins">
<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><line x1="0" y1="0" x2="0" y2="8" stroke="#d9c6a8" stroke-width="2"/></pattern></defs>
<path d="M20 40 C120 10 230 30 300 70 C360 100 420 90 480 120 L480 170 C400 150 330 160 280 140 C200 110 120 120 20 110 Z" fill="url(#hatch)" opacity=".8"/>
<text x="30" y="30" font-size="13" fill="#9b8466" font-style="italic">Aravalli hills</text>
<g stroke="#bfa98a" stroke-width="3" stroke-dasharray="7 6" fill="none"><path d="M150 85 L190 190 L250 290 L270 420 L300 520"/><path d="M250 290 L400 300"/><path d="M250 290 L120 330"/></g>
<text x="300" y="545" font-size="11" fill="#9b8466">→ Airport / Tonk Rd</text><text x="408" y="296" font-size="11" fill="#9b8466">Agra Rd →</text>
'''
def blob(x, y, r, c, label, items):
    col = CLUSTERS[c][1]
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="2.5"/>'
    s += f'<text x="{x}" y="{y - r + 22}" text-anchor="middle" font-size="15" font-weight="700" fill="{col}">{label}</text>'
    for i, it in enumerate(items):
        s += f'<text x="{x}" y="{y - r + 42 + i * 16}" text-anchor="middle" font-size="12" fill="#2A1A12">{it}</text>'
    return s
MAPSVG += blob(130, 150, 82, 'A', 'AMER & NORTH', ['Amer · Jaigarh', 'Panna Meena · Anokhi', 'Jal Mahal · Kanak'])
MAPSVG += blob(330, 115, 72, 'E', 'HILLS', ['Nahargarh', 'Gaitore'])
MAPSVG += blob(235, 300, 76, 'W', 'PINK CITY', ['Hawa Mahal · Isarlat', 'City Palace', 'Jantar Mantar', 'Govind Dev Ji'])
MAPSVG += blob(415, 330, 70, 'E', 'EAST', ['Galtaji', 'Sisodia Rani', 'Vidyadhar'])
MAPSVG += blob(240, 440, 82, 'C', 'CENTRAL & SOUTH', ['Albert Hall · Masala Chowk', 'Birla · Moti Dungri', 'Raj Mandir · JKK', 'Patrika Gate · Jhalana'])
MAPSVG += blob(420, 500, 52, 'O', 'OUTSKIRTS', ['Chokhi Dhani'])
MAPSVG += '</svg>'
page(f'''<div class="body"><div class="eyebrow">Smart route = kam traffic</div><h2>Jaipur ke 5 clusters</h2>
  <p>Ek din me ek-do cluster kariye — shehar ke aar-paar baar baar jaana sabse bada time-waste hai.</p>{MAPSVG}
  <p class="note">Simple diagram hai, scale par nahi. Asli raaste ke liye har jagah ka QR scan kariye.</p></div>''', sec='Map')

# ---------------- places ----------------
big_place('amer', 'amer_pavilion', ['amer_ganeshpol', 'amer_sheesh'], 'Amer & North')
page(f'''<div class="body">{card("jaigarh", "amer_rooftop")}
  <div class="callout"><div class="cbig">AMER<br>COMBO</div><div><b>Ek subah, 4 jagahein:</b> Amer Fort (8:00) → Panna Meena ka Kund → Anokhi Museum → Jaigarh Fort. Gaadi ek baar Amer parking me lagaiye, Panna Meena aur Anokhi paidal, Jaigarh ke liye jeep/cab.<br><br>Dopahar 1 baje tak sab khatam — wapsi me Jal Mahal par photo stop.</div></div></div>''', sec='Amer & North')
page(f'<div class="body">{card("panna")}{card("anokhi")}</div>', sec='Amer & North')
page(f'<div class="body">{card("jalmahal", "nah_jalview")}</div>', sec='Amer & North')
page(f'''<div class="body"><div class="eyebrow">Humari trip se 📸</div><h2>Amer ke 3 photo secrets</h2>
  <div class="ps3 short"><div style="background-image:url({IMG["amer_sheeshvid"]})"><span>Sheesh Mahal</span></div><div style="background-image:url({IMG["amer_umbrella"]})"><span>Rangeen chhatri</span></div><div style="background-image:url({IMG["amer_court"]})"><span>Jharokha view</span></div></div>
  <ul class="ticks"><li><b>Sheesh Mahal:</b> chhat aur deewarein shishe ke tukdon se bani hain — andar mobile ki torch jalaiye, poora hall taaron jaisa chamakta hai.</li>
  <li><b>Rangeen chhatri:</b> Amer ke bahar Rajasthani chhatriyan aur pagdi milti hain — photos ke liye mast prop. Rate pehle tay kariye.</li>
  <li><b>Jharokhe:</b> upar ki manzil ke jharokhon se Maota Lake aur Aravalli ka frame banaiye — wide-angle ya 0.5x lens best.</li></ul>{card("kanak", compact=True)}</div>''', sec='Amer & North')
big_place('nahargarh', 'nah_lights', ['nah_painted', 'nah_madh'], 'Nahargarh & Hills')
page(f'''<div class="body">{card("gaitore", compact=True)}
  <div class="callout night"><div class="cbig">SUNSET<br>PLAN</div><div><b>Nahargarh ka perfect evening:</b><br>5:00 PM pahunchiye → Madhavendra Bhawan → 6:00 sunset point (Jal Mahal side) → raat me Pink City ki lights → 8:30 tak wapsi shuru (fort 9 PM tak).<br><br>Wapsi ki cab pehle se fix rakhiye — upar raat ko auto mushkil se milta hai.</div></div>
  <div class="ps3 short"><div style="background-image:url({IMG["nah_cityview"]})"><span>Shaam: city view</span></div><div style="background-image:url({IMG["nah_night"]})"><span>Raat</span></div><div style="background-image:url({IMG["nah_selfie"]})"><span>Humari trip</span></div></div></div>''', sec='Nahargarh & Hills')
page(f'<div class="body">{card("hawa")}{card("isarlat", compact=True)}</div>', sec='Walled City')
page(f'<div class="body">{card("citypalace")}{card("jantar")}</div>', sec='Walled City')
page(f'''<div class="body">{card("govind")}
  <div class="callout pink"><div class="cbig">WALK<br>THE CITY</div><div><b>Pink City walking route (3–4 hr):</b><br>Badi Chaupar metro → Hawa Mahal → Isarlat → City Palace → Jantar Mantar → Govind Dev Ji → Johari Bazaar me LMB par lassi.<br><br>Gaadi ek baar park kariye, baaki sab paidal ya e-rickshaw. Old city ki galiyon me car le jaana sabse badi galti hai.</div></div>
  <h4 class="mt">Pink City kyun "pink" hai?</h4><div class="facts3">
  <div><b>1727</b>Sawai Jai Singh II ne Jaipur basaya — India ke pehle planned shehron me se ek, grid wali sadkein.</div>
  <div><b>1876</b>Prince of Wales ke swagat me poore shehar ko terracotta pink rang diya gaya — tab se "Pink City".</div>
  <div><b>2019</b>Jaipur ka Walled City UNESCO World Heritage City bana.</div></div></div>''', sec='Walled City')
page(f'<div class="body">{card("albert")}{card("masala", compact=True)}</div>', sec='Central & South')
page(f'<div class="body">{card("birla")}{card("motidungri")}</div>', sec='Central & South')
page(f'''<div class="body">{card("patrika", "patrika")}
  <h4 class="mt">Local etiquette 🙏</h4><ul class="ticks">
  <li>Mandir me joote bahar, kandhe-ghutne dhake kapde best.</li>
  <li>Museum ke andar photography ke niyam board par padhiye — flash aksar mana hota hai.</li>
  <li>Purani deewaron par naam likhna, chadhna ya chhoona — bilkul nahi.</li>
  <li>Plastic bottle dustbin me — Jaipur ko pink rakhiye, kachre se nahi.</li></ul></div>''', sec='Central & South')
page(f'''<div class="body">{card("jkk", compact=True)}{card("rajmandir", compact=True)}
  <div class="callout pink"><div class="cbig">CENTRAL<br>EVENING</div><div><b>Shaam ka plan:</b> 5:30 Albert Hall lights → Masala Chowk dinner → Birla Mandir aarti → Raj Mandir movie. Sab 2–3 km ke andar.</div></div>
</div>''', sec='Central & South')
page(f'<div class="body">{card("galtaji")}{card("sisodia", compact=True)}</div>', sec='Hills & East')
page(f'<div class="body">{card("jhalana")}{card("chokhi")}</div>', sec='Safari & Evening')

# ---------------- day trips ----------------
trips = [('abhaneri', 'Chand Baori, Abhaneri', '~90 km · 2 hr', 'Duniya ki sabse gehri aur badi stepwells me se ek — 3,500 seedhiyan, 13 manzil. Agra jaate hue raaste me bhi kar sakte hain.'),
         ('bhangarh', 'Bhangarh Fort', '~85 km · 2 hr', '"India ka sabse haunted fort" — sooraj dhalne ke baad andar jaana mana hai. Sariska ke saath combine kar sakte hain.'),
         ('sambhar', 'Sambhar Salt Lake', '~90 km · 2 hr', 'India ki sabse badi namak ki jheel — safed zameen, flamingo (sardiyon me) aur sunset photography.')]
tr = ''.join(f'''<div class="trip"><div><h3>{E(n)}</h3><div class="dist">{E(d)} Jaipur se</div><p>{E(t)}</p></div>{qrbox(k, True)}</div>''' for k, n, d, t in trips)
page(f'''<div class="body"><div class="eyebrow">Ek din extra hai?</div><h2>Jaipur se day trips</h2>{tr}
  <p class="note">Teeno ke liye subah jaldi nikalna aur poore din ki cab best hai. Bhangarh ke niyam ASI board par likhe hote hain — unka paalan kariye.</p></div>''', sec='Day trips')

# ---------------- distances ----------------
drows = ''.join(f'<tr><td>{E(a)} → {E(b)}</td><td>{E(d)}</td><td>{E(t)}</td><td>{E(m)}</td></tr>' for a, b, d, t, m in DISTANCES)
page(f'''<div class="body"><div class="eyebrow">Route planner</div><h2>Doori aur time</h2>
  <table class="gl dist"><thead><tr><th>Kahan se → kahan</th><th>Doori</th><th>Time*</th><th>Kaise</th></tr></thead><tbody>{drows}</tbody></table>
  <p class="note">*Normal traffic me road ka andaaza. Shaam 5–8 baje aur weekend par 30–50% zyada time lagta hai.</p></div>''', sec='Route planner')

# ---------------- reach + stay ----------------
page('''<div class="body"><div class="eyebrow">Shuruaat</div><h2>Jaipur kaise pahunchein</h2>
  <div class="grid3"><div><b>✈️ Flight</b>Jaipur International Airport (Sanganer). Hawa Mahal se ~12 km, cab se 35 min.</div>
  <div><b>🚆 Train</b>Main station Jaipur Junction. Durgapura aur Gandhinagar stations bhi kaam aate hain. Junction se metro bhi milti hai.</div>
  <div><b>🚌 Road</b>RSRTC ka Sindhi Camp bus stand (metro station paas me). Delhi se ~280 km (5 hr), Agra se ~240 km (4–5 hr).</div></div>
  <h2 class="mt">Kahan rukein</h2><table class="gl"><thead><tr><th>Area</th><th>Kiske liye best</th></tr></thead><tbody>
  <tr><td><b>Pink City / Walled City</b></td><td>Heritage haveli stay, Hawa Mahal–City Palace paidal. Gaadi parking mushkil.</td></tr>
  <tr><td><b>MI Road · C-Scheme · Bani Park</b></td><td>Central, station ke paas, har budget ke hotel, khaane ke achhe options.</td></tr>
  <tr><td><b>Amer Road</b></td><td>Amer aur Jal Mahal paas, shaant resorts. Shehar thoda door.</td></tr>
  <tr><td><b>Malviya Nagar · Tonk Road</b></td><td>Airport, Jhalana aur Chokhi Dhani ke paas. Family/modern hotels.</td></tr></tbody></table></div>''', sec='Reach & stay')

# ---------------- getting around ----------------
page('''<div class="body"><div class="eyebrow">Local transport</div><h2>Shehar me ghoomna</h2>
  <table class="gl"><thead><tr><th>Mode</th><th>Kab use karein</th><th>Dhyan rakhein</th></tr></thead><tbody>
  <tr><td><b>Metro</b></td><td>Mansarovar → Railway Station → Sindhi Camp → Chandpole → Chhoti/Badi Chaupar. Pink City ke liye best.</td><td>Amer, Nahargarh, Jaigarh, Jal Mahal, Galtaji tak nahi jaati.</td></tr>
  <tr><td><b>City bus</b></td><td>Amer Road, JLN Marg, Tonk Road, Agra Road.</td><td>Route number badalte rehte hain — conductor se poochiye.</td></tr>
  <tr><td><b>E-rickshaw</b></td><td>Old city ke chhote safar.</td><td>Baithne se pehle kiraya tay kariye.</td></tr>
  <tr><td><b>Auto</b></td><td>Last mile aur 2–8 km ke safar.</td><td>Meter nahi to rate pehle fix.</td></tr>
  <tr><td><b>App cab</b></td><td>Amer, Nahargarh, Jhalana, Chokhi Dhani.</td><td>Pahadi jagah se wapsi ki booking pehle.</td></tr>
  <tr><td><b>Full-day cab</b></td><td>Family, 3+ clusters ek din me.</td><td>8 hr/80 km package; toll-parking alag.</td></tr></tbody></table>
  <h4 class="mt">Apni gaadi se aa rahe hain?</h4><ul class="ticks">
  <li>Pink City me gaadi Badi Chaupar/Jalebi Chowk ki parking me lagaiye, bazaar ki galiyon me mat ghusaiye.</li>
  <li>Amer me fort parking aur traffic police ke ishaaron ka paalan.</li>
  <li>Nahargarh/Jaigarh ki pahadi road sankari hai — mod par mat rukiye, raat ko low beam.</li>
  <li>Gaadi me keemti saamaan dikhta hua mat chhodiye.</li></ul></div>''', sec='Getting around')

# ---------------- itineraries ----------------
def tl(rows):
    return '<div class="tl">' + ''.join(f'<div class="tli"><span class="tt">{E(t)}</span><span class="td">{E(d)}</span></div>' for t, d in rows) + '</div>'
page(f'''<div class="body"><div class="eyebrow">Ready-made plan</div><h2>1 din me Jaipur</h2>
  {tl([('7:45 AM', 'Hotel se nikliye (cab 8 hr package)'), ('8:00–10:30', 'Amer Fort ★ (Sheesh Mahal, Ganesh Pol)'), ('10:30–11:00', 'Panna Meena ka Kund'), ('11:15', 'Jal Mahal photo stop ★'),
       ('12:00–1:00', 'Lunch — LMB / MI Road'), ('1:15–2:00', 'Hawa Mahal ★'), ('2:15–4:30', 'City Palace ★ + Jantar Mantar ★'), ('5:00–8:30 PM', 'Nahargarh ★ — sunset + Pink City lights')])}
  <div class="callout pink"><div class="cbig">PRO<br>MOVE</div><div>Subah Amer pehle — 10 baje ke baad tour buses aur dhoop dono badh jaate hain. Nahargarh raat 9 baje tak khula hai, isliye din ka grand finale wahi rakha hai.</div></div>
  <p class="note">Thak gaye to City Palace chhod dijiye.</p></div>''', sec='Itinerary')
page(f'''<div class="body"><div class="eyebrow">Aaram se ghoomna hai?</div><h2>2 din aur 3 din ke plan</h2>
  <div class="days"><div><span class="dn" style="background:{CLUSTERS["A"][1]}">Day 1</span><b>Amer + Nahargarh</b>Amer → Panna Meena → Anokhi → Jaigarh → Jal Mahal → shaam Nahargarh sunset & lights</div>
  <div><span class="dn" style="background:{CLUSTERS["W"][1]}">Day 2</span><b>Pink City + Central</b>Hawa Mahal → Isarlat → City Palace → Jantar Mantar → Govind Dev Ji → Johari Bazaar → Albert Hall (shaam) → Masala Chowk dinner → Birla Mandir</div>
  <div><span class="dn" style="background:{CLUSTERS["E"][1]}">Day 3</span><b>Safari + East + Culture</b>Jhalana safari (subah) → Galtaji → Sisodia Rani Garden → Patrika Gate → Chokhi Dhani (dinner)</div></div>
  <p>2 din wale sirf Day 1 + Day 2 kariye. Raj Mandir me raat ka movie show kisi bhi din add kar sakte hain.</p>
  <div class="photostory"><div style="background-image:url({IMG["nah_sit"]})"></div><div style="background-image:url({IMG["nah_hands"]})"></div></div></div>''', sec='Itinerary')

# ---------------- food ----------------
page(f'''<div class="body"><div class="eyebrow">Swad Rajasthan ka</div><h2>Kya khayein, kahan khayein</h2>
  <table class="gl"><thead><tr><th>Kya</th><th>Kahan try karein (popular)</th></tr></thead><tbody>
  <tr><td><b>Pyaaz kachori, mirchi vada</b></td><td>Rawat Mishthan Bhandar (Station Road) · Masala Chowk</td></tr>
  <tr><td><b>Rajasthani thali / Dal baati churma</b></td><td>Chokhi Dhani · LMB (Johari Bazaar) · MI Road ke thali restaurants</td></tr>
  <tr><td><b>Ghewar, mithai</b></td><td>LMB (Johari Bazaar) · Rawat — sardiyon/Teej me fresh ghewar</td></tr>
  <tr><td><b>Lassi</b></td><td>MI Road ki purani lassi dukaanein — kulhad wali</td></tr>
  <tr><td><b>Ker sangri, gatte ki sabzi</b></td><td>Kisi bhi achhe thali restaurant me</td></tr>
  <tr><td><b>Street food sab ek jagah</b></td><td>Masala Chowk (Albert Hall ke paas)</td></tr>
  <tr><td><b>Chai with view</b></td><td>Hawa Mahal ke saamne rooftop cafés · Nahargarh par sunset chai</td></tr></tbody></table>
  <div class="photostory one"><div style="background-image:url({IMG["resto"]})"></div><p><b>Tip:</b> Bheed wali, saaf-suthri dukaan chuniye. Khaane se pehle rate poochiye — tourist spots par menu me rate na ho to zaroor.</p></div></div>''', sec='Food')

# ---------------- shopping ----------------
page('''<div class="body"><div class="eyebrow">Shopping list</div><h2>Kya kharidein, kahan se</h2>
  <table class="gl"><thead><tr><th>Bazaar</th><th>Kya milega</th></tr></thead><tbody>
  <tr><td><b>Johari Bazaar</b></td><td>Jewellery, gemstones, Bandhej/Leheriya saree</td></tr>
  <tr><td><b>Bapu Bazaar</b></td><td>Mojari/jootiyan, kurte, chadar, souvenirs — bargain zaroor</td></tr>
  <tr><td><b>Tripolia & Maniharon ka Raasta</b></td><td>Lakh (lac) ki chudiyan, brass items</td></tr>
  <tr><td><b>Chandpole Bazaar</b></td><td>Marble murtiyan, handicraft</td></tr>
  <tr><td><b>Kishanpole Bazaar</b></td><td>Kapda, block-print fabric</td></tr>
  <tr><td><b>MI Road · Rajasthali</b></td><td>Blue pottery, handicraft — Rajasthali sarkari emporium hai, fixed rate</td></tr></tbody></table>
  <h4 class="mt">Bargaining ke 4 niyam</h4><ul class="ticks">
  <li>Pehla rate sun kar 40–50% se shuru kariye, araam se.</li><li>2–3 dukaanon par rate compare kariye.</li>
  <li>Jewellery/gems: sirf bill aur certificate ke saath. "Export karke double paise" wale offer = scam.</li>
  <li>Bill maangiye aur return/exchange policy poochiye.</li></ul></div>''', sec='Shopping')

# ---------------- scams ----------------
page('''<div class="body"><div class="eyebrow">Smart traveller bano</div><h2>Scams se bachav</h2>
  <div class="scams">
  <div><b>💎 Gem export scam</b>Koi dost bankar kahe "ye gems apne desh me bech do, double paisa milega" — 100% fraud. Kabhi mat kariye.</div>
  <div><b>🛺 Commission shopping</b>"Sasta ghuma dunga" bolkar auto/guide sirf commission wali dukaanon par le jaate hain. Mana kar dijiye.</div>
  <div><b>🚫 "Aaj band hai"</b>Koi kahe monument band hai, chalo doosri jagah — khud gate par jaakar check kariye.</div>
  <div><b>🪪 Fake guide</b>Amer ya City Palace gate par sirf sarkari ID card wala guide, rate pehle tay.</div>
  <div><b>🐒 Bandar</b>Galtaji/Amer me khaana aur chashma sambhal ke. Khilana mana hai.</div>
  <div><b>💸 Overcharging</b>Auto/e-rickshaw me baithne se pehle kiraya tay; app cab ka rate compare kariye.</div></div>
  <h4 class="mt">Zaroori numbers</h4>
  <div class="nums"><div><b>112</b>Emergency (Police)</div><div><b>108</b>Ambulance</div><div><b>1363</b>Tourist helpline (24×7)</div><div><b>181</b>Women helpline</div></div></div>''', sec='Safety')

# ---------------- season ----------------
page('''<div class="body"><div class="eyebrow">Kab jaayein</div><h2>Mausam aur tyohaar</h2>
  <div class="season"><div class="s1"><b>Oct–Mar</b>Best mausam. Din suhaana, sardiyon ki raat thandi — halki jacket rakhiye.</div>
  <div class="s2"><b>Apr–Jun</b>Bahut garmi (40°C+). Sirf subah-shaam ghoomiye, dopahar museum/hotel.</div>
  <div class="s3"><b>Jul–Sep</b>Monsoon — Aravalli hari-bhari, Nahargarh ke views best. Kabhi kabhi baarish ruka deti hai.</div></div>
  <table class="gl"><thead><tr><th>Tyohaar</th><th>Kab</th><th>Kya khaas</th></tr></thead><tbody>
  <tr><td><b>Makar Sankranti</b></td><td>14 January</td><td>Poora shehar chhato par patang udaata hai</td></tr>
  <tr><td><b>Jaipur Literature Fest</b></td><td>January end</td><td>Duniya ka bada free literature festival</td></tr>
  <tr><td><b>Gangaur</b></td><td>March–April</td><td>City Palace se shahi sawari</td></tr>
  <tr><td><b>Teej</b></td><td>July–August</td><td>Leheriya, ghewar aur Teej sawari</td></tr>
  <tr><td><b>Diwali</b></td><td>Oct–Nov</td><td>Johari/Bapu Bazaar ki roshni dekhne layak</td></tr></tbody></table>
  <h4 class="mt">Packing checklist ✅</h4><div class="checks">
  <span>Comfortable joote</span><span>Paani ki bottle</span><span>Sunglasses + cap</span><span>Sunscreen</span><span>Photo ID (+ student ID)</span><span>Power bank</span><span>Halki jacket (sardi)</span><span>Thoda cash (chhoti dukaanein)</span></div></div>''', sec='Season')

# ---------------- budget ----------------
page('''<div class="body"><div class="eyebrow">Kitna kharcha</div><h2>Budget (per person, per din)</h2>
  <div class="budget"><div><span>Budget</span><b>₹1,000–1,500</b>Metro/bus/auto, local khaana, 2–3 ticket</div>
  <div class="mid"><span>Comfort</span><b>₹2,000–3,500</b>Shared cab/auto, achhe restaurant, 4–5 ticket</div>
  <div><span>Family + private cab</span><b>₹3,000–6,000+</b>Full-day cab, sab monuments, Chokhi Dhani</div></div>
  <p class="note">Hotel, shopping, safari aur Chokhi Dhani package alag. Group me cab share karne se per person kharcha kaafi ghat jaata hai.</p>
  <h4 class="mt">Extra kharche jo log bhool jaate hain</h4><ul class="ticks">
  <li>Camera/video fee kuch monuments par</li><li>Guide ₹ (pehle tay kariye)</li><li>Parking aur toll</li><li>Jhalana safari: ~₹1,350 per seat (Indian)</li><li>Light & Sound show (Amer) — alag ticket</li></ul></div>''', sec='Budget')

# ---------------- sources ----------------
srcs = [('Rajasthan Tourism — Jaipur', 'https://www.tourism.rajasthan.gov.in/jaipur.html'), ('Rajasthan Tourism — Hawa Mahal', 'https://www.tourism.rajasthan.gov.in/hawa-mahal.html'),
        ('Rajasthan Tourism — Jantar Mantar', 'https://www.tourism.rajasthan.gov.in/jantar-mantar.html'), ('Jaipur Metro (JMRC)', 'https://transport.rajasthan.gov.in/jmrc/'),
        ('RTDC City Tour', 'https://www.rtdc.tourism.rajasthan.gov.in/Client/CityTour.aspx'), ('City Palace — official', 'https://citypalace.org/'),
        ('Anokhi Museum', 'https://anokhimuseum.com/'), ('Jhalana safari booking — FMDSS (Forest Dept.)', 'https://fmdss.forest.rajasthan.gov.in/'),
        ('2026 ticket revision — Zee News (Hindi)', 'https://zeenews.india.com/hindi/india/rajasthan/jaipur/rajasthan-monuments-ticket-price-amer-fort-hawa-mahal-albert-hall-museum-hike-2026/1767095395543')]
sl = ''.join(f'<li><a href="{u}">{E(t)}</a></li>' for t, u in srcs)
page(f'''<div class="body"><div class="eyebrow">Bharosa</div><h2>Sources aur disclaimer</h2>
  <p>Jaankari Rajasthan Tourism, sarkari portals aur official websites se li gayi hai, aur Amer–Nahargarh ki timing/experience humari Nov 2026 ki trip se hai.</p>
  <ul class="src">{sl}</ul>
  <div class="callout soft"><div><b>Dhyan dein:</b> Ye ek independent travel guide hai, sarkari publication nahi. Ticket rate, timing aur raaste bina notice badal sakte hain — tyohaar, VIP visit ya maintenance par jagah band ho sakti hai. Jaane wale din counter/official site par ek baar confirm kar lijiye.<br><br><b>Last checked:</b> November 2026</div></div></div>''', sec='Sources')

# ---------------- back cover ----------------
page(f'''<div class="cover back" style="background-image:url({IMG["nah_lights"]})"><div class="bk">
  <div class="hi cvhi">धन्यवाद!</div><h1 class="bkh">Jaipur ka maza lijiye!</h1>
  <p>Guide pasand aayi? Reel ko <b>save</b> kariye, doston ko <b>share</b> kariye aur aise hi aur guides ke liye follow kariye:</p>
  <div class="bkbrand">HOW IS TRAVELLERS LIFE</div><div class="bksub">Instagram · YouTube</div>
  <div class="bkcta"><span>Next guide kahan ki chahiye? Comment me batayiye 👇</span></div>
  <div class="bkcredit">Photos: Amer Fort & Nahargarh Fort, November 2026 — How Is Travellers Life</div></div></div>''', 'nopad cv', footer=False)

# ---------------- render HTML ----------------
CSS = (HERE / 'style.css').read_text()
fonts = ''
for fam, files in (('Poppins', [(400, 'Poppins-400'), (500, 'Poppins-500'), (600, 'Poppins-600'), (700, 'Poppins-700'), (800, 'Poppins-800')]),
                   ('Hind', [(400, 'Hind-400'), (500, 'Hind-500'), (600, 'Hind-600'), (700, 'Hind-700')]), ('Anton', [(400, 'Anton-400')]), ('Yatra', [(400, 'YatraOne-400')])):
    for w, f in files:
        fonts += f"@font-face{{font-family:'{fam}';font-weight:{w};src:url({FONT(f + '.ttf')}) format('truetype')}}\n"
out = ['<!doctype html><html lang="hi"><head><meta charset="utf-8"><title>Jaipur Complete Travel Guide 2026 — How Is Travellers Life</title><style>', fonts, CSS, '</style></head><body>']
N = len(PAGES)
first = {}
for i, p in enumerate(PAGES, 1): first.setdefault(p['sec'], i)
for t, sec in toc: PAGES[1]['body'] = PAGES[1]['body'].replace(f'@@{t}@@', str(first[sec]))
for i, p in enumerate(PAGES, 1):
    foot = f'<footer><span>How Is Travellers Life · Jaipur Guide 2026</span><span>{p["sec"]}</span><b>{i}</b></footer>' if p['footer'] else ''
    out.append(f'<div class="page {p["cls"]}"{p["st"]}>{p["body"]}{foot}</div>')
out.append('</body></html>')
(HERE / 'guide.html').write_text(''.join(out))
print('pages', N)
