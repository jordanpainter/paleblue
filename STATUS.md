# Status

## Done
- Cloned pret/pokered (upstream af519899), rgbds 1.0.4 installed, `make blue`
  builds byte-identical Blue.
- Snom sprites done: front in `art/snom_front.png` (editable PNG), back painted in
  `art/snomb.txt` (option D). Rerun `python3 art/build_snom.py` after edits.

## Next
1. Add Snom as a new species (sprites ready), stats, learnset, TM compat; add Powder Snow.
2. Oak's lab: Snom as the only starter; rival also gets Snom.
3. Block catching (wild battles reuse "The trainer blocked the BALL!"),
   gift Pokémon, in-game trades.
4. HMs usable from the bag (badge + HM in bag, no party move needed).
5. Title screen / name: "Snow Blue".
6. Later: PyBoy agent harness reading RAM via `pokeblue.sym`.

## Open
- Exact learnset (levels). Flash: Route 2 aide gives it free (to implement).
