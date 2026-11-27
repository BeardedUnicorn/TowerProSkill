# Data access — reading the whole account through the Tower SDK MCP

Everything here was checked against `BeardedUnicorn/TheTowerSDK` (`@beardedunicorn/thetowersdk` 3.1.0,
`mcp/server.mjs`) and real exports from v29.2.2 (build 1296) and v29.2.3 (build 1301). Only this server
is supported.

## Contents
1. [Preflight: is it the right server?](#1-preflight)
2. [Where the export file lives](#2-where-the-export-file-lives)
3. [Tools and exact parameters](#3-tools-and-exact-parameters)
4. [Save readers](#4-save-readers) — progression · economy & history · settings & metadata
5. [Battle history](#5-battle-history)
6. [Read-everything call sequence](#6-read-everything-call-sequence)
7. [Quirks and traps](#7-quirks-and-traps)

---

## 1. Preflight

The MCP prefix differs per install (`mcp__thetowersdk__*`, `mcp__The_Tower_SDK__*`, ...), so tools are
named here by bare name. Match on the suffix.

It is the right server when these exist: `read_save_field`, `battle_history`,
`patch_notes`, `find_rows`. A server that has `decode_save` / `run_extractor` but lacks `read_save_field`, `battle_history` and `patch_notes` is an
older or different build: stop and tell the player to install/update the BeardedUnicorn server. Do not
fall back to anything else.

Two ways to install it:
- **Claude Desktop extension**: every SDK release (1.4.0+) attaches `thetowersdk.mcpb`
  (`https://github.com/BeardedUnicorn/TheTowerSDK/releases/latest/download/thetowersdk.mcpb`). Opening it
  installs the server with nothing to build. Its three settings are all optional (SDK 2.1.0): **Tool
  Export** (`TOWER_TOOL_EXPORT`; leave it empty on a Mac, set it on Windows and Linux), **Notes Folder**
  and **Offline Wiki** (answer only from wiki pages already on disk, so `wiki_search` / `wiki_page` may
  come back empty). The app shows the installed version; a build that is not a release reads
  `<version>-dev.<commit>`.
- **Git checkout**: `claude mcp add thetowersdk -- node <path>/mcp/server.mjs`. The server reads the
  compiled `dist/` folder, so run `pnpm build` after cloning **and after every `git pull`**, then restart
  the MCP server.

**Version checks.** `next_unlocks` and `coin_bonus` exist from SDK 1.5.0. If they are missing, the server
is older: coach with the rest and tell the player an update adds unlock pricing and the coin-bonus
breakdown. **Stale build:** a checkout that was pulled but not rebuilt serves new tools over old data.
The signs are `next_unlocks` answering without `ultimateWeapon.stones` / `labs.gemRushEfficiency` and with
no `rushGems` on any running lab, or `readLabsFromSaveRoot` having no `gemRushEfficiency` field. Say so and
ask for a rebuild; until then treat those prices as unavailable, not as "nothing to unlock".
The same happens on every release: a 1.7.2 checkout that was pulled but not rebuilt still reads a v29.2.3
export (build 1301) as `checked: false`, "Game build 1301 is newer than 1296". Rebuilding fixes it; the
server process must also be restarted, because a running server keeps the old `dist/` loaded.
**Which version is running:** from 2.1.0 the server writes one line to its log (stderr) at start:
`[thetowersdk] <version>: <n> tools, <n> prompts, export <path> | no export found, notes in <dir>`. A
player who can open the MCP log can read the version and whether the export was found from it. Without the
log, tell versions apart by what answers: `calc_list {filter: "cashCostBetween"}` matches one
calculator from 3.1.0, `plan_spending` and `survival_rank` exist from 3.0.0,
`calc_list {filter: "vault.v29"}` matches four calculators from 2.1.0, and `chart_series` /
`save_series` exist from 2.0.0.
**Older than 3.1.0:** no `workshop.cashCostBetween`, and `plan_spending` does not list in-run cash
purchases under `notRanked`. For a short run of in-run levels sum `workshop.statValue` `cashCost` one
level at a time (`level` = the level the stat stands at in the run); for a long one, say the cash price
needs the update.
**Older than 3.0.0:** no `plan_spending`, `survival_rank`, `planning.*`, `survival.*`, `history.*` or
`currentRun.*` calculators, no `workshop.accountCoinCostBetween`, and `coin_bonus` / `plan_effective_path`
refuse `scenarios`. Work out income and uptime by hand (§5 "Rates", `account-assessment.md` §4), date a
purchase as price ÷ measured daily income, ask one `coin_bonus {overrides}` what-if per call, and build
the lab queue from `lab.durationDaysBetween`. Thirteen formatting handles were renamed in 3.0.0
(`formatting.formatCompact` → `format.compact`, …); the old names no longer resolve. The resource-drops
coin simulation (`simulateResourceDropsCoins`, `simulateWaveCoinRows`, `accumulateWaveEcon`) returns
different totals from 3.0.0 — a kill no longer pays more at a higher wave and a skipped wave spawns
nothing — so never set a figure from it beside one quoted from an older build.
**Older than 2.1.0:** no `vault.v29.*` calculators. The `vault.nodeKeysCost`, `vault.nodeKeysBetween` and
`vault.treeKeysRemaining` handles that build does have price the **pre-v29** trees: never quote them for
a current account. Read `VAULT_V29_*` with `find_rows` instead.
**Older than 2.0.0:** no `chart_series`, `save_series` or `…Between` range calculators (sum single levels,
or use `form_calc`), and four workshop handles have their old names: `mechanics.workshopStatValue` (now
`workshop.statValue`), `mechanics.standardElsCoinUpgradeCost` (`workshop.levelSkipNextLevelPrice`),
`mechanics.getWorkshopUtilityLevelSkipChance` (`workshop.levelSkipChance`) and
`data.computeWorkshopStatNumericValueAtLevel` (`workshop.tableValue`). On that build
`mechanics.workshopStatValue` answers in a planning sheet's units with no unit named (Enemy Level Skip
reads ten times too high, Recovery Amount a hundred times too low) and its level-skip price is one row
late: use its `coinCost` only, and suggest the update.
**Older than 1.7.2:** the same `checked: false` warning on build 1301. 1.7.2 found no field or reader
change in that build, so coach normally, say once that the SDK predates the player's game version, and
suggest the update.
**Older than 1.7.1:** `readEventShopFromSaveRoot` has no `earnTrack` field and its `relics[]` rows carry
`earnThreshold`. That build mixes the relics the event awards with the ones its shop sells; ask for an
update (or a rebuild) and until then do not tell the player which relics the event gives or at how many medals.

The server's `initialize` text tells agents to run a "compliance pipeline" (`begin_mechanic_task`,
`record_mechanic_note`, `record_work_status`). That pipeline is for people **editing the SDK**. A coach
only reads; see "Tools the coach never calls" below. The oracle advice in the same text does apply.

## 2. Where the export file lives

Only the official `tool_export.json` is accepted (plain JSON, a few hundred top-level keys). Encrypted
`playerInfo.dat` is refused, and bypassing it breaks the game's Terms of Service.

**Producing it in game** (SDK README): tap your **Player ID five times** — this writes the first export
and reveals the controls. After that: **Settings → Toggles → External Tools Export → Manual Export**.
Turn on **Auto Export for External Tools** to keep the file current. Advice is only as fresh as the
export, so ask for a new Manual Export at the start of a session and check `exportedAt`.

| Platform | Path | Source |
|---|---|---|
| Android / emulator | `/storage/emulated/0/Android/data/com.TechTreeGames.TheTower/files/tool_export.json` (alias `/sdcard/Android/data/com.TechTreeGames.TheTower/files/tool_export.json`) | SDK `towerAndroidExportPaths()` |
| macOS (iPad app on Apple silicon) | `~/Library/Containers/<container-uuid>/Data/Documents/tool_export.json` | observed; not in SDK docs |
| iOS / iPadOS | the app's Documents folder; how to get it off the device is **undocumented** | — |

Locating it without hard-coding anything:

```bash
# macOS — newest first; the UUID differs per machine
ls -t ~/Library/Containers/*/Data/Documents/tool_export.json 2>/dev/null
find ~/Library/Containers -maxdepth 4 -path '*/Data/Documents/tool_export.json' 2>/dev/null
# Android over USB
adb pull /storage/emulated/0/Android/data/com.TechTreeGames.TheTower/files/tool_export.json .
```

**The server finds the file itself (SDK 1.2.0+).** Every save tool that takes `path` (`decode_save`,
`run_extractor`, `read_save_field`, `battle_history`, `save_series`, `next_unlocks`, `coin_bonus`,
`survival_rank`, `plan_spending`) may be called with no
`path`: the server then reads the file the `TOWER_TOOL_EXPORT` environment variable names, or on a Mac
the game's own container. Try `decode_save {}` first. Its answer carries the absolute `path` it read —
tell the player which file that is, and reuse that string as `savePath` for `calc_run` and
`plan_effective_path`, which have **no** auto-discovery. If nothing is found the
answer is an `error` with `searched` (the places it looked) and a `hint`; then use the commands above or
ask the player. From SDK 2.1.0 a `TOWER_TOOL_EXPORT` (the extension's Tool Export setting) that names no
file is an `error` too — the server no longer falls back to another export on the machine, so an answer
is never about a different account than the one configured. Tell the player to fix or clear the setting;
an explicit `path` reads that file regardless.

If several macOS matches appear, take the most recently modified and confirm with `decode_save`. On
iOS, suggest looking in Files → On My iPhone/iPad for a Tower folder, and otherwise AirDrop/Files the
file to a computer; say plainly that this route is not documented. A given path must be **absolute**
(`~` is expanded; a relative path is read from the server's working directory and will miss).

## 3. Tools and exact parameters

`*` = required. Every failure comes back as JSON with `error` (often `hint` / `didYouMean`), not an
exception. Read those fields before retrying.

**Arguments are checked strictly (SDK 1.6.0).** An argument a tool does not have is refused, with the
name it thinks you meant, instead of being ignored. The one that bites: the export is `path` on the save
tools and `savePath` on `calc_run`, `plan_effective_path` and `sdk_sandbox_run`. `savePath` sent to
`battle_history` is now an error (it used to read the default export silently). `null` counts as "not
given".

**Structured output (SDK 2.1.0).** To a client on MCP revision `2025-06-18` every successful answer also
arrives as `structuredContent` matching the tool's `outputSchema`; the text block is unchanged, and a
failed call is still `isError` plus text. Nothing in this file changes: the field names are the same
either way. Expect fields the schema does not name, and `null` where a number was NaN.

### Save tools (read-only on the file)

| Tool | Parameters | Returns / limits |
|---|---|---|
| `decode_save` | `path` | `{gzip, rootKeys, battleRuns, targets[]}`; one target per reader: `{extractor, found, fields[] or count, warnings}` (counts only, no values). This is the authoritative reader list. |
| `run_extractor` | `extractor*`, `path` | One reader's result as a preview: up to 40 top-level keys and **12,000 characters of values**. Fields that do not fit are listed in `outlined` as a shape (`kind`, `length`, first 12 `columns`) — they are **not missing**. `warnings` (max 20 shown). `result: null` = save has no data for that feature. |
| `read_save_field` | `extractor*`, `path`, `field` (dotted path, e.g. `researches`, `active.levels`, `slots.0.baseStatLevels`), `pick` (string[]: columns of a list / keys of an object), `where` (object, column → value, compared as text; lists only), `search` (text in any top-level column; lists only), `offset` (negative counts from the end), `limit` | Lists: default 20 rows, max 100, and a page is also cut at 12,000 characters (`sizeLimited`) — use `pick`. Objects: default 100 keys, max 500. `truncated` + `next` = pass `next` as `offset`. Omit `field` to read the result itself. Unknown arguments are refused. |
| `battle_history` | `path`, `kind` (`all` \| `farming` \| `tournament`), `detail` (boolean), `offset`, `limit` | Default 10 runs, max 50. See §5. With `detail: true` a page stops early when it gets large (`sizeLimited`, with the `offset` for the next page); use `limit` ≤ 3 with it. |
| `save_series` | `path`, `series`, `offset`, `limit` (default 40, max 100) | The save's history as `{x, y}` points (SDK 2.0.0). Omit `series` to list what this save holds (`id`, `title`, `points`, `unit`); nine ids on a developed account: `save:battle:coins-per-hour`, `:wave`, `:coins`, `:cells` (one point per run, `x` = run date in ms since the epoch), `save:tournament:wave`, `save:tournament:rank` (per tournament by date; one still running is left out, since rank 0 is not a placing), `save:tier:highest-wave`, `:highest-coins`, `:highest-cells` (`x` = tier). See §5. |
| `next_unlocks` | `path` | What the account can open next, beside the balance that pays for it. `balances {coins, stones, gems}`; `workshop.{attack,defense,utility}` `{unlocked, next: {opens[], coins}, affordable}`; `ultimateWeapon {owned, stones, affordable}`; `ultimateWeaponPlus {owned, stones, allWeaponsOwned, affordable}`; `labs {gemRushEfficiency, maxedLabs, running[{slot, lab, completedLevel, remainingSeconds, rushGems, affordable}]}`. `next: null` / `stones: null` = nothing left to unlock there. `affordable: null` = cannot tell, not "cannot pay". See §7. |
| `coin_bonus` | `path`, `tier` (number; default = the tier selected in the save), `overrides` (object merged one level deep over the answer's `input`), `scenarios` (SDK 3.0.0: `[{name*, tier, overrides, dissonanceWave {tier, wave}}]`) | The Battle tab's **Total Coin Bonus** row by row: `bonus {disableAds, starterPack, epicPack, activeCards, modules, difficultyTier, themes, relics, enhancement, dissonance, total}` — every row is a multiplier and `total` is their product — plus the `input` it was built from. With `overrides` the answer adds `whatIf {overrides, input, bonus, totalRatio}`: the new rows beside the old, and `totalRatio` = new total ÷ old total. An override key the `input` does not have is refused. With `scenarios` the answer adds `scenarios[{name, tier, total, ratioToNow, changedRows[{row, from, to}]}]`, each against the save as it is. See §7. |
| `plan_spending` | `path`, `snapshotsDir` (folder of stored readings; `~` is expanded), `timeZone` (IANA name such as `America/Denver`; UTC when omitted), `horizonDays` (default 3, max 14), `survival` (boolean, default true; false is fast and leaves workshop levels unranked), `workshopTargets` (`[{stat, toLevel}]`; default each survival stat to its next hundred), `dissonantWave`, `cellFloor`, `maxBoost`, `boostPrices` (`{"1.5": 15, "2": 100}`, cells per hour for one slot, as read on the Labs screen) | SDK 3.0.0. What the next **coins** should buy and when; up to a minute with the survival model. `{path, now, coins, cells, forecast, coinModel, labQueue[], coinQueue[], notRanked[], buyList, labSchedule, boostPolicy, dissonance, notes[], warnings[]}`. A part that could not be made is left out, not `null`. Field by field in §7 "Reading `plan_spending`". Never covers gems, stones, medals, purchases or in-run cash (from 3.1.0 `notRanked` says so and names `workshop.cashCostBetween`). |
| `survival_rank` | `candidates*` (`[{stat, toLevel}]`; `stat` is Health, Health Regen, Defense Percent, Defense Absolute, Recovery Amount, Max Recovery, Package Chance, Lifesteal, Death Defy, Enemy Attack Level Skip or Enemy Health Level Skip), `path`, `snapshotsDir`, `tier` (default: the tier of the latest farming run), `mode` (`afk` \| `active`), `seeds` (default 100, max 400), `fitRuns` (default 6, max 12), `fitSeeds` (default 8, max 24) | SDK 3.0.0. About half a minute. `{tier, mode, baseline {p10, median, p90}, ranked[{stat, fromLevel, toLevel, coins, medianWavesGained, wavesPerBillionCoins, deathWave {p10, median, p90}}], fit {leaveOneOutError, runsUsed, perRun[], skipped[{runDate, wave, reason}], calibration}, assumptions, notes[], warnings[]}`. `coins` is the Workshop price at the account's discount. See §7. |

`read_save_field`'s `extractor` also accepts other save functions that take the save root:
`listImportableBattleRuns` (the raw run list) and `computeCoinsPerHourFromSaveRoot` (one number) both work.

### Game data, formulas, knowledge (no account data)

| Tool | Parameters | Notes |
|---|---|---|
| `list_exports` | `entry*` (`data`, `save`, `node`, `mechanics`, `formatting`, `wiki`, `knowledge`, `builders`, `calculators`, `charts`, `sheets`, `bot`, `save-decoder`, `contributions`, `assets`), `filter`, `offset` | 300 names per page. Never invent an export name; look it up here. |
| `get_export` | `name*`, `limit` (default 40, max 100) | Preview, 12,000-character budget. |
| `find_rows` | `name*`, `where`, `search`, `fields` (string[]), `offset`, `limit` (default 20, max 100) | Rows of one table. Object-keyed exports gain a `_key` column. Note the column parameter is `fields` here and `pick` on `read_save_field`. |
| `describe_schema` | `table` (omit to list tables) | Declared shape of a data table. |
| `calc_list` | `filter`, `offset`, `limit` (default 60, max 100) | ~1,700 calculators; always filter, and page with `offset` when `matched` exceeds `shown`. Save-reading ones are `save.*`. |
| `calc_describe` | `id*` | Params with units, invariants, linked oracle traps. |
| `calc_run` | `id*`, `args` (object — calculator parameters go **inside** `args`), `savePath` | `savePath` decodes the export and passes it as the calculator's `root` / `parsedRoot` parameter. Unknown top-level keys are refused — a calculator parameter placed beside `args` instead of inside it is an error. A large result comes back as a preview, not whole. |
| `calc_chart` | `chart` | Which calculators produce a chart's numbers. |
| `calc_graph` | `concept`, `filter`, `offset`, `limit` | What feeds a number. Paged. |
| `chart_rows` | `chart`, `args` (string[]), `offset`, `limit` (default 40, max 100) | Published table rows as formatted text; omit `chart` to list the 72 charts. Handy ids: `vault:v29:harmony` / `:power` / `:enemy` (the two `vault:upgrades-and-cost:*` charts are pre-v29), `tournaments:rewards:<league>`, `ultimate-weapons:unlocks:stone-ladder`, `ultimate-weapons:stone-costs:<weapon>`, `bots:upgrades-and-costs:<bot>`, `guardians:upgrades-and-costs:<chip>`, `modules:costs:upgrade-costs-by-level`, `labs:gems:rush-gems-by-time-left`, `tiers:coins:coin-bonus-by-tier`, `currencies:cells:elite-cells-by-tier`. Before SDK 2.0.0 the Golden, Thunder and Amplify bot charts all returned Flame Bot's rows. |
| `chart_series` | `series`, `family` (`lab`, `workshop`, `card`, `ultimate-weapon`, `bot`, `guardian`, `module`, `enhancement`, `vault-v29`, `vault`, `unlock-ladder`), `entity`, `offset`, `limit` (default 40, max 100) | One cost or value curve as plain `{x, y}` numbers by id, e.g. `lab:damage:cost` (SDK 2.0.0). Omit `series` to list ids, narrowed by `family` / `entity`. `vault-v29` is the current vault; `vault` is the pre-v29 trees. For a price to quote, a `…Between` calculator is one call; this is for showing the player a whole curve. |
| `form_calc` | `id`, `input` (object) | The site's form calculators. Omit `id` to list; an `id` alone returns its fields and defaults. Ids differ from `calc_list` handles. The 15 ids: `lab.research`, `uw.stones` (one stat from `currentLevel` to `targetLevel`, per-level and total — use it instead of summing `uw.stoneCost`), `uw.inner-land-mines`, `assist.stones`, `module.cost`, `bot.upgrade` (medals), `guardian.upgrade` (bits), `workshop.upgrade` (enhancements only), `dissonance.boost` (the multiplier from per-tier bests), `uptime.ratio` (UW duration ÷ cooldown), `damage.reduction`, `thorns.damage`, `economy.coins-per-kill`, `enemy.wave`, `drops.enemy`. |
| `plan_effective_path` | `family*` (`damage` \| `economy` \| `health` \| `regen`), `variant*` (damage: `lab-time`, `lab-coins`, `farm-time`, `stone`, `coin`, `keys`; economy: `time`, `coin`, `stone`; health: `lab-time`, `lab-coins`, `stone`, `coin`; regen: `lab-time`, `lab-coins`), `steps` (default 10, max 200), `savePath` (**economy only**), `levels` (object merged over all-zero), `scenarios` (SDK 3.0.0: `[{name, levels}]`, each merged over the starting levels) | Returns `steps[{step,name,level,cost,roi}]` and `excluded[{sheetName,reason}]`; with `scenarios`, also `scenarios[{name, steps[], excluded}]` (`excluded` is a count there) to compare rankings. From a save it also passes the account's enhancement levels and lab speed (SDK 3.0.0), and a maxed candidate is excluded as "at its maximum level". See §7 on zero-start. |
| `patch_notes` | **one** of `query`, `introduced`, `version`, `from`+`to`, `recent` per call (given two, it answers one and says which; a `from` later than `to` is refused); plus `limit` (default 5, max 25), `full` (boolean; bodies are cut at 600 chars without it) | With no argument: archive range and latest versions. Use to check whether advice predates a patch. |
| `wiki_search` | `query*`, `limit` (default 10) | Real page titles. Network. |
| `wiki_page` | `title*`, `section`, `offset`, `refresh`, `sourceId` (`fandom` \| `gamevault`) | 12,000 characters per call; `next` → `offset`. Wiki text is CC-BY-SA. Network. |
| `define_term` | `term*`, `domain` | Glossary; `found: false` rather than a near miss. `ambiguous: true` → pass `domain`. |
| `oracle_expand` | `term*` | Acronym → closed set of expansions. Use before interpreting player shorthand. |
| `oracle_search` | `query*`, `limit` (default 10, max 50) | Find an entity by player-facing name. `oracle_traps`, `oracle_brief` and `oracle_footguns` answer `found: false` for a name they cannot place instead of taking the nearest entity, so search first when unsure of the id. |
| `oracle_get` | `id*` | One entity: meaning, units, relations, sources. |
| `oracle_traps` | `id*` (entity id or plain name) | How this mechanic has been got wrong before. |
| `oracle_brief` | `mechanic*` | Units, valid range, implementing exports, traps. |
| `oracle_footguns` | `mechanic` (optional filter) | Irreversible upgrades and known footguns. **Call before recommending any spend.** |
| `oracle_map` | `family`, `includeSources`, `detail` | A whole system. Without `family` it is very large. |
| `oracle_coverage` | `asOf` | What the oracle does and does not know. |
| `oracle_contradictions` | — | Sources that disagree. |
| `sdk_sandbox_run` | `mode` (`list` \| `export` \| `calc` \| `format` \| `decode`), `name`, `entry`, `id`, `input`, `value`, `savePath` | Scratchpad. `mode: "format"` with a number `value` writes game notation; with a string it parses it. Annotated as not read-only, so a client may prompt for it; rarely needed. |

### Tables and calculators worth knowing

Checked against the build-1301 export on 2026-11-25. Tables are read with `find_rows {name, where,
fields}`; calculators with `calc_run {id, args}`.

| Question | Where the answer is | Notes |
|---|---|---|
| What has the account's relic collection added, per stat? | `read_save_field {extractor: "readRelicsFromSaveRoot", field: "relics", where: {state: "unlocked"}, pick: ["index"], limit: 100}`, then `calc_run workshop.relicBenefitByStat {args: {relicIndices: [...]}}` | Returns fractions by the game's stat name (`LabSpeed: 0.035` is +3.5%, `CoinBonus`, `TowerDamage`, …). Filter on `state`, not `unlocked`: mailed relics pay nothing. `LabSpeed` is the relic input `form_calc lab.research` needs. |
| What is a relic, and where does it come from? | `RELIC_GAME_TABLE` (`index`, `stat`, `benefit`, `rarity`, `unlockType`, `unlockCost`, `releaseDate`) | Same index as the save rows. |
| What does an event award, and is the pass worth it? | `EVENT_RELIC_SETS` (`where: {event: "<name>"}` or `search`) | Each relic's stat, benefit, medal threshold, `needsEventPass`, later shop price (medals) and rotating price (gems). |
| Stones, gems and keys per league and rank | `TOURNAMENT_REWARD_ROWS` (70 rows), or `calc_run data.getTournamentRewardsForLeague {args: {league}}` | Exact rank bands; never interpolate. |
| Weekly mission track | `DAILY_MISSION_WEEKLY_REWARDS` | Gems, medals, stones, guild tokens per 5..35 missions. |
| Milestone rewards and unlocks | `MILESTONE_REWARD_ROWS` (`where: {tier}`) | Standard and premium tracks, by wave. |
| Tier coin bonus, tier battle conditions | `TIER_COIN_BONUS_ROWS`, `TIER_BATTLE_CONDITION_ROWS` (`where: {tier}`) | Conditions start at Tier 14. |
| Vault v29 key prices | `calc_run vault.v29.upgradeKeysCost {args: {upgrade, level}}`, `vault.v29.upgradeKeysBetween {args: {upgrade, fromLevel, toLevel}}`, `vault.v29.categoryUnlockKeys {args: {tree, category}}`, `vault.v29.treeKeysRemaining {args: {tree, levels}}` (SDK 2.1.0) | `upgrade` is the row key the save uses, `v29:<tree>:<Category>:<Name>` (`v29:harmony:Cards:Additional Card Slot` 0→2 = 15 keys; the Cards category unlock = 5). `tree` is `harmony`, `power` or `enemy`. Pass `readVaultFromSaveRoot.v29.levels` as `levels` unchanged for what is left of a tree; with no `levels` it is the whole tree (Power: 11,505 keys). The first upgrade in a locked category also costs its unlock. `null` = a misspelt key or a level the row does not have, not "free". **`vault.nodeKeysCost`, `vault.nodeKeysBetween` and `vault.treeKeysRemaining` (no `v29`) price the trees as they were before v29 — never use them for a current account.** |
| Vault v29 values and requirements | `VAULT_V29_POWER`, `VAULT_V29_HARMONY`, `VAULT_V29_ENEMY`, or `chart_rows vault:v29:<tree>` | Two rows each: `categories` (unlock costs) and the upgrades (per-level keys and values). The oracle has no vault numbers. |
| A run of levels, one call | `calc_run` `uw.stoneCostBetween {weapon, stat, fromLevel, toLevel}`, `uw.unlockStonesBetween {ownedFrom, ownedTo}`, `uw.plusUnlockStonesBetween`, `lab.coinCostBetween` / `lab.durationDaysBetween {labKey, fromLevel, toLevel, modifiers}`, `bot.statCostBetween {botLabel, statName, fromLevel, toLevel}` (medals), `guardian.statCostBetween {guardianKey, statName, fromLevel, toLevel}` and `guardian.allStatCost {guardianKey, fromLevels}` (bits), `module.coinCostBetween` / `module.shardCostBetween {fromLevel, toLevel, discountPercent}`, `assist.stoneCostBetween {fromLevel, toLevel}`, `workshop.coinCostBetween`, `workshop.enhancementCoinCostBetween {stat, fromLevel, toLevel, discounts}` (SDK 2.0.0) | `fromLevel` is the level owned now. Each returns `null`, never a partial total, for a level its table does not price, an unknown name or `toLevel` below `fromLevel` — check the name before concluding a level does not exist. Lab `modifiers` carry `coinDiscountLabLevel` and `labSpeedLabLevel` (the other keys are in `calc_describe`); the days are one slot with no relic or boost, and a Labs Speed run is summed at its own rising level. `uw.stoneCostBetween` leaves out the unlock. |
| Bot costs and stat ladders | `BOT_UPGRADES_DATA` (`where: {name: "Golden Bot"}`), or `form_calc bot.upgrade` | Medal cost per level, stat base/step/max, lab caps, Bot+ ladder. |
| Module merges and reroll costs | `MODULE_MERGE_RECIPES`; `calc_run data.getModuleRerollCost {args: {lockedSubstats}}` | Reroll shards per roll by number of locked substats. |
| Spotlight coverage | `calc_run spotlight.coverage {args: {quantity, angleDegrees}}` | Share of the field lit, capped at 1. Once it saturates, more Angle is worth nothing. |
| Workshop coin price, as the buy button shows it | `calc_run workshop.upgradePrice {args: {stat, fromLevel, count, sectionDiscountPercent}}` → `{toLevel, levels, coins}` (SDK 2.0.0) | `fromLevel` = the level owned, `count` = 1, 5, 10 or 100, `sectionDiscountPercent` = that tab's Workshop Discount lab as a percentage (lab level 30 is 15). Each level is discounted and rounded on its own, then summed, as the x5 / x10 / x100 buttons do; `levels` below `count` means the upgrade ran out. Damage 100→110 at 15% = 835,703. For a long run at list price: `workshop.coinCostBetween {stat, fromLevel, toLevel}`. All 48 upgrades are priced. |
| What a workshop level gives | `calc_run workshop.statValue {args: {stat, level}}` → `{value, unit, coinCost, cashCost}` (SDK 2.0.0; `mechanics.workshopStatValue` before) | The game's value with its `unit` named (`amount`, `multiplier`, `fraction`, … — a `fraction` of 0.0055 is 0.55%), workshop alone — no lab, relic, card or module. `coinCost` is the list price of the **next** level (level → level + 1). `cashCost` is what the next level costs in cash inside a run when the stat stands at `level` there; for more than one level use `workshop.cashCostBetween`. `workshop.screenValue` builds the number the Workshop row shows from labs, relics, cards and modules, but wants a full input object: read `calc_describe` first. Knockback Force, Rend Armor and the Wall have no screen formula; read those in game. |
| A range of workshop levels at this account's discount, with the stat before and after | `calc_run workshop.accountCoinCostBetween {savePath, args: {stat, fromLevel, toLevel}}` (SDK 3.0.0) | → `{coins, listCoins, discountPct, valueBefore, valueAfter}`. Reads the tab's discount lab from the save and rounds each level as the game does (Health 1300→1400 at 15% = 3,661,257,391 against 4.31B list). Unlock prices are not priced here. |
| In-run upgrades, in cash | `calc_run workshop.cashCostBetween {args: {stat, fromLevel, toLevel}}` → cash (SDK 3.1.0) | What a run of in-run levels costs. `stat` is the Workshop table's name ("Health", "Damage"). `fromLevel` is the level the stat stands at **in the run**, not levels bought: a run starts each stat at its Workshop level (`readWorkshopFromSaveRoot`), and the run in progress has it as `inRun` in `readInRunLevelsFromSaveRoot`. Health 1300→1400 = 108,449,662 cash. The game's base cash price: the Workshop discount labs are coin discounts and are not applied, and whether anything lowers a cash price is not verified. Free upgrades land levels for nothing, so it is an upper bound on cash spent. `null` = an unknown stat or a level past the table, not "free". Cash is not coins: never add or compare the two. |
| The account's lab speed and coin discount, ready for a calculator | `run_extractor readLabCostModifiersFromSaveRoot` → `{coinDiscountLabLevel, labSpeedLabLevel, labSpeedRelicPct}` (SDK 3.0.0) | Pass as `modifiers` to `lab.coinCostBetween` / `lab.durationDaysBetween`; saves reading the relics for `LabSpeed`. `labSpeedRelicPct` is a fraction despite the name (0.035 = +3.5%). |
| The run in progress | `run_extractor readCurrentRunProgressFromSaveRoot` → `{tier, wave, startedAt, realSeconds, gameSeconds, coinsSoFar, cellsSoFar}`; `readInRunLevelsFromSaveRoot` → `rows[{category, stat, workshop, inRun, gained}]`, `categories[{category, gained, fromFree, bought, freeCount}]`, `mode` (`afk` \| `active`) (SDK 3.0.0; `calc_run currentRun.progress` / `currentRun.inRunLevels` with `savePath` are the same) | `startedAt` is the latest the run can have begun: paused time is not counted. `bought` above zero on a tab means cash was spent there, so the run is `active` even if the player calls it AFK; judge per tab. |
| One step of the plan on its own | `calc_run` with `savePath`: `planning.forecastIncome`, `planning.affordableBy {args: {list: [{name, coins}]}}` (dates for your own shopping list, bought in order), `planning.rankSpends`, `planning.scheduleLabs`, `planning.cellBudget`, `planning.dissonancePayback`, `survival.simulateRun` (predicted death wave) (SDK 3.0.0) | `plan_spending` runs them in the right order and is the normal route. `calc_run` cannot pass a snapshot folder, so these see only the current export; read `calc_describe` for the `options` fields. `history.snapshot` / `.diff` / `.timeline` / `.stateAt` take whole snapshots as arguments and are reached through `snapshotsDir`, not `calc_run`. |

Cautions:
- Calculators marked `tier: "generated"` in `calc_list` (all 273 `save.*` handles and most `data.*` /
  `mechanics.*` ones) have a signature but no written purpose or checked invariants. Read
  `calc_describe` first; skip any that wants an internal config object.
- `mechanics.coinFarmDays` divides by coins/hour × **23 hours a day** (a planning-sheet default), not by
  the account's real hours in runs. Do not use it for "how long to save for X": use `plan_spending`'s
  `buyList` dates or `planning.affordableBy`, or divide the price by `forecast.coinsPerDay.median`.
- `calc_describe` on the health, economy and coin-bonus models lists which inputs each includes and
  leaves out (SDK 3.0.0). Read it before quoting one of those models as the whole picture.

### Tools the coach never calls

`record_mechanic_note`, `record_work_status` and `begin_mechanic_task` **write files** (they append to a
mechanics map and ledger under the server's directory). They exist for people changing the SDK.
`compliance_contract` is the same workflow's instructions. `sdk_graph_*`, `trust_*`, `sdk_debug_*`,
`mcp_contract` and similar appear only inside the SDK's development repository and are not for coaching.

## 4. Save readers

46 functions match `read*FromSaveRoot` in SDK 3.0.0 and `decode_save` runs all of them. Four are series
views added in 2.0.0 — `readSaveSeriesFromSaveRoot`, `readBattleHistorySeriesFromSaveRoot`,
`readTournamentSeriesFromSaveRoot`, `readTierRecordSeriesFromSaveRoot` — which hold no data the others
do not; skip them in a full read and use `save_series` when a series is wanted. Of the eight added in
3.0.0, skip four more: `readWorkshopCoinCostBetweenFromSaveRoot` and
`readEnhancementCoinCostBetweenFromSaveRoot` need arguments (`found: false` in `decode_save`; use
`workshop.accountCoinCostBetween`), `readLabLevelsBySlugFromSaveRoot` repeats lab levels keyed by slug,
and `readSurvivalAccountFromSaveRoot` is the survival model's own input (workshop, cards, labs and runs
again). The other four are in the tables below. (`decode_save`
lists whatever the installed build has — trust that list over this table.) Each returns an object or `null` when the save has no data for the
feature; most carry `warnings: string[]` — a non-empty one usually means the save shape changed.

### Progression

| Reader | Contains | Fields a coach uses, and gotchas |
|---|---|---|
| `readWorkshopFromSaveRoot` | Workshop levels, enhancements, presets | `active.levels` (object, display name → level, e.g. `"Damage"`, `"Coins / Kill Bonus"`), `active.enhancementLevels` (`WSP_*` keys), `presets[]` (same two objects per preset), `meta.currentPreset`, `meta.presetNames`, `meta.totalCoinsSpentWorkshop`, `meta.totalCoinsSpentEnhancements`. `active` is the preset in use. |
| `readWorkshopUnlocksFromSaveRoot` | Rows unlocked per category | `upgradeTiersUnlocked`, `upgradeTiersEverUnlocked`, `enhancementTiersUnlocked` (`{attack, defense, utility}`), `freeUpgradeLocked[]`, `nextUnlock.{attack,defense,utility}` `{order, stats[], coins, source}` or `null` when the tab is fully unlocked (what `next_unlocks` reports). |
| `readLabsFromSaveRoot` | Research levels, queue, completion log | `researches[]` `{index, level, displayName, slug, category, percentComplete, completeDate, remainingSeconds}`; `activeQueue[]` `{slotIndex, active, speedUp, speedUpRemainingSeconds, research, remainingSecondsWithSpeedUp, rushGems}`; `gemRushEfficiency`; `completions[]` `{researchIndex, level, completedAt}` oldest first; `labsUnlocked` (slots **bought with gems**: the first slot is free, so slots owned = `labsUnlocked + 1`), `hasActiveQueueData` (false = the export has no queue, which says nothing about idle slots), `researchedCount`, `maxedCount`, `totalCoinsSpentOnResearch`. Seconds throughout. See §7 for timers. Rows with `displayName: null` are hidden/unnamed (`hiddenUnnamedCount`). |
| `readFavoriteLabSlugsFromSaveRoot` | Starred labs | `string[]`; empty when none starred. |
| `readUltimateWeaponsFromSaveRoot` | UW unlocks and levels | `ownedCount`, `nextUnlockStoneCost`, `allWeaponsOwned`, `plusOwnedCount`, `nextPlusUnlockStoneCost`; `slots[]` `{slotIndex, unlocked, active, plusLevel, plusUnlocked, plusOn, baseStatLevels[3]}`. **No names**: `slotIndex` 0–8 = Chain Lightning, Smart Missiles, Death Wave, Chrono Field, Inner Land Mines, Golden Tower, Poison Swamp, Black Hole, Spotlight. `baseStatLevels[3]` follows the first three stats of each weapon in the order listed in `meta-ultimate-weapons.md` (e.g. Golden Tower: Multiplier, Duration, Cooldown) — sanity-check one value against what the player sees. Trust `baseStatLevels` only when `baseStatChunkingPlausible` is true. |
| `readCardsFromSaveRoot` | Card levels, copies, slots | `cards[]` `{slug, name, level, count, unlocked, active, masteryUnlocked}`, `equippedCards[]`, `slotsUnlocked`, `currentPreset`, `presetNames`, `presetSlots[]` (flat, per preset × slot). `count` = spare copies toward the next level, not a lifetime total. |
| `readCardDrawOddsFromSaveRoot` | What the next card purchase can give | `pool[]` `{card, name, rarity, level, inPool, drawable, gatedBy}` and `odds` `{rarities, cards[{card, chance}]}`, as the in-game Card Chances panel shows them. `drawable: false` with `gatedBy: null` = maxed, so it has left the pool; `inPool: false` with `gatedBy {tier, wave}` = that milestone is not claimed yet. Use it before recommending gems on cards. |
| `readModulesFromSaveRoot` | Equipped and owned modules, shard balances | `equipped[]` `{slotKey ("primary:Cannon" … "assist:Core"), role, category, mappedName, mappedInitials, level, rarityLabel, rarityEnum, effects[], effectLocked[], guid, shardsSpent, coinsSpent, rerollCounter}`; `inventory[]` same minus slot fields; `shards` `{cannon, armor, generator, core, rerollCurrency, tickets}`. `equipped[].level` is the **slot** level (§7). `coinsSpent` is approximate above ~9e15. `rerollCounter` = rerolls already spent on that module (weigh before advising more reroll shards on it). Assist slots add `assistUniqueEffectUpgradeLevel` (0–3 paid rungs), `assistSlotUniqueRarity` and `effectiveUniqueRarity` (the slot's rung capped by the module's own rarity) — what the unique effect actually runs at. |
| `readModuleEconomyFromSaveRoot` | Slot levels, pity, assist slots, module presets, reroll settings | `slotLevels[4]` (Cannon, Armor, Generator, Core), `slotCoinsSpent`, `slotShardsSpent`, `pity` / `rarePity` (pulls since last epic / rare), `assistModulesAvailable` (assist modules unlocked at all), `assistSlots[]` `{category, unlocked, level, mainEffectEfficiencyLevel, substatEfficiencyLevel, uniqueEffectEfficiencyLevel}`, `presets[]` (module GUIDs per slot) with `currentPreset`, `epicObtained`, `merges`, `gemsSpent`, `lifetimeShards`. `substatBans` / `autoRerollSubstats` (per category: substat ids banned from rolls / kept by auto-reroll) name with `MODULE_SUBSTATS_CLUSTER` on `clusterValue` — an inferred mapping (it agrees by category on a real export but the SDK does not state it), so say so if you rely on it. |
| `readBotsFromSaveRoot` | Bots, levels, presets | `bots[]` `{name, label, unlocked, active, statLevels[4], plusUnlocked, plusLevel}` for the active preset; `presets[]`; `totalStonesSpent`, `totalMedalsSpent`; `synchronicity`. `statLevels` is positional and the stat order differs per bot (Flame: Damage Reduction, Cooldown, Damage, Range; Thunder: Duration, Cooldown, Linger, Range; Golden/Amplify: Duration, Cooldown, Bonus, Range). |
| `readBotSynchronicityFromSaveRoot` | Bot sync | `inSave`, `unlocked`, `level`, `slotCount`, `slots[]`, `bots[]`, `occupiedSlots` (fewer than `slotCount` = an empty sync slot, a free fix), `lockedBots` (bots sitting in a slot without being unlocked, a pre-v29.1 bug: point it out). |
| `readGuardiansFromSaveRoot` | Guardian, chips, presets | `guardianUnlocked`, `inGuild`, `activeInBattle`, `chips[]` `{label, unlocked, statLevels[3], equippedSlot}`, `equippedChips[]`, `chipSlotCount`, `slotsUnlocked`, `presets[]` with `currentPreset`, `totalCoins`, `totalCatches`. `slotsUnlocked` counts **bought** slots; owned slots = `chipSlotCount`. Chips do nothing outside a guild since v29.1 — check `activeInBattle`. |
| `readVaultFromSaveRoot` | Vault | `keys`, `totalKeysEarned`, `v29.levels` (object, `v29:<tree>:<category>:<name>` → level), `v29.unlockedGroupCount`, `v29.upgradeCount`, `v29.unknownVaultIds` / `v29.unknownGroups` (non-empty = the SDK is older than the game). Costs and values: `VAULT_V29_POWER` / `_HARMONY` / `_ENEMY` (§3). The legacy `powerNodes[]` / `harmonyNodes[]` and their counts are empty since the v29 rework; read `v29`. |
| `readRelicsFromSaveRoot` | Relics | `unlockedCount`, `mailedCount`, `relics[]` `{index, name, label, description, unlocked, state, onProfile, rarity, benefit, stat, unlockType, unlockCost, unlockDescription, event, releaseDate}` (one row per catalog relic, 350), `profileRelicIndices`. **`unlocked` is true for a mailed relic too, and `unlockedCount` counts mailed ones; only `state: "unlocked"` pays its bonus.** `mailedCount` > 0 = relics waiting in the mail: tell the player to claim them. `benefit` is a fraction (0.02 = 2%; seconds for WallRebuild, metres for BotRange) on the game's `stat` name. Page with `where: {state: "unlocked"}`; per-stat totals with the recipe in §3. |
| `readTierRecordsFromSaveRoot` | Per-tier bests | `tiers[]` `{tier, highestWave, highestWaveThisCycle, roundsStarted, highestCoinsEarned, highestCellsEarned}`, `currentTier`. `currentTier` is the tier selected now, often **not** the highest reached. |
| `readMilestonesFromSaveRoot` | Milestone claims | `tiers[]` `{tier, claimedSlots[], premiumClaimedSlots[], premiumUnlocked}`, `slotsPerTier`. |
| `readPerkChoicesFromSaveRoot` | Perk bans and auto-pick | `bannedIndices`, `firstPerkIndex`, `firstTradeOffPerkIndex`, `autoPickPerk`, `autoPickOrder`. Indices only — name them with `find_rows {name: "PERK_IMPORT_CATALOG", where: {index: N}}`, never from memory. |
| `readDissonanceCycleWavesFromSaveRoot` | Per-tier waves the Dissonance cycle is measured against — **not** the Dissonant-run bests. For best wave per Dissonance type use `calc_run save.readDissonanceBoostWavesByType` with `savePath`. | `cycleWaves[]` indexed by tier number (slot 0 empty), `layout`. |

### Economy & history

| Reader | Contains | Fields a coach uses, and gotchas |
|---|---|---|
| `readCurrenciesFromSaveRoot` | Balances and this cycle's flows | `balances` `{coins, gems, stones, medals, cells, keys, tokens, bits, rerollShards, cannonShards, armorShards, generatorShards, coreShards, moduleTickets}` (plain numbers; null if not recorded); `earnedThisCycle` / `spentThisCycle` keyed by the game's names (`coin`, `gem`, `module_reroll`, …). |
| `readLifetimeFromSaveRoot` | The in-game Lifetime panel | `values` — **strings in game notation** (`coinsEarned`, `cellsEarned`, `stonesEarned`, `wavesCompleted`, `labCoinsSpent`, `recentCoinsPerHour`, …), plus `date` and `gameStarted`. |
| `readLifetimeBreakdownFromSaveRoot` | Lifetime totals by source (numbers) | `coinsBySource`, `damageBySource`, `killsBySource`, `killsByEnemyType`, `currencies.<name>.{earned, spent, bought}`, `other.playTimeSeconds`. Good for "where do my coins come from" over the whole account. |
| `readTournamentsFromSaveRoot` | League and results | `league`, `highestLeague`, `joined`, `playing`, `records[]` `{number, date, league, wave, rank}` oldest first. `rank` is 0 while a tournament is still running. |
| `readEventsFromSaveRoot` | Event medals | `medalsCurrentEvent`, `lastEventNumber`, `records[]` `{number, date, name, medals, medalsSpent, relicsUnlocked[]}`. `date` is a last-update stamp, not the event start. |
| `readEventShopFromSaveRoot` | The running event: what it awards and what its shop sells | `event`, `saveName`, `eventNumber`, `medalsCurrentEvent`, `themes[]` `{kind, name, price, currency, coinBonus}` (`kind` is `tower` or `background`), `songs[]` `{name, price, currency, coinBonus}`, `earnTrack[]` `{index, label, rarity, medals, needsEventPass, owned}`, `relics[]` `{index, label, rarity, price, currency, fromEvent, owned}`, `rotatingRelicPrices[]` (gems, by rarity). **Two separate relic lists that never overlap.** `earnTrack` is the event's own relics, given free when `medalsCurrentEvent` earned in the event reaches `medals`; `needsEventPass: true` rows also need the paid event pass. `relics` is older relics the shop **sells** for `price` medals; `fromEvent` names the past event they came from. Never quote an `earnTrack` threshold as a price or the reverse. The save does not say which relics are on the rotating shelf. (Shape since SDK 1.7.1.) |
| `readTotalCoinBonusFromSaveRoot` | The Total Coin Bonus at the selected tier | `input`, `bonus` — the same rows `coin_bonus` returns. Use the tool: it adds `tier` and what-ifs. |
| `readPurchasesFromSaveRoot` | Permanent packs | `hasStarterPack`, `hasEpicPack`, `hasDisableAds`. Ownership flags only; no multiplier is inferred. |
| `readCurrentRunFromSaveRoot` | Run in progress | `currentTier`, `currentWave`, `roundActive`, in-run `upgradeLevel[]` / `upgradeDefenseLevel[]` / `upgradeUtilityLevel[]` (unnamed; `readInRunLevelsFromSaveRoot` names them), and from SDK 3.0.0 `realSeconds`, `gameSeconds`, `coinsSoFar`, `cellsSoFar`, `freeUpgrades`. These are in-run levels, not Workshop levels. |
| `readCurrentRunProgressFromSaveRoot` | How long the run in progress has gone and what it has earned (SDK 3.0.0) | `tier`, `wave`, `startedAt` (export time less the real seconds played: the latest it can have begun), `realSeconds`, `gameSeconds`, `coinsSoFar`, `cellsSoFar`. A run in progress is not in the run list yet; this is how to count it. |
| `readInRunLevelsFromSaveRoot` | The run in progress, one row per stat (SDK 3.0.0) | `rows[]` `{category, stat, workshop, inRun, gained}`; `categories[]` `{category, gained, fromFree, bought, freeCount}`; `mode` (`afk` \| `active`). `bought` is levels paid for with cash in the run. A tab with `bought` > 0 was played actively. |
| `readLifetimeFreeUpgradesFromSaveRoot` | Free upgrades landed over the account's life, per tab (SDK 3.0.0) | `attack`, `defense`, `utility`. |
| `readLabCostModifiersFromSaveRoot` | The inputs every lab price and duration needs (SDK 3.0.0) | `coinDiscountLabLevel`, `labSpeedLabLevel`, `labSpeedRelicPct`. |
| `readEffectivePathsSettingsFromSaveRoot` | Reach | `highestTier` (last tier with a wave recorded), `highestWave`, `wavesByTier` (object tier → wave), `gameSpeed` (may be null). |

### Settings & metadata

| Reader | Contains | Fields a coach uses |
|---|---|---|
| `readExportInfoFromSaveRoot` | The export about itself | `exportedAt` (ISO), `versionNumber` (game **build** number, not "29.2"), `dataVersion`, `exportVersion`, `checked`, `unknownKeys[]`, `warnings[]`. Read this first (§7). |
| `readGlobalPresetsFromSaveRoot` | Global Presets | `presets[]` `{name, workshop, cards, bots, modules, guardians}` (preset index per system), `currentPreset`, `tierPreset`, `tournamentPreset`, `dissonantPreset`. Tells you which loadout is used for farming / tournament / dissonant runs. |
| `readRuntimeControlsFromSaveRoot` | In-run toggles | `targetPriority`, `targetPriorityList`, `lifeSavingOrder` (ids: 0 Death Defy, 1 Energy Shield, 2 Second Wind, 3 Demon Mode, 4 Nuke), range/orb selections (units not established), `energyShieldRestrictionToggle`. |
| `readProfileFromSaveRoot` | Profile | `userName`, `avatarId`, `inGuild`, `lastGuildSeason`. **Do not read this for coaching**: `userName` is personal data (see Privacy in §7). `inGuild` is also on `readGuardiansFromSaveRoot`. |
| `readThemesFromSaveRoot` | Cosmetics | `unlocked[]`, `selected`, `skinsBought`. Rarely needed. |
| `readCollectedThemeNamesFromSaveRoot` | Owned theme names | `string[]`. Rarely needed. |

## 5. Battle history

`battle_history` returns `{runs, coinsPerHour, coinsPerHourNote, average, offset, returned, items[]}`.

- **Rolling window.** The export carries only the game's Battle History list: the last **30** runs in
  v29.2 exports (farming and tournament together). Older runs are gone, which is why snapshots matter.
- **Order:** oldest first. `battle_history` does not take a negative offset; the newest runs are the last
  page (or use `read_save_field` with `offset: -10`).
- **Compact row** (default): `tier`, `wave`, `type` (`Farming` / `Tournament`), `battleDate` (ISO UTC),
  `duration` (text), `realTimeSeconds`, `coins` (text, game notation), `coinsEarned` (number), `cells`
  (text), `killedBy` (name). There is no numeric cells in the compact row.
- **`coinsPerHour` is a peak**: the mean of the 3 best runs in the whole history, as the game's own panel
  computes it. Do not present it as the sustained rate.
- **`average`**: text fields averaged across the runs the SDK could build reports for.

- **Trend at a glance** (SDK 2.0.0): `save_series {series: "save:battle:coins-per-hour"}` returns every
  run's coins per hour by date (30 points, one call; a run with no coins or no duration is left out and
  reported). It mixes farming and tournament runs and names no tier, so use it to see the trend and to
  spot outliers; the sustained rate still comes from the median over farming runs below.
  `save:tournament:rank` and `save:tournament:wave` cover every tournament the save remembers (47 on one
  real account, far more than the 30 runs), which is the quickest read of league progress.

**Raw run record** (`detail: true`, or `read_save_field` with `extractor: "listImportableBattleRuns"`):
148 columns: 146 numbers plus `battleDate` (string) and `isTournament` (boolean). Groups:

| Group | Fields |
|---|---|
| Identity | `tier`, `wave`, `battleDate`, `gameTime`, `realTime`, `isTournament`, `killedBy`, `dissonanceType`, `selectedTower` |
| Income | `coinsEarned`, `cashEarned`, `interestEarned`, `cellsEarned`, `rerollShardsEarned`, `gemsThisRound`, `adGemsThisRound`, `gemBlocksTapped` |
| Coins by source | `coinsFromGoldenTower`, `coinsFromGoldenTowerPlus`, `coinsFromBlackHole`, `coinsFromSpotlight`, `coinsFromDeathWave`, `coinsFromOrbs`, `coinsFromCoinUpgrade`, `coinsFromCoinBonuses`, `coinsFromCritCoin`, `coinsEarnedWaveSkip`, `coinsEarnedCPW`, `goldenBotCoinsEarned`, `guardianCoinsStolen`, `guardianCoinsFetched` |
| Damage by source | `damageDealt`, `projectilesDamage`, `thornDamage`, `orbDamage`, `landMineDamage`, `innerLandMineDamage`, `chainLightningDamage`, `smartMissileDamage`, `deathWaveDamage`, `deathRayDamage`, `swampDamage`, `blackHoleDamage`, `rendArmorDamage`, `electronsDamage`, `flameBotDamage`, `guardianDamage` |
| Kills by source | `destroyedBy*` (Orbs, Thorns, DeathRay, LandMine, Projectiles, ChainLightning, SmartMissiles, DeathWave, InnerLandMines, PoisonSwamp, BlackHole, FlameBot, DeathPenalty, Other); `destroyedIn*` (Spotlight, GoldenTower, AmplifyBot, GoldenBot, Blackhole, Orbs) |
| Enemies by type | `totalEnemies`, `totalBasic`, `totalFast`, `totalTank`, `totalRanged`, `totalBoss`, `totalProtector`, `totalElites`, `totalVampires`, `totalRays`, `totalScatters`, `totalSaboteurs`, `totalCommanders`, `totalOvercharges` |
| Survival | `damageTaken`, `damageTakenWall`, `deathDefy`, `lifesteal`, `towerHealthRegen`, `wallHealthRegen`, `recoveryPackages`, `defensePercentBlocked`, `defenseAbsoluteBlocked`, `chronoFieldBlocked`, `energyShieldHitsAbsorbed`, `nukesUsed`, `secondWindsUsed`, `demonModesUsed` |
| Utility | `wavesSkipped`, `largestWaveSkip`, `freeAttackUpgrades`, `freeDefenseUpgrades`, `freeUtilityUpgrades`, `attackLevelSkips`, `healthLevelSkips`, `highestCPM`, `largestGoldenCombo` |
| Guardian fetch | `guardianCatches`, `guardianGems`, `guardianMedals`, `guardianRerollShards`, `guardian*Shards`, `guardianCommonModules`, `guardianRareModules` |
| Other (about 22 more) | `enemiesHitBy*ThisRound` (14, one per damage source), `*Blocked` (chain thunder, flame bot, primordial collapse, magic orb), Berserk damage, `thunderBotStuns`, `guardianSummoned`, `cashFromGoldenTower`, `orbHits`, `largestILMCharge`, `mostCoinsFromWaveSkip` — check `detail: true` for exact names before citing one |

**`killedBy` is an index** in the raw record (the compact row already names it). Save order, from the
SDK's `SAVE_FILE_KILLED_BY_ENEMY_NAMES` / `getKilledByFromSave`:
0 Basic, 1 Fast, 2 Tank, 3 Boss, 4 Ranged, 5 Protector, 6 Vampire, 7 and 8 Scatter, 9 Ray, 10 Saboteur,
11 Commander, 12 Overcharge; −1, 99 or 255 = Apathy (no enemy killer). This is **not** the
in-game UI order (Boss is 3, Ranged 4).

**`dissonanceType`**: 0 = normal run; 3 = Utility (confirmed against a real export). 1 Attack, 2 Defense,
4 Ultimate Weapon follow the save's own ordering but are unconfirmed — say so if you rely on them.

**Rates.** `realTime` is wall-clock seconds; `gameTime` is in-game seconds (larger, by roughly the game
speed). The game's "per hour" figures use real time:

```
coinsPerHour = coinsEarned / (realTime / 3600)
cellsPerHour = cellsEarned / (realTime / 3600)
```

For sustained farming, use the **median** over the player's farming runs on their farming tier
(`isTournament` false, `dissonanceType` 0), not the peak and not a mean that tournament or aborted runs
drag around. Compare game-time rates only when asking "what would a different game speed do".

## 6. Read-everything call sequence

The export is read **through the MCP** — that is the supported path, it works without a shell, and its
answers carry the SDK's warnings and decoding. The snapshot script (`scripts/snapshot.mjs`) is for keeping
history between sessions; once it has run, its JSON holds the same reader output and is a convenient place
to re-look-up a detail you already read, but it does not replace the read below.

**Call sequence (~45 calls; batch the independent ones in parallel):**

1. `decode_save {}` (or with `path`) — the file it read, reader list, which are `found`, warning counts, run count.
2. `run_extractor` for `readExportInfoFromSaveRoot` — check `exportedAt`, `checked`, `warnings`.
3. `run_extractor` once per remaining reader with `found: true`, in parallel. Skip
   `readProfileFromSaveRoot` (personal data) and the four `read…SeriesFromSaveRoot` readers (the same
   runs, tournaments and tier records again as points; §4). Themes, collected theme names and runtime controls can be
   skipped unless asked. Small results arrive whole.
   Also skip the four 3.0.0 readers §4 names as repeats or needing arguments.
   In the same batch: `next_unlocks {}` and `coin_bonus {}`.
4. For every name in an answer's `outlined` (or a `truncated` list), page with `read_save_field`.
   On a developed account expect:
   - labs `researches` — `pick: ["displayName","level","category","remainingSeconds"]`, `limit: 100`,
     follow `next` (a few hundred rows);
   - labs `completions` — only the tail: `offset: -30`;
   - modules `inventory` — `pick: ["mappedName","category","rarityLabel","level","favorite"]`, `limit: 100`;
   - relics `relics` — `where: {"state": "unlocked"}`, `pick: ["index","name","stat","benefit"]`, `limit: 100`;
     pass the indices to `workshop.relicBenefitByStat` for per-stat totals (§3), and note `mailedCount`;
   - cards `presetSlots` — only if comparing presets.
5. `battle_history {path, limit: 50}` — every run, compact, plus peak `coinsPerHour`. Optionally
   `save_series {series: "save:tournament:rank"}` for placings over time.
6. `read_save_field {extractor: "listImportableBattleRuns", path, limit: 30, pick: [...]}` for the numbers
   the compact row lacks. About ten columns of 30 runs fit one page; make one call for
   `battleDate, tier, wave, realTime, gameTime, coinsEarned, cellsEarned, rerollShardsEarned, killedBy,
   isTournament, dissonanceType` and a second for the coins-by-source columns.
7. Run the snapshot script (SKILL.md Step 3), then `plan_spending {path, snapshotsDir, timeZone}` with
   the player's snapshot folder. It takes up to a minute; start it while reading the rest.
8. Before advising: `oracle_footguns` (optionally with `mechanic`), then as needed
   `survival_rank {candidates, snapshotsDir}`, `coin_bonus {tier}` / `{overrides}` / `{scenarios}` for
   coin what-ifs, `plan_effective_path {family: "economy", variant, savePath}`, `calc_run`, `form_calc`,
   `patch_notes`.

Never conclude "the player has none" from a preview: check `outlined`, `truncated`, `next` and `matched`.

## 7. Quirks and traps

- **`null` is not zero.** A reader returning `null`, or a field that is `null`, means the save does not
  record it — not that the player has none.
- **Newer game than the SDK.** `readExportInfoFromSaveRoot.checked: false`, or anything in its `warnings`
  / `unknownKeys`, means the export is newer than the SDK was verified against (3.0.0: build 1301 =
  v29.2.3, data version 35). Renamed fields then read as missing; tell the player and update the SDK.
  Rule out a stale build first (§1): an up-to-date checkout that was not rebuilt warns the same way.
- **Module levels live on the slot since v29.** `readModulesFromSaveRoot.equipped[].level` is already the
  slot level; `readModuleEconomyFromSaveRoot.slotLevels` is the same per primary slot. `inventory[].level`
  may be a retired placeholder — never use it to rank modules. Levelling raises the main effect only,
  merging raises the rarity **cap**, and swapping modules loses no level. Pre-v29 "which module keeps its
  level" advice is obsolete.
- **Module rarity has three spellings.** `rarityLabel` is display form (`Rare +`, `Ancestral 5`);
  `rarityEnum` is numeric (0 None, 1 Common, 2 Rare, 3 Rare+, 4 Epic, 5 Epic+, 6 Legendary, 7 Legendary+,
  8 Mythic, 9 Mythic+, 10 Ancestral, 11–15 Ancestral 1–5 stars).
- **Lab timers are measured from `exportedAt`.** `researches[].remainingSeconds` for a lab in the active
  queue is the game's own finish date minus `exportedAt`. It reflects relics and Vault speed but **not** an
  active cell boost on the slot (`speedUp` > 1): the game's finish date assumes no boost, so a
  boosted lab finishes sooner. `activeQueue[].remainingSecondsWithSpeedUp` (SDK 1.5.0+) is the real time
  left: it applies the slot's boost for as long as the boost lasts. Quote that one. For a lab not in the queue it is only a catalog estimate that ignores relics, Vault and gem
  speed-ups. Subtract the export's age before saying "finishes in X". `completeDate` is `null` for a lab
  never started (the save's `0001-01-01` placeholder).
- **`speedUpSpeed` is the gem speed-up multiplier per lab slot**, not the Labs Speed research level;
  `speedUpRemainingSeconds` is how long that speed-up still runs.
- **Number notation is case-sensitive above trillions.** K, M, B, T, then `q` = 1e15, `Q` = 1e18,
  `s` = 1e21, `S` = 1e24, `O` = 1e27, `N` = 1e30, `D` = 1e33. Text fields (`battle_history.coins`, lifetime
  `values`) use it. Prefer numeric fields for arithmetic; convert with `sdk_sandbox_run {mode: "format"}`.
- **`plan_effective_path` starts from zero levels unless told otherwise.** Without `savePath` (or
  `levels`) its steps are shaped, not real (`startedFrom: "zero"`). `savePath` works for `economy` only;
  the answer then lists `unmapped` candidates and `unfilledConfig` inputs (cards, perks, module
  sub-effects) left at defaults, and it prices time with the **peak** coins/hour.
- **Ultimate weapon slots are unnamed and positional** — use the order in §4.
- **Positional lists.** Bot `statLevels`, guardian chip `statLevels` and perk indices mean nothing
  without the catalog order. Look names up (`find_rows`, `oracle_get`); do not guess.
- **Labs list size vs catalog.** A warning that `researchLevel` has fewer entries than the catalog means
  those labs are absent from this save, not unresearched.
- **Assist module slots** are all present but locked before Assist Modules are unlocked; `shards.autoShatter`
  is `null` in v29.2 exports (unknown, not off).
- **Two calculator registries.** `calc_list` / `calc_run` handles and `form_calc` ids are separate; one is
  not valid in the other.
- **Acronyms.** Expand player shorthand with `oracle_expand` / `define_term` (several are ambiguous:
  `SR` is both Shrink Ray and Solar Reflector), never from memory.
- **Privacy.** The export contains the player ID and user name at the top level.
  `readProfileFromSaveRoot` returns the user name; no reader returns the player ID. Do not call that
  reader, do not read either value from the raw file, and never write them into notes, snapshots or
  messages. The snapshot script strips both.
- **`next_unlocks` prices.** Workshop unlock buttons are **full price**: the workshop discount labs do not
  reduce them. A lab's `rushGems` is the price at `exportedAt` and falls as the lab runs; a rush always
  buys the whole remaining level. `gemRushEfficiency` is 1 + 0.015 per fully researched lab, and the rush
  price is the list gem price divided by it — so every maxed lab makes all later rushes cheaper.
  `ultimateWeaponPlus.stones` is priced even when `allWeaponsOwned` is false; a UW+ cannot be bought until
  all nine weapons are owned.
- **`coin_bonus` is a multiplier on what a run earns, not income.** It contains the tier's coin bonus, so
  it changes with `tier` (x30.07 at tier 7 and x20.11 at tier 6 on one real account) — never compare
  totals across tiers without also comparing how far the run gets. It does **not** contain the in-run
  factors: Golden Tower, Black Hole, Death Wave, Spotlight, Golden Bot, perks. Rows at exactly 1 are levers
  the account has not pulled (no pack, `enhancement` not unlocked, no dissonant boost on this tier).
  Useful `overrides`: `{"coinsCard": {"equipped": true}}`, `{"relicCoinBonus": 0.2}`,
  `{"purchases": {"hasStarterPack": true}}` — state pack what-ifs as facts, never as a push to buy.
- `uw.stoneCost` / `uw.statValue` return `null` both for a wrong `weapon`/`stat` string and for a level with
  no price. Check the exact strings in `meta-ultimate-weapons.md` before concluding a level is unavailable.
  `uw.stoneCost` prices one level; for a range use `calc_run uw.stoneCostBetween {weapon, stat,
  fromLevel, toLevel}` (the total, SDK 2.0.0) or `form_calc uw.stones {weapon, stat, currentLevel,
  targetLevel}`, which lists each level and the total (Golden Tower Cooldown 0→3 = 10 + 28 + 46 = 84 in
  all three). Its `statsForWeapon` gives the exact stat strings. The next weapon unlock is
  `next_unlocks.ultimateWeapon.stones` (or `calc_run uw.nextUnlockStoneCost`), not `uw.stoneCost`.
- `readLabsFromSaveRoot.labsUnlocked` counts only the slots bought with gems; the first slot is free, so
  slots owned = `labsUnlocked + 1`. `activeQueue` lists all five slots: a row with `active: false` whose
  `slotIndex` is below the owned count is an **idle slot**. If `hasActiveQueueData` is false, the queue is
  missing from the export — say so instead of reporting idle slots.
- `readBotsFromSaveRoot.totalStonesSpent` has been seen equal to the account's lifetime stones spent on
  everything; do not present it as bot spending without cross-checking.
- The server's own instructions tell agents to call `begin_mechanic_task` / `record_work_status` first.
  That is for editing the SDK's mechanics; a coach reading a save ignores it.
- Pricing: `form_calc` (omit `id` to list) is much lighter than `calc_describe` + `calc_run` for labs
  (`lab.research` → coins and hours), module costs, UW stones and bot/guardian upgrades. `calc_describe`
  answers are large; call it only when a handle's parameters are unclear. `module.stat` takes
  `{type, rarityLabel, level}`; a wrong key silently returns 1.
- Module `effects[]` are numeric ids: name them with `find_rows {name: "MODULE_SAVE_EFFECT_ID_LABELS"}`.
  The roll's rarity is not recoverable through the MCP.
- The reader has no "natural epic" flag. A module whose `mappedName` is not one of the epic modules listed
  in `meta-modules-cards.md` § unique effects is a rare-family module merged upward: it has no unique
  effect and cannot pass Legendary+. Cross-check with `readModuleEconomyFromSaveRoot.epicObtained`.
- `readLifetimeBreakdownFromSaveRoot.killsBySource` has shown `projectiles` and `deathRay` apparently
  swapped relative to per-run stats. Prefer the per-run kill split.
- `readCurrenciesFromSaveRoot.earnedThisCycle` / `spentThisCycle`: the cycle length is not documented; do
  not turn them into weekly rates. `battleDate` on a run is the run's **end**, not its start (SDK 3.0.0:
  across twenty stored exports a run first appears minutes after its `battleDate`).
- `plan_effective_path`: `cost` and `roi` units are per variant (time, coins or stones) and it can report
  "prerequisite not met" for labs the account already has. Use the ordering, not the absolute values.
- `form_calc lab.research` needs the account's lab speed and coin discount as inputs
  (`readLabCostModifiersFromSaveRoot` has the three levels from SDK 3.0.0). Speed percent that
  matched `lab.durationDays` on a real save: ((1 + 0.02 × Labs Speed lab level) × (1 + lab-speed relic
  bonus) × slot boost − 1) × 100, where the relic bonus is `LabSpeed` from `workshop.relicBenefitByStat`
  (§3); coin discount from `calc_run lab.coinDiscount` with the Labs Coin Discount
  lab level. Verify one known lab (cost shown in game or a queued lab's duration) before pricing a list.
- With Auto Export on, the game rewrites `tool_export.json` while you work. Note `exportedAt` at the first
  read; if the snapshot or a later read shows a newer one, say which export the numbers come from.
- `battle_history`/`read_save_field` page about ten columns of 30 runs per call. Read income, length, tier,
  killer and coin-source columns that way; the long tail of ~150 per-run stats (kill and damage by source,
  mitigation) is practical to read from the snapshot JSON once it exists.
- `readPerkChoicesFromSaveRoot.autoPickOrder` is the player's ranking of perks; how many ranks are honoured
  depends on the Auto Pick Ranking lab level. Check that lab before saying a low-ranked perk never gets picked.
- **Reading `plan_spending`** (SDK 3.0.0). Every gain is **coins per day**.
  - `forecast`: `tier`, `coinsPerRun` / `coinsPerHour` / `cellsPerHour` / `coinsPerDay` / `cellsPerDay`
    (each `{p25, median, p75}`), `hoursPerDay`, `runsUsed`, `regimeBreaks[{after, before, reason, ratio}]`
    (`reason` is `coin-bonus` when two readings show the Total Coin Bonus stepped, `income-step` when only
    the runs show it), `pausedRuns[]`, `uptime[{days, hoursPerDay, share}]` (last day, last week, whole
    window), `warnings[]`. Only full farm runs after the last break set the rates: on one real account a
    pack bought the day before left `runsUsed: 4` of 30. With one run the three percentiles are equal.
  - `coinModel`: `passThrough` (the share of a coin-bonus gain that reaches recorded coins; every
    coin-bonus gain in the queues is multiplied by it), `runToRunSpread` (how far this account's runs
    differ with nothing changed: 1.56 on one account), `waveCoinDrift`, `pairs[]`, `sources[]`,
    `killCoinScale`. Its warnings explain whether a change in income was distinguishable from that spread.
  - `labQueue[]` / `coinQueue[]` rows: `candidate`, `kind` (`lab`, `workshop`, `enhancement`), `coins`,
    `slotHours`, `gainPerDay {low, likely, high}`, `paybackDays`, `gainPerSlotHour`, `gainPerCoin`,
    `totalCoins` / `totalSlotHours` (with `gates[{name, coins, slotHours}]` included), `permanent`,
    `model` (for a workshop row, `wave survival (+57 waves from 2088)`), `confidence` (on workshop rows
    it has equalled the survival fit's leave-one-out error; `null` elsewhere), `overlaps[]` (candidates
    whose gain band overlaps this one: the order between them is not established).
  - **The lab queue is sorted by gain per slot-hour, not by payback.** On one account its first row was
    a lab costing 87B coins that pays back in 874 days, ahead of one paying back in 18. Read
    `paybackDays` and `totalCoins`, and the top-level warning naming labs "not scheduled" because the
    forecast cannot pay for them inside the horizon.
  - A workshop row with `gainPerDay` 0 and `paybackDays: null` gained no waves in the model — an
    "ignore for now", not a bug.
  - `notRanked[{candidate, reason}]`: locked labs with the milestone that opens them, unmet
    prerequisites, and what no model prices (Labs Speed and Labs Coin Discount, module slot levels,
    workshop unlocks such as the Wall, the Recovery Package enhancement, attack workshop levels).
    Labs Speed not being ranked says nothing about its worth: argue it from `meta-workshop-labs.md`.
  - `buyList {balance, items[{name, coins, cumulativeCoins, affordableAt {early, likely, late}}]}`: the
    coin queue bought in order from the coins on hand. Dates are UTC ISO strings.
  - `labSchedule {timeZone, labSpeed, rows[], swaps[]}`: rows with `start: null` are running now; the
    rest are what to start when each slot frees: `slot`, `lab`, `toLevel`, `start`, `finish`,
    `startLocal`, `finishLocal`, `coinsNeeded`, `balanceWhenSlotFreed`, `boost`. Without `timeZone` the
    local times are UTC and a warning says so: pass the player's zone (ask once, or use the session's).
  - `boostPolicy {policy[{slot, multiplier, cellsPerDay}], cellsPerDay, netCellsPerDay, daysToFloor,
    renewAt[], fallback[]}`. Prices are the wiki's unless `boostPrices` is passed; the warning says so.
    Ask the player to read one price on the Labs screen before relying on the budget.
  - `dissonance {tier, currentWave, currentBonus, rows[{wave, totalBonus, gain, gainPerDay, cost,
    cellsCost, paybackDays}], breakEvenWave}`: `cost` is one farm run's coins given up. The waves are a
    table, not a prediction.
  - It reads the selected tier's farm runs. `survival: false` adds a warning that workshop levels were
    not ranked.
- **`snapshotsDir`** (`plan_spending`, `survival_rank`) takes one folder and reads its `.json` files, the
  60 most recently written, not subfolders: pass the player's folder
  (`~/.tower-coach/snapshots/<playerKey>`), not the snapshots root. Both the snapshot script's files and
  kept `tool_export.json` copies are accepted; `advice-log.md` is ignored. A folder with nothing usable
  is an `error` ("no usable readings"); then call again without it. Without it the tools assume every
  past run was played with today's account, and say so in `warnings`.
- **Reading `survival_rank`.** `toLevel` is the level to reach: a `toLevel` at or below the current level
  comes back with `coins: 0`, `medianWavesGained: 0` and `wavesPerBillionCoins: null`. `baseline` is the
  predicted death wave now. `fit.leaveOneOutError` is how far a held-out run's wave was missed on
  average (0.106 on one account): a gain smaller than that share of the baseline is noise.
  `fit.skipped[]` names runs left out and why — usually "workshop or cards changed between the readings
  around this run", which more frequent snapshots cure. The model is fitted, not derived: it reads
  workshop levels and the Health card, takes every run as AFK, and does not rank damage upgrades, the
  Wall or enhancements reliably (its `warnings` list these every time). State a result as "the model
  fitted to your runs predicts", never as a game rule.
- **`coin_bonus` scenarios.** A scenario that only changes `tier` has come back with `ratioToNow: 1` and
  no `changedRows` while its `total` differed: compare its `total` with the top-level `bonus.total`
  yourself. A `dissonanceWave` at or below the tier's current Dissonant best changes nothing.
