import json, math, subprocess, sys, numpy as np, onnxruntime as ort
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

S = '/tmp/claude-0/-home-user-automation/30a7b273-6306-55c3-bec0-ca5f0409b214/scratchpad'
U = '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/'
W, H, FPS = 1080, 1920, 30
DUR = 58.70
MODE = sys.argv[1] if len(sys.argv) > 1 else 'full'   # full | stills
OUT = sys.argv[2] if len(sys.argv) > 2 else S + '/video_noaudio.mp4'

F = lambda n, s: ImageFont.truetype(f'{S}/fonts/{n}.ttf', s)
SAFFRON = (255, 196, 46); ORANGE = (255, 122, 26); WHITE = (255, 255, 255)

def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c1 = 1.9; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

# ---------------- segmentation (A-roll text-behind) ----------------
sess = ort.InferenceSession(S + '/src/u2net_human_seg.onnx', providers=['CPUExecutionProvider'])
def seg(im):
    x = np.asarray(im.resize((320, 320), Image.BILINEAR)).astype(np.float32) / 255.
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    o = sess.run(None, {sess.get_inputs()[0].name: x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    o = (o - o.min()) / (o.max() - o.min() + 1e-8)
    return Image.fromarray((o * 255).astype(np.uint8)).resize(im.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(2))

# ---------------- sources ----------------
photos = {}
def photo(k):
    if k not in photos:
        photos[k] = (Image.open(f'{S}/prep/{k}.jpg'), Image.open(f'{S}/prep/{k}_m.png'))
    return photos[k]

def photo_frame(k, z, cx, cy):
    im, m = photo(k)
    s0 = max(W / im.width, H / im.height)
    ww, hh = W / (s0 * z), H / (s0 * z)
    x0 = clamp(cx * im.width - ww / 2, 0, im.width - ww); y0 = clamp(cy * im.height - hh / 2, 0, im.height - hh)
    box = (x0, y0, x0 + ww, y0 + hh)
    return im.resize((W, H), Image.BILINEAR, box=box), m.resize((W, H), Image.BILINEAR, box=box)

class Pipe:
    def __init__(self, args):
        self.p = subprocess.Popen(['ffmpeg', '-v', 'error'] + args + ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        self.last = None
    def read(self):
        b = self.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3: self.last = Image.frombytes('RGB', (W, H), b)
        return self.last

aroll = Pipe(['-i', U + '193c93de-Aamer.mp4', '-vf', f'fps={FPS},scale={W}:{H}:flags=bicubic'])
sheesh = Pipe(['-ss', '0.2', '-i', U + 'dae228ce-IMG_8813.mov', '-vf', f'fps={FPS},scale={W}:-2,crop={W}:{H}'])

words = json.load(open(S + '/words.json'))

# ---------------- shot list ----------------
# (start, end, kind, src, z0, z1, (cx0,cy0), (cx1,cy1))
SHOTS = [
    (0.00, 1.70, 'aroll', None, 1.00, 1.10, None, None),
    (1.70, 4.20, 'photo', '8805', 1.00, 1.18, (.5, .45), (.5, .40)),
    (4.20, 6.30, 'photo', '8808', 1.12, 1.00, (.40, .45), (.58, .45)),
    (6.30, 8.28, 'aroll', None, 1.05, 1.22, None, None),
    (8.28, 12.90, 'photo', '8812', 1.25, 1.02, (.5, .50), (.5, .52)),
    (12.90, 15.20, 'photo', '8803', 1.00, 1.15, (.35, .40), (.5, .45)),
    (15.20, 17.70, 'photo', '8836', 1.15, 1.00, (.5, .40), (.5, .50)),
    (17.70, 23.30, 'photo', '8806', 1.00, 1.14, (.5, .45), (.52, .47)),
    (23.30, 26.20, 'video', 'sheesh', 1, 1, None, None),
    (26.20, 27.90, 'photo', '8805', 1.30, 1.40, (.5, .22), (.5, .20)),
    (27.90, 29.70, 'photo', '8816', 1.10, 1.00, (.5, .45), (.5, .5)),
    (29.70, 30.60, 'photo', '8855', 1.05, 1.15, (.5, .5), (.5, .45)),
    (30.60, 31.50, 'photo', '8854', 1.05, 1.15, (.5, .5), (.5, .45)),
    (31.50, 32.90, 'photo', '8875', 1.00, 1.12, (.5, .45), (.5, .40)),
    (32.90, 35.40, 'aroll', None, 1.00, 1.10, None, None),
    (35.40, 38.70, 'photo', '8812', 1.00, 1.10, (.5, .45), (.5, .42)),
    (38.70, 42.40, 'aroll', None, 1.10, 1.00, None, None),
    (42.40, 46.90, 'photo', '8884', 1.00, 1.12, (.5, .45), (.5, .40)),
    (46.90, 51.40, 'photo', '8886', 1.12, 1.00, (.5, .40), (.5, .45)),
    (51.40, 53.80, 'aroll', None, 1.00, 1.08, None, None),
    (53.80, 56.20, 'photo', '8803', 1.10, 1.00, (.55, .40), (.5, .45)),
    (56.20, DUR + 1, 'aroll', None, 1.00, 1.10, None, None),
]
CUTS = [s[0] for s in SHOTS[1:]]

def zoom_img(img, z):
    if abs(z - 1) < 1e-3: return img
    ww, hh = W / z, H / z
    return img.resize((W, H), Image.BILINEAR, box=((W - ww) / 2, (H - hh) / 2 * 0.8, (W + ww) / 2, (H - hh) / 2 * 0.8 + hh))

# ---------------- grading ----------------
xs = np.arange(256) / 255.
curve = np.clip(xs + 0.06 * np.sin(np.pi * (xs - 0.5)), 0, 1)
LUT_R = (np.clip(curve * 1.035 + 0.01, 0, 1) * 255).astype(np.uint8)
LUT_G = (np.clip(curve * 1.0, 0, 1) * 255).astype(np.uint8)
LUT_B = (np.clip(curve * 0.95, 0, 1) * 255).astype(np.uint8)
LUT = list(LUT_R) + list(LUT_G) + list(LUT_B)
yy, xx = np.mgrid[0:H, 0:W]
vig = 1 - 0.38 * np.clip(((xx - W / 2) / (W * .62)) ** 2 + ((yy - H / 2) / (H * .58)) ** 2, 0, 1.4) ** 1.6
VIG = Image.fromarray((np.clip(vig, 0, 1) * 255).astype(np.uint8))
from PIL import ImageEnhance
def grade(img):
    img = img.point(LUT)
    img = ImageEnhance.Color(img).enhance(1.15)
    return ImageChops.multiply(img, Image.merge('RGB', [VIG] * 3))

# ---------------- drawing helpers ----------------
def rr_mask(size, r):
    m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255); return m

def glass(frame, box, r=36, alpha=1.0, tint=(255, 255, 255), tint_a=0.16, blur=22, border=True):
    """Frosted glass panel on `frame` (RGB Image) in place."""
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W), min(y1, H)
    if x1 - x0 < 4 or y1 - y0 < 4 or alpha <= 0.01: return
    w, h = x1 - x0, y1 - y0
    # shadow
    sh = Image.new('L', (w + 80, h + 80), 0)
    ImageDraw.Draw(sh).rounded_rectangle((40, 52, 40 + w, 52 + h), r, fill=int(110 * alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    frame.paste(Image.new('RGB', sh.size, (0, 0, 0)), (x0 - 40, y0 - 40), sh)
    pad = blur * 2
    big = frame.crop((x0 - pad, y0 - pad, x1 + pad, y1 + pad)).filter(ImageFilter.GaussianBlur(blur))
    reg = big.crop((pad, pad, pad + w, pad + h))
    reg = Image.blend(reg, Image.new('RGB', (w, h), tint), tint_a)
    reg = ImageEnhance.Brightness(reg).enhance(1.06)
    # top sheen gradient
    g = Image.linear_gradient('L').resize((w, h)).point(lambda v: int(max(0, 70 - v * 0.45)))
    reg.paste(Image.new('RGB', (w, h), WHITE), (0, 0), g)
    m = rr_mask((w, h), r)
    if alpha < 1: m = m.point(lambda v: int(v * alpha))
    frame.paste(reg, (x0, y0), m)
    if border:
        lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((1, 1, w - 2, h - 2), r, outline=(255, 255, 255, int(150 * alpha)), width=3)
        d.rounded_rectangle((4, 4, w - 5, h - 5), r - 3, outline=(255, 255, 255, int(40 * alpha)), width=2)
        frame.paste(lay, (x0, y0), lay)

def text_layer(txt, font, fill=WHITE, stroke=0, stroke_fill=(0, 0, 0), shadow=True, spacing=0):
    """RGBA image of text with soft shadow. supports letter spacing."""
    tmp = ImageDraw.Draw(Image.new('L', (1, 1)))
    if spacing:
        ws = [tmp.textlength(c, font=font) + spacing for c in txt]; tw = int(sum(ws) - spacing)
    else:
        tw = int(tmp.textlength(txt, font=font))
    asc, desc = font.getmetrics(); th = asc + desc
    P = 30 + stroke
    img = Image.new('RGBA', (tw + 2 * P, th + 2 * P), (0, 0, 0, 0))
    def draw_on(d, col, sw, sf, off=(0, 0)):
        if spacing:
            x = P
            for c, cw in zip(txt, ws):
                d.text((x + off[0], P + off[1]), c, font=font, fill=col, stroke_width=sw, stroke_fill=sf); x += cw
        else:
            d.text((P + off[0], P + off[1]), txt, font=font, fill=col, stroke_width=sw, stroke_fill=sf)
    if shadow:
        sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw_on(ImageDraw.Draw(sh), (0, 0, 0, 150), stroke + 2, (0, 0, 0, 150), (0, 6))
        img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(9)))
    draw_on(ImageDraw.Draw(img), fill, stroke, stroke_fill)
    return img

def paste_c(frame, lay, cx, cy, scale=1.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.01: return
    if abs(scale - 1) > 1e-3:
        lay = lay.resize((max(1, int(lay.width * scale)), max(1, int(lay.height * scale))), Image.BICUBIC)
    if alpha < 1:
        a = lay.getchannel('A').point(lambda v: int(v * alpha)); lay = lay.copy(); lay.putalpha(a)
    frame.paste(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)), lay)

