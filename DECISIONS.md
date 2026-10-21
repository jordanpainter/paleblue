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

## 2026-10-20: Gift Pokémon are refused in _GivePokemon; trades need no change
`_GivePokemon` prints "But SNOM won't share <PLAYER> with anyone!" and returns the
box-full failure, which every caller already handles: Magikarp salesman keeps his
money, Dojo/Eevee/Lapras balls stay, the prize counter keeps your coins, the fossil
lab keeps the revived fossil. Covers all seven GivePokemon sites in one place (the
rest of the routine is now unreachable, left in place).
In-game trades are already impossible: each NPC checks you offer the species they
asked for, none asks for Snom, and you can't catch what they want. Link-cable
trades with another cartridge are not blocked (out of scope for a solo run).

## 2026-10-20: Snom's learnset (closes the open learnset item)
Lv 1 Powder Snow + String Shot, 9 Leech Life, 14 Mist, 18 Aurora Beam, 23 Light Screen,
28 Haze, 33 Ice Beam, 38 Rest, 43 Amnesia, 50 Blizzard. TMs add Reflect (TM33).
Snom is an Ice special attacker (Gen 1 Bug moves run off its 25 Attack), so damage is
all Ice; the rest is Frosmoth's kit translated: Mist (its own), Light Screen for
Aurora Veil, Haze for Defog, Amnesia for Quiver Dance. Moves land ahead of the gyms
they matter for. Amnesia is the win condition (+2 Special is offence and special
defence in Gen 1). Rejected: Growth instead of Amnesia (too slow a grind), Bug
attacks for flavour (useless off 25 Attack).
The Champion's Blizzard override is gone: his Lv 65 Snom already has Ice Beam, Rest,
Amnesia, Blizzard by level (Pidgeot's Sky Attack override stays).

## 2026-10-20: Playthrough stats via one mGBA Lua script

Jordan wanted per-battle stats and per-save snapshots. Both live in one mGBA script
(`stats/stats_log.lua`) rather than a Lua battle logger plus a Python `.sav` watcher,
so there's nothing extra to keep running in a terminal. Save detection compares only
the save block (`sGameData` to `sMainDataCheckSum`): Gen 1 uses the rest of the save
chip as scratch for decompressing pics, so the whole file changes during normal play.
No turn count: Gen 1 keeps no turn counter, so battles log game-time seconds instead.
The CSVs are personal playthrough data; whether they go on GitHub is Jordan's call (open).

## 2026-10-20: Turn-by-turn log reads the battle text box

For the agent later, `stats/turns.csv` logs every battle message with both sides' HP,
status, stat stages and effects (Light Screen, Bide, Mist...) at that moment. mGBA 0.10.5
scripts can't break on game code (that arrived after 0.10.5) and Gen 1 keeps no turn
counter, so the script transcribes the text box: a message counts once it has stayed
put longer than the text speed's per-letter delay, and a turn starts when the FIGHT menu
appears after something happened. Messages give actor and move or item for free
("Enemy STARMIE used WATER GUN!"). HP in a "used" row is before the hit; the rows after
it show the result. Long trainer speeches may log as overlapping screenfuls.
`battles.csv` gained a `battle` id column (date-time plus a session counter, since two
fast-forwarded fights can start in the same second); the script pads older files.

## 2026-10-20: Move relearner in every Pokémon Center, free

With one Pokémon for the whole game, a level-up move you skip is gone forever (Gen 1
has no relearner, and Amnesia has no TM). Jordan hit exactly this at Lv 43. The Cable
Club receptionist is repurposed as the relearner: she's in every center from Viridian
on (plus Indigo Plateau), and link play is pointless in a Snom-only game, so one hook
change (`TX_SCRIPT_CABLE_CLUB_RECEPTIONIST`) covers the whole map. Rejected: one NPC
in Lavender or Celadon (backtracking for anyone who skips an early move). Free,
because it's a soft-lock fix, not a reward. It lists Lv 1 moves too (so a dropped
Powder Snow comes back). Link battles and trades are gone; `cable_club_npc.asm` is
left in place, unused.

## 2026-10-20: Agent goal is the whole game, unassisted (approach open)

Jordan wants the agent to play all of Snow Blue on its own, not just battles. Open:
what "on its own" means (learns from nothing via RL, or autonomous with tools we build
such as pathfinding and a RAM reader), and what makes decisions (RL policy, local LLM
via Ollama, Claude, or layers of those). Jordan wants to be part of these calls.

## 2026-10-20: Agent architecture: layered (closes the approach question above)

