	db DEX_SNOM ; pokedex id

	db  30,  25,  35,  20,  45
	;   hp  atk  def  spd  spc

	db ICE, BUG ; type
	db 190 ; catch rate
	db 37 ; base exp

	INCBIN "gfx/pokemon/front/snom.pic", 0, 1 ; sprite dimensions
	dw SnomPicFront, SnomPicBack

	db POWDER_SNOW, STRING_SHOT, NO_MOVE, NO_MOVE ; level 1 learnset
	db GROWTH_MEDIUM_FAST ; growth rate

	; tm/hm learnset
	tmhm TOXIC,        ICE_BEAM,     BLIZZARD,     MIMIC,        DOUBLE_TEAM,  \
	     REFLECT,      BIDE,         REST,         SUBSTITUTE
	; end

	db 0 ; padding
