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
- No gifts: every gift Pokémon is refused; tested at the Celadon prize counter
  (coins kept). Trades were already impossible (no NPC wants a Snom).

## Next
1. Settle the learnset.
2. Title screen / name: "Snow Blue".
3. Later: agent harness on top of `playtest/` (RAM via `pokeblue.sym`).

## Open
- Exact learnset (levels); see DECISIONS.md.
- Snom's cry is untested by ear.
- Old man's catching tutorial is untested since the ball change (the code path
  for it is unchanged).
- Flash aide and a real Cut on a tree are untested in-game (the code paths are
  vanilla; Surf and Fly were tested for real).
