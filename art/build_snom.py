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

Title poses: small edits to the front (POSES below), one pic each in
gfx/pokemon/front/snom_pose_*.png; the title screen cycles through them. The edits assume
the eye is the 2x2 block at EYE and the top of the frame is empty, so recheck them after
moving the eye.

????, the truck superboss (gfx/pokemon/front/starsnom.png), is the front lifted off the
ground with happy eyes, stars and a shadow (star_snom below); its pink comes from the game.

Surf sprite (gfx/sprites/seel.png, which is also the party menu icon): Wild Card's follower
frames (art/raw/overworld.png, six 32x32), cropped to 16x16 and shaded flat: near-white and
the light shading become light grey (white is see-through in Gen 1 sprites), the mid tone
dark grey, the outline black.

Run: python3 art/build_snom.py   (from the repo root)
Writes gfx/pokemon/front/snom.png, the poses, gfx/pokemon/back/snomb.png and a 4x preview in art/out/.
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


EYE = [(18, 34), (19, 34), (18, 35), (19, 35)]


def put(im, pts, shade):
    for p in pts:
        im.putpixel(p, shade)


def blink(im):
    put(im, EYE, WHITE)
    put(im, [(17, 35), (18, 35), (19, 35), (20, 35)], BLACK)


def happy(im):
    put(im, EYE, WHITE)
    put(im, [(17, 35), (18, 34), (19, 34), (20, 35)], BLACK)


def sleepy(im):
    blink(im)
    put(im, [(24, 10), (25, 10), (26, 10), (25, 11), (24, 12), (25, 12), (26, 12)], BLACK)  # z
    put(im, [(x, y) for x in range(29, 34) for y in (3, 7)] + [(32, 4), (31, 5), (30, 6)], BLACK)  # Z


def surprised(im):
    put(im, [(18, 33), (19, 33)], BLACK)  # wide eye
    put(im, [(x, y) for x in (30, 31) for y in [3, 4, 5, 6, 7, 8, 10, 11]], BLACK)  # !


def hop(im):
    body = im.crop((0, 4, 40, 40))
    im.paste(WHITE, (0, 0, 40, 40))
    im.paste(body, (0, 0))


def look_back(im):
    im.paste(im.transpose(Image.FLIP_LEFT_RIGHT))


STAR = ["..#..", "#####", ".###.", ".#.#."]
TWINKLE = [".#.", "###", ".#."]


def stamp(im, shape, x0, y0):
    put(im, [(x0 + x, y0 + y) for y, row in enumerate(shape) for x, c in enumerate(row) if c == "#"], BLACK)


def star_snom(front):
    im = Image.new("L", (40, 40), WHITE)
    im.paste(front.crop((0, 6, 40, 40)), (0, 0))  # floating 6 px up
    put(im, [(x, y - 6) for x, y in EYE], WHITE)
    put(im, [(17, 29), (18, 28), (19, 28), (20, 29)], BLACK)  # happy eye
    stamp(im, STAR, 3, 3)
    stamp(im, STAR, 31, 1)
    for x, y in ((36, 13), (1, 14), (18, 0)):
        stamp(im, TWINKLE, x, y)
    put(im, [(x, 38) for x in range(10, 31, 2)] + [(x, 37) for x in range(14, 29, 2)], DARK)  # shadow
    return im


def surf_sprite():
    ow = Image.open(ART / "raw" / "overworld.png")
    pal = ow.getpalette()

    def shade(i):
        if i == 0:
            return WHITE  # transparent
        lum = 0.3 * pal[3 * i] + 0.59 * pal[3 * i + 1] + 0.11 * pal[3 * i + 2]
        return BLACK if lum < 70 else DARK if lum < 150 else LIGHT

    out = Image.new("L", (16, 96), WHITE)
    # Gen 1 order: down, up, left, then the walking frames; Wild Card's is down, down 2, up, up 2, left, left 2
    for n, i in enumerate((0, 2, 4, 1, 3, 5)):
        x0 = i * 32 + (9 if i >= 4 else 8)
        frame = ow.crop((x0, 16, x0 + 16, 32))
        tile = Image.new("L", (16, 16))
        tile.putdata([shade(p) for p in frame.get_flattened_data()])
        out.paste(tile, (0, n * 16))
    return out


# Same order as SnomPosePics in engine/movie/title.asm
POSES = {"normal": None, "look_back": look_back, "hop": hop, "blink": blink,
         "happy": happy, "sleepy": sleepy, "surprised": surprised}


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
    for name, edit in POSES.items():
        pose = front.copy()
        if edit:
            edit(pose)
        pose.save(ROOT / f"gfx/pokemon/front/snom_pose_{name}.png")
    star_snom(front).save(ROOT / "gfx/pokemon/front/starsnom.png")
    surf_sprite().save(ROOT / "gfx/sprites/seel.png")
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
