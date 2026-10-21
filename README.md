# Pokémon Pale Blue

A Pokémon Blue ROM hack with one rule: your starter is a Snom, and it's the only
Pokémon you will ever have. Beat the whole game with it.

It can be done. The first full run beat the Champion after a lot of grinding and a lot
of losses along the way.

## What's different

- You get one Snom, it never evolves, and that's it. Wild Pokémon dodge every ball,
  gift Pokémon get turned down, and nobody will trade with you. Your rival asks Oak for
  a Snom of his own.
- HMs work from the bag. Snom doesn't need to learn Cut, Surf and the rest; carry the HM
  and use it from Snom's menu.
- With one Pokémon you run out of PP long before you run out of HP, so marts sell Ethers
  and Elixirs where the Poké Balls used to be.
- The old Cable Club desk in every Pokémon Center is now a free move relearner, so a
  skipped level-up move is never gone for good.
- Snom's learnset is built for the run: Powder Snow (a new move), Leech Life, Aurora
  Beam, Ice Beam, Amnesia, Blizzard and more.
- The title screen cycles through seven Snom poses, Snom carries you when you surf, and
  every name in the credits is SNOM.
- There might be something under the truck.

## Building

You need [RGBDS 1.0.4](https://rgbds.gbdev.io/). Then:

```sh
make blue
```

That produces `pokeblue.gbc`. No ROM is included here, only source. For toolchain setup,
see [INSTALL.md](INSTALL.md).

## Extras

- `stats/stats_log.lua` is an [mGBA](https://mgba.io/) script that logs every battle, turn
  and save to CSV while you play.
- `playtest/` drives the game headlessly in [PyBoy](https://github.com/Baekalfen/PyBoy)
  from step files, and `playtest/route.py` finds walking routes from the map data. They're
  the start of an agent that will play Pale Blue on its own.

## Credits

- Built on [pret/pokered](https://github.com/pret/pokered), the Pokémon Red and Blue
  disassembly.
- Snom's sprites are adapted from
  [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion).
- Pokémon is © Nintendo, Creatures and Game Freak. This is a non-commercial fan project
  and isn't affiliated with any of them.
