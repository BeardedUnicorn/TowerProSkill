# Modules and cards: mechanics and current meta

Verified against game version: v29.2.1 — 2026-11-20

Main sources
- SDK: `compartments/modules.ts`, `cards.ts`, `masteries.ts`; `src/data/modules` (templates, substats, costs, banner rules); patch notes v28.3, v29.0, v29.1.
- Fandom wiki "Epic Module Unique Effect", "Modules", "Guardian", "Gem Guide" (read 2026-11-18/20).
- Community guides: Evan, "Small guide for new Legend tournament players (v28)"; DrAudacious, "Glass Cannon without Chrono Field" (updated Jan 2026); wiki Gem Guide. All pre-v29, so their module advice predates slot levels and the four v29 modules.

Tags: `[mechanic]` game rule · `[consensus]` community view · `[unverified]` unconfirmed or disputed.
Stages: New (no/1 UW) · Early (2–4 UWs) · Mid (5–7 UWs, syncing) · Late (all UWs, legendary+ modules) · Endgame (mythic/ancestral, UW+, Legend/Mythic).

## Contents
1. Decision rules at a glance
2. Module mechanics (slots, rarity, v29 slot levels, currencies)
3. Unique effects and what each module is for
4. Substats: what to chase, rerolls, locks, bans
5. Merging and shattering
6. Pulls, banners and pity
7. Assist modules and Primary Module Bonus labs
8. Cards: slots, presets, levels
9. Card masteries
10. Tools to use instead of quoting tables

---

## 1. Decision rules at a glance

| Stage | Modules | Cards |
|---|---|---|
| New | Do not spend gems on modules. Equip whatever drops; level slots as shards allow. | Gems go to lab slots and the first card slots (section 8). |
| Early | After lab slot 5: pull until you own one natural epic per slot. Use any epic; do not chase a named one. No serious rerolling. | Fill econ cards first; buy a slot only when a card is waiting for it. |
| Mid | Pull steadily so no slot sits at its rarity cap. Merge towards Legendary. Light rerolls on modules you will keep. | Push all commons, then rares, to 7★; build farm and tournament presets. |
| Late | Target specific epics for your build; Legendary+ → Mythic. Start bans, lock good substats. Plan the first assist. | 30 maxed cards + T16 W100 opens masteries; first mastery per section 9. |
| Endgame | Ancestral and stars on build-defining modules; assist slots and efficiency; banner timing matters. | Masteries by ROI; Vault card slots (up to 28). |

Why this order: module power is gated twice, by rarity (which needs duplicate epics, so many pulls) and by shards. Early gems buy more from labs and card slots than from a 2.5% epic roll. `[consensus]`

## 2. Module mechanics

**Slots** `[mechanic]` Cannon (main effect: tower damage), Armor (health), Generator (coin bonus), Core (UW damage). One primary module per slot, plus one assist per slot late (section 7).

**Rarity and level cap** `[mechanic]`

| Rarity | Cap | Rarity | Cap |
|---|---|---|---|
| Common | 20 | Mythic | 140 |
| Rare | 30 | Mythic+ | 160 |
| Rare+ | 40 | Ancestral | 200 |
| Epic | 60 | Ancestral 1★–5★ | 220 / 240 / 260 / 280 / 300 |
| Epic+ | 80 | | |
| Legendary | 100 | | |
| Legendary+ | 120 | | |

**v29: levels live on the slot** `[mechanic]`
- You level the slot (up to 300). The equipped module uses the slot level up to its own rarity cap. The slot number shows orange when it exceeds the equipped module's cap.
- Swapping modules costs nothing and loses nothing. Substats and rarity stay with the module.
- Consequence: a rarer module is an immediate gain if the slot is already above the old cap ("Level Capped by Rarity"), and zero gain otherwise until you buy levels.
- Pre-v29 advice about "which module keeps the levels" is void.

