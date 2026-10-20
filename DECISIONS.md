# Decisions

## 2026-10-20: Base on pret/pokered, build Blue
Name is "Snow Blue", so build the Blue target. pokered builds both from one source.
Rejected: pokeyellow (starter logic tangled with Pikachu follower and rival's Eevee).

## 2026-10-20: Snom only, forever
Snom is the starter and the only Pokémon the player ever has. It never evolves
(no Frosmoth). No catching, no gift Pokémon, no in-game trades.
Expected consequence: Oak's aides gate HM05 Flash (10 caught) and Exp. All
(50 caught) on catches, so both become unobtainable.

## 2026-10-20: Rival also gets Snom
Because it's funny.

## 2026-10-20: Gen 1 Special uses Snom's Special Attack (45)
Gen 1 has a single Special stat; real Snom has 45 SpA / 30 SpD.

## 2026-10-20: HMs work from the bag
Snom learning Cut/Surf/Strength would fill its only moveset with HMs that Gen 1
can't forget. Instead: right badge + HM item in bag lets you use the field effect.
Rejected: deleting obstacles / land bridge to Cinnabar (changes world, trivialises Victory Road).
Status: recommended, user hasn't confirmed explicitly.

## 2026-10-20: Moves: Gen 1 set plus Powder Snow, no Fissure
Gen 1 has no weak Ice move (Aurora Beam, 65, is the weakest) and Bug moves are
physical off Snom's 25 Attack, so the early game needs Powder Snow (40, Ice), added
as a new move reusing an existing animation. No Fissure: X Accuracy makes OHKO moves
always hit in Gen 1, which would trivialise the run. Exact learnset still open.

## 2026-10-20: Flash from the Route 2 aide regardless of catches
He normally wants 10 caught, impossible here. He hands it over with a line about
you having caught none. Usable from the bag like the other HMs.
Rejected: permanently lit Rock Tunnel, leaving it dark.

## 2026-10-20: Sprites start from pokeemerald-expansion's Snom
Taken from `~/games/wildcard/graphics/pokemon/snom/` (stock expansion art, not
Wildcard-made), converted by `art/build_snom.py`. Front fits Gen 1's 40x40 class at
native size (Snom is 34x25); one pixel overridden so the eye is solid black.
Back (`art/snomb.txt`, 28x19): Emerald's back area-resampled to 0.6x for the
silhouette, then its features hand-painted on (bump highlights, left plate, ridge,
creases, head nub). The game shows only the top-left 28x28 of a back pic, doubled,
so 28 wide is the limit; it sits sunk 3px into the text box. Picked from four mock
battle-screen options (small/big x sitting/sunk). Rejected: freehand drawing (looked
nothing like Snom), all-white "snowy" shading (washed out under PAL_CYANMON).
Credit the expansion sprite contributors in the README.
