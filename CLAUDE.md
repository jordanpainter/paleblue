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
  builder (`build_snom.py`, which also makes the title-screen poses), title lettering
  builder (`build_title_text.py`), previews and mockups (`out/`)
- `stats/` playthrough logging: `stats_log.lua` is an mGBA script (Tools > Scripting,
  File > Load script) that appends every battle to `stats/battles.csv`, every battle
  message (with both sides' HP, status, stat stages) to `stats/turns.csv` (joined on
  `battle`), and a Snom snapshot per in-game save to `stats/saves.csv`. Reads addresses from `pokeblue.sym`
  and names from `constants/`, so it follows rebuilds. It watches `pokeblue.sav` in the repo root.
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
  `prize_gift`, and `fly_celadon` -> `relearner` -> `relearner_learn`, and `fly_celadon` ->
  `relearner_twice` -> `relearner_leech`). Rebuild states after a build; old ones can crash. `poke LABEL HEX...` writes RAM,
  e.g. to hand yourself HMs or badges.
- `playtest/route.py MapName X1 Y1 X2 Y2` prints the shortest walk as step lines.
  `playtest/out/dev/` is a scratch copy for building and testing while Jordan plays
  (rsync the source in, `make blue` there).
- Never `make` while Jordan's mGBA has the ROM open: mGBA may read the ROM file live, so a
  rebuild can swap code under a running game. Check `pgrep -lf mGBA` first and ask Jordan to
  quit (save in-game first). Never script-close mGBA.
- PyBoy runs it as a plain Game Boy, so screenshots are grey, not the SGB/GBC palette.

## Git

On this project, commits Claude makes or drafts end with a
`Co-Authored-By: Claude <model> <noreply@anthropic.com>` trailer (Jordan's call,
2026-10-20; overrides the global no-trailer rule here only).

`origin` still points at pret/pokered. When the GitHub repo exists, rename
`origin` to `upstream` and add the new repo as `origin`.