**What each axis improves** `[mechanic]`
- Level → main effect only. Substats do not scale with level; the unique scales with rarity.
- Rarity (merging) → level cap, number of substat slots usable, best substat rarity rollable, unique strength.
- Substat slots open at slot level **41, 101, 141, 161, 201, 241** (2 at start, 8 maximum).
- Level cost depends only on level, never on rarity. It takes coins **and** module shards.

**Currencies** `[mechanic]`
- Coins + **module shards** for levels. Module shards are four separate pools (one per slot type).
- **Reroll shards** for substats: one shared pool. Bosses drop them (15% chance, amount by tier); fleets drop reroll shards 80% / module shards 20% (fleets appear from Tier 14 or at very high waves).
- Module shard sources: bosses, fleets, shattering, daily missions (rate set by highest tier unlocked), events, event and guild shops.
- Gems for pulls. Stones for assists.
- Inventory cap 350 (v29.1).

## 3. Unique effects and what each module is for

Only a module **drawn** as Epic has a unique. A Rare merged up never gains one and stops at Legendary+. `[mechanic]`

Values are Epic / Legendary / Mythic / Ancestral, from the wiki table read 2026-11-18. `[mechanic]` Roles are `[consensus]` unless marked.

**Cannon**
| Module | Unique | Role |
|---|---|---|
| Astral Deliverance (AD) | Bounce range +3% of tower range; each bounce +20/40/60/80% damage | Push and tournament damage; default damage cannon before AS. |
| Amplifying Strike (AS) | Boss, elite or fleet kill: tower damage ×5 for 5/11/18/26 s (affects UW damage) | Best-in-slot for glass cannon, farm and tournament, where kills are frequent. |
| Being Annihilator (BA) | +5/7/10/14% super crit chance; a super crit guarantees the next 5 | Solid generic damage (reworked v28.3). |
| Death Penalty (DP) | 5/8/11/15% of enemies marked at spawn die to the first hit | Helps weak-damage accounts and fleets; avoided in scaled-damage farming because it kills enemies before coin multipliers apply. |
| Havoc Bringer (HB) | 10/13/15/20% chance Rend Armor jumps to max | Boss damage; useless until Rend Armor is unlocked. |
| Shrink Ray (SR) | 1% chance on hit to cut enemy mass 10/20/30/40% | Niche (knockback builds). |
| Gilded Sniper (GS, v29) | On enemy death, 10/20/30/40% chance all active coin bonuses apply even out of range | Economy cannon. Ranking `[unverified]`: no tested guide at the pin. |

**Armor**
| Module | Unique | Role |
|---|---|---|
| Wormhole Redirector (WR) | Health regen can heal up to 25/50/75/100% of package max recovery | Health/eHP builds; the New–Mid farming armor. |
| Anti-Cube Portal (ACP) | Enemies take ×10/15/20/25 damage for 7 s after a shockwave | Damage amplifier for pushing and tournaments; works at low rarity. |
| Negative Mass Projector (NMP) | Orb hits stack −1/1.5/2/2.5% enemy damage and speed, max 50% | Orb builds (blender, devo). |
| Space Displacer (SD) | 15/20/25/30% of land mines spawn as Inner Land Mines (20 max) | Enables glass cannon (ILM stuns). Needs ILM labs to shine. |
| Sharp Fortitude (SF) | Wall health and regen ×1.25/1.5/2/2.5; stacking wall-thorn damage | Wall builds. |
| Orbital Augment (OA) | 2/4/6/8 orbiting Electrons dealing % health damage | Niche. Damage wording differs between SDK and wiki `[unverified]`. |
| Sentry Protocol (SP, v29) | Orb speed zero; orbs fire 1/2/3/4 mini orbs | New; noted for defense-dissonance runs. Ranking `[unverified]`. |