Jordan picked the layered design: we build skills (a RAM reader, a pathfinder from the
disassembly's map data, a battle routine) and the agent plays the whole game with no
human input. The battle brain is learned with RL from save states, since battles are
where a one-Snom run is hard; a planning brain (LLM: local via Ollama, or Claude; open)
picks goals and decides when to grind or heal. Rejected: pure RL from nothing
(unrealistic for a whole game on a laptop) and a pure LLM agent (weakest where Snow
Blue is hardest). Jordan's turns.csv is the benchmark.

## 2026-10-20: Renamed to "Pale Blue"; the title screen is all Snom, in poses

Jordan renamed the game Pale Blue. The repo, folder and internal "snow-blue" names stay
until the GitHub repo exists (renaming the folder mid-playthrough would break the venv
and logger paths); the GitHub repo can start as `pale-blue`. Title lettering ("Pale
Blue" vs "Pale Blue Version") is open, mocked in `art/out/lettering_on_title.png`.
The title screen's Pokémon are all Snom, each time in a random one of seven poses Jordan
approved (normal, look back, hop, blink, happy, sleepy, surprised), never the same twice
running. Poses are code-defined edits of `art/snom_front.png` in `art/build_snom.py`,
so they follow edits to the front sprite (as long as the eye stays put). They live in
their own pics section because Snom's pic bank is full. Snom is peach on the SGB title
because the title gives the mon, the player and the copyright one shared palette.

## 2026-10-20: Title says "Pale Blue"; Snom gets its own icy palette (closes the lettering item)

Jordan picked "Pale Blue" (42 px, shorter than "Pale Blue Version"). It's built by
`art/build_title_text.py` into `gfx/title/blue_version.png`, same font as the original
plus a drawn P and a. On the SGB title, a fourth colour block gives Snom's 5x5 pic area
PAL_CYANMON (palette slot 3 was unused). The player's fist and ball sit inside that
area, so they tint blue too; Jordan accepted it ("no worries if it ends weird").
The SGB border still says BLUE with the vanilla starters.

## 2026-10-20: Title lettering is "Pale Blue Version", centred (supersedes "Pale Blue" above)

Jordan changed it to "Pale Blue Version" and pointed out the lettering sat off centre.
It's 80 px with 4 px word gaps (the original used 6), filling the 10 tiles the title
reserves for this text, printed from column 5 so it's centred on screen (the vanilla
8-tile slot at column 7 sits 8 px right of centre).

## 2026-10-20: Relearner crash: dormant vanilla bug in the move list menu; save lost to 22:07

Picking Leech Life in the relearner froze Jordan's game and filled RAM with junk (a
rescue script that copied RAM into save format found nothing usable). Cause: when you
pick from a MOVESLISTMENU, home/list_menu.asm looks the entry up with GetName in
ItemNames' bank while the redraw has left wNameListType at MOVE_NAME, so it copies 20
bytes of the wrong bank into wNameBuffer. For some moves those bytes hold no '@', and
CopyToStringBuffer then copies through all of RAM. Vanilla never picks from a move list,
so the bug never fired. Fix: that menu path calls GetMoveName for move lists. Tested on
fresh states: the exact Aurora Beam then Leech Life sequence, plus every list entry.
First suspect (setting wNameListType before opening the menu) didn't work, because each
redraw resets it. Jordan lost the shopping and relearns after the 22:07 save, which is
backed up in saves_backup/. Separately, the ROM had been rebuilt while mGBA ran it;
that wasn't the cause (it reproduces on a clean build) but is now banned in CLAUDE.md.

## 2026-10-21: ????, the floating Snom under the Vermilion Dock truck

A post-game superboss Jordan designed: press A on the dock truck (the one from the Mew
myth) to fight ????, Lv 100, Ice/Psychic, Psychic/Blizzard/Amnesia/Light Screen. Win and
Snom learns Psychic, which it can't get any other way (decline it and the truck offers it
again). Leech Life (Bug beats Psychic in Gen 1) plus Light Screen and Amnesia is the
intended answer. Pink floating sprite with stars and happy eyes (mockup E, approved),
built from the editable front in art/build_snom.py. Species slot $20 (a MissingNo. slot)
with no Pokédex number: GetMonHeader, UncompressMonSprite and the palette lookup
special-case STARSNOM, and the battle's "seen" flag is skipped for dex 0 (which also
defuses the vanilla MissingNo. item glitch). Four spare event flags after the dock's.
To make the truck reachable at all: the dock guard now lets you in after the S.S. Anne
sails (vanilla needed a traded Cut user to ever get there), and the dock swaps the ship's
blocks for water on load. Base stats are 100s for now; tuning by simulation is open.

## 2026-10-21: Marts sell PP restores instead of Poké Balls

With one Pokémon, every fight drains the same four moves, and Jordan gave up more than
once mid-dungeon on empty PP (and ran dry at the Elite Four). Vanilla prices PP items at
₽0, so no mart could sell them, while every mart sells balls Pale Blue can't use. Balls
are swapped out: Ether (₽1,200) in the early marts, Ether + Max Ether (₽2,000) from
Celadon/Fuchsia/Saffron/Cinnabar, Elixir (₽3,000) + Max Elixir (₽4,500) at Indigo
Plateau. Prices follow later generations. Jordan's save got ₽50,000 (edited, checksum
fixed; backup in saves_backup/).

## 2026-10-21: Continue refreshes the tileset's ROM pointers

Saves store ROM addresses (wTilesetCollisionPtr and friends). Adding code to the home
bank moved the collision lists 14 bytes, so Jordan's save loaded with a pointer into the
wrong list and every tile counted as a wall. Fix: CopyTilesetHeader (split out of
LoadTilesetHeader, without its warp-position side effects) runs when you pick Continue,
so any save loads cleanly in any later build.

## 2026-10-21: Snom surfs, Snom is the party icon, and the credits are all Snom

Jordan's picks after beating the game. Surf sprite: Wild Card's follower Snom
(art/raw/overworld.png), cropped to 16x16 and shaded flat (option B), written over
gfx/sprites/seel.png by art/build_snom.py. Gen 1's "water" party icon is that same Seel
sprite, so Snom's menu icon is now ICON_WATER and shows the same Snom (the bug icon is
untouched). Credits: every person and team name reads SNOM (job titles kept), the heading
is PALE BLUE STAFF, every credits Pokémon is Snom, and ???? makes a cameo third from last
(LoadFrontSpriteByMonIndex lets STARSNOM through the dex-0 "Rhydon trap"). Credits tested
only by their pieces: jumping into the credits routine headless mangles the screen, so a
full run needs a real Elite Four win.
