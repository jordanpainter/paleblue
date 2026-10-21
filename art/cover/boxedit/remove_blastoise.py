"""Pokémon Blue box art (jadelune's HQ fan recreation, art/cover/boxedit/original.jpg) with
Blastoise taken out and the blue lightened.

Blastoise's blues run into the background's, so it can't be masked out by colour. Instead the
artwork area gets a fresh radial glow like the original's (lighter), and the parts worth
keeping are laid back on top: the side bar, the logo (traced by its outline, then filled),
the TM mark, the white lettering with its dark edging, and the two badges.
Where Blastoise overlapped something it gets rebuilt: the claw over the GAME BOY bar (letters
redrawn from their measured edges, brushed grey borrowed from lower down the same column) and
the "ERS" of MONSTERS (copied from "VERSION" on the same line).
Run: .venv/bin/python art/cover/boxedit/remove_blastoise.py
"""
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
img = cv2.imread(str(HERE / "original.jpg"))
H, W = img.shape[:2]
yy, xx = np.mgrid[0:H, 0:W]


def grow(mask, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.dilate(mask.astype(np.uint8), k).astype(bool)


def fill_holes(mask):
    """Everything enclosed by the mask, found by flooding the outside from a corner."""
    m = mask.astype(np.uint8) * 255
    flood = m.copy()
    cv2.floodFill(flood, np.zeros((H + 2, W + 2), np.uint8), (W - 1, H - 1), 255)
    return mask | (flood == 0)


def rect(x0, y0, x1, y1):
    return (xx >= x0) & (xx <= x1) & (yy >= y0) & (yy <= y1)


# --- the claw over the bar: repaint the "E" and "M" corners it hides
claw = np.zeros((H, W), np.uint8)
cv2.fillPoly(claw, [np.array([(192, 436), (185, 443), (150, 473), (132, 498), (123, 525), (122, 565),
                              (129, 587), (150, 594), (160, 594), (185, 599), (192, 599)], np.int32)], 1)
claw = grow(claw, 6) & (xx < 186)
b, g, r = (img[..., i].astype(int) for i in range(3))
navy = (b > 100) & (r < 90) & (g < 80)


def bar_letter(x, y):
    """Measured from the visible parts: E's arm and spine, M's leg, and M's diagonal to its tip."""
    if x > 162:
        return False
    top, bottom = 560 + (x - 120) * 31 / 40, 604 - (x - 120) * 8 / 40
    return ((x >= 132 and 428 <= y <= 502) or 472 <= y <= 501 or 512 <= y <= 538
            or (x >= 100 and top <= y <= bottom))


src = img.copy()
ys, xs = np.nonzero(claw)
for x in np.unique(xs):
    col = src[620:800, x]
    col_hsv = cv2.cvtColor(col[None], cv2.COLOR_BGR2HSV)[0]
    grey = col[(col_hsv[:, 1] < 20) & (col_hsv[:, 2] > 170)]
    for y in ys[xs == x]:
        if x >= 185:
            img[y, x] = src[y + 180, x]  # the bar's blue edge, same column further down
        elif bar_letter(x, y):
            img[y, x] = (136, 31, 28)
        else:
            img[y, x] = grey[(y - 430) % len(grey)]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL).astype(np.int32)
h = hsv[..., 0] * 360 // 256
s = hsv[..., 1] / 255
v = hsv[..., 2] / 255

bar = xx < 186  # the grey ends at x=185; the blue past it is background

# logo: yellow, its blue outline and darker 3D edge (hue 213-250, unlike the cyan-leaning
# background at ~203 or the pale halo), plus near-black; fill inside, drop specks
yellow = (h >= 38) & (h <= 56) & (s > 0.75) & (v > 0.8)
zone = grow(yellow, 40) & (yy < 262) & (xx >= 200)
logo_blue = (h >= 213) & (h <= 250) & (s > 0.45) & (s < 0.9)
logo = cv2.morphologyEx((zone & (yellow | logo_blue | (v < 0.25))).astype(np.uint8), cv2.MORPH_CLOSE,
                        np.ones((5, 5), np.uint8))
