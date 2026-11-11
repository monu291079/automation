"""3D-style SVG illustrations (code-made, copyright free): glossy balloons, balloon arch, machine, coins, 3D bars, donut."""
import math, itertools

_uid = itertools.count(1)
PAL = {"gold": "#E2BE6A", "teal": "#2BB3AA", "coral": "#FF6B5A", "cream": "#F4F1EA", "blue": "#4C8DFF", "red": "#E5484D", "violet": "#9B6BFF", "pink": "#FF8FB8", "navy": "#1B2F52"}


def _mix(hexc, to, k):
    n = int(hexc[1:], 16)
    c = [((n >> 16) & 255), ((n >> 8) & 255), (n & 255)]
    return "rgb(%d,%d,%d)" % tuple(round(v + (to - v) * k) for v in c)


def defs_balloon(color):
    i = "g" + color[1:]
    return (f'<radialGradient id="{i}" cx="35%" cy="28%" r="80%"><stop offset="0" stop-color="{_mix(color,255,.6)}"/>'
            f'<stop offset=".4" stop-color="{color}"/><stop offset="1" stop-color="{_mix(color,0,.5)}"/></radialGradient>')


def balloon_g(cx, cy, r, color, rot=0, string=0):
    i = "g" + color[1:]
    h = r * 1.22
    s = ""
    if string:
        s = f'<path d="M0 {h*.95:.1f} C {-r*.25:.1f} {h+string*.3:.1f}, {r*.25:.1f} {h+string*.6:.1f}, 0 {h+string:.1f}" stroke="rgba(255,255,255,.65)" fill="none" stroke-width="{max(1,r*.04):.1f}"/>'
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot})">'
            f'<ellipse cx="{r*.12:.1f}" cy="{h*1.18:.1f}" rx="{r*.7:.1f}" ry="{r*.14:.1f}" fill="rgba(0,0,0,.18)" opacity="0"/>'
            f'<path d="M0 {-h} C {r*1.05:.1f} {-h}, {r*1.12:.1f} {h*.25:.1f}, {r*.1:.1f} {h*.92:.1f} L {r*.16:.1f} {h*1.04:.1f} L {-r*.16:.1f} {h*1.04:.1f} L {-r*.1:.1f} {h*.92:.1f} C {-r*1.12:.1f} {h*.25:.1f}, {-r*1.05:.1f} {-h}, 0 {-h} Z" fill="url(#{i})"/>'
            f'<path d="M{-r*.16:.1f} {h*1.04:.1f} L {r*.16:.1f} {h*1.04:.1f} L 0 {h*1.16:.1f} Z" fill="{_mix(color,0,.45)}"/>'
            f'<ellipse cx="{-r*.42:.1f}" cy="{-h*.42:.1f}" rx="{r*.17:.1f}" ry="{r*.36:.1f}" fill="rgba(255,255,255,.65)" transform="rotate(-22 {-r*.42:.1f} {-h*.42:.1f})"/>'
            f'<ellipse cx="{r*.45:.1f}" cy="{h*.42:.1f}" rx="{r*.22:.1f}" ry="{r*.08:.1f}" fill="rgba(255,255,255,.14)" transform="rotate(-35 {r*.45:.1f} {h*.42:.1f})"/>{s}</g>')


def balloon(color="#E2BE6A", w=80, string=True):
    r = 40
    return (f'<svg width="{w}" viewBox="-50 -56 100 {130 if string else 100}" style="overflow:visible"><defs>{defs_balloon(color)}</defs>'
            f'{balloon_g(0,0,r*.95,color,0,22 if string else 0)}</svg>')


def balloons_row(colors, w=60):
    return "".join(f'<span style="display:inline-block;margin:0 -2px">{balloon(c, w)}</span>' for c in colors)