def gradient_text(txt, font, c1, c2, spacing=0, stroke=0):
    base = text_layer(txt, font, WHITE, stroke=0, shadow=False, spacing=spacing)
    g = Image.linear_gradient('L').resize(base.size)
    col = Image.composite(Image.new('RGBA', base.size, c2 + (255,)), Image.new('RGBA', base.size, c1 + (255,)), g)
    col.putalpha(base.getchannel('A'))
    return col

def wt(word, after=0.0):
    for o in words:
        if o['s'] >= after - 1e-6 and o['w'].lower().strip(',.!…') == word.lower(): return o['s']
    raise KeyError(word)

# ---------------- big titles (text-behind-subject) ----------------
fA = lambda s: F('Anton-Regular', s)
TITLES = {}
def big_title(key):
    if key in TITLES: return TITLES[key]
    if key == 'AMER':
        lay = gradient_text('AMER', fA(430), (255, 228, 120), (255, 120, 30), spacing=10)
    elif key == 'FORT':
        lay = gradient_text('FORT', fA(300), (255, 255, 255), (255, 214, 140), spacing=26)
    elif key == '1592':
        lay = gradient_text('1592', fA(420), (255, 236, 160), (255, 110, 30), spacing=6)
    elif key == 'JAIPUR':
        lay = gradient_text('JAIPUR', fA(330), (255, 214, 90), (255, 90, 40), spacing=6)
    elif key == 'JAIPUR2':
        lay = gradient_text('JAIPUR', fA(330), (255, 236, 140), (255, 100, 30), spacing=6)
    TITLES[key] = lay; return lay

