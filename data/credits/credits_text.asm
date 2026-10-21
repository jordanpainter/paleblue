CreditsTextPointers:
; Snow Blue: every name is SNOM (job titles kept)
; entries correspond to CRED_* constants
	table_width 2
	dw CredVersion
	dw CredTajiri
	dw CredTaOota
	dw CredMorimoto
	dw CredWatanabe
	dw CredMasuda
	dw CredNisino
	dw CredSugimori
	dw CredNishida
	dw CredMiyamoto
	dw CredKawaguchi
	dw CredIshihara
	dw CredYamauchi
	dw CredZinnai
	dw CredHishida
	dw CredSakai
	dw CredYamaguchi
	dw CredYamamoto
	dw CredTaniguchi
	dw CredNonomura
	dw CredFuziwara
	dw CredMatsusima
	dw CredTomisawa
	dw CredKawamoto
	dw CredKakei
	dw CredTsuchiya
	dw CredTaNakamura
	dw CredYuda
	dw CredMon
	dw CredDirector
	dw CredProgrammers
	dw CredCharDesign
	dw CredMusic
	dw CredSoundEffects
	dw CredGameDesign
	dw CredMonsterDesign
	dw CredGameScene
	dw CredParam
	dw CredMap
	dw CredTest
	dw CredSpecial
	dw CredProducers
	dw CredProducer
	dw CredExecutive
	dw CredTamada
	dw CredSaOota
	dw CredYoshikawa
	dw CredToOota
	dw CredUSStaff
	dw CredUSCoord
	dw CredTilden
	dw CredKawakami
	dw CredHiNakamura
	dw CredGiese
	dw CredOsborne
	dw CredTrans
	dw CredOgasawara
	dw CredIwata
	dw CredIzushi
	dw CredHarada
	dw CredMurakawa
	dw CredFukui
	dw CredClub
	dw CredPAAD
	assert_table_length NUM_CRED_STRINGS

CredVersion:
IF DEF(_RED)
	db -8, "RED VERSION STAFF@"
ENDC
IF DEF(_BLUE)
	db -7, "PALE BLUE STAFF@" ; Snow Blue
ENDC
CredTajiri:
	db -2, "SNOM@"
CredTaOota:
	db -2, "SNOM@"
CredMorimoto:
	db -2, "SNOM@"
CredWatanabe:
	db -2, "SNOM@"
CredMasuda:
	db -2, "SNOM@"
CredNisino:
	db -2, "SNOM@"
CredSugimori:
	db -2, "SNOM@"
CredNishida:
	db -2, "SNOM@"
CredMiyamoto:
	db -2, "SNOM@"
CredKawaguchi:
	db -2, "SNOM@"
CredIshihara:
	db -2, "SNOM@"
CredYamauchi:
	db -2, "SNOM@"
CredZinnai:
	db -2, "SNOM@"
CredHishida:
	db -2, "SNOM@"
CredSakai:
	db -2, "SNOM@"
CredYamaguchi:
	db -2, "SNOM@"
CredYamamoto:
	db -2, "SNOM@"
CredTaniguchi:
	db -2, "SNOM@"
CredNonomura:
	db -2, "SNOM@"
CredFuziwara:
	db -2, "SNOM@"
CredMatsusima:
	db -2, "SNOM@"
CredTomisawa:
	db -2, "SNOM@"
CredKawamoto:
	db -2, "SNOM@"
CredKakei:
	db -2, "SNOM@"
CredTsuchiya:
	db -2, "SNOM@"
CredTaNakamura:
	db -2, "SNOM@"
CredYuda:
	db -2, "SNOM@"
CredMon:
	db -3, "#MON@"
CredDirector:
	db -3, "DIRECTOR@"
CredProgrammers:
	db -5, "PROGRAMMERS@"
CredCharDesign:
	db -7, "CHARACTER DESIGN@"
CredMusic:
	db -2, "MUSIC@"
CredSoundEffects:
	db -6, "SOUND EFFECTS@"
CredGameDesign:
	db -5, "GAME DESIGN@"
CredMonsterDesign:
	db -6, "MONSTER DESIGN@"
CredGameScene:
	db -6, "GAME SCENARIO@"
CredParam:
	db -8, "PARAMETRIC DESIGN@"
CredMap:
	db -4, "MAP DESIGN@"
CredTest:
	db -7, "PRODUCT TESTING@"
CredSpecial:
	db -6, "SPECIAL THANKS@"
CredProducers:
	db -4, "PRODUCERS@"
CredProducer:
	db -4, "PRODUCER@"
CredExecutive:
	db -8, "EXECUTIVE PRODUCER@"
CredTamada:
	db -2, "SNOM@"
CredSaOota:
	db -2, "SNOM@"
CredYoshikawa:
	db -2, "SNOM@"
CredToOota:
	db -2, "SNOM@"
CredUSStaff:
	db -7, "US VERSION STAFF@"
CredUSCoord:
	db -7, "US COORDINATION@"
CredTilden:
	db -2, "SNOM@"
CredKawakami:
	db -2, "SNOM@"
CredHiNakamura:
	db -2, "SNOM@"
CredGiese:
	db -2, "SNOM@"
CredOsborne:
	db -2, "SNOM@"
CredTrans:
	db -7, "TEXT TRANSLATION@"
CredOgasawara:
	db -2, "SNOM@"
CredIwata:
	db -2, "SNOM@"
CredIzushi:
	db -2, "SNOM@"
CredHarada:
	db -2, "SNOM@"
CredMurakawa:
	db -2, "SNOM@"
CredFukui:
	db -2, "SNOM@"
CredClub:
	db -2, "SNOM@"
CredPAAD:
	db -2, "SNOM@"
