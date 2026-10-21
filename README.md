# Pokémon Pale Blue

<img src="artwork/title_screen_grey.png" alt="Pale Blue title screen: Snom, happy" width="480">

A Pokémon Blue hack: Pretty much the same except your starter pokemon is Snom. And you can't catch anything. Or trade. Or evolve.

- Original 151 Pokémon + Snom
- HMs work from the bag.
- Marts sell Ethers and Elixirs
- Every Pokémon Center has a free move relearner - you'll need it

It's been beaten start to finish.

## Playing it

Install [RGBDS](https://rgbds.gbdev.io) 1.0.4, then run `make blue` to build `pokeblue.gbc`.
Open it in any Game Boy emulator. It works on Game Boy and Super Game Boy.

## The agent

The plan is to train a local agent to beat Pale Blue on its own, with no one at the
controls. It'll build on what's already here: `playtest/` plays the game headlessly and
finds walking routes from the map data, and `stats/` has an mGBA script that logs every
battle and turn of a human run to compare against. This repo will be updated as it makes
progress.

## Credits

Built on [pret/pokered](https://github.com/pret/pokered). Snom sprites from
[pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion). Thanks to
JadeLune for the [HQ Blue box art](https://www.deviantart.com/jadelune/art/Pokemon-Blue-Version-Game-Boy-HQ-Box-Art-593872935)
that `artwork/box_art.png` is built on.
