# Glossary: community shorthand and jargon

Verified against game version: v29.2.1 — 2026-11-20

Main sources
- SDK compartments `jargon.ts`, `naming.ts`, `build-targets.ts`, `masteries.ts`, `uw-plus.ts`; `src/data/glossary`; module templates (initials).
- Community guides cited by the SDK (Evan, DrAudacious) for the shorthand used in practice; Fandom wiki guide pages.

## Contents
1. Rule for the coach
2. Composition grammar (P-prefix, digits, %, +, #)
3. Ambiguous acronyms (resolve by context)
4. Ultimate weapons and UW+
5. Modules (initials and nicknames)
6. Cards, masteries and perks
7. Bots, guardian, guild
8. Stats, economy and measures
9. Builds and playstyles
10. Tournament and progression terms

---

## 1. Rule for the coach

**Never expand an acronym from memory when unsure.** Call the MCP `oracle_expand` (closed set of known readings, with guidance on which to use) or `define_term`. If more than one reading is returned and the context does not settle it, ask the player. A plausible wrong expansion is worse than a question. Game names must be spelled as the game spells them (`Berserker`, `Astral Deliverance`, `Ranged Ultimate` without a possessive).

Status tags: entries here are vocabulary, so they are `[consensus]` by nature. Numbers attached to a term are `[mechanic]` only where marked.

## 2. Composition grammar

Players build targets by gluing tokens together. An unseen combination still parses by these rules.

| Form | Meaning | Example |
|---|---|---|
| `P` + UW initials | "perma": duration ≥ cooldown, so the UW is always active. Several initials = all of them at once. Letter order carries no meaning. | `PBH`, `PBHGT` = `PGTBH`, `PCF` |
| UW + digit | The UW's **Quantity** stat at that value. | `DW3`, `SL4`, `CL5` |
| UW + number (as %) | A stat threshold, almost always Chrono Field slow. | `CF75`, `PCF75`, `PCF90` |
| UW + `+` | The UW's enhancement (UW+). A digit after it is the UW+ level. | `GT+`, `SL+3` |
| card + `#` or card + `m` | That card's mastery. A digit after `#` is the mastery level. | `WA#`, `ISm`, `RPC#3` |
| bot + `+` | The bot's Bot+ ability. | `GB+` |
| `T#` / `W#` | Tier / wave. | `T14 W4500` |
| `a:b` | Cooldown sync ratio or a cooldown written as min:sec. | `2:1`, `3:20` |

**Undefined targets** `[mechanic]`
- Perma needs **both** a Duration and a Cooldown stat. Only four UWs have both: **Golden Tower, Black Hole, Chrono Field, Poison Swamp**. `PDW`, `PCL`, `PSL`, `PSM`, `PILM` name nothing.
- Quantity exists only on **Chain Lightning, Smart Missiles, Death Wave, Inner Land Mines, Spotlight**. Those are exactly the five that cannot be perma, so one UW never takes both a `P` and a digit.
- Quantity maxima from stones: DW 5, CL 5, SL 4, SM 20 `[mechanic]`. Module quantity substats **floor**, so a fractional assist contribution adds nothing.
- Chrono Field's own slow stat tops out at 75%; 90% is the hard cap across all sources. `CF90` cannot come from stones alone. `[mechanic]`
- The game has no "perma" state or `DW3` flag. These are names for relationships between numbers.

## 3. Ambiguous acronyms

| Term | Readings | How to choose |
|---|---|---|
| `GC` | Glass Cannon (build) / Galaxy Compressor (generator, also `GComp`) | "running GC" = build; "Anc GC", "GC assist" = module |
| `CF` | Chrono Field / Crit Factor | UW talk vs attack-stat talk |
| `SL` | Spotlight / Stellar Lift (rare module) | Almost always Spotlight |
| `PC` | Plasma Cannon (card) / Primordial Collapse (core) | Cards vs modules |
| `DC` | Dimension Core (core) | Sometimes typed "DimCore" |
| `AS` | Amplifying Strike (cannon) / Attack Speed | Module vs stat |
| `SD` | Space Displacer (armor) | — |
| `SR` | Shrink Ray (cannon) / Solar Reflector (rare module) | — |
| `RB` | Restorative Bonus (generator) / Rapidreach Blitzer (rare cannon) | Almost always Restorative Bonus |
| `CB` | Coin Bot (= Golden Bot) / Coin Bonus | Bots vs economy |
| `GB` | Golden Bot | — |
| `SW` | Second Wind (card) / Shockwave | Cards vs defense stats |
| `DM` | Demon Mode (card). Damage per meter is written `DPM` or `dmg/m` | — |
| `ES` | Energy Shield (card) | — |
| `ELS` | Enemy Level Skip. **Not** Energy Shield | — |
| `EB` | Enemy Balance (card) | — |
| `OC` | Om Chip (core) / Overcharge (fleet enemy, also "OCs") | Modules vs enemies |
| `SP` | Sentry Protocol (armor, v29) | Do not confuse with `PS` |
| `PS` | Poison Swamp | — |
| `RTO` | Regen Trade-Off / Ranged Trade-Off (perks) | Ask |
| `CC#` | Critical Chance mastery / Critical Coin mastery | Ask, or read context (crit vs coins) |
| `BC` | Battle Condition | — |
| `PF` | Project Funding (generator) | — |
| `TB` | Tactical Barrage (core) / Thunder Bot | Modules vs bots |
| `BB` | Bot Bot | — |
| `IS` | Intro Sprint | — |

## 4. Ultimate weapons and UW+

| Short | Name | UW+ name (`X+`) |
|---|---|---|
| UW | Ultimate Weapon (nine exist) | UW+ = the enhancement, unlocked per weapon with stones |
| GT | Golden Tower | Golden Combo |
| BH | Black Hole | Consume |
| DW | Death Wave | Kill Wall |
| CL | Chain Lightning | Smite |
| SL | Spotlight | Light Range |
| SM | Smart Missiles | Cover Fire |
| CF | Chrono Field | Chrono Loop |
| PS | Poison Swamp | Death Creep |
| ILM | Inner Land Mines | Charged Mines |

- `sync` – two cooldowns in a fixed ratio so effects overlap (usually GT:BH at 1:1, bots at 2:1 to the UW sync).
- `natural sync` – sync reached by equal cooldown levels, without Multiverse Nexus.
- `3:20` – a 200-second GT/BH cooldown, the first natural-sync point guides name.
- `desync` – cooldowns that drift apart; also a deliberate strategy.
- `uptime` – fraction of time a UW is active (duration ÷ cooldown).
- `goldbox` – a lab (or stat) at its maximum level; the lab tile shows a gold box.
- `floodlight` – community name for a Spotlight set-up wide enough to cover most of the field `[unverified threshold]`.

## 5. Modules

Slots: Cannon (attack), Armor (defense, sometimes written "Defense"), Generator (utility), Core (ultimate weapons).

| Initials | Module | Slot |
|---|---|---|
| AD | Astral Deliverance | Cannon |
| BA | Being Annihilator | Cannon |
| DP | Death Penalty | Cannon |
| HB | Havoc Bringer | Cannon |
| SR | Shrink Ray | Cannon |
| AS / AmpStrike | Amplifying Strike | Cannon |
| GS | Gilded Sniper (v29) | Cannon |
| ACP | Anti-Cube Portal | Armor |
| NMP | Negative Mass Projector | Armor |
| WR / WHR | Wormhole Redirector | Armor |
| SD | Space Displacer | Armor |
| SF | Sharp Fortitude | Armor |
| OA | Orbital Augment | Armor |
| SP | Sentry Protocol (v29) | Armor |
| SH | Singularity Harness | Generator |
| GC / GComp | Galaxy Compressor | Generator |
| PH | Pulsar Harvester | Generator |
| BHD | Black Hole Digestor | Generator |
| PF | Project Funding | Generator |
| RB | Restorative Bonus | Generator |
| IT | Infinity Threshold (v29) | Generator |
| OC / OMchip | Om Chip | Core |
| HC | Harmony Conductor | Core |
| DC / DimCore | Dimension Core | Core |
| MVN | Multiverse Nexus | Core |
| MH | Magnetic Hook | Core |
| PC | Primordial Collapse | Core |
| TB | Tactical Barrage (v29) | Core |

Module vocabulary
- `natural epic` – a module drawn at Epic. Only these have a unique effect and can reach Ancestral.
- `unique` – the named effect of a natural epic; scales with rarity (Epic → Ancestral).
- `main` / `main effect` – the slot's headline multiplier; the only thing levels raise.
- `subs` / `substats` / `sub-effects` – rolled extra stats, 2 to 8 per module.
- `Anc`, `Myth`, `Leg` – Ancestral, Mythic, Legendary. `5★` / `Anc5` = Ancestral 5 (level cap 300).
- `fodder` – modules consumed by a merge.
- `shatter` – destroy a module for module shards.
- `shards` – **two different currencies**: module shards (level-ups, one pool per slot type) and reroll shards (substat rerolls, one shared pool; also called reroll dice).
- `lock` – keep a substat fixed while rerolling the rest (cost rises with locks).
- `ban` – an Effect Bans lab removing a substat from that slot's reroll pool.
- `assist` – the second module in a slot (from T19 W40), giving a fraction of its effects.
- `ME` / `SE` – assist main (multiplier) efficiency / assist substat efficiency, both in %.
- `BiS` – best in slot.
- `pity` – guaranteed Epic after 150 pulls without one.
- `featured banner` / `standard banner` / `Lucky banner` – pull pools with different odds.
- `PMB` – Primary Module Bonus labs (v29.1).
- Substat shorthand: `EHLS` / `EALS` (enemy health / attack level skip), `CPK` (coins per kill bonus), `MST` (multishot targets), `BSC` (bounce shot chance), `SCC` / `SCM` (super crit chance / mult), `DD` (Death Defy), `SLA` / `SLB` (Spotlight angle / bonus), `CLQ` / `CLC` / `CLD` (Chain Lightning quantity / chance / damage), `GTB` (GT bonus).

## 6. Cards, masteries and perks

Cards: `WA` Wave Accelerator, `WS` Wave Skip, `IS` Intro Sprint, `EB` Enemy Balance, `EO` Extra Orb, `SLA` Slow Aura (also `SA`), `PC` Plasma Cannon, `DR` Death Ray, `EN` Energy Net, `ST` Super Tower, `SW` Second Wind, `DM` Demon Mode, `ES` Energy Shield, `UC` Ultimate Crit, `LMS` Land Mine Stun, `RPC` Recovery Package Chance, `FU` Free Upgrades, `ED` Extra Defense, `AoE` Area of Effect, `CritCoin` Critical Coin, `Zerk` / `BZ` Berserker.

Masteries: card shorthand + `#` (SDK convention: `wa#`, `is#`, `rpc#`, `en#`, `st#`, `eo#`, `pc#`, `fu#` …) or + `m` (`WAm`, `ISm`, `ENm`, `EOm`, `RPCm`, `AOEm`, `FUm`). Named masteries: **Viking Funeral** = Berserker mastery ("Viking mastery"); **Coin Orb** = Extra Orb mastery; **Elite Balance** = Enemy Balance mastery.

Card levels are `1★`–`7★`; "maxed" means 7★.

Perks
- `PWR` – Perk Wave Requirement (the perk that shortens the waves between perks).
- `TO` – trade-off perk (a bonus with a penalty). `CTO` – the coins trade-off `[unverified expansion, confirm]`. `RTO` – see ambiguous table.
- `FPC` – First Perk Choice (lab that fixes the first perk offered).
- `ban` (perks) – Ban Perks lab; removes a perk from the pool.
- `auto-pick` – automatic perk selection by priority list.

## 7. Bots, guardian, guild

- Bots: `FB` Flame Bot, `TB` Thunder Bot (also "stun bot"), `GB` / `CB` Golden Bot (coin bot), `AB` Amplify Bot (amp bot), `BB` Bot Bot.
- Bot+ abilities: `FB+` Wildfire, `TB+` Titan Shock, `GB+` Bonus Cells, `AB+` Echoing Shot, `BB+` Maximum Power.
- `Synchronicity` – stone upgrade that makes assigned bots share a path.
- `medals` – event currency (bots, themes, relics, songs).
- Guardian chips: Ally, Attack, Bounty, Fetch, Summon, Scout. `bits` – guardian currency. `tokens` – guild tokens (guild shop).
- `guild box` / `chest` – weekly guild reward thresholds.
- `relic` – permanent passive bonus; `theme` / `skin` / `song` – cosmetics that add a passive coin bonus when owned.
- `keys` – Vault currency (Legend and Mythic tournaments only). `Harmony` / `Power` / `Enemy` – the three Vault tabs.

## 8. Stats, economy and measures

| Term | Meaning |
|---|---|
| `eHP` | Effective health: how much raw damage the tower absorbs once health, defense %, defense absolute and regen are combined. Also the name of the health-based build. |
| `CPH` / `CPM` | Coins per hour / per minute of **real** time (CPH = CPM × 60). A derived measure, not a game stat. Always state tier and clock. |
| `CPK` | Coins per kill bonus (workshop "Coins / Kill Bonus"). |
| `cells/h` | Cells per hour (lab-speed currency from elites). |
| `LTC` / `LTS` | Lifetime coins / lifetime stones earned. Never decreases; not spending power. |
| `PB` | Personal best wave, **per tier**. |
| `ELS` | Enemy Level Skip (`EHLS` health, `EALS` attack). `ELS+` is its enhancement. |
| `DPM` | Damage per meter. |
| `Def%` / `Dabs` | Defense percent (hard cap 98%) / Defense Absolute. |
| `DD` | Death Defy (cap 40% with assists per SDK caps table). |
| `WS+`, `Dmg+` … | Workshop enhancements ("workshop+"), bought with coins after the base stat is maxed. |
| `freeups` | Free upgrades (attack / defense / utility). |
| `RPC` | Recovery package chance. `packages` = recovery packages. |
| `stones` | Power stones. `gems`, `cells`, `coins`, `cash` (in-run only). |
| `q`, `Q`, `s`, `S` … | Number notation is case-sensitive: `q` quadrillion, `Q` quintillion. |
| `F2P` / `P2P` | Free to play / pays (changes milestone track and gem income, no formula). `P2W` is an opinion about the game, not an account type. |
| `ROI` | Return on investment, usually % gain per stone, coin or lab-day. |
| `ePaths` | "Effective Paths", a community planning spreadsheet that ranks upgrades by ROI. |

## 9. Builds and playstyles

- `turtle` – first-days build on defense %, defense absolute and thorns.
- `eHP` / `health build` – survive on health, regen, defense and lifesteal; the standard New–Mid farming build.
- `blender` – orbs (and often thorns) kill everything before it touches the tower.
- `devo` – a deliberately "devolved" (under-developed) tower, classically built around Death Wave health/coin bonuses with low kill speed; variants "Orb Devo", "Reverse Orb devo", "SMAX Devo". `[unverified expansion: sources also write "devourer"; use define_term]`
- `undevelop` / `devolve` – respec stats off before a run on purpose.
- `GC` / `glass cannon` – no health investment; enemies are stunned and killed before they hit (Space Displacer ILM stuns, Energy Shield, Second Wind, scaled damage).
- `hybrid` – health plus damage, common in tournaments.
- `wall` – the Wall defensive structure (Fortress card, wall health/rebuild, wall thorns); "wall build" relies on it. "Thorbs" = wall thorns + boss orbs.
- `orbless` – a build that does not use orbs.
- `perma BH` / `pBH` – Black Hole always up. `pBHGT`, `pCF` likewise.
- `farm` / `farming` – repeatable runs for coins and cells. `push` / `milestone run` – a run for maximum wave. `tourney` – tournament.
- `AFK` / `overnight` – unattended farming; `Auto Restart` is the Vault upgrade for it.
- `damage slider` / `damage cap` – Vault "Damage Cap Slider", used to avoid killing coin-multiplied enemies too early.
- `orb slider` / `orb adjuster` – workshop orb distance control (Vault ▸ Harmony ▸ Workshop).
- `disso` / `dissonant run` – v28 Dissonance: a run with one workshop tab disabled. `Echo` – Dissonant Echo labs.
- `training wheels` – said of Multiverse Nexus: a sync aid to be outgrown.

## 10. Tournament and progression terms

- Leagues: Copper, Silver, Gold, Platinum (`Plat`), Champion (`Champ`), Legend (players say "Legends"), Mythic (v29).
- `tier+` / `T17+` – league difficulty: tier-like scaling that grows faster than the campaign tier.
- `BC` – battle condition. `heat` – tournament battle-condition pressure that ramps with wave. `overheat` – conditions fixed by league (More Bosses) or starting late in a run.
- `Skip Decay`, `Skip Reduction – Multiply / Subtract` – conditions that cut ELS.
- `death save` / `shield` – anything that prevents a killing blow: Death Defy, Energy Shield, Second Wind, Smart Demon Mode, Smart Nuke.
- `Wave Speed Up` – v29 built-in unlimited Intro Sprint in tournaments.
- `fleet` – Saboteur, Commander, Overcharge. `elite` – Vampire, Ray, Scatter. `protector`, `ranged`, `tank`, `fast`, `basic`, `boss`.
- `promo` / `demo` – promotion (top 4) / demotion (ranks 25–30 from Platinum up).
- `bracket` – the 30 players you are ranked against.
- `sandbagging` – placing low on purpose.
- `milestone` – per-tier wave rewards and unlocks. `T16 W100` style = tier and wave.
- `lab slot`, `gem rush` – research slot; finishing a lab with gems.
