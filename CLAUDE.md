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

## Playtesting

- `python3 -m venv .venv && .venv/bin/pip install pyboy pillow` once (`.venv/` is git-ignored).
- `.venv/bin/python playtest/playtest.py steps/FILE.txt [--state IN] [--save OUT]` runs a
  step file headless and writes screenshots to `playtest/out/` (ignored). Step syntax is in
  the script's docstring; `until a TEXT` mashes until TEXT is on screen (reads the tile map).
- Regression chain, each `--save`-ing a state the next one `--state`s from:
  `new_game_to_lab` -> `one_ball` -> `rival_fight` -> `to_water` -> `shore` -> `surf`
  (`hm_menu` also runs off the `rival_fight` state; `wild_ball` -> `powder_snow`
  runs off the `to_water` state; so does `fly_celadon` -> `to_prize_room` ->
  `prize_gift`). `poke LABEL HEX...` writes RAM,
  e.g. to hand yourself HMs or badges.
- PyBoy runs it as a plain Game Boy, so screenshots are grey, not the SGB/GBC palette.

## Git

`origin` still points at pret/pokered. When the GitHub repo exists, rename
`origin` to `upstream` and add the new repo as `origin`.