def arch_hero(W=520, H=420, colors=None, seed=3):
    colors = colors or ["#E2BE6A", "#2BB3AA", "#F4F1EA", "#4C8DFF", "#FF8FB8"]
    cx, base, rx, ry = W / 2, H - 52, W * .40, H * .72
    defs = "".join(defs_balloon(c) for c in set(colors + ["#FF6B5A"]))
    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="overflow:visible"><defs>{defs}'
           '<radialGradient id="floor" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="rgba(0,0,0,.45)"/><stop offset="1" stop-color="rgba(0,0,0,0)"/></radialGradient>'
           '<linearGradient id="fl2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(255,255,255,.14)"/><stop offset="1" stop-color="rgba(255,255,255,0)"/></linearGradient></defs>']
    out.append(f'<ellipse cx="{cx}" cy="{base+34}" rx="{rx*1.18:.0f}" ry="26" fill="url(#floor)"/>')
    pts = []
    n = 46
    for i in range(n + 1):
        a = math.pi * i / n
        x = cx - math.cos(a) * rx
        y = base - math.sin(a) * ry
        # lower pillars straight
        pts.append((x, y, i))
    # pillar extension
    pil = []
    for side in (-1, 1):
        for k in range(1, 6):
            pil.append((cx + side * rx, base + k * 16 - 8, k + side * 7))
    allp = pts + pil
    rnd = lambda k: abs(math.sin((k + seed) * 12.9898) * 43758.5453) % 1
    order = sorted(allp, key=lambda p: p[1])
    for j, (x, y, i) in enumerate(order):
        c = colors[(i + j // 7) % len(colors)] if rnd(j) > .15 else colors[(i * 2) % len(colors)]
        r = 24 + rnd(j + 40) * 8
        out.append(balloon_g(x + (rnd(j + 7) - .5) * 5, y + (rnd(j + 9) - .5) * 5, r, c, (rnd(j + 3) - .5) * 20))
    # small filler layer
    for j in range(22):
        a = math.pi * (j + .5) / 22
        x, y = cx - math.cos(a) * (rx * .93), base - math.sin(a) * (ry * .93)
        out.append(balloon_g(x, y, 15 + rnd(j + 60) * 5, colors[(j * 3 + 1) % len(colors)], (rnd(j + 5) - .5) * 30))
    out.append('</svg>')
    return "".join(out)


def machine(W=360, H=300):
    """isometric auto-inflator: box + 2 nozzles + hose + button + balloons inflating"""
    d = "".join(defs_balloon(c) for c in ["#E2BE6A", "#2BB3AA", "#FF6B5A", "#4C8DFF"])
    return f'''<svg viewBox="0 0 {W} {H}" width="100%" style="overflow:visible"><defs>{d}
<linearGradient id="mt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5C6F92"/><stop offset="1" stop-color="#2C3E63"/></linearGradient>
<linearGradient id="mf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2B3F66"/><stop offset="1" stop-color="#16243F"/></linearGradient>
<linearGradient id="ms" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1C2C4B"/><stop offset="1" stop-color="#0F1B33"/></linearGradient>
<radialGradient id="btn" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="#F6E2A6"/><stop offset=".6" stop-color="#E2BE6A"/><stop offset="1" stop-color="#A9812E"/></radialGradient>
<radialGradient id="fs" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="rgba(0,0,0,.5)"/><stop offset="1" stop-color="rgba(0,0,0,0)"/></radialGradient></defs>
<ellipse cx="190" cy="262" rx="150" ry="22" fill="url(#fs)"/>
<polygon points="70,150 190,110 310,150 190,190" fill="url(#mt)"/>
<polygon points="70,150 190,190 190,262 70,222" fill="url(#mf)"/>
<polygon points="190,190 310,150 310,222 190,262" fill="url(#ms)"/>
<polygon points="70,150 190,110 310,150 190,190" fill="none" stroke="rgba(255,255,255,.45)" stroke-width="1.5"/>
<polygon points="70,150 190,190 190,262 70,222" fill="none" stroke="rgba(255,255,255,.18)"/>
<g stroke="rgba(255,255,255,.12)" stroke-width="2">{"".join(f'<line x1="{84+i*8}" y1="{160+i*3.2}" x2="{84+i*8}" y2="{188+i*3.2}"/>' for i in range(8))}</g>
<ellipse cx="148" cy="214" rx="26" ry="12" fill="#0B1526"/><ellipse cx="148" cy="210" rx="24" ry="11" fill="url(#btn)"/><ellipse cx="144" cy="206" rx="9" ry="3.5" fill="rgba(255,255,255,.7)"/>
<text x="112" y="244" font-family="Poppins" font-weight="800" font-size="10" fill="#F6E2A6" transform="rotate(25 112 244) skewY(0)">ON / OFF</text>
<rect x="206" y="168" width="40" height="10" rx="5" fill="#2BB3AA" transform="skewY(-22)"/>
<rect x="206" y="182" width="26" height="8" rx="4" fill="#4C8DFF" transform="skewY(-22)"/>
<rect x="132" y="86" width="14" height="52" rx="7" fill="#C9D3E6"/><rect x="132" y="86" width="5" height="52" rx="2.5" fill="#fff" opacity=".7"/>
<rect x="224" y="106" width="14" height="46" rx="7" fill="#C9D3E6"/><rect x="224" y="106" width="5" height="46" rx="2.5" fill="#fff" opacity=".7"/>
{balloon_g(139,52,30,"#E2BE6A",-4)}{balloon_g(231,66,24,"#2BB3AA",6)}
{balloon_g(40,70,16,"#FF6B5A",-12,26)}{balloon_g(330,58,14,"#4C8DFF",10,26)}
<path d="M310 190 C 345 200, 350 240, 300 252" stroke="#10192D" stroke-width="9" fill="none" stroke-linecap="round"/>
<path d="M310 190 C 345 200, 350 240, 300 252" stroke="rgba(255,255,255,.18)" stroke-width="2.5" fill="none" stroke-linecap="round"/>
<g fill="#F6E2A6" opacity=".95"><path d="M96 40 l3 8 8 3 -8 3 -3 8 -3 -8 -8 -3 8 -3z"/><path d="M290 22 l2 6 6 2 -6 2 -2 6 -2 -6 -6 -2 6 -2z"/></g></svg>'''


def coin(cx, cy, r, ry_k=.34, label="₹"):
    ry = r * ry_k
    return (f'<g><ellipse cx="{cx}" cy="{cy+10}" rx="{r}" ry="{ry}" fill="#8A6A22"/><rect x="{cx-r}" y="{cy}" width="{2*r}" height="10" fill="#B88F35"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry}" fill="url(#coinG)"/><ellipse cx="{cx}" cy="{cy}" rx="{r*.72}" ry="{ry*.72}" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="1.5"/>'
            f'<text x="{cx}" y="{cy+ry*.45}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="{r*.62}" fill="#8A6A22">{label}</text></g>')


def coins(W=240, H=190, n=(5, 3, 4)):
    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="overflow:visible"><defs><linearGradient id="coinG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF1BD"/><stop offset=".5" stop-color="#E2BE6A"/><stop offset="1" stop-color="#B88F35"/></linearGradient>'
           '<radialGradient id="cs" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="rgba(0,0,0,.4)"/><stop offset="1" stop-color="rgba(0,0,0,0)"/></radialGradient></defs>']
    out.append(f'<ellipse cx="{W/2}" cy="{H-18}" rx="{W*.42}" ry="16" fill="url(#cs)"/>')
    xs = [W * .3, W * .68, W * .5]
    ys = [H - 34, H - 40, H - 36 - 12 * 0]
    for k, (x, base) in enumerate(zip(xs, [H - 38, H - 44, H - 28])):
        for i in range(n[k]):
            out.append(coin(x, base - i * 13, 36 if k != 2 else 40))
    out.append('</svg>')
    # reorder so front stack last: fine
    return "".join(out)


def tile3d(emoji, color="#E2BE6A", size=64):
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{size}px;border-radius:{size*.28:.0f}px;'
            f'background:radial-gradient(120% 120% at 25% 15%,{_mix(color,255,.55)},{color} 45%,{_mix(color,0,.45)});'
            f'box-shadow:0 {size*.14:.0f}px {size*.22:.0f}px rgba(18,33,58,.32),inset 0 2px 2px rgba(255,255,255,.75),inset 0 -4px 8px rgba(0,0,0,.18);font-size:{size*.52:.0f}px;line-height:1">'
            f'<span style="filter:drop-shadow(0 3px 2px rgba(0,0,0,.3))">{emoji}</span></span>')