def behind(frame, mask, items):
    """items: list of (layer, cx, cy, scale, alpha). Draw behind subject using mask."""
    if not items: return frame
    bg = frame.copy()
    for lay, cx, cy, sc, al in items:
        # glow
        paste_c(bg, lay, cx, cy, sc, al)
    return Image.composite(frame, bg, mask)

# ---------------- captions ----------------
CAP_FONT = F('PoppinsBlack-Regular', 74)
pages = []
cur = []
for i, o in enumerate(words):
    if cur and (o['g'] != cur[-1]['g'] or len(cur) >= 3 or sum(len(x['w']) for x in cur) + len(o['w']) > 17):
        pages.append(cur); cur = []
    cur.append(o)
pages.append(cur)
for i, p in enumerate(pages):
    nxt = pages[i + 1][0]['s'] if i + 1 < len(pages) else DUR
    p_end = min(nxt, p[-1]['e'] + 0.6)
    p.append({'_ps': p[0]['s'] - 0.05, '_pe': p_end})

cap_cache = {}
def word_img(w, state, hl):
    key = (w, state, hl)
    if key in cap_cache: return cap_cache[key]
    txt = w.upper()
    if state == 'active':
        col = SAFFRON if not hl else (255, 150, 40)
    elif hl:
        col = (255, 214, 120)
    elif state == 'done':
        col = WHITE
    else:
        col = (255, 255, 255, 150)
    lay = text_layer(txt, CAP_FONT, col, stroke=4, stroke_fill=(40, 20, 0), shadow=True)
    cap_cache[key] = lay; return lay

