"""Crops the brand assets (logo, QR codes, poster jars) and checks that the
cropped QR codes still scan. Also renders the plan PDF pages to PNG."""
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "assets" / "images"

# logo: already transparent, just trim
logo = Image.open(A / "raw_logo.png").convert("RGBA")
logo.crop(logo.getbbox()).save(A / "logo.png")

# QR codes: keep a generous white quiet zone around the code
yt = Image.open(A / "raw_qr_youtube.jpg").convert("RGB")      # 1290x1450, white page
yt.crop((235, 490, 1055, 1310)).save(A / "qr_youtube.png")
tg = Image.open(A / "raw_qr_telegram.jpg").convert("RGB")     # white rounded card on dark bg
tg.crop((300, 255, 990, 945)).save(A / "qr_telegram.png")

# three flavour jars from the plan poster
poster = Image.open(A / "raw_poster.png").convert("RGB")
poster.crop((400, 650, 1086, 1110)).save(A / "jars.jpg", quality=93)

# PDF pages
pdf = ROOT / "assets" / "source" / "Butter_Candle_Plan.pdf"
out = ROOT / "assets" / "pdf_pages"
out.mkdir(exist_ok=True)
if not (out / "page-01.png").exists():
    subprocess.run(["pdftoppm", "-r", "150", "-png", str(pdf), str(out / "page")], check=True,
                   stderr=subprocess.DEVNULL)

try:
    import zxingcpp  # pip install zxing-cpp
    for n in ("qr_youtube.png", "qr_telegram.png"):
        r = zxingcpp.read_barcodes(Image.open(A / n))
        print(n, "->", r[0].text if r else "NOT DECODED")
except ImportError:
    print("zxing-cpp not installed; skipped QR check")
