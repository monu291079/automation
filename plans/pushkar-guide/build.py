import base64, io, pathlib, urllib.parse, html, sys
import segno
from data import *

HERE = pathlib.Path(__file__).parent
A = HERE / 'assets'
b64 = lambda p, m: f'data:{m};base64,' + base64.b64encode(p.read_bytes()).decode()
IMG = {p.stem: b64(p, 'image/jpeg') for p in (A / 'img').glob('*.jpg')}
E = html.escape
AI = lambda k: k.startswith('ai_')

def maps_url(k): return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote_plus(MAPQ[k])
def qr(url):
    q = segno.make(url, error='m'); buf = io.BytesIO()
    q.save(buf, kind='svg', scale=4, border=1, dark='#1E1A2B', light=None, xmldecl=False, svgns=True)
    return 'data:image/svg+xml;base64,' + base64.b64encode(buf.getvalue()).decode()

G = {r[0]: r for r in GLANCE}

def make(lang, off=0):
    hi = lang == 'hi'
    t = lambda pair: pair[0] if hi else pair[1]
    L = lambda h, e: h if hi else e
    PAGES = []
    def page(body, cls='', sec='', footer=True, pid=None):
        PAGES.append(dict(body=body, cls=cls, sec=sec, footer=footer, pid=pid))

    def credit(img):
        return f'<span class="aicred">{L("AI चित्रण", "AI illustration")}</span>' if AI(img) else f'<span class="aicred own">{L("हमारी ट्रिप", "Our trip")}</span>'
    def ctag(c): return f'<span class="ctag" style="--c:{CLUSTERS[c][1]}">{E(t(CLUSTERS[c][0]))}</span>'
    def cdot(c): return f'<span class="cdot" style="background:{CLUSTERS[c][1]}"></span>'
    def facts(k):
        _, n, c, tk, tm, need, best, must = G[k]
        lab = [L('टिकट', 'Ticket'), L('समय', 'Timing'), L('कितना समय', 'Time needed'), L('सबसे अच्छा', 'Best time')]
        return '<div class="facts">' + ''.join(f'<div><b>{a}</b><span>{E(t(v))}</span></div>' for a, v in zip(lab, (tk, tm, need, best))) + '</div>'
    def qrbox(k, small=False):
        return f'<a class="qr{" sm" if small else ""}" href="{maps_url(k)}"><img src="{qr(maps_url(k))}"><span>{L("स्कैन करें<br>Maps", "Scan / tap<br>Maps")}</span></a>'
    def see_row(k):
        P = PLACES[k]
        if 'see' not in P: return ''
        return f'<div class="see"><b>{L("क्या देखें", "See")}</b>' + ''.join(f'<span>{E(x)}</span>' for x in t(P['see'])) + '</div>'
    def card(k, img=None, h=None):
        _, n, c, *_r = G[k]; P = PLACES[k]; must = G[k][7]
        im = ''
        if img:
            im = f'<div class="cimg" style="background-image:url({IMG[img]});{"height:" + h if h else ""}">{credit(img)}</div>'
        star = f' <i class="star">★ {L("ज़रूर देखें", "MUST SEE")}</i>' if must else ''
        return f'''<section class="card">{im}<div class="chead"><h3>{E(t(n))}{star}</h3>{ctag(c)}</div>
          <p class="intro">{E(t(P["intro"]))}</p>{facts(k)}{see_row(k)}
          <div class="reach"><b>📍 {L("कैसे पहुँचें", "Getting there")}</b> {E(t(P["reach"]))}</div>
          <div class="tipqr"><div class="tip"><b>{L("प्रो टिप", "Pro tip")}:</b> {E(t(P["tip"]))}</div>{qrbox(k, True)}</div></section>'''
    def hero_place(k, hero, sides, sec, pid=None):
        _, n, c, *_r = G[k]; P = PLACES[k]
        sd = ''.join(f'<div class="sideimg" style="background-image:url({IMG[s]})">{credit(s)}</div>' for s in sides)
        hh = '' if sides else 'height:104mm'
        two = f'<div class="two"><div><h4>{L("क्या देखें", "What to see")}</h4><ul class="ticks">{"".join(f"<li>{E(x)}</li>" for x in t(P["see"]))}</ul></div><div class="sides">{sd}</div></div>' if sides else f'<div><h4>{L("क्या देखें", "What to see")}</h4><ul class="ticks cols">{"".join(f"<li>{E(x)}</li>" for x in t(P["see"]))}</ul></div>'
        page(f'''<div class="hero" style="background-image:url({IMG[hero]});{hh}">{credit(hero)}<div class="herotxt">{ctag(c)}<h2>{E(t(n))}</h2></div></div>
          <div class="pad"><p class="intro lg">{E(t(P["intro"]))}</p>{facts(k)}
          {two}
          <div class="reach"><b>📍 {L("कैसे पहुँचें", "Getting there")}</b> {E(t(P["reach"]))}</div>
          <div class="tipqr"><div class="tip"><b>{L("प्रो टिप", "Pro tip")}:</b> {E(t(P["tip"]))}</div>{qrbox(k)}</div></div>''', 'nopad', sec, pid=pid)

    # ---- cover
    page(f'''<div class="cover" style="background-image:url({IMG["couple_temple"]})">
      <div class="cv-top"><span class="brand">HOW IS TRAVELLERS LIFE</span><span class="ed">EDITION 2026</span></div>
      <div class="cv-mid"><div class="cvhi">{L("तीर्थराज", "Tirthraj")}</div><h1>{L("पुष्कर", "PUSHKAR")}</h1>
      <div class="cvsub">{L("संपूर्ण यात्रा गाइड", "Complete Travel Guide")}</div>
      <div class="cvpills"><span>{L("15 जगहें", "15 places")}</span><span>{L("टिकट और समय", "Tickets & timings")}</span><span>{L("QR मैप्स", "QR maps")}</span><span>{L("1–3 दिन प्लान", "1–3 day plans")}</span><span>{L("हर तरह के यात्री", "Every traveller")}</span></div></div>
      <div class="cv-bot"><b>{L("हमने ख़ुद घूमकर बनाया", "Made from our own trip")}</b> · {L("ब्रह्मा मंदिर और झील की फ़ोटो हमारी नवंबर 2026 यात्रा की हैं", "Brahma Temple & lake photos are from our November 2026 visit")}<br>{L("हिंदी संस्करण", "English edition")} · {L("अंतिम जाँच: नवंबर 2026", "Last checked: November 2026")}</div></div>''', 'nopad', footer=False)

    # ---- TOC (filled later)
    page('@@TOC@@', sec=L('विषय सूची', 'Contents'), pid='toc')

    # ---- why pushkar + quick facts
    page(f'''<div class="body"><div class="eyebrow">{L("नमस्ते! 🙏", "Namaste! 🙏")}</div><h2>{L("पुष्कर क्यों जाएँ?", "Why Pushkar?")}</h2>
      <p>{L("अजमेर से सिर्फ़ 15 किमी दूर, अरावली की पहाड़ियों के बीच बसा पुष्कर हिंदुओं के पाँच सबसे पवित्र तीर्थों में गिना जाता है। यहाँ ब्रह्मा जी का प्रसिद्ध मंदिर, पवित्र झील के 52 घाट, पहाड़ियों पर मंदिर, रंगीन बाज़ार और कार्तिक का विश्व-प्रसिद्ध ऊँट मेला — सब एक छोटे-से, पैदल घूमने लायक कस्बे में है।",
        "Just 15 km from Ajmer and tucked into the Aravalli hills, Pushkar counts among the five holiest Hindu pilgrimage sites. The famous Brahma temple, 52 ghats on a sacred lake, hilltop temples, colourful bazaars and the world-famous Kartik camel fair all sit in one small, walkable town.")}</p>
      <div class="qf">
        <div><b>📍</b><span>{L("ज़िला", "District")}</span>{L("अजमेर, राजस्थान", "Ajmer, Rajasthan")}</div>
        <div><b>🗣️</b><span>{L("भाषा", "Language")}</span>{L("हिंदी, राजस्थानी, अंग्रेज़ी", "Hindi, Rajasthani, English")}</div>
        <div><b>🌡️</b><span>{L("सबसे अच्छा मौसम", "Best season")}</span>{L("अक्टूबर–मार्च", "October–March")}</div>
        <div><b>🐪</b><span>{L("ऊँट मेला", "Camel fair")}</span>{L("कार्तिक (अक्टू–नवं)", "Kartik (Oct–Nov)")}</div>
        <div><b>🥗</b><span>{L("खाना", "Food")}</span>{L("पूरी तरह शाकाहारी", "Fully vegetarian")}</div>
        <div><b>🚶</b><span>{L("घूमना", "Getting around")}</span>{L("पैदल + ई-रिक्शा", "On foot + e-rickshaw")}</div></div>
      <div class="callout"><div class="cbig">{L("पवित्र<br>नगरी", "HOLY<br>TOWN")}</div><div><b>{L("ज़रूरी नियम:", "House rules:")}</b> {L("पुष्कर में माँस, अंडा और शराब पर रोक है। घाट और मंदिर में जूते बाहर, कंधे-घुटने ढके कपड़े। सार्वजनिक जगहों पर प्यार का दिखावा (PDA) अच्छा नहीं माना जाता।",
        "Meat, eggs and alcohol are banned in Pushkar. Shoes off at ghats and temples; cover shoulders and knees. Public displays of affection are frowned upon.")}</div></div>
      <div class="photo2"><div style="background-image:url({IMG["ai_lake_sunset"]})">{credit("ai_lake_sunset")}</div><div style="background-image:url({IMG["temple_wide"]})">{credit("temple_wide")}</div></div></div>''',
         sec=L('परिचय', 'Intro'), pid='why')

    # ---- cheat sheet
    rows = ''.join(f'<tr><td>{cdot(c)}<a href="{maps_url(k)}">{E(t(n))}</a>{" <i class=star>★</i>" if must else ""}</td><td>{E(t(tk))}</td><td>{E(t(tm))}</td><td>{E(t(need))}</td><td>{E(t(best))}</td></tr>'
                   for (k, n, c, tk, tm, need, best, must) in GLANCE)
    legend = ''.join(f'<span>{cdot(c)}{E(t(n))}</span>' for c, (n, _) in CLUSTERS.items())
    page(f'''<div class="body"><div class="eyebrow">{L("स्क्रीनशॉट ले लीजिए 📸", "Screenshot this 📸")}</div><h2>{L("पुष्कर एक नज़र में", "Pushkar at a glance")}</h2><div class="legend">{legend}</div>
      <table class="gl glc"><thead><tr><th>{L("जगह", "Place")}</th><th>{L("टिकट", "Ticket")}</th><th>{L("समय*", "Timing*")}</th><th>{L("कितना समय", "Time")}</th><th>{L("सबसे अच्छा", "Best")}</th></tr></thead><tbody>{rows}</tbody></table>
      <p class="note">{L("*समय अनुमानित हैं; त्योहार और ग्रहण पर बदलते हैं। जगह के नाम पर टैप करें — Google Maps खुलेगा।", "*Timings are approximate and change on festivals and eclipses. Tap a place name to open Google Maps.")}</p></div>''',
         sec=L('एक नज़र में', 'At a glance'), pid='glance')

    # ---- map
    svg = '<svg viewBox="0 0 500 520" class="map" xmlns="http://www.w3.org/2000/svg" font-family="Poppins, Hind">'
    svg += '<ellipse cx="250" cy="250" rx="120" ry="70" fill="#9ED3DE" stroke="#1F7A8C" stroke-width="3"/>'
    svg += f'<text x="250" y="256" text-anchor="middle" font-size="17" font-weight="700" fill="#14505C">{E(L("पुष्कर झील", "PUSHKAR LAKE"))}</text>'
    def pin(x, y, c, label, sub=''):
        col = CLUSTERS[c][1]
        s = f'<circle cx="{x}" cy="{y}" r="9" fill="{col}" stroke="#fff" stroke-width="3"/><text x="{x}" y="{y - 16}" text-anchor="middle" font-size="13" font-weight="700" fill="#1E1A2B">{E(label)}</text>'
        if sub: s += f'<text x="{x}" y="{y + 26}" text-anchor="middle" font-size="11" fill="#5E5870">{E(sub)}</text>'
        return s
    svg += '<path d="M40 470 C120 420 160 380 140 330" stroke="#C9B9D9" stroke-width="3" fill="none" stroke-dasharray="6 6"/>'
    svg += pin(120, 270, 'T', L('ब्रह्मा मंदिर', 'Brahma Temple'), L('पश्चिमी किनारा', 'west shore'))
    svg += pin(200, 345, 'L', L('वराह घाट', 'Varaha Ghat'))
    svg += pin(300, 345, 'L', L('गऊ घाट', 'Gau Ghat'))
    svg += pin(370, 300, 'L', L('मान महल', 'Man Mahal'))
    svg += pin(250, 400, 'M', L('सदर बाज़ार', 'Sadar Bazaar'))
    svg += pin(165, 395, 'T', L('रंगजी', 'Rangji'))
    svg += pin(80, 120, 'H', L('सावित्री मंदिर', 'Savitri Temple'), L('पहाड़ी + रोपवे', 'hill + ropeway'))
    svg += pin(420, 150, 'H', L('गायत्री मंदिर', 'Gayatri Temple'), L('पहाड़ी', 'hill'))
    svg += pin(60, 430, 'D', L('मेला ग्राउंड', 'Fair ground'))
    svg += pin(440, 460, 'X', L('अजमेर →', 'Ajmer →'), '15 km')
    svg += pin(250, 490, 'D', L('डेज़र्ट कैंप ↓', 'Desert camps ↓'))
    svg += '</svg>'
    page(f'''<div class="body"><div class="eyebrow">{L("छोटा कस्बा, सब पास-पास", "Small town, all close")}</div><h2>{L("पुष्कर का नक्शा", "Pushkar map")}</h2>
      <p>{L("ज़्यादातर जगहें झील के चारों ओर 1–2 किमी में हैं। पहाड़ी मंदिर और डेज़र्ट कैंप ही थोड़े दूर हैं।", "Most sights sit within 1–2 km of the lake. Only the hill temples and desert camps are a little further.")}</p>{svg}
      <p class="note">{L("सरल चित्र है, स्केल पर नहीं। असली रास्ते के लिए हर जगह का QR स्कैन करें।", "A simple diagram, not to scale. Scan each place's QR for real directions.")}</p></div>''', sec=L('नक्शा', 'Map'), pid='map')

    # ---- places
    hero_place('brahma', 'temple_wide', ['temple_gate', 'temple_inside'], L('मंदिर', 'Temples'), pid='places')
    hero_place('lake', 'ai_lake_sunset', ['lake_petals', 'ghat_covered'], L('झील और घाट', 'Lake & Ghats'))
    page(f'<div class="body">{card("varaha_ghat", "ai_aarti", "54mm")}{card("gau_ghat")}</div>', sec=L('झील और घाट', 'Lake & Ghats'))
    hero_place('savitri', 'ai_savitri', [], L('पहाड़ी मंदिर', 'Hill Temples'))
    page(f'<div class="body">{card("gayatri")}{card("rangji", "temple_gate", "42mm")}</div>', sec=L('मंदिर', 'Temples'))
    page(f'<div class="body">{card("varaha_temple")}{card("aptaeshwar")}<div class="photo2"><div style="background-image:url({IMG["corridor"]})">{credit("corridor")}</div><div style="background-image:url({IMG["temple_inside"]})">{credit("temple_inside")}</div></div></div>', sec=L('मंदिर', 'Temples'))
    page(f'''<div class="body">{card("manmahal")}
      <div class="callout pink"><div class="cbig">{L("स्कैम<br>अलर्ट", "SCAM<br>ALERT")}</div><div><b>{L("“पुष्कर पासपोर्ट” स्कैम:", "The “Pushkar passport” scam:")}</b> {L("घाट पर कोई “पंडित” हाथ में फूल देकर आपके परिवार के नाम पर पूजा करवाएगा और फिर ₹500–5000 “दक्षिणा” माँगेगा। फूल लेने से पहले ही विनम्रता से मना कर दें। पूजा करवानी हो तो मंदिर के काउंटर से रसीद वाली पूजा करवाएँ।",
        "On the ghats a ‘priest’ hands you flowers, performs a prayer for your family and then demands ₹500–5000. Politely refuse before taking the flowers. If you want a puja, book a receipted one at a temple counter.")}</div></div></div>''', sec=L('मंदिर', 'Temples'))
    hero_place('bazaar', 'ai_bazaar', ['corridor'], L('बाज़ार', 'Bazaar'))
    hero_place('desert', 'ai_desert', [], L('रेगिस्तान', 'Desert'))
    hero_place('fair', 'ai_camelfair', [], L('ऊँट मेला', 'Camel Fair'))
    page(f'''<div class="body"><div class="eyebrow">{L("एक दिन और है?", "One more day?")}</div><h2>{L("अजमेर डे-ट्रिप", "Ajmer day trip")}</h2>{card("ajmer")}{card("anasagar")}
      <div class="callout"><div class="cbig">{L("अजमेर<br>प्लान", "AJMER<br>PLAN")}</div><div>{L("सुबह 8 बजे पुष्कर से निकलें → 8:45 दरगाह शरीफ़ → 10:30 अढ़ाई दिन का झोंपड़ा (पैदल 10 मिनट) → 12:30 लंच → 4 बजे आना सागर → शाम 6 बजे वापस पुष्कर।", "Leave Pushkar at 8 AM → 8:45 Dargah Sharif → 10:30 Adhai Din Ka Jhonpra (10-min walk) → 12:30 lunch → 4 PM Ana Sagar → back in Pushkar by 6 PM.")}</div></div>
      <p class="note">{L("अजमेर में और: अढ़ाई दिन का झोंपड़ा, तारागढ़ क़िला, सोनीजी की नसियाँ (जैन मंदिर)।", "More in Ajmer: Adhai Din Ka Jhonpra, Taragarh Fort, Soniji Ki Nasiyan (Jain temple).")}</p></div>''', sec=L('आस-पास', 'Nearby'))

    # ---- traveller types
    tp = ''.join(f'<div class="tt"><div class="tth"><span>{em}</span><b>{E(t(n))}</b></div><ul class="ticks">{"".join(f"<li>{E(x)}</li>" for x in t(tips))}</ul></div>' for n, em, tips in TYPES)
    page(f'''<div class="body"><div class="eyebrow">{L("आप किस तरह के यात्री हैं?", "What kind of traveller are you?")}</div><h2>{L("हर यात्री के लिए टिप्स", "Tips for every traveller")}</h2><div class="types">{tp}</div></div>''',
         sec=L('यात्री गाइड', 'Traveller guide'), pid='types')

    # ---- itineraries
    def tl(rows): return '<div class="tl">' + ''.join(f'<div class="tli"><span class="tt2">{E(a)}</span><span class="td">{E(b)}</span></div>' for a, b in rows) + '</div>'
    page(f'''<div class="body"><div class="eyebrow">{L("रेडी-मेड प्लान", "Ready-made plan")}</div><h2>{L("1 दिन में पुष्कर", "Pushkar in 1 day")}</h2>
      {tl([('5:45 AM', L('सावित्री मंदिर — सूर्योदय (रोपवे/सीढ़ियाँ)', 'Savitri Temple at sunrise (ropeway or steps)')), ('7:30', L('ब्रह्मा मंदिर दर्शन ★ (फ़ोन बाहर जमा)', 'Brahma Temple darshan ★ (deposit phone)')),
          ('8:30', L('नाश्ता — मालपुआ, कचौरी, लस्सी', 'Breakfast: malpua, kachori, lassi')), ('9:30–12', L('घाट परिक्रमा: गऊ घाट, ब्रह्मा घाट', 'Ghat walk: Gau Ghat, Brahma Ghat')),
          ('12–3 PM', L('लंच + आराम (मंदिर 1:30–3 बंद)', 'Lunch + rest (temples close 1:30–3)')), ('3–5', L('रंगजी मंदिर + सदर बाज़ार शॉपिंग', 'Rangji Temple + Sadar Bazaar shopping')),
          ('5:30–7', L('वराह घाट पर सूर्यास्त आरती ★', 'Sunset aarti at Varaha Ghat ★')), ('7:30 PM', L('छत वाले कैफ़े पर डिनर', 'Dinner at a rooftop café'))])}</div>''', sec=L('प्लान', 'Itinerary'), pid='plans')
    page(f'''<div class="body"><div class="eyebrow">{L("आराम से घूमना है?", "Taking it slow?")}</div><h2>{L("2 और 3 दिन के प्लान", "2- and 3-day plans")}</h2>
      <div class="days"><div><span class="dn" style="background:#C0392B">{L("दिन 1", "Day 1")}</span><b>{L("मंदिर और घाट", "Temples & ghats")}</b>{L("ब्रह्मा मंदिर → आप्तेश्वर → घाट परिक्रमा → रंगजी → वराह मंदिर → वराह घाट आरती", "Brahma Temple → Aptaeshwar → ghat walk → Rangji → Varaha Temple → Varaha Ghat aarti")}</div>
      <div><span class="dn" style="background:#7B4BA8">{L("दिन 2", "Day 2")}</span><b>{L("पहाड़ी + रेगिस्तान", "Hills + desert")}</b>{L("सावित्री मंदिर सूर्योदय → नाश्ता → बाज़ार → मान महल → दोपहर आराम → डेज़र्ट कैंप: ऊँट सफ़ारी, सूर्यास्त, डिनर", "Savitri sunrise → breakfast → bazaar → Man Mahal → afternoon rest → desert camp: camel safari, sunset, dinner")}</div>
      <div><span class="dn" style="background:#4F7A28">{L("दिन 3", "Day 3")}</span><b>{L("अजमेर", "Ajmer")}</b>{L("गायत्री मंदिर सूर्योदय → अजमेर: दरगाह शरीफ़ → अढ़ाई दिन का झोंपड़ा → आना सागर पर शाम", "Gayatri sunrise → Ajmer: Dargah Sharif → Adhai Din Ka Jhonpra → evening at Ana Sagar")}</div></div>
      <div class="photo2"><div style="background-image:url({IMG["family_temple"]})">{credit("family_temple")}</div><div style="background-image:url({IMG["ai_desert"]})">{credit("ai_desert")}</div></div></div>''', sec=L('प्लान', 'Itinerary'))

    # ---- reach + stay
    page(f'''<div class="body"><div class="eyebrow">{L("शुरुआत", "Getting started")}</div><h2>{L("पुष्कर कैसे पहुँचें", "How to reach Pushkar")}</h2>
      <div class="grid3"><div><b>✈️ {L("फ़्लाइट", "Flight")}</b>{L("नज़दीकी: किशनगढ़ एयरपोर्ट (~40 किमी, 1 घंटा)। ज़्यादा फ़्लाइट: जयपुर एयरपोर्ट (~145 किमी, 3 घंटे)।", "Nearest: Kishangarh Airport (~40 km, 1 hr). More flights: Jaipur Airport (~145 km, 3 hr).")}</div>
      <div><b>🚆 {L("ट्रेन", "Train")}</b>{L("अजमेर जंक्शन (15 किमी) — दिल्ली, जयपुर, मुंबई से सीधी ट्रेनें। पुष्कर स्टेशन पर बहुत कम ट्रेनें।", "Ajmer Junction (15 km) has direct trains from Delhi, Jaipur and Mumbai. Pushkar station has very few trains.")}</div>
      <div><b>🚌 {L("बस / कार", "Bus / car")}</b>{L("अजमेर से हर 15–20 मिनट बस (₹30–40)। जयपुर से 3 घंटे (NH-48)। टैक्सी अजमेर से ₹400–600।", "Buses from Ajmer every 15–20 min (₹30–40). 3 hours from Jaipur (NH-48). Taxi from Ajmer ₹400–600.")}</div></div>
      <h2 class="mt">{L("कहाँ रुकें", "Where to stay")}</h2><table class="gl"><thead><tr><th>{L("प्रकार", "Type")}</th><th>{L("कहाँ", "Where")}</th><th>{L("लगभग/रात", "Approx/night")}</th></tr></thead><tbody>
      <tr><td><b>{L("हॉस्टल / गेस्टहाउस", "Hostel / guesthouse")}</b></td><td>{L("ब्रह्मा मंदिर रोड, बाज़ार", "Brahma Temple Rd, bazaar")}</td><td>₹400–1,500</td></tr>
      <tr><td><b>{L("धर्मशाला", "Dharamshala")}</b></td><td>{L("घाटों के पास", "Near the ghats")}</td><td>₹300–1,000</td></tr>
      <tr><td><b>{L("हेरिटेज हवेली", "Heritage haveli")}</b></td><td>{L("झील किनारे / पुराना कस्बा", "Lakeside / old town")}</td><td>₹2,000–6,000</td></tr>
      <tr><td><b>{L("लग्ज़री रिसॉर्ट", "Luxury resort")}</b></td><td>{L("कस्बे के बाहर, अरावली की ओर", "Outskirts, towards the Aravallis")}</td><td>₹8,000+</td></tr>
      <tr><td><b>{L("डेज़र्ट कैंप / टेंट", "Desert camp / tent")}</b></td><td>{L("रेत के टीले, 3–8 किमी", "Dunes, 3–8 km out")}</td><td>₹2,500–10,000</td></tr></tbody></table>
      <p class="note">{L("ऊँट मेले के दिनों में दाम 2–3 गुना। सभी दाम अनुमानित हैं।", "Prices rise 2–3× during the camel fair. All prices are estimates.")}</p></div>''', sec=L('पहुँचें और रुकें', 'Reach & stay'), pid='reach')

    drows = ''.join(f'<tr><td>{E(t(a))} → {E(t(b))}</td><td>{d}</td><td>{E(t(tm))}</td><td>{E(t(m))}</td></tr>' for a, b, d, tm, m in DISTANCES)
    page(f'''<div class="body"><div class="eyebrow">{L("रूट प्लानर", "Route planner")}</div><h2>{L("दूरी और समय", "Distances & time")}</h2>
      <table class="gl"><thead><tr><th>{L("कहाँ से → कहाँ", "From → to")}</th><th>{L("दूरी", "Distance")}</th><th>{L("समय", "Time")}</th><th>{L("कैसे", "How")}</th></tr></thead><tbody>{drows}</tbody></table>
      <h4 class="mt">{L("पुष्कर में घूमना", "Getting around Pushkar")}</h4><ul class="ticks">
      <li>{L("कस्बा छोटा है — ज़्यादातर पैदल। बाज़ार और घाट की गलियों में गाड़ी नहीं जाती।", "The town is small and mostly walkable; cars can't enter the bazaar and ghat lanes.")}</li>
      <li>{L("ई-रिक्शा: ₹20–50 छोटा सफ़र — बैठने से पहले किराया तय करें।", "E-rickshaw: ₹20–50 for short hops — agree the fare first.")}</li>
      <li>{L("स्कूटी किराया: ₹300–500/दिन, ड्राइविंग लाइसेंस साथ रखें।", "Scooter rental: ₹300–500/day; carry your licence.")}</li>
      <li>{L("अपनी कार: बाहर की पार्किंग (बस स्टैंड / मेला ग्राउंड के पास) में लगाएँ।", "Own car: use outer parking near the bus stand or fairground.")}</li></ul></div>''', sec=L('रूट', 'Routes'))

    # ---- food & shopping
    page(f'''<div class="body"><div class="eyebrow">{L("शुद्ध शाकाहारी स्वाद", "Pure veg flavours")}</div><h2>{L("क्या खाएँ", "What to eat")}</h2>
      <div class="photo1" style="background-image:url({IMG["ai_food"]})">{credit("ai_food")}</div>
      <table class="gl"><thead><tr><th>{L("क्या", "Dish")}</th><th>{L("ख़ासियत", "Why try it")}</th></tr></thead><tbody>
      <tr><td><b>{L("मालपुआ और रबड़ी", "Malpua & rabri")}</b></td><td>{L("पुष्कर की सबसे मशहूर मिठाई — बाज़ार की पुरानी हलवाई दुकानों पर गरम।", "Pushkar's signature sweet — hot from the old sweet shops in the bazaar.")}</td></tr>
      <tr><td><b>{L("कचौरी, समोसा", "Kachori, samosa")}</b></td><td>{L("सुबह का नाश्ता, चाय के साथ।", "Breakfast with chai.")}</td></tr>
      <tr><td><b>{L("कुल्हड़ लस्सी", "Kulhad lassi")}</b></td><td>{L("गाढ़ी, मलाई वाली — गर्मी में सबसे अच्छी।", "Thick and creamy — best on a hot day.")}</td></tr>
      <tr><td><b>{L("राजस्थानी थाली", "Rajasthani thali")}</b></td><td>{L("दाल-बाटी-चूरमा, गट्टे, केर-सांगरी — ₹150–300।", "Dal-baati-churma, gatte, ker-sangri — ₹150–300.")}</td></tr>
      <tr><td><b>{L("कैफ़े फ़ूड", "Café food")}</b></td><td>{L("इज़रायली, इटालियन, फ़लाफ़ेल — विदेशी यात्रियों की वजह से बहुत लोकप्रिय (सब शाकाहारी)।", "Israeli, Italian, falafel — popular thanks to foreign travellers (all vegetarian).")}</td></tr></tbody></table>
      <h2 class="mt">{L("क्या ख़रीदें", "What to buy")}</h2><div class="checks">
      <span>{L("चाँदी के गहने", "Silver jewellery")}</span><span>{L("गुलकंद, गुलाब जल", "Gulkand, rose water")}</span><span>{L("चमड़े के बैग", "Leather bags")}</span><span>{L("बंधेज/हिप्पी कपड़े", "Bandhej / boho clothes")}</span><span>{L("पीतल की मूर्तियाँ", "Brass idols")}</span><span>{L("रंगीन जूतियाँ", "Mojaris")}</span></div></div>''',
         sec=L('खाना और शॉपिंग', 'Food & shopping'), pid='food')

    # ---- season & festivals
    page(f'''<div class="body"><div class="eyebrow">{L("कब जाएँ", "When to go")}</div><h2>{L("मौसम और त्योहार", "Seasons & festivals")}</h2>
      <div class="season"><div class="s1"><b>{L("अक्टू–मार्च", "Oct–Mar")}</b>{L("सबसे अच्छा। दिन सुहाना, रातें ठंडी (दिसं–जन 5°C तक)।", "Best. Pleasant days, cold nights (down to 5°C in Dec–Jan).")}</div>
      <div class="s2"><b>{L("अप्रैल–जून", "Apr–Jun")}</b>{L("बहुत गर्मी (40°C+)। सिर्फ़ सुबह-शाम घूमें।", "Very hot (40°C+). Sightsee only early and late.")}</div>
      <div class="s3"><b>{L("जुलाई–सितं", "Jul–Sep")}</b>{L("मानसून, झील भरी और पहाड़ हरे। भीड़ कम।", "Monsoon: full lake, green hills, fewer crowds.")}</div></div>
      <table class="gl"><thead><tr><th>{L("त्योहार", "Festival")}</th><th>{L("कब", "When")}</th><th>{L("क्या ख़ास", "Highlight")}</th></tr></thead><tbody>
      <tr><td><b>{L("पुष्कर ऊँट मेला", "Pushkar Camel Fair")}</b></td><td>{L("कार्तिक, अक्टू–नवं", "Kartik, Oct–Nov")}</td><td>{L("ऊँट, बैलून, लोक संगीत", "Camels, balloons, folk music")}</td></tr>
      <tr><td><b>{L("कार्तिक पूर्णिमा", "Kartik Purnima")}</b></td><td>{L("मेले का आख़िरी दिन", "Last day of the fair")}</td><td>{L("पवित्र स्नान, दीपदान", "Holy dip, floating lamps")}</td></tr>
      <tr><td><b>{L("होली", "Holi")}</b></td><td>{L("मार्च", "March")}</td><td>{L("पूरा कस्बा रंगों में — बहुत भीड़", "The whole town in colour — very crowded")}</td></tr>
      <tr><td><b>{L("दीवाली", "Diwali")}</b></td><td>{L("अक्टू–नवं", "Oct–Nov")}</td><td>{L("घाट दीयों से रोशन", "Ghats lit with lamps")}</td></tr></tbody></table>
      <div class="photo1 s" style="background-image:url({IMG["ai_camelfair"]})">{credit("ai_camelfair")}</div>
      <p class="note">{L("मेले की सही तारीख़ें हर साल हिंदू पंचांग से तय होती हैं — Rajasthan Tourism की वेबसाइट देखें।", "Fair dates follow the Hindu calendar each year — check the Rajasthan Tourism website.")}</p></div>''', sec=L('मौसम', 'Season'), pid='season')

    # ---- budget
    page(f'''<div class="body"><div class="eyebrow">{L("कितना ख़र्च", "How much")}</div><h2>{L("बजट (प्रति व्यक्ति, प्रति दिन)", "Budget (per person, per day)")}</h2>
      <div class="budget"><div><span>{L("बैकपैकर", "Backpacker")}</span><b>₹1,000–1,800</b>{L("हॉस्टल, थाली, पैदल, ज़्यादातर मंदिर निःशुल्क", "Hostel, thali, walking, most temples free")}</div>
      <div class="mid"><span>{L("कम्फ़र्ट", "Comfort")}</span><b>₹2,500–4,500</b>{L("हवेली होटल, कैफ़े, रोपवे, सफ़ारी", "Haveli hotel, cafés, ropeway, safari")}</div>
      <div><span>{L("लग्ज़री", "Luxury")}</span><b>₹8,000+</b>{L("रिसॉर्ट, निजी कार, डेज़र्ट डिनर", "Resort, private car, desert dinner")}</div></div>
      <h4 class="mt">{L("2 दिन का अनुमानित ख़र्च (2 लोग, कम्फ़र्ट)", "Sample 2-day cost (2 people, comfort)")}</h4>
      <table class="gl"><tbody>
      <tr><td>{L("होटल (1 रात)", "Hotel (1 night)")}</td><td>₹3,000</td></tr><tr><td>{L("खाना (2 दिन)", "Food (2 days)")}</td><td>₹2,000</td></tr>
      <tr><td>{L("रोपवे (2 लोग)", "Ropeway (2 people)")}</td><td>₹400–600</td></tr><tr><td>{L("डेज़र्ट कैंप / सफ़ारी", "Desert camp / safari")}</td><td>₹2,500–4,000</td></tr>
      <tr><td>{L("लोकल ट्रांसपोर्ट", "Local transport")}</td><td>₹500</td></tr><tr><td><b>{L("कुल (लगभग)", "Total (approx)")}</b></td><td><b>₹8,400–10,100</b></td></tr></tbody></table>
      <p class="note">{L("अजमेर/जयपुर से आने-जाने का किराया और शॉपिंग अलग। सभी आँकड़े अनुमानित हैं।", "Travel to and from Ajmer or Jaipur and shopping are extra. All figures are estimates.")}</p></div>''', sec=L('बजट', 'Budget'), pid='budget')

    # ---- safety & etiquette
    page(f'''<div class="body"><div class="eyebrow">{L("स्मार्ट यात्री बनिए", "Travel smart")}</div><h2>{L("सुरक्षा, शिष्टाचार और स्कैम", "Safety, etiquette & scams")}</h2>
      <div class="scams">
      <div><b>🌸 {L("फूल-पूजा स्कैम", "Flower-puja scam")}</b>{L("घाट पर फूल न लें, “पूजा” के बाद मोटी दक्षिणा माँगते हैं।", "Don't accept flowers on the ghats; a big ‘donation’ demand follows.")}</div>
      <div><b>📵 {L("फ़ोटो नियम", "Photo rules")}</b>{L("नहाते लोग और कई घाट — फ़ोटो मना। मंदिर के अंदर कैमरा नहीं।", "No photos of bathers or at many ghats. No cameras inside temples.")}</div>
      <div><b>🐒 {L("बंदर और गाय", "Monkeys & cows")}</b>{L("पहाड़ी मंदिरों पर खाना छिपाकर रखें। गलियों में गायों से दूरी।", "Hide food on the hill temples; give cows space in the lanes.")}</div>
      <div><b>🐪 {L("ऊँट सफ़ारी", "Camel rides")}</b>{L("रेट और समय पहले तय करें, बीच में दाम बढ़ाने न दें।", "Fix price and duration upfront; don't allow mid-ride increases.")}</div>
      <div><b>🍵 {L("भांग लस्सी", "Bhang lassi")}</b>{L("कई दुकानें खुलेआम बेचती हैं — असर तेज़ और देर तक; बचें।", "Openly sold in some shops — strong and long-lasting; avoid it.")}</div>
      <div><b>👗 {L("कपड़े", "Dress")}</b>{L("मंदिर और घाट पर कंधे-घुटने ढकें, जूते बाहर।", "Cover shoulders and knees at temples and ghats; shoes off.")}</div></div>
      <h4 class="mt">{L("ज़रूरी नंबर", "Useful numbers")}</h4>
      <div class="nums"><div><b>112</b>{L("आपातकाल", "Emergency")}</div><div><b>108</b>{L("एम्बुलेंस", "Ambulance")}</div><div><b>1363</b>{L("टूरिस्ट हेल्पलाइन", "Tourist helpline")}</div><div><b>181</b>{L("महिला हेल्पलाइन", "Women helpline")}</div></div>
      <h4 class="mt">{L("पैकिंग चेकलिस्ट ✅", "Packing checklist ✅")}</h4><div class="checks"><span>{L("आरामदायक चप्पल (बार-बार उतारनी)", "Easy slip-on shoes")}</span><span>{L("दुपट्टा / स्टोल", "Scarf / stole")}</span><span>{L("पानी की बोतल", "Water bottle")}</span><span>{L("सनस्क्रीन, टोपी", "Sunscreen, cap")}</span><span>{L("टॉर्च (सूर्योदय)", "Torch (sunrise)")}</span><span>{L("नक़द (छोटी दुकानें)", "Cash (small shops)")}</span><span>{L("सर्दी में जैकेट", "Winter jacket")}</span><span>{L("फ़ोटो ID", "Photo ID")}</span></div></div>''',
         sec=L('सुरक्षा', 'Safety'), pid='safety')

    # ---- sources
    srcs = [('Rajasthan Tourism — Pushkar', 'https://www.tourism.rajasthan.gov.in/pushkar.html'), ('Rajasthan Tourism — Pushkar Fair', 'https://www.tourism.rajasthan.gov.in/pushkar-fair.html'),
            ('Rajasthan Tourism — Ajmer', 'https://www.tourism.rajasthan.gov.in/ajmer.html'), ('Indian Railways — enquiry', 'https://enquiry.indianrail.gov.in/'), ('RSRTC bus booking', 'https://rsrtconline.rajasthan.gov.in/')]
    sl = ''.join(f'<li><a href="{u}">{E(n)}</a></li>' for n, u in srcs)
    page(f'''<div class="body"><div class="eyebrow">{L("भरोसा", "Trust")}</div><h2>{L("स्रोत और ज़रूरी सूचना", "Sources & disclaimer")}</h2>
      <p>{L("जानकारी Rajasthan Tourism, सरकारी पोर्टल और हमारी नवंबर 2026 की पुष्कर यात्रा से ली गई है।", "Information comes from Rajasthan Tourism, government portals and our own November 2026 trip to Pushkar.")}</p><ul class="src">{sl}</ul>
      <div class="callout soft"><div><b>{L("ध्यान दें:", "Please note:")}</b> {L("यह एक स्वतंत्र यात्रा गाइड है, सरकारी प्रकाशन नहीं। टिकट, समय और रास्ते बिना सूचना बदल सकते हैं। जाने वाले दिन एक बार पुष्टि कर लें।", "This is an independent travel guide, not a government publication. Fares, timings and routes can change without notice; confirm on the day you travel.")}<br><br>
      <b>{L("फ़ोटो:", "Photos:")}</b> {L("“हमारी ट्रिप” लेबल वाली फ़ोटो हमारी असली यात्रा की हैं। “AI चित्रण” लेबल वाली तस्वीरें AI से बनी हैं, जगह का अंदाज़ा देने के लिए — असली दृश्य थोड़ा अलग हो सकता है।", "Images labelled ‘Our trip’ are from our real visit. Images labelled ‘AI illustration’ are AI-generated to give a feel for the place; the real view may differ.")}<br><br><b>{L("अंतिम जाँच:", "Last checked:")}</b> {L("नवंबर 2026", "November 2026")}</div></div></div>''', sec=L('स्रोत', 'Sources'), pid='sources')

    # ---- back cover
    page(f'''<div class="cover back" style="background-image:url({IMG["ai_aarti"]})"><div class="bk">
      <div class="cvhi">{L("धन्यवाद!", "Thank you!")}</div><h1 class="bkh">{L("पुष्कर की यात्रा शुभ हो!", "Have a blessed Pushkar trip!")}</h1>
      <p>{L("गाइड पसंद आई? रील को <b>सेव</b> करें, दोस्तों के साथ <b>शेयर</b> करें और ऐसी ही गाइड्स के लिए फ़ॉलो करें:", "Liked the guide? <b>Save</b> the reel, <b>share</b> it with friends and follow for more guides:")}</p>
      <div class="bkbrand">HOW IS TRAVELLERS LIFE</div><div class="bksub">@howistravellerslife · Instagram</div>
      <div class="bkcta"><span>{L("अगली गाइड कहाँ की चाहिए? कमेंट में बताइए 👇", "Which guide next? Tell us in the comments 👇")}</span></div>
      <div class="bkcredit">{L("कवर: ब्रह्मा मंदिर, नवंबर 2026 — How Is Travellers Life · पीछे का चित्र: AI चित्रण", "Cover: Brahma Temple, November 2026 — How Is Travellers Life · Back image: AI illustration")}</div></div></div>''', 'nopad', footer=False)

    # ---- page ids + TOC
    for i, p in enumerate(PAGES, 1):
        if not p['pid']: p['pid'] = f'p{i}'
    first = {}
    for i, p in enumerate(PAGES, 1): first.setdefault(p['pid'], i)
    toc = [('why', L('पुष्कर क्यों जाएँ + ज़रूरी नियम', 'Why Pushkar + house rules')), ('glance', L('पुष्कर एक नज़र में (चीट शीट)', 'Pushkar at a glance (cheat sheet)')),
           ('map', L('पुष्कर का नक्शा', 'Pushkar map')), ('places', L('घूमने की 15 जगहें', '15 places to visit')), ('types', L('हर यात्री के लिए टिप्स', 'Tips for every traveller')),
           ('plans', L('1, 2, 3 दिन के प्लान', '1-, 2- and 3-day plans')), ('reach', L('कैसे पहुँचें + कहाँ रुकें + दूरी', 'Getting there, stays & distances')), ('food', L('खाना और शॉपिंग', 'Food & shopping')),
           ('season', L('मौसम, त्योहार और ऊँट मेला', 'Seasons, festivals & camel fair')), ('budget', L('बजट', 'Budget')), ('safety', L('सुरक्षा, स्कैम और पैकिंग', 'Safety, scams & packing')), ('sources', L('स्रोत', 'Sources'))]
    pnum = {p['pid']: i + off for i, p in enumerate(PAGES, 1)}
    tocl = ''.join(f'<li><a href="#{pid}"><span>{E(name)}</span><i></i><b>{pnum[pid]}</b></a></li>' for pid, name in toc)
    sub = ''.join(f'<a href="#{PAGES[i - 1]["pid"]}"><span>{E(t(n))}</span><b>{i + off}</b></a>' for k, n, *_r in GLANCE for i in [next((j for j, p in enumerate(PAGES, 1) if E(t(n)) in p['body'] and ('<h2>' + E(t(n)) in p['body'] or '<h3>' + E(t(n)) in p['body'])), None)] if i)
    PAGES[1]['body'] = f'''<div class="body"><div class="eyebrow">{L("इस गाइड में", "In this guide")}</div><h2>{L("विषय सूची", "Contents")}</h2>
      <p class="note">{L("किसी भी लाइन पर टैप करें — सीधे उस पेज पर पहुँचेंगे।", "Tap any line to jump straight to that page.")}</p><ol class="toc">{tocl}</ol>
      <h4 class="mt">{L("जगहें — सीधे पेज पर जाएँ", "Places — jump to page")}</h4><div class="toc2">{sub}</div>
      <div class="howto"><div><b>📍 {L("QR स्कैन करें", "Scan the QR")}</b>{L("हर जगह के साथ QR — Google Maps खुलेगा।", "Every place has a QR that opens Google Maps.")}</div>
      <div><b>🎨 {L("रंग = इलाक़ा", "Colour = area")}</b>{L("एक रंग की जगहें साथ घूमें।", "Visit same-colour places together.")}</div>
      <div><b>★ {L("ज़रूर देखें", "Must see")}</b>{L("समय कम है? सिर्फ़ स्टार वाली जगहें।", "Short on time? Just the starred ones.")}</div></div></div>'''

    CSS = (HERE / 'style.css').read_text()
    FONT = lambda n: b64(A / 'fonts' / n, 'font/ttf')
    fonts = ''
    for fam, files in (('Poppins', [(400, 'Poppins-400'), (500, 'Poppins-500'), (600, 'Poppins-600'), (700, 'Poppins-700'), (800, 'Poppins-800')]),
                       ('Hind', [(400, 'Hind-400'), (500, 'Hind-500'), (600, 'Hind-600'), (700, 'Hind-700')]), ('Anton', [(400, 'Anton-400')]), ('Yatra', [(400, 'YatraOne-400')])):
        for w, f in files: fonts += f"@font-face{{font-family:'{fam}';font-weight:{w};src:url({FONT(f + '.ttf')}) format('truetype')}}\n"
    out = [f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>Pushkar Complete Travel Guide 2026 — हिंदी + English</title><style>', fonts, CSS, '</style></head><body class="' + lang + '">']
    for i, p in enumerate(PAGES, 1):
        foot = f'<footer><span>How Is Travellers Life · {L("पुष्कर गाइड 2026", "Pushkar Guide 2026")}</span><span>{p["sec"]}</span><a href="#home">⌂ {L("होम", "Home")}</a><a href="#toc">↑ {L("सूची", "Contents")}</a><b>{i + off}</b></footer>' if p['footer'] else ''
        out.append(f'<div class="page {lang} {p["cls"]}" id="{p["pid"]}">{p["body"]}{foot}</div>')
    import re
    divs = out[4:]
    divs = [re.sub(r'id="([\w-]+)"', lambda m: f'id="{lang}-{m.group(1)}"', d) for d in divs]
    divs = [re.sub(r'href="#(?!home)([\w-]+)"', lambda m: f'href="#{lang}-{m.group(1)}"', d) for d in divs]
    print(lang, 'pages', len(PAGES))
    return out[:3], divs, len(PAGES)

head, hi_divs, nh = make('hi', off=1)
_, en_divs, ne = make('en', off=1 + nh)
CS = head[2] + '''
.home{height:100%;position:relative;color:#fff;background-size:cover;background-position:center;display:flex;flex-direction:column;padding:10mm}
.home:before{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,14,30,.55),rgba(20,14,30,.15) 35%,rgba(20,14,30,.9))}
.home>*{position:relative}
.home h1{font-family:'Anton',sans-serif;font-weight:400;font-size:64pt;line-height:.95;color:#FFB547;margin-top:auto}
.home .hh{font-family:'Hind',sans-serif;font-weight:700;font-size:30pt;color:#FFD27A;line-height:1.1}
.home .sub{font-size:12pt;font-weight:700;margin:1mm 0 5mm}
.home .pick{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.home .pick a{display:block;background:rgba(255,255,255,.14);border:.4mm solid rgba(255,255,255,.7);border-radius:4mm;padding:4mm;color:#fff;text-decoration:none}
.home .pick a b{display:block;font-family:'Hind','Poppins',sans-serif;font-size:17pt;line-height:1.1}
.home .pick a span{font-size:8pt;opacity:.9}
.home .pick a i{display:inline-block;margin-top:2mm;background:#FFB547;color:#1E1A2B;font-style:normal;font-weight:700;font-size:8pt;padding:.8mm 3mm;border-radius:5mm}
.home .jump{margin-top:4mm;display:grid;grid-template-columns:1fr 1fr;gap:1.2mm 4mm;font-size:7.6pt}
.home .jump a{color:#fff;text-decoration:none;border-bottom:.25mm dotted rgba(255,255,255,.5);display:flex;justify-content:space-between;padding:.6mm 0}
.home .brandtop{font-size:7pt;font-weight:700;letter-spacing:.16em;background:#fff;color:#B0303A;padding:1mm 2.6mm;border-radius:5mm;align-self:flex-start}
'''
jumps = [('toc', 'विषय सूची', 'Contents'), ('glance', 'एक नज़र में', 'At a glance'), ('places', 'घूमने की जगहें', 'Places'), ('plans', 'प्लान', 'Itineraries'), ('budget', 'बजट', 'Budget'), ('safety', 'सुरक्षा', 'Safety')]
import re as _re
def pg(divs, lang, pid):
    for i, d in enumerate(divs):
        if f'id="{lang}-{pid}"' in d: return i
jl = lambda lang, base: ''.join(f'<a href="#{lang}-{p}"><span>{h if lang == "hi" else e}</span><b>{base + pg(hi_divs if lang == "hi" else en_divs, lang, p) + 1}</b></a>' for p, h, e in jumps)
home = f'''<div class="page nopad" id="home"><div class="home" style="background-image:url({IMG["ai_lake_sunset"]})">
  <span class="brandtop">HOW IS TRAVELLERS LIFE · 2026</span>
  <div class="hh">पुष्कर</div><h1>PUSHKAR</h1><div class="sub">संपूर्ण यात्रा गाइड · Complete Travel Guide</div>
  <div class="pick"><a href="#hi-toc"><b>हिंदी गाइड</b><span>पेज 2–{1 + nh}</span><br><i>यहाँ टैप करें →</i></a>
  <a href="#en-toc"><b>English Guide</b><span>Pages {2 + nh}–{1 + nh + ne}</span><br><i>Tap here →</i></a></div>
  <div class="jump"><div>{jl("hi", 1)}</div><div>{jl("en", 1 + nh)}</div></div></div></div>'''
html_out = ''.join(head[:2]) + CS + '</style></head><body>' + home + ''.join(hi_divs) + ''.join(en_divs) + '</body></html>'
(HERE / 'guide.html').write_text(html_out)
print('total pages', 1 + nh + ne)
