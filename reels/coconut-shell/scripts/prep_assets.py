"""Crops logo and QR codes, grabs a product still for the plan card, and checks the QR codes scan."""
import subprocess
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent; A = ROOT / "assets" / "images"
logo = Image.open(A / "raw_logo.png").convert("RGBA"); logo.crop(logo.getbbox()).save(A / "logo.png")
Image.open(A / "raw_qr_youtube.jpg").convert("RGB").crop((235, 490, 1055, 1310)).save(A / "qr_youtube.png")
Image.open(A / "raw_qr_telegram.jpg").convert("RGB").crop((300, 255, 990, 945)).save(A / "qr_telegram.png")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "6.5", "-i", str(ROOT / "assets/source/broll_c4_products.mp4"),
                "-frames:v", "1", "-q:v", "2", str(A / "products.jpg")], check=True)
try:
    import zxingcpp
    for n in ("qr_youtube.png", "qr_telegram.png"):
        r = zxingcpp.read_barcodes(Image.open(A / n)); print(n, "->", r[0].text if r else "NOT DECODED")
except ImportError:
    print("zxing-cpp not installed; skipped QR check")