logo = cv2.morphologyEx(logo, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(logo, 8)
has_yellow = np.bincount(lab[yellow], minlength=n)
logo = fill_holes(np.isin(lab, [i for i in range(1, n) if st[i][4] > 3000 and has_yellow[i] > 50]))
tm = rect(835, 222, 880, 248) & (v > 0.75) & (s < 0.25)


def letters(box, max_h, max_w, min_area):
    """White glyphs: letter-sized white blobs inside the box, not touching its edge (shell bands do)."""
    x0, y0, x1, y1 = box
    white = rect(*box) & (s < 0.2) & (v > 0.78)
    n, lab, st, _ = cv2.connectedComponentsWithStats(white.astype(np.uint8), 8)
    out = np.zeros((H, W), bool)
    for i in range(1, n):
        x, y, w, hh, a = st[i]
        inside = x > x0 and y > y0 and x + w - 1 < x1 and y + hh - 1 < y1
        if inside and hh <= max_h and w <= max_w and a >= min_area:
            out |= lab == i
    return out


def edged(glyphs, edge):
    """The glyphs plus their dark outline and drop shadow."""
    return glyphs | (grow(glyphs, edge) & (v < 0.5))




def outlined(box):
    """Lettering with a thick dark outline: drop thin art lines, close gaps, fill what's enclosed,
    then keep only its white and dark pixels (and any blob that has white in it)."""
    dark = (rect(*box) & (v < 0.3)).astype(np.uint8)
    opened = cv2.morphologyEx(dark, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    thick = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    flood = thick * 255
    cv2.floodFill(flood, np.zeros((H + 2, W + 2), np.uint8), (0, 0), 255)
    white = (s < 0.2) & (v > 0.78)
    filled = (thick > 0) | (flood == 0)
    m = filled & (white | (grow(white & filled, 5) & grow(opened, 1) & (v < 0.45)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    has_white = np.bincount(lab[white & m], minlength=n)
    return np.isin(lab, np.nonzero(has_white >= 10)[0]) & m


tagline = outlined((372, 222, 782, 330)) & (xx >= 381)  # stray shell lines left of the G
bottom = edged(letters((335, 775, 735, 880), 60, 80, 8), 3)

# "MONSTERS" ends on a white claw (whose outline also cuts through its T), so its TERS gets
# rebuilt from the same line: T from "TO", ERS from "VERSION". Whole patches, so edges blend into blue.
patched = np.zeros((H, W), bool)
for (x0, x1), dx in (((499, 507), 165), ((447, 472), 224)):
    dy = -2
    img[841 + dy:875 + dy, x0 + dx:x1 + dx] = img[841:875, x0:x1]
    patched |= np.roll(np.roll(bottom & rect(x0, 841, x1 - 1, 874), dy, 0), dx, 1)
bottom = (bottom & ~rect(664, 836, 712, 878)) | patched

esrb = fill_holes(rect(205, 728, 322, 878) & (v < 0.3) & grow(rect(205, 728, 322, 878) & (v > 0.9), 6))
red = ((h >= 340) | (h <= 12)) & (s > 0.55) & (v > 0.5)
pill = fill_holes(grow(red & rect(733, 828, 885, 872), 1)) & rect(733, 828, 885, 872)
# the tagline's own edging is ragged where it met the shell, so it gets a fresh, even one
tag_fill = tagline * np.clip((img.min(axis=2).astype(np.float32) - 120) / 100, 0, 1)
n, lab, st, _ = cv2.connectedComponentsWithStats((tag_fill > 0.5).astype(np.uint8), 8)
tag_fill *= grow(np.isin(lab, [i for i in range(1, n) if st[i][4] >= 25]), 1)  # drop stray specks
tag_edge = cv2.dilate(tag_fill, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
tag_edge = cv2.GaussianBlur(tag_edge, (0, 0), 0.7)
keep = bar | logo | tm | bottom | esrb | pill


def glow(center, edge):
    """The box's radial light: bright behind where Blastoise stood, deep blue at the edges."""
    cx, cy, rad = 560, 500, 640
    t = np.clip(np.hypot(xx - cx, yy - cy) / rad, 0, 1)[..., None] ** 0.9
    return (np.array(center, np.float32) * (1 - t) + np.array(edge, np.float32) * t)


def compose(center, edge, keep=keep):
    bg = glow(center, edge)
    halo = cv2.GaussianBlur(logo.astype(np.float32), (0, 0), 9)[..., None] * 0.85  # the box's glow behind the logo
    bg = bg * (1 - halo) + 255 * halo
    k = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 0.8)[..., None]
    out = img.astype(np.float32) * k + bg * (1 - k)
    out *= 1 - tag_edge[..., None]
    out = out * (1 - tag_fill[..., None]) + 255 * tag_fill[..., None]
    return out.astype(np.uint8)


# BGR colours sampled from the original (glow ~ (209,149,1), edge ~ (144,74,20)), then lifted
variants = {
    "original_blue": ((238, 195, 70), (95, 30, 5)),
    "lighter_a": ((252, 228, 160), (125, 55, 12)),
    "lighter_b": ((254, 242, 205), (160, 90, 30)),
}
outs = {}
for name, (c, e) in variants.items():
    outs[name] = compose(c, e)
    cv2.imwrite(str(HERE / f"no_blastoise_{name}.png"), outs[name])
    # same, minus "BLUE VERSION" and the "link to Red" line, as the base for build_cover.py's new title
    cv2.imwrite(str(HERE / f"blank_{name}.png"), compose(c, e, keep & ~rect(335, 760, 730, 880)))
cv2.imwrite(str(HERE / "keep_mask.png"), keep.astype(np.uint8) * 255)
half = [cv2.resize(o, (W // 2, H // 2), interpolation=cv2.INTER_AREA) for o in outs.values()]
cv2.imwrite(str(HERE / "compare.png"), np.hstack(half))
print("wrote", ", ".join(f"no_blastoise_{n}.png" for n in variants), "and compare.png")