def draw_captions(frame, t, cy=1390):
    for p in pages:
        meta = p[-1]; ws = p[:-1]
        if not (meta['_ps'] <= t < meta['_pe']): continue
        k = ease((t - meta['_ps']) / 0.16)
        out = clamp((meta['_pe'] - t) / 0.08)
        imgs = []
        for o in ws:
            st = 'active' if o['s'] <= t < o['e'] + 0.04 else ('done' if t >= o['e'] else 'todo')
            imgs.append((o, st, word_img(o['w'], st, o['hl'])))
        gap = -40
        h = imgs[0][2].height
        sc = 0.86 + 0.14 * back(k)
        scs = []
        for o, st, im in imgs:
            ws_ = sc
            if st == 'active':
                pk = clamp((t - o['s']) / 0.12)
                ws_ = sc * (1.06 + 0.12 * math.sin(math.pi * min(pk, 1)))
            scs.append(ws_)
        total = sum(im.width * s_ + gap * sc for (_, _, im), s_ in zip(imgs, scs)) - gap * sc
        bw, bh = total - 24 * sc, 130 * sc
        glass(frame, (W / 2 - bw / 2, cy - bh / 2, W / 2 + bw / 2, cy + bh / 2), r=int(40 * sc),
              alpha=k * out, tint=(30, 20, 10), tint_a=0.28, blur=18)
        x = W / 2 - total / 2
        for (o, st, im), s_ in zip(imgs, scs):
            dy = -6 if st == 'active' else 0
            paste_c(frame, im, x + im.width * s_ / 2, cy + dy, s_, k * out)
            x += im.width * s_ + gap * sc
        break

# ---------------- overlays ----------------
fM = lambda s: F('Montserrat-Black', s)
fMb = lambda s: F('Montserrat-Bold', s)
fP = lambda s: F('PoppinsExtraBold-Regular', s)
fY = lambda s: F('YatraOne-Regular', s)
LCACHE = {}
def L(key, fn):
    if key not in LCACHE: LCACHE[key] = fn()
    return LCACHE[key]

def chip(frame, txt, cx, cy, t0, t, t1=None, dot=SAFFRON, size=40):
    if t < t0: return
    k = ease((t - t0) / 0.25)
    out = 1 if t1 is None else clamp((t1 - t) / 0.2)
    if out <= 0: return
    lay = L(('chip', txt, size), lambda: text_layer(txt, fMb(size), WHITE, shadow=False, spacing=4))
    w = lay.width + 40; h = size + 52
    x = cx - w / 2 + (1 - k) * 60
    glass(frame, (x, cy - h / 2, x + w, cy + h / 2), r=h // 2, alpha=k * out, tint=(20, 20, 20), tint_a=0.25)
    d = ImageDraw.Draw(frame)
    d.ellipse((x + 26, cy - 9, x + 44, cy + 9), fill=dot)
    paste_c(frame, lay, x + w / 2 + 18, cy + 2, 1, k * out)

def check_icon(frame, cx, cy, k):
    r = 30
    d = ImageDraw.Draw(frame)
    if k <= 0:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255), width=4); return
    rr = r * (0.6 + 0.4 * back(k))
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 170, 30))
    pts = [(cx - 13, cy + 1), (cx - 3, cy + 11), (cx + 15, cy - 11)]
    d.line(pts, fill=(255, 255, 255), width=7, joint='curve')

def draw_bookmark(frame, cx, cy, s, fillk):
    d = ImageDraw.Draw(frame)
    w, h = 70 * s, 95 * s
    poly = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx, cy + h / 2 - 26 * s), (cx - w / 2, cy + h / 2)]
    if fillk > 0: d.polygon(poly, fill=SAFFRON)
    d.line(poly + [poly[0]], fill=WHITE, width=int(7 * s), joint='curve')

