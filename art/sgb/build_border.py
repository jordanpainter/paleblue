"""Pale Blue's Super Game Boy border, from Blue's.

Starts from the vanilla border (art/sgb/blue_border_vanilla.png + .tilemap), then:
- the title reads "PALE BLUE" (P and A drawn to match Blue's B, L, U, E tiles),
- the four circles hold Snom poses (happy, look-back, alert, sleepy) in the border's own blues
  (palette PAL_SGB1: 0 backdrop, 1 mid blue, 2 navy, 3 light blue),
then cuts the 256x224 picture back into tiles (deduplicated, flips allowed) and writes
gfx/sgb/blue_border.png and gfx/sgb/blue_border.tilemap. The game copies 128 tiles.
Run: .venv/bin/python art/sgb/build_border.py
"""
from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from render_border import render, tiles  # noqa: E402

VANILLA_PNG, VANILLA_MAP = HERE / "blue_border_vanilla.png", HERE / "blue_border_vanilla.tilemap"
FRONT = ROOT / "gfx/pokemon/front"
PAL1 = 4  # border palette number of PAL_SGB1

# --- start: vanilla border as colour indices + a palette per tile
ts = tiles(VANILLA_PNG)
d = VANILLA_MAP.read_bytes()
idx = np.zeros((224, 256), int)
pal = np.zeros((28, 32), int)
for i in range(896):
    t, a = d[2 * i], d[2 * i + 1]
    r, c = divmod(i, 32)
    tile = ts[t]
    if a & 0x40: tile = tile[:, ::-1]
    if a & 0x80: tile = tile[::-1]
    idx[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = tile
    pal[r, c] = (a >> 2) & 7

# --- title: "(ball) PALE BLUE" on row 3, centred like Blue's
P = ["22222222", "2.....22", "2..22..2", "2.....22", "2..22222", "2..21111", "12221111", "11111111"]
A = ["22222222", "22....22", "2..22..2", "2......2", "2..22..2", "2..22..2", "12211221", "11111111"]


def drawn(rows):
    return np.array([[".123".index(ch) for ch in row] for row in rows])


space = idx[24:32, 12 * 8:13 * 8].copy()  # the stripes beside the vanilla title, so the lines run through
title = [ts[0x1b], drawn(P), drawn(A), ts[0x18], ts[0x1a], space, ts[0x17], ts[0x18], ts[0x19], ts[0x1a]]
for k, tile in enumerate(title):
    c = 11 + k
    idx[24:32, c * 8:c * 8 + 8] = tile
    pal[3, c] = PAL1

# --- circles: repaint in PAL_SGB1, widen the white middle, sit a Snom in it
NEAREST = {(248, 232, 248): 0, (82, 139, 213): 1, (41, 74, 164): 2, (131, 164, 222): 3}
SHADE = {255: None, 170: 3, 85: 1, 0: 2}  # sprite white stays see-through
CIRCLES = [  # tile box (col, row, w, h), centre of the white middle, sprite, keep its extras?, nudge right
    ((0, 5, 5, 7), (19, 67), "snom_pose_happy.png", True, 2),
    ((27, 5, 5, 7), (235, 67), "snom_pose_look_back.png", True, 0),
    ((0, 16, 5, 7), (19, 155), "snom_pose_surprised.png", False, 2),  # no "!" either
    ((27, 16, 5, 7), (235, 155), "snom_pose_sleepy.png", False, 0),  # no Zs: no room; flipped below to face like look-back
]
rgb = render(VANILLA_PNG, VANILLA_MAP).astype(int)
yy, xx = np.mgrid[0:224, 0:256]
for (c0, r0, w, h), (cx, cy), sprite, extras, nudge in CIRCLES:
    ys, xs = slice(r0 * 8, (r0 + h) * 8), slice(c0 * 8, (c0 + w) * 8)
    region = rgb[ys, xs]
    keys = np.array(list(NEAREST))
    near = np.abs(region[..., None, :] - keys[None, None]).sum(-1).argmin(-1)
    idx[ys, xs] = np.array(list(NEAREST.values()))[near]
    pal[r0:r0 + h, c0:c0 + w] = PAL1
    dist = np.hypot(xx - cx, yy - cy)
    ring = (dist < 25) & (dist >= 19)
    box = np.zeros_like(ring); box[ys, xs] = True
    idx[box & (dist < 19)] = 0
    idx[box & ring] = 2
    spr = np.array(Image.open(FRONT / sprite).convert("L"))
    if "sleepy" in sprite:
        spr = spr[:, ::-1]
    n, lab, stats, _ = cv2.connectedComponentsWithStats((spr < 255).astype(np.uint8), connectivity=8)
    body = lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))  # Snom itself, not Zs or stars
    if not extras:
        spr = np.where(body, spr, 255)
    by, bx = np.nonzero(body)
    top = cy - (by.min() + by.max() + 1) // 2 - 1  # centred on the body, a pixel high to sit right
    left = cx - (bx.min() + bx.max() + 1) // 2 + nudge  # the left circles sit half off screen
    sy, sx = np.nonzero(spr < 255)
    for y, x in zip(sy, sx):
        v = SHADE[min(SHADE, key=lambda k: abs(k - int(spr[y, x])))]
        if v is not None and box[top + y, left + x]:
            idx[top + y, left + x] = v

# --- cut back into tiles
tileset, tilemap = [np.zeros((8, 8), int)], []  # tile 0 stays blank: the game screen shows through it
for r in range(28):
    for c in range(32):
        t = idx[r * 8:r * 8 + 8, c * 8:c * 8 + 8]
        found = None
        for n, have in enumerate(tileset):
            for flags, view in ((0, have), (0x40, have[:, ::-1]), (0x80, have[::-1]), (0xC0, have[::-1, ::-1])):
                if np.array_equal(view, t):
                    found = (n, flags)
                    break
            if found:
                break
        if not found:
            tileset.append(t.copy())
            found = (len(tileset) - 1, 0)
        n, flags = found
        p = pal[r, c] if n else 0
        tilemap += [n, flags | (p << 2)]
assert len(tileset) <= 128, f"{len(tileset)} tiles; the game copies 128"
while len(tileset) % 16:
    tileset.append(np.zeros((8, 8), int))
sheet = np.vstack([np.hstack(tileset[i:i + 16]) for i in range(0, len(tileset), 16)])
Image.fromarray(np.array([255, 170, 85, 0], np.uint8)[sheet]).save(ROOT / "gfx/sgb/blue_border.png")
(ROOT / "gfx/sgb/blue_border.tilemap").write_bytes(bytes(tilemap))
print(f"{len([t for t in tileset if t.any()]) + 1} tiles used; wrote gfx/sgb/blue_border.png and .tilemap")
