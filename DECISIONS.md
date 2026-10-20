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

## 2026-10-20: Snom is index $1F, Pokédex #152, following pret's tutorial
First free MissingNo. slot. Mew's base stats moved into the main table (Snom has to
follow it); Mew's pics stay in bank 1. Pokédex flags are 19 bytes for 151 or 152, so RAM
and save layout are unchanged from vanilla (existing Red/Blue RAM maps still apply).
Cry: Caterpie's (SFX_CRY_16) pitched up ($E0, $10). Dex text is our own, not Sword's.

## 2026-10-20: All three starter constants are SNOM
STARTER1/2/3 = SNOM. The one place that needed the balls to be different (the
rival's walk to his ball) now branches on wRivalStarterBallSpriteIndex. The
`cp STARTER2` checks that pick the rival's team now always take their first branch,
so he fields the same team variant every run; every rival variant has Snom in the
starter slot. Champion's Snom gets Blizzard (was Mega Drain/Fire Blast/Blizzard by starter).
Rejected: keeping the constants as hidden "ball IDs" and swapping Snom in at every
display/give site (far more places to touch).
Ball lines: "ice #MON", "bug #MON", "only #MON I have".

## OPEN: Snom's learnset (draft in game)
Lv 1 Leech Life + String Shot, 15 Mist, 20 Aurora Beam, 28 Haze. TMs: Toxic, Ice Beam,
Blizzard, Mimic, Double Team, Bide, Rest, Substitute (no HMs, no Fissure). Powder Snow
still to add and slot in.

## 2026-10-20: One Poké Ball in Oak's lab (supersedes the three-ball lines)
Only the middle ball is shown (the other two start hidden in
`data/maps/toggleable_objects.asm`). The rival doesn't walk to a ball: he says
"Gramps! Gimme one too!" and receives a Snom where he stands; his later walk to
challenge you paths from wherever he is, so nothing else needed changing. Oak's
speech now mentions one ball and "only have SNOM left. Lots of SNOM."
The rival-walk branching added earlier today was removed with it.

## 2026-10-20: HMs: an HM in the bag shows up as Snom's field move (confirms the HM decision)
`GetMonFieldMoves` appends CUT/FLY/SURF/STRENGTH/FLASH for each HM in the bag, so
you use them the vanilla way (START > POKéMON > SNOM > CUT) with vanilla badge checks
and text ("BLUE got on SNOM!"). The field-move buffer and party submenu grew from 4 to
5 entries (MAX_FIELD_MOVES); five fit the screen exactly. RAM layout unchanged (the
buffer sits in a union). Rejected: a new "use HM from the ITEM menu" path (new code
for each move, and you'd still need the party-menu one for Fly's map) and
auto-use on pressing A (more code, and Strength/Fly/Flash don't map onto a single A press).

## 2026-10-20: Route 2 aide wants 1 Pokémon for Flash (supersedes the custom line)
His requirement drops from 10 to 1; Snom always counts as caught, so he always gives
HM05, and vanilla text congratulates you on catching "1 kinds of POKéMON".
Rejected: new dialogue (more text, same result). Itemfinder (30) and Exp. All (50)
aides are left unreachable.

## 2026-10-20: Powder Snow added as move $A5 (Struggle moves to $A6)
Gen 2 stats: Ice, 40 power, 100 accuracy, 25 PP, 10% freeze (Gen 1's
FREEZE_SIDE_EFFECT1, same as Ice Beam). Reuses Blizzard's animation and sound.
Followed pret's "Add a new move" tutorial. Snom's Lv 1 moves are now Powder Snow +
String Shot; Leech Life moved to Lv 9 (learnset still a draft).

## 2026-10-20: Balls are dodged like a ghost's (supersedes "The trainer blocked the BALL!")
Every wild ball (Safari Balls included) takes the unidentified-ghost path: toss
animation, "It dodged the thrown BALL! This POKéMON can't be caught!", ball used up.
Vanilla text that reads right in a wild battle; the trainer message didn't. The old
man's tutorial catch (BATTLE_TYPE_OLD_MAN) is the one exception. The vanilla catch
calculation below the check is now unreachable and left in place.
