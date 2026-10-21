"""Walking routes from the game's own data (the start of the agent's pathfinder).

Reads, for one map: its size (constants/map_constants.asm), tileset (data/maps/headers),
blocks (maps/*.blk), walkable tiles (data/tilesets/collision_tile_ids.asm), the tile pairs
you can't step between (pair_collision_tile_ids.asm, fake cliffs), one-way ledges
(ledge_tiles.asm), and objects standing in the way (data/maps/objects). A square is a
16x16 step; Gen 1 checks the bottom-left 8x8 tile of it.

Not modelled: NPCs that wander, gates scripts swap in (see the Mansion solver), water.

Usage: .venv/bin/python playtest/route.py MapName X1 Y1 X2 Y2   (prints playtest steps)
"""
import re
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


def _camel(const):
    return "".join(w.title() for w in const.split("_"))


def _hexes(text):
    return [int(h, 16) for h in re.findall(r"\$([0-9A-Fa-f]{2})", text)]


class Map:
    def __init__(self, name):
        const = re.search(r"map_header\s+\w+,\s*(\w+),\s*(\w+)",
                          (ROOT / f"data/maps/headers/{name}.asm").read_text())
        self.const, tileset = const.group(1), const.group(2)
        size = re.search(rf"map_const {self.const},\s*(\d+),\s*(\d+)",
                         (ROOT / "constants/map_constants.asm").read_text())
        self.w, self.h = int(size.group(1)), int(size.group(2))
        tname = _camel(tileset)
        gfx = (ROOT / "gfx/tilesets.asm").read_text()
        # labels that share an INCBIN are stacked on the lines above it
        m = re.search(rf"{tname}_Block::(?:\s*\w+_Block::)*\s*INCBIN \"([^\"]+)\"", gfx)
        self.bst = (ROOT / m.group(1)).read_bytes()
        self.blk = (ROOT / f"maps/{name}.blk").read_bytes()
        coll = (ROOT / "data/tilesets/collision_tile_ids.asm").read_text()
        m = re.search(rf"{tname}_Coll::(?:\s*\w+_Coll::)*\s*coll_tiles([^\n]*)", coll)
        self.walk = set(_hexes(m.group(1)))
        pairs = (ROOT / "data/tilesets/pair_collision_tile_ids.asm").read_text()
        land = pairs.split("TilePairCollisionsLand::")[1].split("TilePairCollisionsWater::")[0]
        self.pairs = {frozenset(_hexes(l)) for l in land.splitlines() if re.search(rf"db {tileset},", l)}
        self.ledges = []
        if tileset == "OVERWORLD":
            for l in (ROOT / "data/tilesets/ledge_tiles.asm").read_text().splitlines():
                m = re.search(r"SPRITE_FACING_(\w+),\s*\$(\w+),\s*\$(\w+)", l)
                if m: self.ledges.append((m.group(1).lower(), int(m.group(2), 16), int(m.group(3), 16)))
        objs = (ROOT / f"data/maps/objects/{name}.asm").read_text()
        self.blocked = {(int(x), int(y)) for x, y in re.findall(r"object_event\s+(\d+),\s*(\d+)", objs)}
        self.warps = [(int(x), int(y)) for x, y in re.findall(r"warp_event\s+(\d+),\s*(\d+)", objs)]

    def tile(self, x, y):
        """Collision tile of square (x, y), or None off the map."""
        if not (0 <= x < self.w * 2 and 0 <= y < self.h * 2): return None
        tx, ty = 2 * x, 2 * y + 1
        b = self.blk[(ty // 4) * self.w + tx // 4]
        return self.bst[b * 16 + (ty % 4) * 4 + tx % 4]

    def moves(self, x, y):
        here = self.tile(x, y)
        for d, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            t = self.tile(nx, ny)
            if t is None: continue
            if any(d == ld and here == st and t == lt for ld, st, lt in self.ledges):
                yield d, (x + 2 * dx, y + 2 * dy)  # hop down the ledge
                continue
            if t in self.walk and (nx, ny) not in self.blocked and frozenset((here, t)) not in self.pairs:
                yield d, (nx, ny)

    def route(self, start, goal):
        """Directions from start to goal (squares), shortest first; None if unreachable."""
        prev, q = {start: None}, deque([start])
        while q:
            cur = q.popleft()
            if cur == goal:
                out = []
                while prev[cur]: cur, d = prev[cur]; out.append(d)
                return out[::-1]
            for d, nxt in self.moves(*cur):
                if nxt not in prev:
                    prev[nxt] = (cur, d)
                    q.append(nxt)
        return None


def as_steps(dirs):
    """Playtest step lines, collapsing runs ("mash right 5 4")."""
    out, i = [], 0
    while i < len(dirs):
        j = i
        while j < len(dirs) and dirs[j] == dirs[i]: j += 1
        out.append(f"mash {dirs[i]} {j - i} 4" if j - i > 1 else f"{dirs[i]} 4")
        i = j
    return out


if __name__ == "__main__":
    name, *xy = sys.argv[1:]
    x1, y1, x2, y2 = map(int, xy)
    r = Map(name).route((x1, y1), (x2, y2))
    print("unreachable" if r is None else "\n".join(as_steps(r)))