**Generator**
| Module | Unique | Role |
|---|---|---|
| Galaxy Compressor (GComp) | Each recovery package cuts all UW cooldowns by 10/13/17/20 s (wiki: except Poison Swamp) | Early–Mid farming staple: cheap route to perma BH/GT. Later a fallback to sync. |
| Black Hole Digestor (BHD) | +3/5/7/10% coins/kill per free upgrade gained this wave | Best coin generator once GT/BH/DW are synced (Late+). |
| Singularity Harness (SH) | Bot range +5/8/11/15 m; Flame Bot hits take double damage | Alternative for bot-heavy farming. |
| Pulsar Harvester (PH) | 1/1.5/2/2.5% per projectile hit to lower enemy health and attack level by 1 | Push/tournament alternative. Diminishing after 100 reductions. |
| Project Funding (PF) | Tower damage × 12.5/25/50/100% of the digits of current cash | Best tournament/push generator; worth using at Epic. |
| Restorative Bonus (RB) | Packages give +50% attack speed for 15/20/25/30 s | Tournament assist generator. |
| Infinity Threshold (IT, v29) | Free upgrades to Damage, Health, Regen may exceed the in-run limit by 1,000–4,000 levels | Long runs. Ranking `[unverified]`. |

**Core** (each needs its UW to do anything)
| Module | Unique | Role |
|---|---|---|
| Multiverse Nexus (MVN) | GT, BH, DW fire together; cooldown = average +20 / +10 / +1 / −10 s | Farm sync aid. A cost below Mythic (see `footguns.md`). |
| Dimension Core (DC) | CL 60% to hit the first target; shock chance and multiplier doubled; stacks to 5/10/15/20 | Best damage core for tournaments and pushing. Needs CL. |
| Om Chip (OC) | Spotlight tracks the boss; nearby enemies take ×2/4/7/15 | Tournament assist core; primary before SL4. Needs SL. |
| Harmony Conductor (HC) | Poisoned enemies miss 15/20/25/30% of attacks (bosses half) | Survival; after SL4 and perma PS. Needs PS. |
| Primordial Collapse (PC) | +1 Black Hole; enemies inside deal 60/65/75/90% less damage | Survival for health and wall builds. Needs BH. |
| Magnetic Hook (MH) | 1/2/3/4 ILMs fired at bosses and fleets entering range (25% of elites) | ILM builds. Needs ILM. |
| Tactical Barrage (TB, v29) | Doubles SM radius and amplifier lab bonuses; homing missile every 14/10/6/2 s | Smart Missile builds. Needs SM. |

**Preset summary** `[consensus, from v28 Legend and GC guides]`
- Farming, health build (New–Mid): any cannon · WR · GComp (BHD later) · MVN or PC.
- Farming, glass cannon (Late+): AS · SD · BHD · MVN (DC assist).
- Tournament / push: AS or AD · ACP or SD · PF (RB assist) · DC (OC assist).
- A core whose UW the player does not own is a stat stick. Check the UW list in the export first.

## 4. Substats

**Mechanics** `[mechanic]`
- Substat rarities: Common, Rare, Epic, Legendary, Mythic, Ancestral. A roll's rarity is capped by the module's rarity, so an Epic module cannot roll Legendary substats.
- Pool sizes differ: Core 27, Cannon 17, Armor 17, Generator 13. Core rerolls are the least predictable.
- Reroll cost in reroll shards by number of locked substats: **40 / 160 / 500 / 1,000 / 1,600 / 2,250 / 3,000**. Shards are never refunded.
- Effect Bans labs (one per slot type) remove a substat from the pool entirely; each extra ban is worth more than the last.
- Vault ▸ Harmony ▸ Modules: Module Reroll Discount, 2.5% per level to 20%.
- Quantity substats floor. On an assist, +4 DW quantity needs 34% substat efficiency to give +1; CL quantity needs 25%.
- Value tables: look up with `oracle_get` rather than quoting.

