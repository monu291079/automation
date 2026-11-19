import json, math, subprocess, sys, numpy as np, onnxruntime as ort
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

S = '/tmp/claude-0/-home-user-automation/30a7b273-6306-55c3-bec0-ca5f0409b214/scratchpad'
U = '/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/'
W, H, FPS = 1080, 1920, 30
DUR = 42.70
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
        photos[k] = (Image.open(f'{S}/pprep/{k}.jpg'), Image.open(f'{S}/pprep/{k}_m.png'))
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

class _D:
    def read(self): return None
aroll = _D()
DELOGO = 'delogo=x=60:y=255:w=290:h=90,'
VSRC = {
    'exp': ('/root/.claude/uploads/30a7b273-6306-55c3-bec0-ca5f0409b214/efac07b6-export.mp4', 0.0, f'fps={FPS},scale={W}:{H}:flags=bicubic'),
}
def vspec(src):
    n, off = src.split('@'); p, ss, vf = VSRC[n]; return p, ss + float(off), vf
vpipes = {}
def vframe(shot):
    key = (shot[0], shot[3])
    if key not in vpipes:
        path, ss, vf = vspec(shot[3])
        vpipes[key] = Pipe(['-ss', str(ss), '-i', path, '-vf', vf])
    return vpipes[key].read()
def grab(path, ss, vf):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', path, '-vf', vf, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), b[:W * H * 3])

words = json.load(open(S + '/pwords.json'))

