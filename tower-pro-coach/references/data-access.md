# Data access — reading the whole account through the Tower SDK MCP

Everything here was checked against `BeardedUnicorn/TheTowerSDK` (`@beardedunicorn/thetowersdk` 1.0.0,
`mcp/server.mjs`) and a real v29.2.1 export. Only this server is supported.

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

It is the right server when **all four** of these exist: `read_save_field`, `battle_history`,
`patch_notes`, `find_rows`. A server that has `decode_save` / `run_extractor` but not those four (checking the first three is enough) is an
older or different build: stop and tell the player to install/update the BeardedUnicorn server
(`claude mcp add thetowersdk -- node <path>/mcp/server.mjs`; a git checkout needs `pnpm build` first,
because the server reads `dist/`). Do not fall back to anything else.

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

If several macOS matches appear, take the most recently modified and confirm with `decode_save`. On
iOS, suggest looking in Files → On My iPhone/iPad for a Tower folder, and otherwise AirDrop/Files the
file to a computer; say plainly that this route is not documented. If nothing is found, ask the player
for the path. All save tools want an **absolute** path (`~` is expanded; a relative path is read from the
server's working directory and will miss).

## 3. Tools and exact parameters

`*` = required. Every failure comes back as JSON with `error` (often `hint` / `didYouMean`), not an
exception. Read those fields before retrying.

### Save tools (read-only on the file)

| Tool | Parameters | Returns / limits |
|---|---|---|
| `decode_save` | `path*` | `{gzip, rootKeys, battleRuns, targets[]}`; one target per reader: `{extractor, found, fields[] or count, warnings}` (counts only, no values). This is the authoritative reader list. |
| `run_extractor` | `extractor*`, `path*` | One reader's result as a preview: up to 40 top-level keys and **12,000 characters of values**. Fields that do not fit are listed in `outlined` as a shape (`kind`, `length`, first 12 `columns`) — they are **not missing**. `warnings` (max 20 shown). `result: null` = save has no data for that feature. |
| `read_save_field` | `extractor*`, `path*`, `field` (dotted path, e.g. `researches`, `active.levels`, `slots.0.baseStatLevels`), `pick` (string[]: columns of a list / keys of an object), `where` (object, column → value, compared as text; lists only), `search` (text in any top-level column; lists only), `offset` (negative counts from the end), `limit` | Lists: default 20 rows, max 100, and a page is also cut at 12,000 characters (`sizeLimited`) — use `pick`. Objects: default 100 keys, max 500. `truncated` + `next` = pass `next` as `offset`. Omit `field` to read the result itself. Unknown arguments are refused. |
| `battle_history` | `path*`, `kind` (`all` \| `farming` \| `tournament`), `detail` (boolean), `offset`, `limit` | Default 10 runs, max 50. See §5. Not size-capped: `detail: true` on all runs is >100 KB, so use `limit` ≤ 3 with it. |

`read_save_field`'s `extractor` also accepts other save functions that take the save root:
`listImportableBattleRuns` (the raw run list) and `computeCoinsPerHourFromSaveRoot` (one number) both work.

### Game data, formulas, knowledge (no account data)

| Tool | Parameters | Notes |
|---|---|---|
| `list_exports` | `entry*` (`data`, `save`, `node`, `mechanics`, `formatting`, `wiki`, `knowledge`, `builders`, `calculators`, `charts`, `sheets`, `bot`, `save-decoder`, `contributions`, `assets`), `filter`, `offset` | 300 names per page. Never invent an export name; look it up here. |
| `get_export` | `name*`, `limit` (default 40, max 100) | Preview, 12,000-character budget. |
| `find_rows` | `name*`, `where`, `search`, `fields` (string[]), `offset`, `limit` (default 20, max 100) | Rows of one table. Object-keyed exports gain a `_key` column. Note the column parameter is `fields` here and `pick` on `read_save_field`. |
| `describe_schema` | `table` (omit to list tables) | Declared shape of a data table. |
| `calc_list` | `filter`, `limit` (default 60, max 100) | ~2,000 calculators; always filter. Save-reading ones are `save.*`. |
| `calc_describe` | `id*` | Params with units, invariants, linked oracle traps. |
| `calc_run` | `id*`, `args` (object — calculator parameters go **inside** `args`), `savePath` | `savePath` decodes the export and passes it as the calculator's `root` / `parsedRoot` parameter. Unknown top-level keys are refused. |
| `calc_chart` | `chart` | Which calculators produce a chart's numbers. |
| `calc_graph` | `concept` | What feeds a number. |
| `chart_rows` | `chart`, `args` (string[]), `offset`, `limit` (default 40, max 100) | Published table rows; omit `chart` to list charts. |
| `form_calc` | `id`, `input` (object) | The site's form calculators (lab research, workshop upgrade, module cost, UW stones, bot/guardian upgrades). Omit `id` to list. Ids differ from `calc_list` handles. |
| `plan_effective_path` | `family*` (`damage` \| `economy` \| `health` \| `regen`), `variant*` (damage: `lab-time`, `lab-coins`, `stone`, `coin`, `keys`; economy: `time`, `coin`, `stone`; health: `lab-time`, `lab-coins`, `stone`, `coin`; regen: `lab-time`, `lab-coins`), `steps` (default 10, max 200), `savePath` (**economy only**), `levels` (object merged over all-zero) | Returns `steps[{step,name,level,cost,roi}]` and `excluded[{sheetName,reason}]`. See §7 on zero-start. |
| `patch_notes` | one of `query`, `introduced`, `version`, `from`+`to`, `recent`; plus `limit` (default 5, max 25), `full` (boolean; bodies are cut at 600 chars without it) | With no argument: archive range and latest versions. Use to check whether advice predates a patch. |
| `wiki_search` | `query*`, `limit` (default 10) | Real page titles. Network. |
| `wiki_page` | `title*`, `section`, `offset`, `refresh`, `sourceId` (`fandom` \| `gamevault`) | 12,000 characters per call; `next` → `offset`. Wiki text is CC-BY-SA. Network. |
| `define_term` | `term*`, `domain` | Glossary; `found: false` rather than a near miss. `ambiguous: true` → pass `domain`. |
| `oracle_expand` | `term*` | Acronym → closed set of expansions. Use before interpreting player shorthand. |
| `oracle_search` | `query*`, `limit` (default 10, max 50) | Find an entity by player-facing name. |
| `oracle_get` | `id*` | One entity: meaning, units, relations, sources. |
| `oracle_traps` | `id*` (entity id or plain name) | How this mechanic has been got wrong before. |
| `oracle_brief` | `mechanic*` | Units, valid range, implementing exports, traps. |
| `oracle_footguns` | `mechanic` (optional filter) | Irreversible upgrades and known footguns. **Call before recommending any spend.** |
| `oracle_map` | `family`, `includeSources`, `detail` | A whole system. Without `family` it is very large. |
| `oracle_coverage` | `asOf` | What the oracle does and does not know. |
| `oracle_contradictions` | — | Sources that disagree. |
| `sdk_sandbox_run` | `mode` (`list` \| `export` \| `calc` \| `format` \| `decode`), `name`, `entry`, `id`, `input`, `value`, `savePath` | Scratchpad. `mode: "format"` with a number `value` writes game notation; with a string it parses it. Annotated as not read-only, so a client may prompt for it; rarely needed. |

### Tools the coach never calls

`record_mechanic_note`, `record_work_status` and `begin_mechanic_task` **write files** (they append to a
mechanics map and ledger under the server's directory). They exist for people changing the SDK.
`compliance_contract` is the same workflow's instructions. `sdk_graph_*`, `trust_*`, `sdk_debug_*`,
`mcp_contract` and similar appear only inside the SDK's development repository and are not for coaching.

## 4. Save readers

30 readers match `read*FromSaveRoot` in SDK 1.0.0 (`decode_save` lists whatever the installed build has —
trust that list over this table). Each returns an object or `null` when the save has no data for the
feature; most carry `warnings: string[]` — a non-empty one usually means the save shape changed.

### Progression

| Reader | Contains | Fields a coach uses, and gotchas |
|---|---|---|
| `readWorkshopFromSaveRoot` | Workshop levels, enhancements, presets | `active.levels` (object, display name → level, e.g. `"Damage"`, `"Coins / Kill Bonus"`), `active.enhancementLevels` (`WSP_*` keys), `presets[]` (same two objects per preset), `meta.currentPreset`, `meta.presetNames`, `meta.totalCoinsSpentWorkshop`, `meta.totalCoinsSpentEnhancements`. `active` is the preset in use. |
| `readWorkshopUnlocksFromSaveRoot` | Rows unlocked per category | `upgradeTiersUnlocked`, `enhancementTiersUnlocked` (`{attack, defense, utility}`), `freeUpgradeLocked[]`. |
| `readLabsFromSaveRoot` | Research levels, queue, completion log | `researches[]` `{index, level, displayName, slug, category, percentComplete, completeDate, remainingSeconds}`; `activeQueue[]` `{slotIndex, active, speedUp, speedUpRemainingSeconds, research}`; `completions[]` `{researchIndex, level, completedAt}` oldest first; `labsUnlocked`, `researchedCount`, `maxedCount`, `totalCoinsSpentOnResearch`. Seconds throughout. See §7 for timers. Rows with `displayName: null` are hidden/unnamed (`hiddenUnnamedCount`). |
| `readFavoriteLabSlugsFromSaveRoot` | Starred labs | `string[]`; empty when none starred. |
| `readUltimateWeaponsFromSaveRoot` | UW unlocks and levels | `slots[]` `{slotIndex, unlocked, active, plusLevel, plusUnlocked, plusOn, baseStatLevels[3]}`. **No names**: `slotIndex` 0–8 = Chain Lightning, Smart Missiles, Death Wave, Chrono Field, Inner Land Mines, Golden Tower, Poison Swamp, Black Hole, Spotlight. `baseStatLevels[3]` follows the first three stats of each weapon in the order listed in `meta-ultimate-weapons.md` (e.g. Golden Tower: Multiplier, Duration, Cooldown) — sanity-check one value against what the player sees. Trust `baseStatLevels` only when `baseStatChunkingPlausible` is true. |
| `readCardsFromSaveRoot` | Card levels, copies, slots | `cards[]` `{slug, name, level, count, unlocked, active, masteryUnlocked}`, `equippedCards[]`, `slotsUnlocked`, `currentPreset`, `presetNames`, `presetSlots[]` (flat, per preset × slot). `count` = spare copies toward the next level, not a lifetime total. |
| `readModulesFromSaveRoot` | Equipped and owned modules, shard balances | `equipped[]` `{slotKey ("primary:Cannon" … "assist:Core"), role, category, mappedName, mappedInitials, level, rarityLabel, rarityEnum, effects[], effectLocked[], guid, shardsSpent, coinsSpent}`; `inventory[]` same minus slot fields; `shards` `{cannon, armor, generator, core, rerollCurrency, tickets}`. `equipped[].level` is the **slot** level (§7). `coinsSpent` is approximate above ~9e15. |
| `readModuleEconomyFromSaveRoot` | Slot levels, pity, assist slots, module presets | `slotLevels[4]` (Cannon, Armor, Generator, Core), `slotCoinsSpent`, `slotShardsSpent`, `pity` / `rarePity` (pulls since last epic / rare), `assistSlots[]` `{category, unlocked, level, mainEffectEfficiencyLevel, substatEfficiencyLevel, uniqueEffectEfficiencyLevel}`, `presets[]` (module GUIDs per slot), `epicObtained`, `merges`, `gemsSpent`, `lifetimeShards`. |
| `readBotsFromSaveRoot` | Bots, levels, presets | `bots[]` `{name, label, unlocked, active, statLevels[4], plusUnlocked, plusLevel}` for the active preset; `presets[]`; `totalStonesSpent`, `totalMedalsSpent`; `synchronicity`. `statLevels` is positional and the stat order differs per bot (Flame: Damage Reduction, Cooldown, Damage, Range; Thunder: Duration, Cooldown, Linger, Range; Golden/Amplify: Duration, Cooldown, Bonus, Range). |
| `readBotSynchronicityFromSaveRoot` | Bot sync | `inSave`, `unlocked`, `level`, `slotCount`, `slots[]`, `bots[]`. |
| `readGuardiansFromSaveRoot` | Guardian, chips, presets | `guardianUnlocked`, `inGuild`, `activeInBattle`, `chips[]` `{label, unlocked, statLevels[3], equippedSlot}`, `equippedChips[]`, `chipSlotCount`, `slotsUnlocked`, `presets[]`, `totalCoins`, `totalCatches`. `slotsUnlocked` counts **bought** slots; owned slots = `chipSlotCount`. Chips do nothing outside a guild since v29.1 — check `activeInBattle`. |
| `readVaultFromSaveRoot` | Vault | `keys`, `totalKeysEarned`, `v29.levels` (object, `v29:…` key → level), `v29.unlockedGroupCount`, `v29.upgradeCount`; legacy `powerNodes[]` / `harmonyNodes[]` `{id, name, level, unlocked, maxLevel}`. Read `v29` first on a v29+ account. |
| `readRelicsFromSaveRoot` | Relics | `unlockedCount`, `relics[]` `{index, name, label, description, unlocked, onProfile}` (one row per catalog relic, hundreds), `profileRelicIndices`. Page with `where: {unlocked: true}`. A mailed-but-unclaimed relic is not `unlocked`. |
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
| `readPurchasesFromSaveRoot` | Permanent packs | `hasStarterPack`, `hasEpicPack`, `hasDisableAds`. Ownership flags only; no multiplier is inferred. |
| `readCurrentRunFromSaveRoot` | Run in progress | `currentTier`, `currentWave`, in-run `upgradeLevel[]` / `upgradeDefenseLevel[]` / `upgradeUtilityLevel[]`. These are in-run cash upgrades, not Workshop levels. |
| `readEffectivePathsSettingsFromSaveRoot` | Reach | `highestTier` (last tier with a wave recorded), `highestWave`, `wavesByTier` (object tier → wave), `gameSpeed` (may be null). |

### Settings & metadata

| Reader | Contains | Fields a coach uses |
|---|---|---|
| `readExportInfoFromSaveRoot` | The export about itself | `exportedAt` (ISO), `versionNumber` (game **build** number, not "29.2"), `dataVersion`, `exportVersion`, `checked`, `unknownKeys[]`, `warnings[]`. Read this first (§7). |
| `readGlobalPresetsFromSaveRoot` | Global Presets | `presets[]` `{name, workshop, cards, bots, modules, guardians}` (preset index per system), `currentPreset`, `tierPreset`, `tournamentPreset`, `dissonantPreset`. Tells you which loadout is used for farming / tournament / dissonant runs. |
| `readRuntimeControlsFromSaveRoot` | In-run toggles | `targetPriority`, `targetPriorityList`, `lifeSavingOrder`, range/orb selections, `energyShieldRestrictionToggle`. |
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

**Raw run record** (`detail: true`, or `read_save_field` with `extractor: "listImportableBattleRuns"`):
148 numeric fields plus `battleDate` (string) and `isTournament` (boolean). Groups:

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

**Call sequence (~35 calls; batch the independent ones in parallel):**

1. `decode_save {path}` — reader list, which are `found`, warning counts, run count.
2. `run_extractor` for `readExportInfoFromSaveRoot` — check `exportedAt`, `checked`, `warnings`.
3. `run_extractor` once per remaining reader with `found: true`, in parallel. Themes, collected theme
   names and runtime controls can be skipped unless asked. Small results arrive whole.
4. For every name in an answer's `outlined` (or a `truncated` list), page with `read_save_field`.
   On a developed account expect:
   - labs `researches` — `pick: ["displayName","level","category","remainingSeconds"]`, `limit: 100`,
     follow `next` (a few hundred rows);
   - labs `completions` — only the tail: `offset: -30`;
   - modules `inventory` — `pick: ["mappedName","category","rarityLabel","level","favorite"]`, `limit: 100`;
   - relics `relics` — `where: {"unlocked": true}`, `pick: ["name","description"]`, `limit: 100`;
   - cards `presetSlots` — only if comparing presets.
5. `battle_history {path, limit: 50}` — every run, compact, plus peak `coinsPerHour`.
6. `read_save_field {extractor: "listImportableBattleRuns", path, limit: 30, pick: [...]}` for the numbers
   the compact row lacks. About ten columns of 30 runs fit one page; make one call for
   `battleDate, tier, wave, realTime, gameTime, coinsEarned, cellsEarned, rerollShardsEarned, killedBy,
   isTournament, dissonanceType` and a second for the coins-by-source columns.
7. Before advising: `oracle_footguns` (optionally with `mechanic`), then as needed
   `plan_effective_path {family: "economy", variant, savePath}`, `calc_run`, `form_calc`, `patch_notes`.

Never conclude "the player has none" from a preview: check `outlined`, `truncated`, `next` and `matched`.

## 7. Quirks and traps

- **`null` is not zero.** A reader returning `null`, or a field that is `null`, means the save does not
  record it — not that the player has none.
- **Newer game than the SDK.** `readExportInfoFromSaveRoot.checked: false`, or anything in its `warnings`
  / `unknownKeys`, means the export is newer than the SDK was verified against (1.0.0: build 1294 =
  v29.2.1, data version 35). Renamed fields then read as missing; tell the player and update the SDK.
- **Module levels live on the slot since v29.** `readModulesFromSaveRoot.equipped[].level` is already the
  slot level; `readModuleEconomyFromSaveRoot.slotLevels` is the same per primary slot. `inventory[].level`
  may be a retired placeholder — never use it to rank modules. Levelling raises the main effect only,
  merging raises the rarity **cap**, and swapping modules loses no level. Pre-v29 "which module keeps its
  level" advice is obsolete.
- **Module rarity has three spellings.** `rarityLabel` is display form (`Rare +`, `Ancestral 5`);
  `rarityEnum` is numeric (0 None, 1 Common, 2 Rare, 3 Rare+, 4 Epic, 5 Epic+, 6 Legendary, 7 Legendary+,
  8 Mythic, 9 Mythic+, 10 Ancestral, 11–15 Ancestral 1–5 stars).
- **Lab timers are measured from `exportedAt`.** `researches[].remainingSeconds` for a lab in the active
  queue is the game's own finish date minus `exportedAt` (it already includes relics, Vault and gem
  speed-ups). For a lab not in the queue it is only a catalog estimate that ignores relics, Vault and gem
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
- **Privacy.** The export contains the player ID and user name at the top level. No reader returns them;
  do not read them from the raw file, and never write them into notes, snapshots or messages.
- `uw.stoneCost` / `uw.statValue` return `null` both for a wrong `weapon`/`stat` string and for a level with
  no price. Check the exact strings in `meta-ultimate-weapons.md` before concluding a level is unavailable.
  `uw.stoneCost` prices one level; sum a range level by level.
- `readLabsFromSaveRoot.labsUnlocked` has been seen one lower than the number of active queue slots. Count
  slots from `activeQueue` (and which have `active: true`) when checking for an idle slot.
- `readBotsFromSaveRoot.totalStonesSpent` has been seen equal to the account's lifetime stones spent on
  everything; do not present it as bot spending without cross-checking.
- The server's own instructions tell agents to call `begin_mechanic_task` / `record_work_status` first.
  That is for editing the SDK's mechanics; a coach reading a save ignores it.
- Lab `remainingSeconds` on a real save matched the un-boosted duration, i.e. an active cell speed-up
  (`speedUpSpeed`, `speedUpRemainingSeconds`) did not appear to be included. Give finish times as a range
  (boosted vs un-boosted) unless the player confirms what the game shows.
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
  not turn them into weekly rates. `battleDate` on a run appears to be the run's end time.
- `plan_effective_path`: `cost` and `roi` units are per variant (time, coins or stones) and it can report
  "prerequisite not met" for labs the account already has. Use the ordering, not the absolute values.
