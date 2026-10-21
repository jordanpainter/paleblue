"""The Pale Blue cover: remove_blastoise.py's title-less box, Snom's official artwork where
Blastoise stood, and "PALE BLUE VERSION" in the box's own lettering.

The title font isn't one we have, so PALE is built from letters already in "BLUE VERSION":
L and E as they are, P is the B with its lower bowl cut away, A is the V flipped with a
crossbar. Every letter is re-edged the same way (black outline, drop shadow), so they match.
Run: .venv/bin/python art/cover/boxedit/build_cover.py   (after remove_blastoise.py)
"""
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
orig = cv2.imread(str(HERE / "original.jpg")).astype(np.float32)

# glyph white, as a soft mask: 0 on the black edging, 1 on the white fill
TOP, BOT = 782, 836
white = np.clip((orig[TOP:BOT].min(axis=2) - 90) / 110, 0, 1)
white[:3] = white[-3:] = 0  # specks from the art above and below the line
COLS = {"B": (418, 440), "L": (440, 457), "U": (456, 477), "E": (477, 497), "V": (506, 531),
        "R": (548, 571), "S": (570, 589), "I": (588, 598), "O": (598, 622), "N": (622, 646)}


def glyph(ch):
    x0, x1 = COLS[ch]
    return white[:, x0:x1].copy()


def make_p():
    g = glyph("B")
    cols = (g > 0.5).sum(axis=0)
    full = cols > 0.9 * cols.max()
    stem = int(np.argmax(full))
    while full[stem]:  # right edge of the B's stem (its bowls are nearly as tall, so stop at the first gap)
        stem += 1
    bars = g[:, stem + 1:stem + 4].mean(axis=1) > 0.5  # top, middle and bottom bars of the B
    mid = g.shape[0] // 2
    while bars[mid]:  # walk down to the bottom edge of the middle bar
        mid += 1
    g[mid:, stem:] = 0
    return g


def make_a():
    g = glyph("V")[::-1].copy()
    h = g.shape[0]
    y0, y1 = int(h * 0.62), int(h * 0.72)
    for y in range(y0, y1):
        xs = np.nonzero(g[y] > 0.5)[0]
        if len(xs):
            g[y, xs.min():xs.max() + 1] = 1
    return g


GLYPHS = {"P": make_p(), "A": make_a()}
GAP, SPACE = 2, 12


def word(text):
    parts = []
    for ch in text:
        if ch == " ":
            parts.append(np.zeros((BOT - TOP, SPACE), np.float32))
        else:
            g = GLYPHS.get(ch, glyph(ch) if ch in COLS else None)
            parts += [g, np.zeros((BOT - TOP, GAP), np.float32)]
    return np.hstack(parts)


def edged_layer(fill):
    """White fill, black outline and a down-right shadow, like the box's lettering."""
    pad = 8
    f = np.pad(fill, pad)
    outline = cv2.dilate(f, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    shadow = np.roll(np.roll(outline, 2, 0), 2, 1)
    black = np.maximum(outline, shadow)
    rgb = np.dstack([f * 255] * 3)
    alpha = np.maximum(black, f)
    return rgb, alpha


def paste(base, rgb, alpha, x, y):
    h, w = alpha.shape
    region = base[y:y + h, x:x + w]  # clipped at the box's edges
    h, w = region.shape[:2]
    a = alpha[:h, :w, None]
    base[y:y + h, x:x + w] = region * (1 - a) + rgb[:h, :w] * a


def build(variant):
    base = cv2.imread(str(HERE / f"blank_{variant}.png")).astype(np.float32)
    H, W = base.shape[:2]

    # Snom: official art, scaled into the space Blastoise filled, with a soft shadow under it
    snom = cv2.imread(str(HERE / "snom_src" / "snom.png"), cv2.IMREAD_UNCHANGED).astype(np.float32)
    ys, xs = np.nonzero(snom[..., 3] > 8)
    snom = snom[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    sw = 600
    sh = round(snom.shape[0] * sw / snom.shape[1])
    a = snom[..., 3:] / 255
    premult = np.dstack([snom[..., :3] * a, a])  # resize premultiplied, so edges don't fringe
    premult = cv2.resize(premult, (sw, sh), interpolation=cv2.INTER_CUBIC)
    a_new = np.clip(premult[..., 3], 0, 1)
    snom = np.dstack([np.clip(premult[..., :3] / np.maximum(a_new, 1e-3)[..., None], 0, 255), a_new * 255])
    sx, sy = 236, 760 - sh
    a = np.clip(snom[..., 3] / 255, 0, 1)
    pad = 50  # room for the blur, so the shadow doesn't stop at a hard edge
    shade = cv2.GaussianBlur(np.pad(a, pad), (0, 0), 14) * 0.35
    paste(base, np.zeros((*shade.shape, 3), np.float32), shade, sx + 10 - pad, sy + 14 - pad)
    paste(base, snom[..., :3], a, sx, sy)

    # title, centred where "BLUE VERSION" sat
    rgb, alpha = edged_layer(word("PALE BLUE VERSION"))
    cx = 532
    paste(base, rgb, alpha, cx - alpha.shape[1] // 2, TOP + 8)
    return base.astype(np.uint8)


for v in ("original_blue", "lighter_a", "lighter_b"):
    cv2.imwrite(str(HERE / f"pale_blue_cover_{v}.png"), build(v))
print("wrote pale_blue_cover_*.png")
