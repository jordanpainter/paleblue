# Status

## Done
- Cloned pret/pokered (upstream af519899), rgbds 1.0.4 installed, `make blue`
  builds byte-identical Blue.
- Snom sprites done: front in `art/snom_front.png` (editable PNG), back painted in
  `art/snomb.txt` (option D). Rerun `python3 art/build_snom.py` after edits.
- Snom is species $1F / Pokédex #152 and your starter; the rival gets one too and
  fields it in every fight (Lv 65 with Blizzard as Champion).
- One ball in Oak's lab; the rival asks Oak for his own Snom.
  Verified in PyBoy: Pokédex page, the lab scene, first rival battle.
- PyBoy playtester in `playtest/`.
- HMs in the bag appear as Snom's field moves (all five, vanilla badge checks).
  Tested: menu with 0/1/5 HMs, every entry's handler, badge refusal, real Surf.
- Route 2 aide gives Flash for 1 Pokémon owned.
- Powder Snow (new move, Snom's Lv 1 move); tested on a wild Pidgey.
- No catching: every wild ball is dodged; tested on Route 1 (ball used, party still 1).
- Learnset settled (see DECISIONS.md); checked the rival's Snom moves at four fights
  and a Rare Candy level-up.
- No gifts: every gift Pokémon is refused; tested at the Celadon prize counter
  (coins kept). Trades were already impossible (no NPC wants a Snom).
- Jordan's first real playthrough (mGBA): through Brock with no other issues (2026-10-20).
  Misty is the first real wall, at Snom Lv 24 (balancing data point); beaten after farming.
- Stats logging (`stats/stats_log.lua`, mGBA script): battles and save snapshots to CSV.
  Tested headless on a copy of Jordan's save: trainer win, wild win, run away, blackout
  loss (money halving caught), save snapshot. Turn-by-turn transcript (`turns.csv`)
  added and tested headless; Jordan's log has real rows from Cerulean on.
- Move relearner: the Cable Club receptionist in every Pokémon Center (and Indigo
  Plateau) lists Lv 1 and level-up moves Snom has passed but doesn't know; free.
  Tested: Celadon center, Lv 48 Snom relearns Amnesia. Found because Jordan skipped
  Amnesia at Lv 43 (the turn log showed it). Crash on picking Leech Life fixed in
  home/list_menu.asm (2026-10-20); every list entry tested.
- Title screen: Snom in seven random poses (no repeats), checked in colour in headless
  mGBA. Game renamed Pale Blue; title reads "Pale Blue Version" (centred) and Snom is icy cyan
  on the SGB title (see DECISIONS.md).

- ???? easter egg (truck at Vermilion Dock, Lv 100, teaches Psychic): built and tested
  end to end headless (dock access, surf, encounter, win, reward, "just a truck").
- Marts sell Ethers/Elixirs instead of balls; Jordan's save +₽50,000.
- Continue now refreshes tileset pointers (a rebuilt ROM had frozen Jordan's save).
- playtest/route.py: shortest walking routes from map data (start of the agent's
  pathfinder); playtest.py takes --sav (boot a save, read only) and LABEL+offset.

- Jordan beat the game (2026-10-21). Then: Snom surf sprite + party icon, all-Snom
  credits with a ???? cameo and PALE BLUE STAFF heading (built in playtest/out/dev,
  goes into the real ROM at the next mGBA quit).

- Jordan beat ???? and got Psychic (2026-10-21). Sprite-over-menu fix for its reward is
  in source and the dev copy; goes into the ROM at the next mGBA quit.

## Next
1. Agent: layered design chosen (DECISIONS.md); first piece to build is open.
2. Maybe: SGB border art (still says BLUE, vanilla starters).
3. Followers (Snom walking behind you): possible via Yellow's Pikachu engine, big job; parked.

## Open
- The stats log has no Elite Four battles (logger likely not loaded those sessions), so
  end-game difficulty data is Jordan's account only (many losses late on, won with grinding).
- route.py disagrees with the game about counters in the Indigo Plateau lobby (MART
  tileset): check before the agent relies on it indoors. Outdoors it matched exactly.
- Jordan saw garbled text when the rival got his Snom (first play, mGBA, 2026-10-20).
  Not reproduced: frame-by-frame recordings in PyBoy, grey and colour, are clean.
  Waiting on a screenshot.
- Snom's cry is untested by ear.
- Old man's catching tutorial is untested since the ball change (the code path
  for it is unchanged).
- A real Cut on a tree is untested in-game (Flash aide confirmed by Jordan's playthrough;
  Surf and Fly were tested for real).