**When to reroll** `[consensus]`
- Rule: reroll only modules you will keep, and only once they are at the rarity where the substats you want can roll at a worthwhile tier (Legendary at least, Mythic/Ancestral for end builds).
- Lock as you go. Rolling with 0–2 locks is cheap; the cost curve punishes locking mediocre rolls early.
- Do not spend shards replacing an acceptable substat with a slightly better one (the Legend guide's example: leave Crit Chance alone).
- Bans before big reroll sessions; ban the stats that are dead for every build you run.

**What to chase**
| Slot | Farm | Tournament / push |
|---|---|---|
| Cannon | Attack Speed, Crit Factor, Super Crit Chance and Mult. Glass cannon adds Bounce Shot Chance and Multishot Targets. | Same damage set; swap Crit Chance for Damage / Meter once SL+ is in play. Crit Chance is the weakest keeper. |
| Armor | Health build: Defense %, Health Regen, Defense Absolute, Death Defy `[consensus, older guidance]`. Glass cannon: Death Defy, Wall Rebuild, Land Mine Chance, Knockback Force. | Death Defy, Wall Rebuild, Knockback Force; Shockwave Frequency and Size with ACP; Land Mine Chance with SD. |
| Generator | Coins / Kill Bonus and Enemy Health Level Skip always. Free-upgrade subs with BHD. Package Chance with GComp or the RPC mastery. | Cash Bonus (feeds PF), EHLS, Free Utility Upgrade, Package Chance for RB. Coins/Kill is dead weight. |
| Core | GT Bonus, GT Duration, BH and DW subs that serve the sync; DW Quantity; SL Angle. | CL Chance, CL Quantity, CL Damage, SL Bonus, SL Angle, ILM Quantity; CF Speed Reduction towards the 90% cap. |

Warning on core cooldown substats `[mechanic → footgun]`: GT, BH and DW cooldown substats change real cooldowns. One −12 s GT roll can break a natural sync or fix one. Check the resulting cooldowns before locking. Detail in `footguns.md`.

Caps a substat cannot pass `[mechanic]`: Defense % 98, CF slow 90%, wall rebuild 150 s, shockwave frequency 7 s, Death Defy 40%, ILM cooldown 37 s. A substat that pushes past a cap is wasted.

## 5. Merging and shattering

`[mechanic]`
- Commons cannot be merged. Rares stop at Legendary+ (cap 120). Only natural epics reach Ancestral and stars.
- **The first module selected keeps its substats. Everything else in the merge is destroyed**, substats included. Start the merge from the well-rolled copy.
- Some steps need the **same named module** (Epic → Epic+, Legendary → Legendary+, Mythic+ → Ancestral, every star); others accept any epic of the same slot type.
- A natural epic needs 18 copies of itself to reach Ancestral 5★, plus 20 other natural epics of its type. Stars add +20 level cap each.
- Merging raises the cap, not the slot level.
- Shatter returns 5 module shards per common and 10 per rare; a merged module returns the combined value. Natural epics can only be shattered once a 5★ Ancestral of that type exists.
- An "Unmerge Module" lab exists; its exact refund behaviour is `[unverified]`. Do not present merges as reversible.

`[consensus]`
- Keep every natural epic. Duplicates are star material; off-meta epics are type fodder.
- Auto-shatter commons; shatter rares once your epics no longer need rare fodder (Vault adds auto-shatter for rares).
- Do not merge two different well-rolled copies of the same module together unless you accept losing one set of substats.

## 6. Pulls, banners and pity

`[mechanic]`
- 20 gems per pull. Rarity roll: Common 68.5%, Rare 29%, Epic 2.5%. Epic pity at 150 pulls (so at most 3,000 gems per epic, about 39 pulls or roughly 780 gems on average). Rare pity 10. One pity counter across all banners.
- Within Epic, each module has a Chance share. A featured banner fixes the featured share (50% for a single new module; 12.5% each when four were featured together) and splits the rest evenly.
- A non-featured epic you own at Ancestral 5★ keeps 0.25× its share; the freed share goes to your unmaxed non-featured epics. A lone unmaxed module is capped at 50%. The in-game drop-rate panel shows your real odds.
- The four v29 modules: featured Aug 31 – Nov 9, 2026. Whether each is now in the standard pool is `[unverified]` (patch note says each joins after its banner; the SDK owner reports they join only once all four are out). Check the panel.
- Planned: type-exclusive banners in January 2027 (developer statement, Nov 9).

**How to spend** `[consensus]`
- New/Early: no banner saving. Pull only after lab slot 5, until one epic per slot.
- Mid: pull continuously at a rate that keeps slots off their rarity caps. A featured banner for a module your build needs is a good time to pull harder, because for an account missing most epics a 50% featured share beats a 1-in-28 standard share by a wide margin.
- Late/Endgame with most old epics at 5★: the opposite holds. SDK model: chasing each new module on its own 50% banner costs about 51% more gems than waiting for the standard pool, where the 5★ adjustment concentrates odds on the new ones; break-even is a featured share near 76%. `[mechanic-derived estimate]`
- Type banners favour players who need one slot. If one slot is far behind, holding gems for its type banner is reasonable once the date is announced.
- Always keep enough gems for the fortnightly "buy cards" event mission and card slots that have a card waiting.
- For a real account's numbers use `calc_run` with `mechanics.estimateModuleBannerCost`, `mechanics.moduleBannerEpicWeights`, `mechanics.modulePullsPerEpic` and `mechanics.moduleCopiesSpentToReach` (find them with `calc_list` filter "banner").

## 7. Assist modules and Primary Module Bonus labs

`[mechanic]`
- Assist slot milestone: Tier 19 Wave 40. One assist per slot type; it cannot be the same named module as the primary.
- Stones per slot type: slot unlock 1,000 (arrives at Epic unique strength); unique ladder Legendary 1,000 / Mythic 1,200 / Ancestral 1,400; main-effect efficiency and substat efficiency are two separate ladders, 15 stones for the first point and +3 per point after.
- Efficiency is per slot type, not per module. Multiplier efficiency reaches 130% with the Assist Module Bonus labs (v28.3); substat efficiency is extended by the Assist Module Substats labs.
- The assist's own level uses the same per-type shard pool as the primary.
- Since v27.1 all assist multipliers are multiplicative.
- Assists never bypass hard caps.

`[consensus, Evan's Legend guide]`
- Unlock order: Core (Om Chip beside Dimension Core) → Armor (ACP + SD) → Generator (RB beside PF) → Cannon (AD beside AS).
- Buy about 10% main efficiency on a slot (≈243 stones) before opening the next; aim near 25% later. Skip quantity substats on assists until the efficiency breakpoint.
- Assists compete with UW stats, UW+ and masteries for stones. Cost any plan with `calc_run`.

**Primary Module Bonus labs** `[mechanic]` Four labs, 30 levels, +1% per level to the primary module's main effect; they do not affect the assist. SDK records the unlock at Tier 23 Wave 500, so they are Endgame content.

## 8. Cards

**Mechanics** `[mechanic]`
- 20 gems per card. 32 cards: 12 Common, 9 Rare, 11 Epic. Draw odds 80 / 17 / 3% by rarity; once all commons are maxed the weight shifts to rares.
- Levels are stars 1–7. 7★ takes 80 copies (1,600 gems at list price). Rarity sets draw odds only, not power: common Damage beats several epics.
- A card does nothing unless slotted. 22 slots are bought with gems (58,400 total); the Vault adds up to 6 more (28).
- Milestone-gated cards: Recovery Package Chance (T2 W750), Cells (T4 W40), Land Mine Stun (T7 W250), Nuke (T11 W10), Ultimate Crit (T14 W50), Area of Effect (T20 W80).
- Cards lock while a boss or fleet is alive; a preset that differs in a locked card cannot be selected mid-run.
- Energy Shield's value falls with level because it is a recharge time (lower is better).

**Gem priority, New → Early** `[consensus, wiki Gem Guide]`
1. Lab slot 2.
2. Three card slots; pull until Attack Speed, Enemy Balance, Coins.
3. Lab slot 3.
4. Five slots; add Health and Cash.
5. Lab slot 4.
6. Two of Critical Coin, Wave Skip, Extra Orb, with slots for them.
7. Lab slot 5.
8. One epic module per slot type.
9. Then split gems between cards (always enough for the buy-cards event mission), modules, event-shop relics, and, later, lab rushing.

Slot rule: buy a slot only when a card that would help the current build is waiting for it. `[consensus]`

**Presets** `[consensus]`
- Farm: Coins, Critical Coin, Enemy Balance, Wave Accelerator, Wave Skip, Cash, Free Upgrades, Cells (v29), Extra Orb, plus the survival or damage cards the build needs. Intro Sprint once its mastery is owned.
- Push / milestone: drop economy cards for Damage, Attack Speed, Critical Chance, Range, Slow Aura, Plasma Cannon, Energy Net, Super Tower, Ultimate Crit, Berserker, Demon Mode, Energy Shield, Second Wind, Death Ray, Nuke, Land Mine Stun.
- Tournament: as push; see `meta-tournaments.md` for swaps by league.
- Health builds keep Health, Health Regen, Extra Defense, Fortress as needed; glass cannon drops them.

## 9. Card masteries

`[mechanic]`
- Unlock condition: 30 cards at 7★ and the Tier 16 Wave 100 milestone. Each mastery is then bought with stones (500–1,250; all 32 cost 28,500).
- Level 0 comes with the purchase and already gives a bonus. Levels 1–9 come from mastery labs, identical for every mastery: 20.8 days at level 1 rising to 104.2 days at level 9, about 562 days for 1 → 9 before lab speed. They use ordinary lab slots.
- The card must be equipped for its mastery to work. A mastery bought mid-run does not apply to that run (v29.1).
- Only six scale the card's own number (Damage, Attack Speed, Health, Health Regen, Coins, Extra Defense). The rest add a new effect, for example: Recovery Package → packages can drop common modules; Cash → elites drop reroll shards; Wave Skip → chance to skip two waves; Super Tower → 35% of its bonus applies to UWs; Berserker (Viking Funeral) → damage cap ×500 after a death save; Enemy Balance → chance of double elites; Cells → ×1.05–1.32 cells.
- Stone costs: 500 Cash, Free Upgrades · 750 Damage, Attack Speed, Health, Health Regen, Range, Critical Chance, Fortress, Extra Orb, Death Ray, Energy Net, Berserker, Ultimate Crit, Nuke · 1,000 Slow Aura, Enemy Balance, Extra Defense, Critical Coin, Wave Skip, Land Mine Stun, Recovery Package, Super Tower, Second Wind, Demon Mode, Energy Shield, Wave Accelerator, Area of Effect, Cells · 1,250 Coins, Plasma Cannon, Intro Sprint.

**Which first** `[consensus, v28 guides]`
- First for most accounts: **Recovery Package Chance** (module shards from common module drops).
- Economy next: Wave Accelerator and Intro Sprint (the GC guide calls T14+ farming without them hard to justify), then Coins, Extra Orb (top econ mastery once the orb adjuster is owned), Wave Skip, Critical Coin. Cells is new and unranked `[unverified]`.
- Tournament damage line: Super Tower → Damage → Ultimate Crit → Energy Net → Berserker; then Critical Chance, Demon Mode (only with the Vault's Demon Mode automation), Attack Speed, Range (after SL+).
- Decide by the account's bottleneck: coins limiting labs → economy masteries; stones limited by tournament rank → damage masteries.
- Mastery labs are long. Unlocking five masteries at level 0 usually beats pushing one to level 5 early, because level 0 is the largest single step. `[consensus]`

## 10. Tools instead of tables

- Module main effect at a rarity and level: `calc_run` → `module.stat`; caps: `module.levelCapForRarity`.
- Assist contribution: `assist.substatCap`.
- Stone prices for UW stats when weighing assists and masteries against them: `uw.stoneCost`, `uw.statValue`.
- Any single entity (a module, a mastery, a lab): `oracle_get`; names: `oracle_search`.
- What the account actually owns and has equipped: `get_export`.
- Acronyms: `oracle_expand` / `define_term`.
