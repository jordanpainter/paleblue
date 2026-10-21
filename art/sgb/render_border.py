"""Render the SGB border (gfx/sgb/blue_border.png + .tilemap, palettes from data/sgb/sgb_border.asm)
the way a Super Game Boy shows it. Usage: render_border.py TILES.png TILEMAP OUT.png [SCALE]"""
import re, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def palettes():
    """Border palettes 4, 5, 6 (PAL_SGB1-3, the _BLUE ones) as RGB888, colour 0 left to the backdrop."""
    src = (ROOT / "data/sgb/sgb_border.asm").read_text()
    blue = [m for m in re.split(r"IF DEF\(_BLUE\)", src)[1:]]
    pals = {}
    for i, chunk in enumerate(blue[1:4]):
        rgb = re.findall(r"RGB (\d+),(\d+),(\d+)", chunk.split("ENDC")[0])
        pals[4 + i] = [tuple(int(c) * 255 // 31 for c in t) for t in rgb]
    return pals


def tiles(png):
    im = np.array(Image.open(png).convert("L"))
    shade = {255: 0, 170: 1, 85: 2, 0: 3}  # rgbgfx: white is colour 0
    idx = np.vectorize(lambda v: shade[min(shade, key=lambda k: abs(k - v))])(im)
    h, w = idx.shape
    return [idx[r * 8:r * 8 + 8, c * 8:c * 8 + 8] for r in range(h // 8) for c in range(w // 8)]


def render(tile_png, tilemap, backdrop=(248, 232, 248)):
    ts, pals = tiles(tile_png), palettes()
    d = Path(tilemap).read_bytes()
    out = np.zeros((224, 256, 3), np.uint8)
    for i in range(896):
        t, a = d[2 * i], d[2 * i + 1]
        r, c = divmod(i, 32)
        tile = ts[t] if t < len(ts) else np.zeros((8, 8), int)
        if a & 0x40: tile = tile[:, ::-1]
        if a & 0x80: tile = tile[::-1]
        pal = pals.get((a >> 2) & 7, [backdrop, (170,) * 3, (85,) * 3, (0,) * 3])
        colours = np.array([backdrop] + list(pal[1:]), np.uint8)
        out[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = colours[tile]
    return out


if __name__ == "__main__":
    img = render(sys.argv[1], sys.argv[2])
    s = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    Image.fromarray(img).resize((256 * s, 224 * s), Image.NEAREST).save(sys.argv[3])
