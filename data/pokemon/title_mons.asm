TitleMons:
; mons on the title screen are randomly chosen from here
IF DEF(_RED)
	db STARTER1
	db STARTER2
	db STARTER3
	db WEEDLE
	db NIDORAN_M
	db SCYTHER
	db PIKACHU
	db CLEFAIRY
	db RHYDON
	db ABRA
	db GASTLY
	db DITTO
	db PIDGEOTTO
	db ONIX
	db PONYTA
	db MAGIKARP
ENDC
IF DEF(_BLUE)
; Snow Blue: there is only Snom
	REPT 16
	db SNOM
	ENDR
ENDC