# ---------------- shot list ----------------
# (start, end, kind, src, z0, z1, (cx0,cy0), (cx1,cy1))
SHOTS = [
    (0.00, 2.10, 'photo', '9244', 1.12, 1.00, (.5, .42), (.5, .45)),
    (2.10, 4.90, 'video', 'exp@20.0', 1.00, 1.08, None, None),
    (4.90, 8.30, 'photo', '9245', 1.00, 1.10, (.5, .42), (.5, .40)),
    (8.30, 10.20, 'video', 'exp@4.5', 1.00, 1.08, None, None),
    (10.20, 12.40, 'video', 'exp@10.0', 1.00, 1.06, None, None),
    (12.40, 14.40, 'video', 'exp@12.4', 1.05, 1.15, None, None),
    (14.40, 17.00, 'video', 'exp@17.0', 1.00, 1.10, None, None),
    (17.00, 19.40, 'video', 'exp@15.0', 1.00, 1.05, None, None),
    (19.40, 21.20, 'photo', '9241', 1.08, 1.00, (.5, .45), (.5, .42)),
    (21.20, 23.90, 'video', 'exp@25.0', 1.00, 1.08, None, None),
    (23.90, 27.20, 'video', 'exp@27.3', 1.00, 1.06, None, None),
    (27.20, 31.80, 'video', 'exp@0.3', 1.00, 1.10, None, None),
    (31.80, 37.10, 'video', 'exp@30.0', 1.00, 1.08, None, None),
    (37.10, 39.50, 'photo', '9244', 1.00, 1.08, (.5, .45), (.5, .45)),
    (39.50, DUR + 1, 'photo', '9245', 1.08, 1.00, (.5, .45), (.5, .45)),
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
    if key == 'BRAHMA':
        lay = gradient_text('BRAHMA', fA(330), (255, 236, 150), (255, 110, 30), spacing=6)
    elif key == 'PUSHKAR':
        lay = gradient_text('PUSHKAR', fA(320), (255, 240, 200), (255, 120, 60), spacing=4)
    elif key == 'PUSHKAR2':
        lay = gradient_text('PUSHKAR', fA(300), (255, 236, 150), (255, 110, 30), spacing=4)
    if lay.width > W + 40: lay = lay.resize((W + 40, int(lay.height * (W + 40) / lay.width)), Image.LANCZOS)
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

T_LIKH = wt('likhiye'); T_FOL = wt('follow')
T_PUSH1 = wt('Pushkar', 4.0); T_JHEEL = wt('jheel'); T_KAMAL = wt('kamal'); T_AARTI = wt('aarti'); T_DIYE = wt('diye')
T_BM = wt('Brahma', 17.0); T_SHIKHAR = wt('shikhar'); T_CHAANDI = wt('chaandi'); T_BHEED = wt('Bheed'); T_SUBAH = wt('subah'); T_PAISE = wt('paise')
T_PLAN = wt('2', 31.0); T_RUK = wt('rukein'); T_KHA = wt('khaayein'); T_KHARCH = wt('kharch?')

def title_card(frame, t, t0, t1, top, main, y0, w=860):
    if not (t0 <= t < t1): return
    k = ease((t - t0) / 0.35); o = clamp((t1 - t) / 0.2)
    ch = 220; x0 = W / 2 - w / 2; y = y0 - (1 - k) * 60
    glass(frame, (x0, y, x0 + w, y + ch), r=46, alpha=k * o, tint=(30, 15, 5), tint_a=0.25)
    l1 = L(('tc1', top), lambda: text_layer(top, fMb(40), WHITE, shadow=False, spacing=12))
    l2 = L(('tc2', main), lambda: gradient_text(main, fA(92), (255, 230, 120), (255, 120, 30), spacing=3))
    if l2.width - 60 > w - 40: l2 = l2.resize((w - 40 + 60, int(l2.height * (w - 40 + 60) / l2.width)), Image.LANCZOS)
    paste_c(frame, l1, W / 2, y + 62, 1, k * o); paste_c(frame, l2, W / 2, y + 145, 1, k * o)

def big_front(frame, t, t0, t1, key, txt, font, y, c1=(255, 255, 255), c2=(255, 200, 90), pop=True):
    if not (t0 <= t < t1): return
    k = ease((t - t0) / 0.3); o = clamp((t1 - t) / 0.15)
    lay = L(('bf', key), lambda: gradient_text(txt, font, c1, c2, spacing=4))
    sh = L(('bfs', key), lambda: text_layer(txt, font, (40, 15, 0), stroke=8, stroke_fill=(40, 15, 0), shadow=True, spacing=4))
    sc = 0.75 + 0.25 * back(k) if pop else 1
    paste_c(frame, sh, W / 2, y, sc, k * o); paste_c(frame, lay, W / 2, y, sc, k * o)

def overlays(frame, t, mask):
    items = []
    if t < 2.10 and mask is not None:
        k = ease(t / 0.35)
        items.append((big_title('BRAHMA'), W / 2, 470, 1.25 - 0.25 * k, k))
    if 4.90 <= t < 8.30 and mask is not None and t >= T_PUSH1 - 0.15:
        k = ease((t - T_PUSH1 + 0.15) / 0.3)
        items.append((big_title('PUSHKAR'), W / 2, 500 - (t - T_PUSH1) * 8, 1.4 - 0.4 * k, k))
    if t >= 39.50 and mask is not None:
        k = ease((t - 39.5) / 0.3)
        items.append((big_title('PUSHKAR2'), W / 2, 520, 0.85 + 0.15 * back(k), k))
    if mask is not None and items: frame = behind(frame, mask, items)

    if t < 2.10:
        chip(frame, 'PUSHKAR • RAJASTHAN', W / 2, 1430, 0.4, t, 2.05)
    if 2.10 <= t < 4.90:
        big_front(frame, t, 2.3, 4.85, 'rare1', 'BHARAT ME GINE-CHUNE', fA(96), 380)
        big_front(frame, t, 2.6, 4.85, 'rare2', 'BRAHMA MANDIR', fA(150), 520, (255, 236, 140), (255, 110, 30))
    if 4.90 <= t < 8.30:
        if t >= T_PUSH1 + 0.3:
            k = ease((t - T_PUSH1 - 0.3) / 0.35)
            lay = L(('hin',), lambda: text_layer('पुष्कर, राजस्थान', fY(92), WHITE, shadow=True))
            paste_c(frame, lay, W / 2, 1180, 1, k)
        chip(frame, 'TIRTHRAJ PUSHKAR', W / 2, 260, 5.4, t, 8.25)
    if 8.30 <= t < 12.40:
        title_card(frame, t, 8.4, 12.35, 'STOP 1', 'PUSHKAR LAKE', 280, w=720)
        lay = L(('ch', 'BRAHMA JI KE KAMAL SE BANI', 40), lambda: text_layer('BRAHMA JI KE KAMAL SE BANI', fMb(40), WHITE, shadow=False, spacing=4))
        chip(frame, 'BRAHMA JI KE KAMAL SE BANI', W / 2, 560, T_KAMAL - 0.2, t, 12.35)
    if 12.40 <= t < 17.00:
        lay = L(('ch', 'GHAAT PAR BAITHIYE', 40), lambda: text_layer('GHAAT PAR BAITHIYE', fMb(40), WHITE, shadow=False, spacing=4))
        chip(frame, 'GHAAT PAR BAITHIYE', 70 + (lay.width + 40) / 2, 300, 12.6, t, 16.95)
        l2 = L(('ch', 'SHAAM KI AARTI', 40), lambda: text_layer('SHAAM KI AARTI', fMb(40), WHITE, shadow=False, spacing=4))
        chip(frame, 'SHAAM KI AARTI', 70 + (l2.width + 40) / 2, 418, T_AARTI - 0.2, t, 16.95)
        l3 = L(('ch', 'TAIRTE DIYE', 40), lambda: text_layer('TAIRTE DIYE', fMb(40), WHITE, shadow=False, spacing=4))
        chip(frame, 'TAIRTE DIYE', 70 + (l3.width + 40) / 2, 536, T_DIYE - 0.2, t, 16.95)
    if 17.00 <= t < 23.90:
        title_card(frame, t, 17.1, 23.85, 'STOP 2', 'BRAHMA MANDIR', 280, w=760)
        for i, (nm, tt) in enumerate([('SANGMARMAR KI SEEDHIYAN', 19.4), ('LAAL SHIKHAR', T_SHIKHAR), ('CHAANDI KI NAKKASHI', T_CHAANDI)]):
            lay = L(('ch', nm, 40), lambda nm=nm: text_layer(nm, fMb(40), WHITE, shadow=False, spacing=4))
            chip(frame, nm, W / 2, 560 + i * 116, tt - 0.15, t, 23.85)
    if 23.90 <= t < 31.80:
        k = ease((t - 24.0) / 0.25); o = clamp((31.75 - t) / 0.2)
        cw, ch = 900, 470; x0 = W / 2 - cw / 2; y0 = 230 + (1 - k) * 60
        glass(frame, (x0, y0, x0 + cw, y0 + ch), r=46, alpha=k * o, tint=(70, 10, 10), tint_a=0.35)
        l0 = L(('warn',), lambda: gradient_text('⚠ DHYAAN RAKHIYE', fA(84), (255, 230, 120), (255, 90, 40), spacing=3) if False else gradient_text('DHYAAN RAKHIYE!', fA(84), (255, 230, 120), (255, 90, 40), spacing=3))
        paste_c(frame, l0, W / 2, y0 + 80, 1, k * o)
        for i, (nm, tt) in enumerate([('Bheed jaldi badhti hai', T_BHEED), ('Subah jaldi aaiye', T_SUBAH), ('Paise maangne walon se bacho', T_PAISE)]):
            yy_ = y0 + 195 + i * 95
            ki = ease((t - tt + 0.1) / 0.3)
            lay = L(('cli', nm), lambda nm=nm: text_layer(nm, fP(42), WHITE, shadow=False))
            if k * o > 0.3:
                check_icon(frame, x0 + 80, yy_, ki if t >= tt - 0.1 else 0)
                paste_c(frame, lay, x0 + 130 + lay.width / 2 - 30, yy_ + 4, 1, (0.5 + 0.5 * ki) * k * o)
    if 31.80 <= t < 37.10:
        k = ease((t - 31.9) / 0.35); o = clamp((37.05 - t) / 0.2)
        cw, ch = 900, 560; x0 = W / 2 - cw / 2; y0 = 230 + (1 - k) * 60
        glass(frame, (x0, y0, x0 + cw, y0 + ch), r=50, alpha=k * o, tint=(25, 12, 4), tint_a=0.32)
        l0 = L(('pl0',), lambda: gradient_text('2 DIN KA PUSHKAR PLAN', fA(78), (255, 230, 120), (255, 120, 30), spacing=3))
        paste_c(frame, l0, W / 2, y0 + 80, 1, k * o)
        for i, (nm, tt) in enumerate([('Kahan rukein', T_RUK), ('Kya khaayein', T_KHA), ('Kitna kharch', T_KHARCH), ('Ghat, mandir & timings', T_KHARCH + 0.6)]):
            yy_ = y0 + 190 + i * 92
            ki = ease((t - tt + 0.1) / 0.3)
            lay = L(('cli', nm), lambda nm=nm: text_layer(nm, fP(44), WHITE, shadow=False))
            if k * o > 0.3:
                check_icon(frame, x0 + 80, yy_, ki if t >= tt - 0.1 else 0)
                paste_c(frame, lay, x0 + 130 + lay.width / 2 - 30, yy_ + 4, 1, (0.55 + 0.45 * ki) * k * o)
    if 37.10 <= t < 39.50:
        s_ = 1 + 0.05 * math.sin((t - 37.1) * 2 * math.pi * 1.6) if t > T_LIKH else 1
        k = ease((t - 37.2) / 0.3)
        l1 = L(('cm1',), lambda: text_layer('COMMENT', fMb(50), WHITE, shadow=False, spacing=6))
        l2 = L(('cm2p',), lambda: gradient_text('"PUSHKAR"', fA(96), (255, 230, 120), (255, 120, 30), spacing=4))
        inner = 70 + 20 + (l1.width - 60) + 24 + (l2.width - 60)
        cw, ch = (inner + 90) * s_, 150 * s_; x0 = W / 2 - cw / 2; y0 = 250 + (1 - k) * 60
        glass(frame, (x0, y0, x0 + cw, y0 + ch), r=int(ch / 2), alpha=k, tint=(30, 15, 5), tint_a=0.35)
        x = x0 + 45 * s_
        if k > 0.3: bubble_icon(frame, x + 35 * s_, y0 + ch / 2, s_)
        x += 90 * s_
        paste_c(frame, l1, x + (l1.width - 60) * s_ / 2, y0 + ch / 2 + 2, s_, k); x += (l1.width - 60 + 24) * s_
        paste_c(frame, l2, x + (l2.width - 60) * s_ / 2, y0 + ch / 2 + 2, s_, k)
    if t >= 39.50:
        k = ease((t - 39.6) / 0.4)
        cw, ch = 900, 300; x0 = W / 2 - cw / 2; y0 = 1180 + (1 - k) * 60
        glass(frame, (x0, y0, x0 + cw, y0 + ch), r=50, alpha=k, tint=(30, 15, 5), tint_a=0.3)
        l1 = L(('e1',), lambda: text_layer('FOLLOW', fMb(42), WHITE, shadow=False, spacing=18))
        l2 = L(('e2',), lambda: gradient_text('HOW IS TRAVELLERS LIFE', fA(84), (255, 230, 120), (255, 120, 30), spacing=3))
        l3 = L(('e3',), lambda: text_layer('asli travel guides ke liye', fP(38), WHITE, shadow=False))
        paste_c(frame, l1, W / 2, y0 + 60, 1, k); paste_c(frame, l2, W / 2, y0 + 145, 1, k); paste_c(frame, l3, W / 2, y0 + 235, 1, k)
    return frame

# ---------------- main loop ----------------
def shot_at(t):
    for s in SHOTS:
        if s[0] <= t < s[1]: return s
    return SHOTS[-1]

def render(t, aroll_img, sheesh_img=None):
    s = shot_at(t)
    if s[2] == 'video': sheesh_img = vframe(s)
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
    else:
        frame = zoom_img(sheesh_img, (z0 + (z1 - z0) * pe) + (punch - 1))
    frame = grade(frame)
    frame = overlays(frame, t, mask)
    # flash at cut
    fl = 0
    for c in CUTS:
        if 0 <= t - c < 0.12: fl = max(fl, 0.55 * (1 - (t - c) / 0.12))
    if 0 <= t - 8.30 < 0.15: fl = max(fl, 0.8 * (1 - (t - 8.30) / 0.15))
    if 0 <= t - 17.0 < 0.15: fl = max(fl, 0.8 * (1 - (t - 17.0) / 0.15))
    if fl > 0: frame = Image.blend(frame, Image.new('RGB', (W, H), (255, 248, 235)), fl)
    if t >= 0.15: brand_tag(frame, t) if not (t >= 39.5) else None
    draw_captions(frame, t, CAPY.get(s[0], 1390))
    progress(frame, t)
    # fade in/out
    if t < 0.15: frame = Image.blend(Image.new('RGB', (W, H)), frame, t / 0.15)
    return frame

# ---------------- face-aware caption placement ----------------
import cv2, os
CASC = [cv2.CascadeClassifier(cv2.data.haarcascades + n) for n in ('haarcascade_frontalface_default.xml', 'haarcascade_profileface.xml')]
def faces(img):
    g = cv2.cvtColor(np.asarray(img.resize((540, 960))), cv2.COLOR_RGB2GRAY)
    g = cv2.equalizeHist(g)
    out = []
    for c in CASC:
        for flip in (False, True):
            gg = cv2.flip(g, 1) if flip else g
            for (x, y, w, h) in c.detectMultiScale(gg, 1.08, 7, minSize=(34, 34)):
                if flip: x = 540 - x - w
                out.append((x * 2, (y - 0.45 * h) * 2, (x + w) * 2, (y + h * 1.3) * 2))
    return out
RESERVED = [
    (0.0, 2.1, 200, 800), (2.1, 4.9, 300, 620), (4.9, 8.3, 200, 880), (8.3, 12.4, 220, 620), (12.4, 17.0, 240, 600),
    (17.0, 23.9, 220, 950), (23.9, 31.8, 220, 720), (31.8, 37.1, 220, 810), (37.1, 39.5, 230, 420), (39.5, 99, 300, 1500)]
CANDS = [1390, 1530, 1250, 1110, 1630, 960, 820, 330]
def base_for(shot, t):
    st, en, kind, src, z0, z1, c0, c1 = shot
    pe = ease_io((t - st) / ((min(en, DUR)) - st)); z = z0 + (z1 - z0) * pe
    if kind == 'photo':
        cx = c0[0] + (c1[0] - c0[0]) * pe; cy = c0[1] + (c1[1] - c0[1]) * pe
        return photo_frame(src, z, cx, cy)
    if kind == 'aroll':
        return zoom_img(grab(U + '193c93de-Aamer.mp4', t, f'scale={W}:{H}'), z)
    path, ss, vf = vspec(src)
    return zoom_img(grab(path, ss + t - st, vf.replace(f'fps={FPS},', '')), z)
CAPY = {}
cache_f = S + '/pcapy.json'
if os.path.exists(cache_f) and os.path.getmtime(cache_f) > os.path.getmtime(__file__):
    CAPY = {float(k): v for k, v in json.load(open(cache_f)).items()}
else:
    for sh in SHOTS:
        st, en = sh[0], min(sh[1], DUR)
        boxes = []
        if sh[2] == 'aroll':
            CAPY[st] = 1390; continue
        for f in (0.1, 0.35, 0.6, 0.9):
            b = base_for(sh, st + (en - st) * f)
            if isinstance(b, tuple):
                img, m = b; ma = np.asarray(m)
                for bx in faces(img):
                    cx_, cy_ = int((bx[0] + bx[2]) / 2), int(min(H - 1, (bx[1] + bx[3]) / 2))
                    if ma[cy_, min(W - 1, cx_)] > 128: boxes.append(bx)
            else:
                boxes += faces(b)
        res = [(a, b) for (t0, t1, a, b) in RESERVED if t0 < en and t1 > st]
        def cost(cy):
            y0, y1 = cy - 80, cy + 80
            c = sum(max(0, min(y1, b[3]) - max(y0, b[1])) for b in boxes) * 3
            c += sum(max(0, min(y1, b) - max(y0, a)) for a, b in res) * 2
            return c + abs(cy - 1390) * 0.05
        CAPY[st] = min(CANDS, key=cost)
        print('shot', st, 'faces', [tuple(int(v) for v in b) for b in boxes][:6], '->', CAPY[st], flush=True)
    json.dump(CAPY, open(cache_f, 'w'))

N = int(DUR * FPS)
if MODE == 'stills':
    ts = [float(x) for x in sys.argv[3].split(',')]
    fi = 0; want = sorted(int(x * FPS) for x in ts)
    for i in range(max(want) + 1):
        a = aroll.read(); t = i / FPS
        if i not in want and shot_at(t)[2] == 'video': vframe(shot_at(t))
        if i in want:
          fr = render(t, a)
          if i in want:
            fr.save(f'{S}/frames/still_{t:05.2f}.jpg', quality=88); print('still', t, flush=True)
    sys.exit()

enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
for i in range(N):
    t = i / FPS
    a = aroll.read()
    enc.stdin.write(render(t, a).tobytes())
    if i % 150 == 0: print('frame', i, '/', N, flush=True)
enc.stdin.close(); enc.wait()
print('done')
