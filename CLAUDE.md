# Snow Blue

A Pokémon Blue ROM hack: your starter is Snom, it's the only Pokémon you ever
get, and you have to beat the whole game with it. Later goal: a local agent
that learns to play it.

Built on the pret/pokered disassembly (assembly source that builds Red and Blue).

## Picking it up cold

- Read `STATUS.md` (what's next) and `DECISIONS.md` (what's settled and why).
- Build: `make blue` produces `pokeblue.gbc` and `pokeblue.sym` (RAM/ROM labels,
  useful for the agent). Needs rgbds 1.0.4 (`brew install rgbds`).
- Upstream unmodified build is SHA1 `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`
  (see `roms.sha1`); once we change things, `make compare` will fail, which is expected.
- Toolchain setup details: `INSTALL.md` (upstream). Upstream overview: `README.md`.

## Where things live (pokered layout)

- `data/pokemon/` stats, learnsets, evos, dex entries
- `gfx/pokemon/` front/back sprites (PNG, converted at build)
- `engine/` game logic (battle, overworld, items, menus)
- `scripts/`, `maps/`, `data/maps/` map events and layouts
- `text/` dialogue
- `art/` Snom art: editable front (`snom_front.png`), hand-painted back grid
  (`snomb.txt`), Emerald source (`raw/`),
  builder (`build_snom.py`), preview (`out/`)
- pret wiki has tutorials: https://github.com/pret/pokered/wiki

## Git

`origin` still points at pret/pokered. When the GitHub repo exists, rename
`origin` to `upstream` and add the new repo as `origin`.
