"""Build Snom's Gen 1 pics.

Front: art/snom_front.png, 40x40, yours to edit in any pixel editor. Off-palette colours
are snapped to the nearest of the 4 shades. It started as a conversion of the Gen 3
sprite in art/raw/ (pokeemerald-expansion); `--reconvert-front` redoes that and
OVERWRITES art/snom_front.png.
Back: hand-painted over a resample of the Gen 3 back, in art/snomb.txt, one character per pixel:
    . or w  white      +  light grey      o  dark grey      #  black

Gen 1 front pics are square, 40/48/56 px, bottom-aligned. Back pics are 32x32, but the
game only shows the top-left 28x28, doubled (engine/battle/scale_sprites.asm), sitting on
the text box. Only 4 shades: white, light grey, dark grey, black.

Run: python3 art/build_snom.py   (from the repo root)
Writes gfx/pokemon/front/snom.png, gfx/pokemon/back/snomb.png and a 4x preview in art/out/.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art"
OUT = ART / "out"

WHITE, LIGHT, DARK, BLACK = 255, 170, 85, 0

# Gen 3 palette index -> Gen 1 shade. Index 0 is the transparent background.
# Picked by eye: outlines go black, the blue ice goes light/dark grey, the body stays white.
SHADES = {
    0: WHITE,
    1: BLACK,   # (120,136,152) ice outline
    2: LIGHT,   # (168,192,200) ice shading
    3: WHITE,   # (216,232,240) ice highlight
    4: WHITE,   # (240,248,248)
    5: BLACK,   # face/body outline
    6: BLACK,   # (16,16,16) eyes
    7: WHITE,   # body
    8: DARK,    # body shading
    9: WHITE,   # (248,248,248)
}

# Per-pixel overrides on the Gen 3 front, in its own coordinates.
FRONT_FIXES = {
    (30, 38): BLACK,  # top-left of the 2x2 eye is body shading in Emerald; make the eye solid
}

GRID_SHADES = {".": WHITE, "w": WHITE, "+": LIGHT, "o": DARK, "#": BLACK}

BACK_SHOWN = 28  # visible part of the 32x32 back pic
BACK_SUNK = 3    # rows pushed below the visible area, so Snom sinks into the text box


def place(im, box):
    """Centre horizontally, sitting on the bottom of a box x box white frame."""
    frame = Image.new("L", (box, box), WHITE)
    frame.paste(im, ((box - im.width) // 2, box - im.height))
    return frame


def nearest_shade(v):
    return min((WHITE, LIGHT, DARK, BLACK), key=lambda s: abs(s - v))


def build_front():
    im = Image.open(ART / "snom_front.png").convert("L")
    assert im.size == (40, 40), f"art/snom_front.png is {im.size}, needs to be 40x40"
    off = sum(1 for v in im.get_flattened_data() if v not in (WHITE, LIGHT, DARK, BLACK))
    if off:
        print(f"snom_front.png: snapped {off} off-palette pixels to the nearest shade")
    return im.point(nearest_shade)


def convert_front():
    src = Image.open(ART / "raw" / "front.png")
    im = Image.new("L", src.size, WHITE)
    im.putdata([SHADES[i] for i in src.get_flattened_data()])
    for xy, shade in FRONT_FIXES.items():
        im.putpixel(xy, shade)
    im = im.crop(im.point(lambda v: 255 - v).getbbox())
    return place(im, 40)


def build_back():
    rows = (ART / "snomb.txt").read_text().splitlines()
    w, h = max(map(len, rows)), len(rows)
    assert w <= BACK_SHOWN, f"back is {w} wide; only {BACK_SHOWN} columns show in game"
    pic = Image.new("L", (32, 32), WHITE)
    ox, oy = (BACK_SHOWN - w) // 2, BACK_SHOWN - h + BACK_SUNK
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            pic.putpixel((ox + x, oy + y), GRID_SHADES[c])
    return pic


def main():
    OUT.mkdir(exist_ok=True)
    if "--reconvert-front" in sys.argv:
        convert_front().save(ART / "snom_front.png")
    front, back = build_front(), build_back()
    front.save(ROOT / "gfx/pokemon/front/snom.png")
    back.save(ROOT / "gfx/pokemon/back/snomb.png")
    # Preview at in-game proportions: front 1:1, back cropped and doubled as the game draws it, then 4x.
    shown = BACK_SHOWN * 2
    preview = Image.new("L", (40 + 8 + shown, shown), WHITE)
    preview.paste(front, (0, shown - 40))
    preview.paste(back.crop((0, 0, BACK_SHOWN, BACK_SHOWN)).resize((shown, shown), Image.NEAREST), (48, 0))
    preview.resize((preview.width * 4, preview.height * 4), Image.NEAREST).save(OUT / "preview.png")
    print("wrote gfx/pokemon/front/snom.png, gfx/pokemon/back/snomb.png, art/out/preview.png")


if __name__ == "__main__":
    main()