def bubble_icon(frame, cx, cy, s):
    d = ImageDraw.Draw(frame)
    r = 34 * s
    d.ellipse((cx - r, cy - r * 0.85, cx + r, cy + r * 0.85), outline=WHITE, width=int(6 * s))
    d.polygon([(cx - r * 0.5, cy + r * 0.55), (cx - r * 0.9, cy + r * 1.1), (cx - r * 0.05, cy + r * 0.78)], fill=WHITE)

def viewfinder(frame, t, t0):
    d = ImageDraw.Draw(frame)
    m, L_ = 70, 110
    for (x, y, sx, sy) in [(m, 250, 1, 1), (W - m, 250, -1, 1), (m, 1650, 1, -1), (W - m, 1650, -1, -1)]:
        d.line([(x, y + sy * L_), (x, y), (x + sx * L_, y)], fill=WHITE, width=7)
    if int(t * 2) % 2 == 0: d.ellipse((m + 30, 290, m + 62, 322), fill=(255, 50, 50))
    rec = L(('rec',), lambda: text_layer('REC', fMb(38), WHITE, shadow=False))
    paste_c(frame, rec, m + 130, 306)
    d.line([(W / 2 - 40, H / 2), (W / 2 + 40, H / 2)], fill=(255, 255, 255), width=3)
    d.line([(W / 2, H / 2 - 40), (W / 2, H / 2 + 40)], fill=(255, 255, 255), width=3)

def brand_tag(frame, t):
    lay = L(('brand',), lambda: text_layer('HOW IS TRAVELLERS LIFE', fMb(30), WHITE, shadow=False, spacing=3))
    w = lay.width + 30; h = 66
    x = W / 2 - w / 2; y = 120
    glass(frame, (x, y, x + w, y + h), r=33, tint=(20, 20, 20), tint_a=0.2, blur=14)
    d = ImageDraw.Draw(frame)
    paste_c(frame, lay, W / 2 + 14, y + h / 2 + 1)
    d.ellipse((x + 20, y + h / 2 - 8, x + 36, y + h / 2 + 8), fill=SAFFRON)

def progress(frame, t):
    d = ImageDraw.Draw(frame)
    d.rectangle((0, 0, W, 9), fill=(0, 0, 0))
    d.rectangle((0, 0, int(W * t / DUR), 9), fill=SAFFRON)

T_REVEAL = 8.28
T_1592 = wt('1592')
T_MAN = wt('Man')
T_SHEESH, T_GANESH, T_MAOTA = wt('Sheesh'), wt('Ganesh'), wt('Maota')
T_LOC, T_DIST, T_OPEN, T_TRANS = wt('location'), wt('distance'), wt('opening'), wt('transport')
T_LIKH = wt('likhiye'); T_SAVE = wt('save')

