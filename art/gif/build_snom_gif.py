"""artwork/snom.gif: Snom hops, lands in a new pose, hops again. Built from the title poses
(gfx/pokemon/front/snom_pose_*.png) in Game Boy greys, outside made see-through
so it sits on GitHub's light and dark themes. Run: .venv/bin/python art/gif/build_snom_gif.py
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
POSES = ["normal", "happy", "look_back", "blink", "surprised", "hop"]
SHADES = {0: (0, 0, 0), 85: (85, 85, 85), 170: (153, 153, 153), 255: (255, 255, 255)}  # Game Boy greys, as on the README's title screen
HOP = [0, -3, -5, -6, -5, -3, 0]  # pixels up, one per frame
SCALE, PAD, LIFT = 3, 7, 2  # LIFT: clear rows under Snom, to raise it off the heading line


def pose(name):
    g = np.array(Image.open(ROOT / f"gfx/pokemon/front/snom_pose_{name}.png").convert("L"))
    g = np.array([[min(SHADES, key=lambda k: abs(k - int(v))) for v in row] for row in g])
    # see-through: white reachable from the edge (Snom's own white stays)
    outside = np.zeros(g.shape, bool)
    stack = [(y, x) for y in range(40) for x in (0, 39)] + [(y, x) for x in range(40) for y in (0, 39)]
    while stack:
        y, x = stack.pop()
        if 0 <= y < 40 and 0 <= x < 40 and not outside[y, x] and g[y, x] == 255:
            outside[y, x] = True
            stack += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    rgba = np.zeros((40, 40, 4), np.uint8)
    for k, c in SHADES.items():
        rgba[g == k] = (*c, 255)
    rgba[outside] = 0
    return Image.fromarray(rgba)


frames, durations = [], []
for i, name in enumerate(POSES):
    nxt = POSES[(i + 1) % len(POSES)]
    for f, dy in enumerate(HOP):
        im = Image.new("RGBA", (40, 40 + PAD + LIFT), (0, 0, 0, 0))
        im.alpha_composite(pose(name if f < len(HOP) // 2 else nxt), (0, PAD + dy))
        frames.append(im)
        durations.append(70)
    durations[-1] = 2200  # hold the new pose a while before the next hop
# explicit palette: index 0 see-through, then Snom's four colours
colours = list(SHADES.values())
palette = [0, 0, 0] + [v for c in colours for v in c]


def indexed(im):
    a = np.array(im)
    idx = np.zeros(a.shape[:2], np.uint8)
    for n, c in enumerate(colours, 1):
        idx[(a[..., 3] > 0) & np.all(a[..., :3] == c, axis=-1)] = n
    p = Image.fromarray(idx, "P")
    p.putpalette(palette)
    return p.resize((im.width * SCALE, im.height * SCALE), Image.NEAREST)


big = [indexed(f) for f in frames]
out = ROOT / "artwork/snom.gif"
big[0].save(out, save_all=True, append_images=big[1:], duration=durations, loop=0, disposal=2,
            transparency=0, optimize=False)
print("wrote", out, out.stat().st_size, "bytes")
