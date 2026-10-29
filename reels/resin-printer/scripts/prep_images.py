"""Prepare still assets: crop phone screenshots, cut the printer out of its white
background, and build the illustrative 'photo -> resin miniature' still."""
import numpy as np
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from scipy import ndimage

A = Path(__file__).resolve().parent.parent / "assets" / "images"

def cutout_white(img, thr=238, feather=2):
    """Remove the near-white background connected to the image border."""
    rgb = np.asarray(img.convert("RGB")).astype(np.int16)
    light = (rgb.min(axis=2) >= thr)
    lab, _ = ndimage.label(light)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    # also drop enclosed pure-white holes (e.g. gaps between a figure's legs)
    pure = (rgb.min(axis=2) >= 246)
    lab2, n2 = ndimage.label(pure)
    sizes = ndimage.sum(pure, lab2, range(1, n2 + 1))
    big = [i + 1 for i, v in enumerate(sizes) if v > 40]
    holes = np.isin(lab2, big)
    hh, ww = holes.shape
    holes[:, int(ww * 0.30):] = False      # keep the white ANYCUBIC logo on the printer
    holes[: int(hh * 0.45), :] = False
    bg |= holes
    alpha = (~bg).astype(np.uint8) * 255
    a = Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(feather))
    out = img.convert("RGBA"); out.putalpha(a)
    return out.crop(out.getbbox())

# 1) Hero printer + figurine (Amazon app screenshot -> drop orange header + thumbnails)
hero = Image.open(A / "raw_printer_hero.png").convert("RGB")
w, h = hero.size
s = w / 923
hero = hero.crop((0, int(470 * s), w, int(1570 * s)))
hero_cut = cutout_white(hero)
hero_cut.save(A / "printer_hero_cutout.png")
# separate pieces for animation
W, H = hero_cut.size
fig = hero_cut.crop((0, int(H * 0.28), int(W * 0.292), H))
fa = np.asarray(fig.getchannel("A")).astype(np.float32)
fw = fa.shape[1]; ramp = np.clip((fw - np.arange(fw)) / (fw * 0.10), 0, 1)
fig.putalpha(Image.fromarray((fa * ramp[None, :]).astype(np.uint8)))
fig.crop(fig.getbbox()).save(A / "figurine_cutout.png")

# 2) 10K LCD banner
lcd = Image.open(A / "raw_lcd_10k.png").convert("RGB")
w, h = lcd.size; s = w / 923
lcd.crop((0, int(560 * s), w, int(1480 * s))).save(A / "lcd_10k_banner.jpg", quality=93)
# angel model only (the dark panel)
lcd.crop((int(40 * s), int(866 * s), int(890 * s), int(1446 * s))).save(A / "angel_detail.jpg", quality=93)

# 3) Build size + package images are clean already, just normalise
Image.open(A / "raw_build_size.jpg").convert("RGB").save(A / "build_size.jpg", quality=93)
Image.open(A / "raw_package.jpg").convert("RGB").save(A / "package_contents.jpg", quality=93)

# 4) Illustrative 'resin miniature' version of the creator photo (grey resin look)
src = Image.open(A / "creator_ref_2.png").convert("RGB")
w, h = src.size
bust = src.crop((int(w * 0.18), int(h * 0.17), int(w * 0.84), int(h * 0.62)))
g = ImageOps.grayscale(bust).filter(ImageFilter.MedianFilter(9))
g = ImageOps.autocontrast(g, cutoff=2)
g = g.point(lambda v: int(round(v / 32) * 32 * 0.85 + v * 0.15))  # soft posterise = sculpted planes
g = g.filter(ImageFilter.GaussianBlur(1.5))
emb = g.filter(ImageFilter.EMBOSS).filter(ImageFilter.GaussianBlur(1))
mix = Image.blend(g, emb, 0.38)
mix = ImageEnhance.Contrast(mix).enhance(1.35)
tint = ImageOps.colorize(mix, black="#18222e", mid="#8696a8", white="#eef2f6").convert("RGBA")
# oval vignette so it reads as a bust, not a photo
bw, bh = tint.size
yy, xx = np.mgrid[0:bh, 0:bw]
d = ((xx - bw / 2) / (bw * 0.36)) ** 2 + ((yy - bh * 0.50) / (bh * 0.52)) ** 2
m = np.clip((1.0 - d) / 0.18, 0, 1)
tint.putalpha(Image.fromarray((m * 255).astype(np.uint8)))
tint.save(A / "creator_resin_style.png")
bust.save(A / "creator_photo_crop.jpg", quality=92)
print("ok", hero_cut.size)