def overlays(frame, t, mask):
    """returns frame. mask = subject mask (L) or None"""
    items = []
    # --- HOOK: JAIPUR behind him
    if t < 1.70 and mask is not None:
        k = ease(t / 0.35)
        items.append((big_title('JAIPUR'), W / 2, 520, 0.9 + 0.1 * back(k), k))
    # --- REVEAL AMER FORT behind subjects
    if 8.28 <= t < 12.90 and mask is not None:
        k = ease((t - T_REVEAL) / 0.30)
        k2 = ease((t - T_REVEAL - 0.30) / 0.35)
        drift = (t - T_REVEAL) * 6
        items.append((big_title('AMER'), W / 2, 470 - drift, 1.6 - 0.6 * k, k))
        items.append((big_title('FORT'), W / 2, 790 - drift, 0.7 + 0.3 * back(k2), k2))
    if 17.70 <= t < 23.30 and mask is not None and t >= T_1592 - 0.1:
        k = ease((t - T_1592 + 0.1) / 0.3)
        items.append((big_title('1592'), W / 2, 470 - (t - T_1592) * 8, 1.4 - 0.4 * k, k))
    if 51.40 <= t < 53.80 and mask is not None:
        k = ease((t - 51.40) / 0.3)
        items.append((big_title('JAIPUR2'), W / 2, 540, 0.85 + 0.15 * back(k), k))
    if mask is not None and items:
        frame = behind(frame, mask, items)

    # --- FRONT elements
    if t < 1.70:
        pass
    if 1.70 <= t < 6.30:
        lay = L(('raja',), lambda: text_layer('राजा-महाराजा का दौर', fY(96), (255, 222, 150), shadow=True))
        k = ease((t - 2.2) / 0.4); o = clamp((6.25 - t) / 0.2)
        if t > 2.2: paste_c(frame, lay, W / 2, 330, 0.9 + 0.1 * k, k * o)
    if 6.30 <= t < 8.28:
        lay = L(('naam',), lambda: text_layer('नाम है…?', fY(120), WHITE, shadow=True))
        k = ease((t - 6.6) / 0.4)
        if t > 6.6: paste_c(frame, lay, W / 2, 1020, 1, k)
    if 8.28 <= t < 12.90:
        k = ease((t - 9.0) / 0.4)
        if t > 9.0:
            lay = L(('hindi_amer',), lambda: text_layer('आमेर किला', fY(92), WHITE, shadow=True))
            paste_c(frame, lay, W / 2, 1110, 1, k)
        chip(frame, 'JAIPUR • RAJASTHAN', W / 2, 1230, 9.5, t, 12.85)
    if 12.90 <= t < 17.70:
        chip(frame, 'ARAVALLI HILLS', W / 2, 330, 13.1, t, 15.15)
        chip(frame, 'UNESCO WORLD HERITAGE', W / 2, 330, 15.3, t, 17.65)
    if 17.70 <= t < 23.30:
        if t >= T_1592 - 0.1:
            k = ease((t - T_1592) / 0.3)
            lay = L(('est',), lambda: text_layer('ESTABLISHED', fMb(44), WHITE, shadow=True, spacing=14))
            paste_c(frame, lay, W / 2, 230, 1, k)
        if t >= T_MAN - 0.2:
            k = ease((t - T_MAN + 0.2) / 0.35)
            cw, ch = 780, 190; x0 = W / 2 - cw / 2; y0 = 1010 + (1 - k) * 80
            glass(frame, (x0, y0, x0 + cw, y0 + ch), r=40, alpha=k, tint=(30, 15, 5), tint_a=0.25)
            l1 = L(('man',), lambda: text_layer('RAJA MAN SINGH I', fM(56), SAFFRON, shadow=False, spacing=2))
            l2 = L(('kach',), lambda: text_layer('Kachwaha ruler of Amber', fMb(36), WHITE, shadow=False))
            paste_c(frame, l1, W / 2, y0 + 70, 1, k); paste_c(frame, l2, W / 2, y0 + 135, 1, k)
    if 23.30 <= t < 29.70:
        y = 300
        for i, (nm, tt) in enumerate([('SHEESH MAHAL', T_SHEESH), ('GANESH POL', T_GANESH), ('MAOTA LAKE', T_MAOTA)]):
            chip(frame, nm, 60 + 230, y + i * 120, tt - 0.15, t, 29.65, size=40) if False else None
        # left-aligned stack
        for i, (nm, tt) in enumerate([('SHEESH MAHAL', T_SHEESH), ('GANESH POL', T_GANESH), ('MAOTA LAKE', T_MAOTA)]):
            lay = L(('chip', nm, 40), lambda nm=nm: text_layer(nm, fMb(40), WHITE, shadow=False, spacing=4))
            chip(frame, nm, 70 + (lay.width + 40) / 2, 300 + i * 118, tt - 0.15, t, 29.65)
    if 29.70 <= t < 32.90:
        viewfinder(frame, t, 29.7)
        lay = L(('photo',), lambda: text_layer('PHOTO POINT!', fA(150), SAFFRON, stroke=6, stroke_fill=(60, 20, 0)))
        k = ease((t - 30.0) / 0.25)
        if t > 30.0: paste_c(frame, lay, W / 2, 470, 0.8 + 0.2 * back(k), k)
    if 35.40 <= t < 38.70:
        lay = L(('more',), lambda: text_layer('JAIPUR MEIN AUR BHI…', fA(96), WHITE, stroke=4, stroke_fill=(60, 20, 0)))
        k = ease((t - 35.5) / 0.3)
        paste_c(frame, lay, W / 2, 260, 0.9 + 0.1 * back(k), k)
        for i, nm in enumerate(['HAWA MAHAL', 'CITY PALACE', 'NAHARGARH FORT', 'JAL MAHAL', 'JANTAR MANTAR']):
            lay2 = L(('chip', nm, 40), lambda nm=nm: text_layer(nm, fMb(40), WHITE, shadow=False, spacing=4))
            chip(frame, nm, W / 2, 400 + i * 112, 35.9 + i * 0.35, t, 38.65)
    if 38.70 <= t < 42.40:
        k = ease((t - 38.9) / 0.35)
        cw, ch = 860, 230; x0 = W / 2 - cw / 2; y0 = 240 - (1 - k) * 60
        glass(frame, (x0, y0, x0 + cw, y0 + ch), r=46, alpha=k, tint=(30, 15, 5), tint_a=0.22)
        l1 = L(('cg1',), lambda: text_layer('COMPLETE', fMb(44), WHITE, shadow=False, spacing=16))
        l2 = L(('cg2',), lambda: gradient_text('JAIPUR TRAVEL GUIDE', fA(96), (255, 230, 120), (255, 120, 30), spacing=3))
        paste_c(frame, l1, W / 2, y0 + 60, 1, k); paste_c(frame, l2, W / 2, y0 + 145, 1, k)
    if 42.40 <= t < 51.40:
        k = ease((t - 42.5) / 0.35); o = clamp((51.35 - t) / 0.2)
        cw, ch = 900, 640; x0 = W / 2 - cw / 2; y0 = 790 + (1 - k) * 80
        glass(frame, (x0, y0, x0 + cw, y0 + ch), r=50, alpha=k * o, tint=(25, 12, 4), tint_a=0.30)
        l0 = L(('cl0',), lambda: gradient_text('JAIPUR TRAVEL GUIDE', fA(78), (255, 230, 120), (255, 120, 30), spacing=3))
        paste_c(frame, l0, W / 2, y0 + 80, 1, k * o)
        items_ = [('Tourist Places Location', T_LOC), ('Distance Between Places', T_DIST),
                  ('Opening & Closing Time', T_OPEN), ('Car / Public Transport Route', T_TRANS)]
        for i, (nm, tt) in enumerate(items_):
            yy_ = y0 + 200 + i * 112
            ki = ease((t - tt + 0.1) / 0.3)
            lay = L(('cli', nm), lambda nm=nm: text_layer(nm, fP(44), WHITE, shadow=False))
            if k * o > 0.3:
                check_icon(frame, x0 + 80, yy_, ki if t >= tt - 0.1 else 0)
                paste_c(frame, lay, x0 + 130 + lay.width / 2 - 30, yy_ + 4, 1, (0.55 + 0.45 * ki) * k * o)
    if 51.40 <= t < 53.80:
        s = 1 + 0.05 * math.sin((t - 51.4) * 2 * math.pi * 1.6) if t > T_LIKH else 1
        k = ease((t - 51.6) / 0.3)
        l1 = L(('cm1',), lambda: text_layer('COMMENT', fMb(50), WHITE, shadow=False, spacing=6))
        l2 = L(('cm2',), lambda: gradient_text('"JAIPUR"', fA(96), (255, 230, 120), (255, 120, 30), spacing=4))
        inner = 70 + 20 + (l1.width - 60) + 24 + (l2.width - 60)
        cw, ch = (inner + 90) * s, 150 * s; x0 = W / 2 - cw / 2; y0 = 1020 + (1 - k) * 60
        glass(frame, (x0, y0, x0 + cw, y0 + ch), r=int(ch / 2), alpha=k, tint=(30, 15, 5), tint_a=0.28)
        x = x0 + 45 * s
        if k > 0.3: bubble_icon(frame, x + 35 * s, y0 + ch / 2, s)
        x += 90 * s
        paste_c(frame, l1, x + (l1.width - 60) * s / 2, y0 + ch / 2 + 2, s, k); x += (l1.width - 60 + 24) * s
        paste_c(frame, l2, x + (l2.width - 60) * s / 2, y0 + ch / 2 + 2, s, k)
    if 53.80 <= t < 56.20:
        k = ease((t - 53.9) / 0.3)
        cw, ch = 720, 300; x0 = W / 2 - cw / 2; y0 = 330
        glass(frame, (x0, y0, x0 + cw, y0 + ch), r=50, alpha=k, tint=(30, 15, 5), tint_a=0.25)
        if k > 0.2:
            draw_bookmark(frame, W / 2, y0 + 100, 1.0, 1 if t >= T_SAVE else 0)
        l1 = L(('sv',), lambda: text_layer('SAVE FOR YOUR TRIP', fM(52), WHITE, shadow=False, spacing=3))
        paste_c(frame, l1, W / 2, y0 + 225, 1, k)
    if t >= 56.20:
        k = ease((t - 56.4) / 0.4)
        cw, ch = 900, 300; x0 = W / 2 - cw / 2; y0 = 980 + (1 - k) * 60
        glass(frame, (x0, y0, x0 + cw, y0 + ch), r=50, alpha=k, tint=(30, 15, 5), tint_a=0.28)
        l1 = L(('e1',), lambda: text_layer('FOLLOW', fMb(42), WHITE, shadow=False, spacing=18))
        l2 = L(('e2',), lambda: gradient_text('HOW IS TRAVELLERS LIFE', fA(84), (255, 230, 120), (255, 120, 30), spacing=3))
        l3 = L(('e3',), lambda: text_layer('for more travel guides', fP(38), WHITE, shadow=False))
        paste_c(frame, l1, W / 2, y0 + 60, 1, k); paste_c(frame, l2, W / 2, y0 + 145, 1, k); paste_c(frame, l3, W / 2, y0 + 235, 1, k)
    return frame

