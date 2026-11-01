"""Crops logo, QR codes and the plan-poster pieces, and checks the QR codes still scan."""
from pathlib import Path
from PIL import Image
A = Path(__file__).resolve().parent.parent / "assets" / "images"
logo = Image.open(A / "raw_logo.png").convert("RGBA"); logo.crop(logo.getbbox()).save(A / "logo.png")
Image.open(A / "raw_qr_youtube.jpg").convert("RGB").crop((235, 490, 1055, 1310)).save(A / "qr_youtube.png")
Image.open(A / "raw_qr_telegram.jpg").convert("RGB").crop((300, 255, 990, 945)).save(A / "qr_telegram.png")
poster = Image.open(A / "raw_poster.png").convert("RGB")             # 1087x1447 plan poster
poster.save(A / "poster.jpg", quality=93)
poster.crop((380, 560, 1087, 1050)).save(A / "product.jpg", quality=93)   # temple + flowers + agarbatti bag
try:
    import zxingcpp
    for n in ("qr_youtube.png", "qr_telegram.png"):
        r = zxingcpp.read_barcodes(Image.open(A / n)); print(n, "->", r[0].text if r else "NOT DECODED")
except ImportError:
    print("zxing-cpp not installed; skipped QR check")