def bars3d(series, W=500, H=250, colors=("#2BB3AA", "#E5484D", "#E2BE6A"), labels=None, names=("Kamai", "Kharcha", "Munafa"), maxv=None, fmt=lambda v: f"{v/1000:.0f}k", gap=None):
    """series: list of groups, each a tuple of 3 values (revenue, expenses, profit)."""
    n = len(series)
    maxv = maxv or max(max(g) for g in series) * 1.12
    pl, pb, pt = 36, 34, 14
    gw = (W - pl) / n
    bw = min(22, gw / 4.4)
    d = 7
    out = [f'<svg viewBox="0 0 {W} {H+16}" width="100%" style="overflow:visible"><defs>']
    for i, c in enumerate(colors):
        out.append(f'<linearGradient id="b{i}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{_mix(c,255,.3)}"/><stop offset="1" stop-color="{_mix(c,0,.12)}"/></linearGradient>')
    out.append('</defs>')
    for g in range(5):
        y = H - pb - (H - pb - pt) * g / 4
        out.append(f'<line x1="{pl}" y1="{y:.1f}" x2="{W}" y2="{y:.1f}" stroke="rgba(18,33,58,.12)" stroke-dasharray="3 4"/><text x="{pl-6}" y="{y+3:.1f}" text-anchor="end" font-size="8.5" fill="#6B7487" font-family="Inter">{fmt(maxv*g/4)}</text>')
    for gi, grp in enumerate(series):
        x0 = pl + gi * gw + (gw - 3 * bw - 2 * 3) / 2
        for bi, v in enumerate(grp):
            h = max(0.0, (H - pb - pt) * v / maxv)
            x = x0 + bi * (bw + 3)
            y = H - pb - h
            c = colors[bi]
            if v < 0:
                h = (H - pb - pt) * (-v) / maxv
                y = H - pb
            out.append(f'<polygon points="{x+bw:.1f},{y:.1f} {x+bw+d:.1f},{y-d*.7:.1f} {x+bw+d:.1f},{y-d*.7+h:.1f} {x+bw:.1f},{y+h:.1f}" fill="{_mix(c,0,.38)}"/>'
                       f'<polygon points="{x:.1f},{y:.1f} {x+d:.1f},{y-d*.7:.1f} {x+bw+d:.1f},{y-d*.7:.1f} {x+bw:.1f},{y:.1f}" fill="{_mix(c,255,.45)}"/>'
                       f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="url(#b{bi})"/>')
        lab = (labels or [str(i + 1) for i in range(n)])[gi]
        out.append(f'<text x="{x0+1.5*bw+3:.1f}" y="{H-pb+15}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#12213A" font-family="Inter">{lab}</text>')
    lx = pl
    for i, nm in enumerate(names):
        out.append(f'<rect x="{lx}" y="{H+2}" width="10" height="10" rx="3" fill="{colors[i]}"/><text x="{lx+14}" y="{H+11}" font-size="10" font-weight="700" fill="#12213A" font-family="Inter">{nm}</text>')
        lx += 86
    out.append('</svg>')
    return "".join(out)


def donut(parts, size=250, center_big="", center_small=""):
    """parts: list of (label,value,color)"""
    tot = sum(v for _, v, _ in parts)
    r, w = size * .38, size * .17
    c = size / 2
    out = [f'<svg viewBox="0 0 {size} {size}" width="{size}" style="overflow:visible"><circle cx="{c}" cy="{c+5}" r="{r}" fill="none" stroke="rgba(0,0,0,.14)" stroke-width="{w}"/>']
    a0 = -math.pi / 2
    for _, v, col in parts:
        a1 = a0 + 2 * math.pi * v / tot
        x0, y0, x1, y1 = c + r * math.cos(a0), c + r * math.sin(a0), c + r * math.cos(a1), c + r * math.sin(a1)
        big = 1 if a1 - a0 > math.pi else 0
        out.append(f'<path d="M{x0:.2f} {y0:.2f} A{r} {r} 0 {big} 1 {x1:.2f} {y1:.2f}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="butt"/>')
        a0 = a1
    out.append(f'<text x="{c}" y="{c+4}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="{size*.1:.0f}" fill="#12213A">{center_big}</text>'
               f'<text x="{c}" y="{c+size*.08+6:.0f}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="{size*.045:.0f}" letter-spacing="2" fill="#6B7487">{center_small}</text></svg>')
    return "".join(out)


def line_chart(vals, W=500, H=180, color="#2BB3AA", zero_label="Setup wapas", marks=None):
    n = len(vals)
    lo, hi = min(min(vals), 0), max(max(vals), 0) * 1.1 + 2000
    pl, pb, pt = 40, 24, 10
    X = lambda i: pl + (W - pl - 14) * i / (n - 1)
    Y = lambda v: H - pb - (H - pb - pt) * (v - lo) / (hi - lo)
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
    area = f"{X(0):.1f},{Y(0):.1f} " + pts + f" {X(n-1):.1f},{Y(0):.1f}"
    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="overflow:visible"><defs><linearGradient id="la" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{color}" stop-opacity=".45"/><stop offset="1" stop-color="{color}" stop-opacity=".02"/></linearGradient></defs>']
    for g in range(5):
        v = lo + (hi - lo) * g / 4
        out.append(f'<line x1="{pl}" y1="{Y(v):.1f}" x2="{W-10}" y2="{Y(v):.1f}" stroke="rgba(18,33,58,.1)"/><text x="{pl-5}" y="{Y(v)+3:.1f}" text-anchor="end" font-size="8.5" fill="#6B7487" font-family="Inter">{v/1000:.0f}k</text>')
    out.append(f'<line x1="{pl}" y1="{Y(0):.1f}" x2="{W-10}" y2="{Y(0):.1f}" stroke="#E5484D" stroke-width="1.6" stroke-dasharray="5 4"/>')
    out.append(f'<polygon points="{area}" fill="url(#la)"/><polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, v in enumerate(vals):
        out.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4.2" fill="#fff" stroke="{color}" stroke-width="2.5"/><text x="{X(i):.1f}" y="{H-8}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#12213A" font-family="Inter">M{i+1}</text>')
    out.append('</svg>')
    return "".join(out)


def cluster(seed=1, W=520, H=190):
    """bunch of glossy balloons tied to a gift-weight, used as 3D decoration at the bottom of pages"""
    cols = ["#E2BE6A", "#2BB3AA", "#FF6B5A", "#F4F1EA", "#4C8DFF", "#FF8FB8", "#9B6BFF"]
    rnd = lambda k: abs(math.sin((k + seed * 7) * 12.9898) * 43758.5453) % 1
    defs = "".join(defs_balloon(c) for c in cols)
    cx = W / 2 + (seed % 3 - 1) * 30
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="overflow:visible;max-height:190px"><defs>{defs}<radialGradient id="df" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="rgba(0,0,0,.35)"/><stop offset="1" stop-color="rgba(0,0,0,0)"/></radialGradient></defs>']
    o.append(f'<ellipse cx="{W/2}" cy="{H-6}" rx="{W*.4}" ry="9" fill="url(#df)"/>')
    # gift box weight
    o.append(f'<g transform="translate({cx},{H-26})"><rect x="-22" y="0" width="44" height="22" rx="4" fill="#12213A"/><rect x="-22" y="0" width="44" height="6" rx="3" fill="#E2BE6A"/><rect x="-3" y="0" width="6" height="22" fill="#E2BE6A"/></g>')
    n = 9
    for i in range(n):
        a = (i / (n - 1) - .5) * 2.0
        bx = cx + a * (W * .34) + (rnd(i) - .5) * 30
        by = 62 + abs(a) * 38 + rnd(i + 3) * 26
        r = 27 + rnd(i + 8) * 9
        o.append(f'<path d="M{cx} {H-26} Q {(cx+bx)/2} {(H-26+by)/2+20} {bx:.1f} {by+r*1.2:.1f}" stroke="rgba(255,255,255,.55)" stroke-width="1.2" fill="none"/>')
    for i in sorted(range(n), key=lambda i: -(62 + abs((i / (n - 1) - .5) * 2) * 38)):
        a = (i / (n - 1) - .5) * 2.0
        bx = cx + a * (W * .34) + (rnd(i) - .5) * 30
        by = 62 + abs(a) * 38 + rnd(i + 3) * 26
        r = 27 + rnd(i + 8) * 9
        o.append(balloon_g(bx, by, r, cols[(i + seed) % len(cols)], a * 14))
    o.append('</svg>')
    return "".join(o)