# ---------------- main loop ----------------
def shot_at(t):
    for s in SHOTS:
        if s[0] <= t < s[1]: return s
    return SHOTS[-1]

def render(t, aroll_img, sheesh_img):
    s = shot_at(t)
    st, en, kind, src, z0, z1, c0, c1 = s
    p = (t - st) / (en - st if en < DUR else DUR - st)
    pe = ease_io(p)
    z = z0 + (z1 - z0) * pe
    # punch-in at cut
    dt = t - st
    punch = 1 + 0.10 * (1 - ease(dt / 0.25)) if st > 0 else 1
    mask = None
    if kind == 'photo':
        cx = c0[0] + (c1[0] - c0[0]) * pe; cy = c0[1] + (c1[1] - c0[1]) * pe
        frame, mask = photo_frame(src, z * punch, cx, cy)
    elif kind == 'aroll':
        # subtle handheld + zoom
        frame = zoom_img(aroll_img, z * punch)
        if t < 1.70 or 51.40 <= t < 53.80:
            mask = seg(frame)
    else:
        frame = zoom_img(sheesh_img, 1.0 + 0.08 * pe + (punch - 1))
    frame = grade(frame)
    frame = overlays(frame, t, mask)
    # flash at cut
    fl = 0
    for c in CUTS:
        if 0 <= t - c < 0.12: fl = max(fl, 0.55 * (1 - (t - c) / 0.12))
    if 0 <= t - T_REVEAL < 0.2: fl = max(fl, 0.9 * (1 - (t - T_REVEAL) / 0.2))
    if 29.7 <= t < 32.9:
        for c in (29.7, 30.6, 31.5):
            if 0 <= t - c < 0.1: fl = max(fl, 0.95)
    if fl > 0: frame = Image.blend(frame, Image.new('RGB', (W, H), (255, 248, 235)), fl)
    if t >= 0.15: brand_tag(frame, t) if not (t >= 56.2) else None
    draw_captions(frame, t, 1530 if 42.4 <= t < 51.4 else 1390)
    progress(frame, t)
    # fade in/out
    if t < 0.15: frame = Image.blend(Image.new('RGB', (W, H)), frame, t / 0.15)
    return frame

N = int(DUR * FPS)
if MODE == 'stills':
    ts = [float(x) for x in sys.argv[3].split(',')]
    fi = 0; want = sorted(int(x * FPS) for x in ts)
    for i in range(max(want) + 1):
        a = aroll.read(); t = i / FPS
        sh = sheesh.read() if 23.30 <= t < 26.20 else (sheesh.last or Image.new('RGB', (W, H)))
        if i in want:
            render(t, a, sh).save(f'{S}/frames/still_{t:05.2f}.jpg', quality=88); print('still', t, flush=True)
    sys.exit()

enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
for i in range(N):
    t = i / FPS
    a = aroll.read()
    sh = sheesh.read() if 23.30 <= t < 26.20 else (sheesh.last or Image.new('RGB', (W, H)))
    enc.stdin.write(render(t, a, sh).tobytes())
    if i % 150 == 0: print('frame', i, '/', N, flush=True)
enc.stdin.close(); enc.wait()
print('done')
