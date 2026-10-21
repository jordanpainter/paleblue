-- Snow Blue stats logger for mGBA (0.10+). Load it once per session:
-- Tools > Scripting..., then File > Load script... and pick this file.
--
-- stats/battles.csv: a row for every battle (wild, trainer, the old man's demo).
-- stats/saves.csv:   a snapshot of Snom every time you save in-game.
--
-- RAM addresses come from pokeblue.sym and names from constants/, both read from
-- the repo at load time, so a rebuild can't leave this script pointing at stale RAM.

local DIR = (script and script.dir) or debug.getinfo(1, "S").source:match("^@(.*)[/\\]") or "."
local ROOT = DIR .. "/.."

local function slurp(path)
	local f = assert(io.open(path, "rb"), "can't open " .. path)
	local t = f:read("*a")
	f:close()
	return t
end

local SYM, BANK = {}, {}
for line in slurp(ROOT .. "/pokeblue.sym"):gmatch("[^\r\n]+") do
	local bank, addr, name = line:match("^(%x+):(%x+) ([%w_]+)$")
	if addr then SYM[name], BANK[name] = tonumber(addr, 16), tonumber(bank, 16) end
end

-- Every constant line we care about ends in its value as a hex comment ("; $1F" or "; a5").
local function names(file, kinds)
	local t = {}
	for line in slurp(ROOT .. "/constants/" .. file):gmatch("[^\r\n]+") do
		local kind, name, hex = line:match("^%s*([%w_]+)%s+([%w_]+).-;%s*%$?(%x+)%s*$")
		if kind and kinds[kind] then t[tonumber(hex, 16)] = kinds[kind] .. (name:gsub("_", " ")) end
	end
	return t
end
local MON = names("pokemon_constants.asm", { const = "" })
local MOVE = names("move_constants.asm", { const = "" })
local MAP = names("map_constants.asm", { map_const = "" })
local ITEM = names("item_constants.asm", { const = "", add_tm = "TM ", add_hm = "HM " })
local TRAINER = names("trainer_constants.asm", { trainer_const = "" })

local LOST_BATTLE, PARTYMON_STRUCT_LENGTH = 0xFF, 44
local FPS = 59.73

local function rd(name, off) return emu:read8(SYM[name] + (off or 0)) end
local function rd16(name, off) off = off or 0; return rd(name, off) * 256 + rd(name, off + 1) end
local function bcd(name, n)
	local v = 0
	for i = 0, n - 1 do
		local b = rd(name, i)
		v = v * 100 + (b >> 4) * 10 + (b & 15)
	end
	return v
end
local function text(name, max) -- the game's charmap, letters only (rival names)
	local s = ""
	for i = 0, max - 1 do
		local c = rd(name, i)
		if c == 0x50 then break end
		if c >= 0x80 and c <= 0x99 then s = s .. string.char(65 + c - 0x80) end
	end
	return s
end

local function badges()
	local b, n = rd("wObtainedBadges"), 0
	for i = 0, 7 do n = n + ((b >> i) & 1) end
	return n
end
local function bag()
	local t = {}
	for i = 0, rd("wNumBagItems") - 1 do t[rd("wBagItems", 2 * i)] = rd("wBagItems", 2 * i + 1) end
	return t
end
local function common()
	return {
		time = os.date("%Y-%m-%d %H:%M:%S"),
		playtime = string.format("%d:%02d", rd("wPlayTimeHours"), rd("wPlayTimeMinutes")),
		map = MAP[rd("wCurMap")] or rd("wCurMap"),
		badges = badges(),
		level = rd("wPartyMon1Level"),
		exp = rd("wPartyMon1Exp") * 65536 + rd16("wPartyMon1Exp", 1),
		money = bcd("wPlayerMoney", 3),
		bag = bag(),
	}
end

local checked = {}

-- A file written by an older version of this script gets the new trailing columns, left
-- empty on its old rows.
local function upgrade(path, header)
	local old = slurp(path)
	local first = old:match("^[^\n]*")
	if first == header or header:sub(1, #first + 1) ~= first .. "," then return end
	local pad = select(2, header:gsub(",", "")) - select(2, first:gsub(",", ""))
	local f = assert(io.open(path, "w"))
	f:write(header .. "\n")
	for line in old:gmatch("[^\n]+") do
		if line ~= first then f:write(line .. string.rep(",", pad) .. "\n") end
	end
	f:close()
end

local function csv(file, header, row)
	local path = DIR .. "/" .. file
	local f = io.open(path, "r")
	local fresh = f == nil
	if f then f:close() end
	if not fresh and not checked[file] then upgrade(path, table.concat(header, ",")) end
	checked[file] = true
	f = assert(io.open(path, "a"))
	if fresh then f:write(table.concat(header, ",") .. "\n") end
	local out = {}
	for i, k in ipairs(header) do
		local v = tostring(row[k] == nil and "" or row[k])
		if v:find('[,"]') then v = '"' .. v:gsub('"', '""') .. '"' end
		out[i] = v
	end
	f:write(table.concat(out, ",") .. "\n")
	f:close()
end

local b = nil        -- the battle in progress
local battles = 0    -- this session's count, to keep battle ids unique within a second

-- Turn by turn ---------------------------------------------------------------
-- Gen 1 keeps no turn counter and mGBA 0.10 scripts can't stop on game code, so this
-- transcribes the battle text box: every message that finishes printing becomes a row
-- with both sides' HP, status, stat stages and effects at that moment. A new turn
-- starts when the FIGHT menu comes up after something has happened.

local TURN_COLS = { "battle", "turn", "message", "actor", "action",
	"snom_hp", "snom_max_hp", "snom_status", "snom_mods", "snom_effects",
	"enemy", "enemy_level", "enemy_hp", "enemy_max_hp", "enemy_status", "enemy_mods", "enemy_effects" }

local CHARS = { [0x7F] = " ", [0x75] = "…", [0x9A] = "(", [0x9B] = ")", [0x9C] = ":", [0x9D] = ";",
	[0x9E] = "[", [0x9F] = "]", [0xBA] = "é", [0xBB] = "'d", [0xBC] = "'l", [0xBD] = "'s",
	[0xBE] = "'t", [0xBF] = "'v", [0xE0] = "'", [0xE1] = "PK", [0xE2] = "MN", [0xE3] = "-",
	[0xE4] = "'r", [0xE5] = "'m", [0xE6] = "?", [0xE7] = "!", [0xE8] = ".", [0xEF] = "♂",
	[0xF0] = "¥", [0xF1] = "×", [0xF3] = "/", [0xF4] = ",", [0xF5] = "♀" }
for i = 0, 25 do CHARS[0x80 + i], CHARS[0xA0 + i] = string.char(65 + i), string.char(97 + i) end
for i = 0, 9 do CHARS[0xF6 + i] = tostring(i) end

local function boxRow(y) -- the battle text box's lines are tile map rows 14 and 16
	local s = {}
	for x = 1, 18 do s[#s + 1] = CHARS[emu:read8(SYM.wTileMap + y * 20 + x)] or "" end
	return table.concat(s):match("^%s*(.-)%s*$")
end

local function status(label)
	local s = rd(label)
	if s & 7 ~= 0 then return "SLP" end
	return (s >> 3) & 1 == 1 and "PSN" or (s >> 4) & 1 == 1 and "BRN"
		or (s >> 5) & 1 == 1 and "FRZ" or (s >> 6) & 1 == 1 and "PAR" or ""
end

local STAT_NAMES = { "atk", "def", "spd", "spc", "acc", "eva" }
local function mods(label) -- stat stages, 7 is neutral
	local t = {}
	for i = 0, 5 do
		local v = rd(label, i) - 7
		if v ~= 0 then t[#t + 1] = string.format("%s%+d", STAT_NAMES[i + 1], v) end
	end
	return table.concat(t, " ")
end

local EFFECTS = { -- {battle status byte, bit, name}, from constants/battle_constants.asm
	{ 1, 0, "bide" }, { 1, 4, "charging" }, { 1, 5, "trapping" }, { 1, 7, "confused" },
	{ 2, 1, "mist" }, { 2, 2, "focus energy" }, { 2, 4, "substitute" }, { 2, 5, "recharging" },
	{ 2, 7, "seeded" }, { 3, 0, "toxic" }, { 3, 1, "light screen" }, { 3, 2, "reflect" },
	{ 3, 3, "transformed" } }
local function effects(side)
	local t = {}
	for _, e in ipairs(EFFECTS) do
		if (rd(side .. "BattleStatus" .. e[1]) >> e[2]) & 1 == 1 then t[#t + 1] = e[3] end
	end
	return table.concat(t, "; ")
end

local function logMessage(msg)
	local actor, action = msg:match("^(.-) used (.-)!$")
	local row = {
		battle = b.id, turn = b.turn, message = msg, actor = actor, action = action,
		enemy = MON[rd("wEnemyMonSpecies")], enemy_level = rd("wEnemyMonLevel"),
		enemy_hp = rd16("wEnemyMonHP"), enemy_max_hp = rd16("wEnemyMonMaxHP"),
		enemy_status = status("wEnemyMonStatus"), enemy_mods = mods("wEnemyMonStatMods"),
		enemy_effects = effects("wEnemy"),
	}
	if rd("wBattleMonSpecies") ~= 0 then -- blank until Snom is sent out
		row.snom_hp, row.snom_max_hp = rd16("wBattleMonHP"), rd16("wBattleMonMaxHP")
		row.snom_status, row.snom_mods = status("wBattleMonStatus"), mods("wPlayerMonStatMods")
		row.snom_effects = effects("wPlayer")
	end
	csv("turns.csv", TURN_COLS, row)
end

local function trackText()
	local text = (boxRow(14) .. " " .. boxRow(16)):match("^%s*(.-)%s*$")
	if text ~= b.text then b.text, b.still = text, 0; return end
	b.still = b.still + 1
	-- finished printing = unchanged for longer than the text speed's per-letter delay
	if b.still ~= (rd("wOptions") & 7) + 3 then return end
	if text:find("FIGHT") and text:find("RUN") then
		if b.events > 0 then b.turn, b.events = b.turn + 1, 0 end
	elseif text:find("[!?.]$") then
		logMessage(text)
		b.events = b.events + 1
	end
end

-- Battles ------------------------------------------------------------------

local BATTLE_COLS = { "time", "playtime", "map", "badges", "kind", "opponent", "enemy_team", "result",
	"level_start", "level_end", "hp_start", "hp_end", "max_hp", "exp_gained", "money_change",
	"items_used", "game_seconds", "battle" }

local settle = 0     -- frames left before writing a finished battle (blackout halves money just after)

local function finishBattle()
	local now = common()
	local row = {
		time = b.start.time, playtime = b.start.playtime, map = b.start.map, badges = b.start.badges,
		level_start = b.start.level, level_end = now.level,
		hp_start = b.hpStart, hp_end = b.hp, max_hp = b.maxHp,
		exp_gained = now.exp - b.start.exp, money_change = now.money - b.start.money,
		game_seconds = string.format("%.0f", b.frames / FPS), battle = b.id,
	}
	local used = {}
	for id, n in pairs(b.start.bag) do
		local left = now.bag[id] or 0
		if left < n then used[#used + 1] = (ITEM[id] or id) .. " x" .. (n - left) end
	end
	table.sort(used)
	row.items_used = table.concat(used, "; ")

	local lost = b.lost or b.hp == 0
	if b.inBattle == 2 then
		local name = TRAINER[b.class] or ("trainer " .. tostring(b.class))
		if name:match("^RIVAL") then name = text("wRivalName", 8) .. " (" .. name .. ")" end
		local team = {}
		for i = 0, rd("wEnemyPartyCount") - 1 do
			team[#team + 1] = (MON[rd("wEnemyPartySpecies", i)] or "?") .. " " .. rd("wEnemyMon1Level", i * PARTYMON_STRUCT_LENGTH)
		end
		row.kind, row.opponent, row.enemy_team = "trainer", name, table.concat(team, "; ")
		row.result = lost and "lost" or "won"
	else
		row.kind = b.oldMan and "old man demo" or "wild"
		row.opponent = MON[b.opp] or tostring(b.opp)
		row.enemy_team = row.opponent .. " " .. tostring(b.wildLevel)
		row.result = lost and "lost" or (b.enemyHp == 0 and "won" or "escaped")
	end
	csv("battles.csv", BATTLE_COLS, row)
	console:log(string.format("[stats] %s vs %s: %s", row.kind, row.opponent, row.result))
	b = nil
end

local function trackBattle()
	local inb = rd("wIsInBattle")
	if inb ~= 0 then
		if settle > 0 then finishBattle(); settle = 0 end -- a new battle before the old one settled
		if not b then
			b = { start = common(), frames = 0, lost = false,
				hpStart = rd16("wPartyMon1HP"), maxHp = rd16("wPartyMon1Stats"),
				turn = 0, events = 0, text = "", still = 0 }
			battles = battles + 1
			b.id = os.date("%Y%m%d-%H%M%S-") .. battles -- joins battles.csv to turns.csv
			b.hp = b.hpStart
		end
		b.frames = b.frames + 1
		if inb == LOST_BATTLE then b.lost = true else b.inBattle = inb end
		if inb == 2 and rd("wTrainerClass") ~= 0 then b.class = rd("wTrainerClass") end
		if rd("wBattleType") == 1 then b.oldMan = true end
		-- wild: wCurOpponent stays 0 for random encounters, so read the battle struct
		-- (it holds the last fight's mon for the first frames; the last value wins)
		if b.inBattle == 1 and rd("wEnemyMonSpecies") ~= 0 then
			b.opp, b.wildLevel = rd("wEnemyMonSpecies"), rd("wEnemyMonLevel")
		end
		-- the battle structs hold the previous fight's numbers until the mons are sent out,
		-- which is fine: only the last value counts
		if rd("wBattleMonSpecies") ~= 0 then b.hp = rd16("wBattleMonHP") end
		if rd("wEnemyMonSpecies") ~= 0 then b.enemyHp = rd16("wEnemyMonHP") end
		trackText()
	elseif b then
		if settle == 0 then settle = 60 end
		settle = settle - 1
		if settle == 0 then finishBattle() end
	end
end

-- Saves --------------------------------------------------------------------

local SAVE_COLS = { "time", "playtime", "map", "badges", "level", "hp", "max_hp", "attack", "defense",
	"speed", "special", "exp", "moves", "money" }
local SAV = ROOT .. "/pokeblue.sav"

-- Only the save block itself: the game also uses the save chip as scratch space for
-- decompressing Pokémon pics, so the rest of the file changes without any saving.
local function sramOffset(name) return BANK[name] * 0x2000 + SYM[name] - 0xA000 end
local SAVE_FROM, SAVE_TO = sramOffset("sGameData") + 1, sramOffset("sMainDataCheckSum") + 1

local function savFile()
	local f = io.open(SAV, "rb")
	if not f then return nil end
	local t = f:read("*a")
	f:close()
	return t:sub(SAVE_FROM, SAVE_TO)
end

local function snapshot()
	local row = common()
	local stat = function(i) return rd16("wPartyMon1Stats", 2 * i) end
	row.hp, row.max_hp = rd16("wPartyMon1HP"), stat(0)
	row.attack, row.defense, row.speed, row.special = stat(1), stat(2), stat(3), stat(4)
	local moves = {}
	for i = 0, 3 do
		local m = rd("wPartyMon1Moves", i)
		if m ~= 0 then moves[#moves + 1] = MOVE[m] or m end
	end
	row.moves = table.concat(moves, "; ")
	csv("saves.csv", SAVE_COLS, row)
	console:log(string.format("[stats] saved: Snom Lv %d, %d badges", row.level, row.badges))
end

local lastSav, pending, frame = savFile(), nil, 0

local function trackSaves()
	frame = frame + 1
	if frame % 120 ~= 0 then return end -- the .sav lands on disk a moment after the game writes it
	local now = savFile()
	if now == lastSav then pending = nil; return end
	if now ~= pending then pending = now; return end -- wait for the file to hold still
	lastSav, pending = now, nil
	snapshot()
end

local lastError
-- Loading the script again replaces the running copy instead of logging everything twice.
if SNOW_BLUE_STATS_CALLBACK then callbacks:remove(SNOW_BLUE_STATS_CALLBACK) end
SNOW_BLUE_STATS_CALLBACK = callbacks:add("frame", function()
	if not emu then return end
	local ok, err = pcall(function() trackBattle(); trackSaves() end)
	if not ok then
		b, settle = nil, 0 -- drop the battle rather than fail on every frame after
		if err ~= lastError then console:error("[stats] " .. tostring(err)) end
		lastError = err
	end
end)

console:log("[stats] Snow Blue logger running: writing to " .. DIR .. "/battles.csv and saves.csv")
