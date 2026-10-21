"""Build the title screen's version lettering, gfx/title/blue_version.png (80x8, 1bpp).

Glyphs are copied from the original "Blue Version" art, plus a P and an a drawn to
match. Run: python3 art/build_title_text.py   (from the repo root)
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# 5 rows tall, drawn from row 3 of the 8-pixel strip like the original
GLYPHS = {
    "P": ["####.", "##.##", "####.", "##...", "##..."],
    "a": ["....", "###.", ".###", "##.#", ".###"],
    "l": ["##", "##", "##", "##", "##"],
    "e": ["....", ".###", "##.#", "###.", ".###"],
    "B": ["####.", "##.##", "####.", "##.##", "####."],
    "u": ["....", "##.#", "##.#", "##.#", ".###"],
    "V": ["##..##", "##..##", "##..##", ".####.", "..##.."],
    "r": ["....", "####", "##..", "##..", "##.."],
    "s": [".....", ".####", "###..", "..###", "####."],
    "i": ["##", "..", "##", "##", "##"],
    "o": [".....", ".###.", "##.##", "##.##", ".###."],
    "n": ["....", "###.", "##.#", "##.#", "##.#"],
}
TEXT = "Pale Blue Version"
WORD_GAP = 4  # the original used 6, but 4 makes this fit the title's 10 tiles exactly
WIDTH = 80    # 10 tiles; engine/movie/title.asm prints them centred on the screen


def main():
    pieces = []
    for word in TEXT.split():
        if pieces:
            pieces.append(WORD_GAP - 1)  # each glyph already adds a 1 px gap
        pieces += [GLYPHS[c] for c in word]
    width = sum(p if isinstance(p, int) else len(p[0]) + 1 for p in pieces) - 1
    assert width <= WIDTH, f"{TEXT!r} is {width} px; the title has room for {WIDTH}"
    im = Image.new("1", (WIDTH, 8), 1)
    x = (WIDTH - width) // 2
    for p in pieces:
        if isinstance(p, int):
            x += p
            continue
        for y, row in enumerate(p):
            for dx, c in enumerate(row):
                if c == "#":
                    im.putpixel((x + dx, y + 3), 0)
        x += len(p[0]) + 1
    im.save(ROOT / "gfx/title/blue_version.png")
    print(f"wrote gfx/title/blue_version.png: {TEXT!r}, {width} px wide")


if __name__ == "__main__":
    main()
