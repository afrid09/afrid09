"""Generate card-dark.svg and card-light.svg: an ASCII portrait plus a neofetch-style card.

Usage:
    pip install pillow rembg onnxruntime opencv-python-headless numpy
    python scripts/make_card.py

Edit LINES below to change what the card says.
"""

from pathlib import Path
from xml.sax.saxutils import escape

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from rembg import new_session, remove

ROOT = Path(__file__).resolve().parent.parent
PHOTO = ROOT / "assets" / "profile.jpg"

TITLE = "afrid09@prod"
LINES = [
    ("OS", "Distributed Systems (mostly up)"),
    ("Host", "Austin, TX · runs on breakfast tacos"),
    ("Uptime", "5+ years in prod, 0 outages I'll admit to"),
    ("Kernel", "Java · Go · TypeScript · Python"),
    ("Shell", "retry --exponential-backoff --jitter"),
    ("Delivery", "at-least-once (sorry for the duplicates)"),
    ("Consistency", "eventual. same goes for my replies"),
    ("Idempotency", "say hi twice, I'll only wave once"),
    ("Packages", "Kafka, Postgres, Redis, AWS, too much YAML"),
    ("Debugger", 'console.log("here 2")'),
    ("Fuel", "chai, horizontally scaled"),
    ("Currently", "reading Cadence internals at 2 a.m."),
    ("Famous words", '"works on my machine"'),
    None,
    ("GitHub", "github.com/afrid09"),
    ("LinkedIn", "linkedin.com/in/afrid-abdul-shaik"),
]

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", art="#c9d1d9", title="#58a6ff",
                 key="#ffa657", value="#c9d1d9", dots="#484f58"),
    "light": dict(bg="#ffffff", border="#d0d7de", art="#24292f", title="#0969da",
                  key="#953800", value="#24292f", dots="#afb8c1"),
}
PALETTE = ["#f85149", "#ffa657", "#e3b341", "#3fb950", "#58a6ff", "#bc8cff", "#ff7b72", "#8b949e"]

COLS = 76
RAMP = " .:-=+*#%@"
ART_FONT, ART_CHAR_W, ART_LINE_H = 9, 5.4, 9.6
TXT_FONT, TXT_CHAR_W, TXT_LINE_H = 14, 8.43, 21
KEY_WIDTH = 14  # key + dot leader width, in characters


def ascii_rows(dense_is_bright: bool) -> list[str]:
    cut = remove(Image.open(PHOTO), session=new_session("u2net_human_seg")).convert("RGBA")
    cut = cut.crop(cut.getbbox())
    cut = cut.crop((round(cut.width * 0.1), 0, round(cut.width * 0.9), round(cut.height * 0.7)))  # head and shoulders
    w, h = cut.size
    rows = round(COLS * (h / w) * (ART_CHAR_W / ART_LINE_H))
    small = cut.resize((COLS, rows), Image.LANCZOS)
    alpha = small.split()[-1]
    big = ImageOps.grayscale(cut.convert("RGB"))
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6, 6))
    big = Image.fromarray(clahe.apply(np.array(big)))
    gray = big.resize((COLS, rows), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1, 120, 1))
    fg = [g for g, a in zip(gray.get_flattened_data(), alpha.get_flattened_data()) if a > 110]
    lo, hi = sorted(fg)[len(fg) // 50], sorted(fg)[-len(fg) // 50]
    out = []
    for y in range(rows):
        line = ""
        for x in range(COLS):
            if alpha.getpixel((x, y)) <= 110:
                line += " "
                continue
            v = min(max((gray.getpixel((x, y)) - lo) / max(hi - lo, 1), 0), 1)
            density = v if dense_is_bright else 1 - v
            line += RAMP[max(1, round(density * (len(RAMP) - 1)))]
        out.append(line.rstrip())
    return out


def tspan(x, text, color, weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    return f'<tspan x="{x:.1f}" fill="{color}"{w}>{escape(text)}</tspan>'


def build(theme: str) -> str:
    c = THEMES[theme]
    art = ascii_rows(dense_is_bright=(theme == "dark"))
    pad = 28
    art_w = COLS * ART_CHAR_W
    art_h = len(art) * ART_LINE_H
    tx = pad + art_w + 36
    text_lines = 2 + len(LINES) + 2
    text_h = text_lines * TXT_LINE_H
    width = round(tx + 58 * TXT_CHAR_W + pad)
    height = round(max(art_h, text_h) + pad * 2)
    art_y = pad + (height - pad * 2 - art_h) / 2 + ART_FONT
    ty = pad + (height - pad * 2 - text_h) / 2 + TXT_FONT

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="afrid09 profile card">',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" '
        f'fill="{c["bg"]}" stroke="{c["border"]}"/>',
        '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;'
        'white-space:pre}</style>',
        f'<text font-size="{ART_FONT}" fill="{c["art"]}" xml:space="preserve">',
    ]
    for i, row in enumerate(art):
        parts.append(f'<tspan x="{pad}" y="{art_y + i * ART_LINE_H:.1f}">{escape(row)}</tspan>')
    parts.append("</text>")

    parts.append(f'<text font-size="{TXT_FONT}" xml:space="preserve">')
    y = ty
    parts.append(f'<tspan y="{y:.1f}">{tspan(tx, TITLE, c["title"], "bold")}</tspan>')
    y += TXT_LINE_H
    parts.append(f'<tspan y="{y:.1f}">{tspan(tx, "─" * len(TITLE), c["dots"])}</tspan>')
    for item in LINES:
        y += TXT_LINE_H
        if item is None:
            continue
        key, value = item
        dots = " " + "." * max(KEY_WIDTH - len(key) - 2, 1) + " "
        parts.append(
            f'<tspan x="{tx:.1f}" y="{y:.1f}"><tspan fill="{c["key"]}" font-weight="bold">{escape(key)}:</tspan>'
            f'<tspan fill="{c["dots"]}">{dots}</tspan><tspan fill="{c["value"]}">{escape(value)}</tspan></tspan>'
        )
    parts.append("</text>")

    y += TXT_LINE_H
    for i, color in enumerate(PALETTE):
        parts.append(f'<rect x="{tx + i * 26:.1f}" y="{y - 4:.1f}" width="24" height="14" rx="2" fill="{color}"/>')

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    for theme in THEMES:
        (ROOT / f"card-{theme}.svg").write_text(build(theme), encoding="utf-8")
        print(f"wrote card-{theme}.svg")
