; Snow Blue: ????, the floating Snom under the Vermilion Dock truck (a Lv 100 superboss).
; Not in BaseStats (it has no Pokédex number); GetMonHeader special-cases STARSNOM.
	db 0 ; pokedex id

	db 100, 100, 100, 100, 100
	;   hp  atk  def  spd  spc

	db ICE, PSYCHIC_TYPE ; type
	db 3 ; catch rate
	db 255 ; base exp

	INCBIN "gfx/pokemon/front/starsnom.pic", 0, 1 ; sprite dimensions
	dw StarSnomPicFront, StarSnomPicFront

	db PSYCHIC_M, BLIZZARD, AMNESIA, LIGHT_SCREEN ; level 1 learnset
	db GROWTH_SLOW ; growth rate

	; tm/hm learnset
	tmhm
	; end

	db 0 ; padding
