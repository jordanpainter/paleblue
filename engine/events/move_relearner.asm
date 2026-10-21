; Snow Blue: the Cable Club receptionist in every Pokémon Center remembers moves instead.
; With one Pokémon for the whole game, a move skipped at level-up would be gone for good.
; Lives next to EvosMovesPointerTable so it can read learnsets directly.
MoveRelearner::
	ld hl, MoveRelearnerHelloText
	call PrintText
	call YesNoChoice
	ld a, [wCurrentMenuItem]
	and a
	jr nz, .bye
	xor a
	ld [wWhichPokemon], a ; the one and only
	call BuildRelearnableMoves
	ld a, [wItemList]
	and a
	jr z, .nothingToRemember
	ld hl, MoveRelearnerWhichMoveText
	call PrintText
	ld hl, wItemList
	ld a, l
	ld [wListPointer], a
	ld a, h
	ld [wListPointer + 1], a
	xor a
	ld [wCurrentMenuItem], a
	ld [wListScrollOffset], a
	ld [wPrintItemPrices], a
	ld a, MOVESLISTMENU
	ld [wListMenuID], a
	call DisplayListMenuID
	jr c, .bye
	ld a, [wCurListMenuItem]
	ld [wMoveNum], a
	ld [wNamedObjectIndex], a
	call GetMoveName
	call CopyToStringBuffer
	xor a
	ld [wWhichPokemon], a
	predef LearnMove
.bye
	ld hl, MoveRelearnerByeText
	jp PrintText
.nothingToRemember
	ld hl, MoveRelearnerNothingText
	jp PrintText

; Fills wItemList (count, moves, $ff) with the first party mon's level 1 moves and
; level-up moves up to its level that it doesn't know right now.
BuildRelearnableMoves:
	ld hl, wItemList + 1
	ld c, 0
	ld a, [wPartySpecies]
	ld [wCurSpecies], a
	call GetMonHeader
	ld de, wMonHMoves
	ld b, NUM_MOVES
.levelOneMovesLoop
	ld a, [de]
	inc de
	call .tryAdd
	dec b
	jr nz, .levelOneMovesLoop
	push hl
	ld a, [wPartySpecies]
	dec a
	ld hl, EvosMovesPointerTable
	ld d, 0
	ld e, a
	add hl, de
	add hl, de
	ld a, [hli]
	ld h, [hl]
	ld l, a
.skipEvolutionDataLoop
	ld a, [hli]
	and a
	jr nz, .skipEvolutionDataLoop
	ld d, h
	ld e, l
	pop hl
.learnSetLoop
	ld a, [de] ; level
	inc de
	and a
	jr z, .done
	ld b, a
	ld a, [de] ; move
	inc de
	push af
	ld a, [wPartyMon1Level]
	cp b
	jr c, .notYet
	pop af
	call .tryAdd
	jr .learnSetLoop
.notYet
	pop af
	jr .learnSetLoop
.done
	ld [hl], $ff
	ld a, c
	ld [wItemList], a
	ret

; adds move a at hl (c moves listed so far) unless it's NO_MOVE, known or already listed
.tryAdd
	and a
	ret z
	push bc
	push de
	push hl
	ld d, a
	ld hl, wPartyMon1Moves
	ld b, NUM_MOVES
.knownLoop
	ld a, [hli]
	cp d
	jr z, .skip
	dec b
	jr nz, .knownLoop
	ld a, c
	and a
	jr z, .add
	ld b, c
	ld hl, wItemList + 1
.listedLoop
	ld a, [hli]
	cp d
	jr z, .skip
	dec b
	jr nz, .listedLoop
.add
	pop hl
	ld [hl], d
	inc hl
	pop de
	pop bc
	inc c
	ret
.skip
	pop hl
	pop de
	pop bc
	ret

MoveRelearnerHelloText:
	text "Hi! I help #MON"
	line "remember moves"
	cont "they've forgotten."

	para "Shall I jog your"
	line "#MON's memory?"
	done

MoveRelearnerWhichMoveText:
	text "Which move should"
	line "it remember?"
	done

MoveRelearnerNothingText:
	text "Hmm. Your #MON"
	line "already knows"
	cont "everything it can"
	cont "remember!"
	done

MoveRelearnerByeText:
	text "Come back if it"
	line "forgets again!"
	done
