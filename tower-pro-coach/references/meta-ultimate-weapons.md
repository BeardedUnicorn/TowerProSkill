# Meta: Ultimate Weapons (UWs), stones, sync, perma targets, UW+

Verified against game version: v29.2.3 — 2026-11-20, updated 2026-11-25

Main sources
- SDK knowledge base (`TheTowerSDK`: compartments ultimate-weapons, uw-plus, build-targets, footguns/permanence, perks, jargon; shipped stone chart `uwStoneChartData`; `LAB_CATALOG`; official patch notes to 2026-11-19). Source of every `[mechanic]` and of all stone totals below.
- tower-hub.com fan wiki (tier-specific guide verified 2026-07-29; UW pages and UW tier list verified 2026-11-01, v29.0.5–v29.1.2; the tier list is one Legend farming account).
- towerstats.org guides (Nov 2026) for common-mistake framing.
- "Guide to first 5 UWs" Google Doc (game v25.7.2) and "Tower Build Guide" (v23.4): `[older]`.
- Not reachable: Fandom wiki, Reddit, Discord. No Reddit "consensus" thread was read first-hand.

Tag legend: `[mechanic]` verifiable rule; `[consensus]` community strategy; `[unverified]` unconfirmed or disputed; `[older]` pre-2026. Stage keys S0–S5 are defined in `account-assessment.md`.

The SDK oracle is explicit: UW pick order, whether a sync target is worth chasing, and every "perma"/quantity target are opinion. Only permanence, stat ranges and stone prices are mechanics. Keep that split when advising.

Stone prices: for a range of levels use `calc_run uw.stoneCostBetween {args: {weapon, stat, fromLevel, toLevel}}` for the total (SDK 2.0.0; `null` for a wrong name or a level the ladder lacks), or `form_calc uw.stones {weapon, stat, currentLevel, targetLevel}` — one call returns each level's price and the total, plus `statsForWeapon` with the exact stat strings. `calc_run` `uw.stoneCost` returns the price of the **single level** passed as `level` (the level being bought); all three agree (Golden Tower Cooldown 0→3: 10 + 28 + 46 = 84). Also `uw.statValue` and `uw.maxLevel`. Unlock prices are positional (`uw.stoneCost` returns `null` at level 0): read the account's next weapon and next UW+ unlock price from `next_unlocks` (`ultimateWeapon.stones`, `ultimateWeaponPlus.stones`), which shows them beside the stone balance; `calc_run` `uw.nextUnlockStoneCost` and `uw.nextPlusUnlockStoneCost` give the same numbers. Several unlocks ahead: `uw.unlockStonesBetween {ownedFrom, ownedTo}` and `uw.plusUnlockStonesBetween` (all nine weapons come to 9,705 stones, all nine pluses to 14,650).

Exact `weapon` / `stat` strings the calculators accept (the fourth stat is the UW+ ability). A wrong name returns `null` with no error, the same as an unpriced level — if you get `null`, check the name first:

| weapon | stat |
|---|---|
| Golden Tower | Multiplier, Duration, Cooldown, Golden Combo |
| Black Hole | Size, Duration, Cooldown, Consume |
| Death Wave | Damage, Quantity, Cooldown, Kill Wall |
| Spotlight | Multiplier, Angle, Quantity, Light Range |
| Chrono Field | Duration, Speed, Cooldown, Chrono Loop |
| Chain Lightning | Damage, Quantity, Chance, Smite |
| Smart Missiles | Damage, Quantity, Cooldown, Cover Fire |
| Inner Land Mines | Damage, Quantity, Cooldown, Charged Mines |
| Poison Swamp | Damage, Duration, Cooldown, Death Creep |

("Bonus" in this file's prose for Golden Tower and Spotlight is the `Multiplier` stat.)
 Totals quoted here are from the shipped chart and are for orientation.

## Contents
1. Rules that never change (permanence, pricing, the stone pool)
2. The nine UWs: what each is for and its stat ranges
3. Unlock order: consensus and reasoning
4. Stone spending priorities by stage
5. Cooldown sync (GT / BH / DW, bots, MVN, Galaxy Compressor)
6. Perma targets (PBH, PBHGT, PCF, PPS)
7. Quantity and threshold breakpoints (DW, SL, CL, SM, ILM, CF slow)
8. Trap stats and common mistakes
9. UW+ (enhancements)
10. How labs, perks, modules and cards touch UWs
11. What v27–v29 changed

---

## 1. Rules that never change

- `[mechanic]` UW picks and UW stat upgrades (including cooldown) are permanent. There is no respec, refund or reset for stones spent on UWs. Workshop respec does not touch them. Every stone recommendation must be treated as irreversible and stated that way.
- `[mechanic]` Buying a UW offers three random choices from those not owned. Price is positional (by how many you own): 5, 50, 150, 300, 800, 1,250, 1,750, 2,400, 3,000 stones; 9,705 for all nine. `[mechanic]` v29.2 added a preview and a cancel option to the selection flow. `[consensus]` Backing out keeps the same three options, so cancelling does not reroll.
- `[mechanic]` Each UW has exactly three stone stats plus a separate UW+ ability. Maxing every base stat on all nine costs an order of magnitude more than unlocking them; per-weapon totals differ by more than 2x.
- `[mechanic]` Lower cooldown is not always better: sync is a ratio, the purchase is permanent, and a cooldown bought now can raise the price of a sync you want later.
- `[mechanic]` One stone pool pays for: UW unlocks, UW stats, UW+ unlocks and levels, Bot+ unlocks (1,250 each, once every bot is owned), Synchronicity, assist-module rarity and efficiency. A stone plan must say what it is not buying.
- `[mechanic]` Stone income: tournaments (main source), daily-mission weekly track (45 per full week), milestones. v29 reduced Legend stones per rank. Income is calendar-bound, so the cost of a wrong purchase is weeks.
- `[mechanic]` UWs fire automatically at cooldown zero. Toggling a UW off and on resets its cooldown; 40 toggles per run.

## 2. The nine UWs

Stat ranges are min to max from stones alone `[mechanic]`; stone totals in parentheses are the full ladder for that stat.

| UW | Role | Stat 1 | Stat 2 | Stat 3 |
|---|---|---|---|---|
| Golden Tower (GT) | coins and cash multiplier while active; no damage | Bonus x5 to x21 (8,434) | Duration 15s to 53s (14,052) | Cooldown 300s to 100s (4,700) |
| Black Hole (BH) | holds enemies; coin bonus via lab on kills inside | Size 30m to 70m (2,291) | Duration 15s to 38s (5,392) | Cooldown 200s to 50s (2,040) |
| Death Wave (DW) | tags enemies (coin and cell bonus labs), health bonus, damage | Damage (17,591) | Quantity 1 to 5 (2,950) | Cooldown 300s to 50s (8,850) |
| Spotlight (SL) | damage bonus and coin bonus (lab) in beams; no cooldown stat | Bonus x8 to x50 (20,071) | Angle 30 to 90 degrees (29,690) | Quantity 1 to 4 (3,725) |
| Chrono Field (CF) | slow; damage reduction via lab; no damage | Duration 5s to 40s (5,530) | Speed Reduction 20% to 75% (2,910) | Cooldown 180s to 60s (1,506) |
| Chain Lightning (CL) | sustained damage; no cooldown stat | Damage (15,710) | Quantity 1 to 5 (655) | Chance 5% to 27.5% (2,010) |
| Smart Missiles (SM) | burst damage | Damage (29,661) | Quantity 5 to 20 (6,966) | Cooldown 180s to 20s (2,550) |
| Poison Swamp (PS) | damage over time, stun via labs | Damage (28,716) | Duration 30s to 100s (3,500) | Cooldown 125s to 50s (2,010) |
| Inner Land Mines (ILM) | close-range damage, stun via lab | Damage (20,817) | Quantity 3 to 6 (425) | Cooldown 200s to 50s (1,800) |

- `[mechanic]` GT and CF deal no damage; never run them through a damage model. UW damage = UW multiplier x core module multiplier x tower damage x crit terms, so tower Damage and the Core module scale every damage UW.
- `[mechanic]` Naming: the catalog calls GT/SL "Bonus" Multiplier and CF "Speed Reduction" Speed.

## 3. Unlock order

Decision rule: get the three economy UWs (GT, BH, DW) first, in whatever order the offers allow, because they multiply coins together and coins buy everything else. After that, pick by what limits the account: Spotlight for more coins, Chrono Field for survival/control, Chain Lightning for damage and tournaments.

- First pick `[consensus]`: take GT if offered; otherwise BH or DW; Spotlight is acceptable but weak early. About 88% of first offers contain at least one of GT/DW/BH/SL (tower-hub). Guides say an unlucky first pick is worth considering a restart on a brand-new account; that is opinion, and only relevant in the first days.
- Farmer order `[consensus]` (tower-hub tier list, Nov 2026): GT, BH, DW, SL, CF, CL, ILM, PS, SM. With strong permanent lab speed, CL fifth and CF sixth or seventh.
- `[older]` order (v25): GT, BH, DW, SL, CL, CF, SM, PS/ILM; CL before SL if you own Dimension Core.
- Tournament-first order `[consensus]` (towerstats UW tier list, Nov 2026): GT, DW, BH, CF, CL, SL. It moves DW ahead of BH and brings CF and CL ahead of SL.
- Last two `[unverified]`: towerstats puts SM before PS; tower-hub puts PS before SM. Neither matters until seven are owned.
- `[unverified]` A tenth UW, "The Dome" (defensive), was announced on 2026-11-23 for the end-of-year update with no price or numbers. See `version.md` § upcoming before advising a large unlock.
- Disagreements `[unverified]`: second pick BH vs DW (tower-hub's tier guide ranks DW above BH for the second slot, most others BH first); SM ranked sixth by a generic 2026 blog and last by tower-hub. Poison Swamp, ILM and SM are consistently the last three for farmers.
- Reasoning to adapt:
  - GT multiplies coins and cash for every kill in its window; nothing else does both. BH's coin lab reaches x11 on kills inside it and BH also controls enemies, which helps survival. DW's coin lab reaches x2.5 and its cell lab x3, and its health bonus helps eHP builds.
  - `[mechanic]` Spotlight Coin Bonus lab unlocks only at T7 W80 (x3 at max), so SL does nothing for coins before that milestone.
  - CF is the main defensive UW and a tournament staple; CL is the strongest sustained damage UW and scales with tournament play (Dimension Core). Tournament-focused accounts move CL and CF ahead of SL (order above).
- Offers are random, so the practical rule is: among the three shown, take the highest on the list above; if none of GT/BH/DW is shown while missing, take the best remaining rather than waiting (you cannot reroll).

## 4. Stone spending priorities by stage

Rule: unlock before upgrading until GT, BH and DW are owned; then buy sync; then duration/bonus on the coin UWs; damage UWs last. At every step compute the candidate costs with `uw.stoneCost` and compare against the next unlock price.

Stopping points per UW `[consensus]` (towerstats UW tier list, Nov 2026; one site's targets, price each with `uw.stoneCost` before quoting): GT Bonus to about x14.6, then Duration to 30s · BH Size to 50m, then Duration to 30s · DW to 3 effect waves · SL Bonus to about x29, then a second beam · CF Cooldown to 60s · CL Quantity to 5, then Chance to 27.5%. `[unverified]` The Spotlight order is disputed: older guides want three beams and angle before Bonus (S3 below). `[mechanic]` Settle the Angle part with `calc_run spotlight.coverage {args: {quantity, angleDegrees}}`: coverage is capped at 1, and once it is saturated further Angle levels add nothing.

### S0–S1 (0–2 UWs)
- `[consensus]` Save for unlocks. After the first UW a small spend (about 50–150 stones `[older]`) on GT Bonus/Duration or BH Size/Duration is fine while saving for the next unlock. Cheap early levels cost 5–40 stones each `[mechanic]`.
- Never buy cooldown levels yet (section 5).

### S2 (3–4 UWs, GT+BH+DW arriving)
- `[consensus]` If GT or BH is still missing, keep saving for unlocks (through the 6th if needed); if only DW is missing you can start upgrading.
- `[consensus]` With all three: establish a sync (section 5), raise BH Size until it covers the kill zone (about 38–50m for devo farms), GT Bonus and Duration early levels. `[older]` v25 "pre-sync" package: GT Bonus about x9, GT Duration about 27s, BH Size 40m for under 300 stones.
- Leave DW Quantity at 1 until DW is synced `[older]`.

### S3 (5–8 UWs)
- `[consensus]` Deepen the coin engine: GT Duration and Bonus, BH Duration (toward perma BH with the perk), sync tighter ratios, DW Quantity, first Spotlight investment once T7 W80 lab is running (3 beams and angle before bonus `[older]`).
- `[consensus]` Keep unlocking: remaining UWs are the gate to UW+ (all nine required).
- Chrono Field: cooldown and duration toward perma CF if tournaments or survival limit the account (section 6).

### S4 (all nine, starting UW+)
- `[consensus]` First UW+ is GT+ (Golden Combo) for a farming account; see section 9. Then finish perma BH, tight GT/BH sync, Spotlight angle/quantity, CF slow and perma CF.
- Sample allocation `[consensus, one account]` (tower-hub Legend farmer, about 53.5K stones): GT largest, then CF, BH, DW, SL, CL; ILM token; SM and PS zero. It shows the shape (coin UWs and CF first, three damage UWs untouched), not a target.

### S5 (endgame)
- `[consensus]` Remaining UW+ unlocks and levels, Spotlight to full coverage, damage UW stats that the tournament/fleet build uses, assist-module stone sinks. Here stones compete with Bot+ and assist efficiency; rank by the binding goal (coins vs tournament placement).

## 5. Cooldown sync

Rule: GT, BH and DW should fire together, because the coin factors multiply only on kills inside overlapping windows. Any integer ratio works (BH firing 1x, 2x or 3x per GT cycle). Pick the cheapest ratio that the account's next 6–12 months of stones can keep extending, and never buy a single cooldown level that breaks the ratio.

Cumulative stone cost to reach a cooldown `[mechanic]` (from the stone chart; each level is -10s):
- GT (300s base): 250s 230 · 200s 910 · 150s 2,040 · 120s 3,184 · 100s 4,700.
- BH (200s base): 150s 230 · 100s 910 · 50s 2,040.
- DW (300s base): 250s 200 · 200s 800 · 150s 1,800 · 100s 3,450 · 50s 8,850.

Common sync shapes (BH : GT : DW), total stones from untouched cooldowns `[mechanic]` arithmetic:
| Target | Stones | Note |
|---|---|---|
| 150 : 300 : 300 | 230 | BH twice per GT/DW cycle; cheapest sync |
| 100 : 300 : 300 | 910 | BH three times per cycle |
| 200 : 200 : 200 | 1,710 | natural 1:1:1, the classic "3:20" sync |
| 100 : 200 : 200 | 2,620 | |
| 50 : 300 : 300 | 2,040 | BH at floor |
| 50 : 200 : 200 | 3,750 | pairs with Golden Bot at 100s `[consensus]` |
| 100 : 100 : 100 | 9,060 | 1:1:1 at GT's floor |
| 50 : 100 : 50 | 15,590 | every cooldown at its floor (2:1 GT:BH) |

- `[mechanic]` Floors on stones: BH 50s, DW 50s, GT 100s. Four bots floor at 50s (ladder 75s plus the cooldown lab's -25s); Flame Bot floors at 5s. So the end state is a 2:1 relationship with Golden Bot able to match BH/DW.
- Which path `[unverified]` — real disagreement between eras and sites:
  - `[older]` v23–25 guides: 1:1:1 at 200s, "never touch BH cooldown", sync GT to BH first then DW; do not use multiples.
  - tower-hub (2026): start with 230 stones on BH for 150:300, then step down in matched pairs (140:280, 130:260...), "cooldowns are usually the more important investment".
  - towerstats (2026) lists "cutting BH to 150s before syncing GT" as a mistake because matching GT to a 150s BH costs 2,040 instead of 910.
  - Resolution for the coach: both are arithmetic. If the plan is 1:1:1, leave BH at 200 and spend 1,710. If the plan is an integer ratio, 230 stones gets a working sync immediately and every later step must lower GT and DW by twice what BH drops. State the chosen target, compute the full path, and check current cooldowns in the save before recommending any cooldown level; an account that already has off-ratio cooldowns needs the cheapest path to the nearest ratio, not the textbook one.
- Buying cooldown `[consensus]`: buy all levels needed for the next ratio at once (save up), not one at a time, so the account is never sitting off-sync.
- GT duration vs BH duration `[consensus]`: keep GT duration at least BH duration (older guides: BH + 12s to cover the BH duration perk) so GT is active for the whole BH hold.
- Multiverse Nexus (MVN, core module) `[consensus]`: forces GT, BH and DW to share one cooldown (their average, plus an offset that improves with rarity: positive seconds at Epic/Legendary, about zero at Mythic, negative at Ancestral `[older]` figures +20/+10/+1/-10s; re-derive from module data before quoting). It is a way to be synced without buying cooldowns, called "training wheels" by the wiki; tower-hub estimates it becomes a small loss at the very end game. It occupies the core slot, which damage builds want for Dimension Core. tower-hub's footguns page (29 Jul 2026) treats it as a stopgap: it adds seconds to the averaged cooldown below Mythic, so the goal remains a natural sync of 3:20 (200s) or better bought with stones.
- Galaxy Compressor (generator module) `[consensus]`: each recovery package collected cuts UW cooldowns (10–20s by rarity; not Poison Swamp). It makes cooldowns variable, which is how GT and BH reach permanent uptime late; `[mechanic]` v28.3.x made DW effect waves behave consistently with it.
- Bots `[mechanic]`: bot cooldown labs are permanent. Decide Golden Bot's target cooldown from the UW cycle (for example 100s or 120s against a 200s or 240s cycle) before researching.
- Cost of being unsynced `[consensus]`: tower-hub estimates most coin income depends on GT and BH being active together; treat exact percentages as illustrative. The battle-report check is in `account-assessment.md`.

### When Black Hole is not owned yet (GT + DW only)

- Judgement call, state both sides. For matching Death Wave's cooldown down to Golden Tower's when DW sits
  above GT: cooldowns only ever go down and the end-state sync has DW well below its starting value, so
  those DW levels are not wasted in the long run, and they are cheap. Against: every stone spent now
  delays the Black Hole unlock, and the coin gain from a GT/DW match alone cannot be quantified (next
  point). `[consensus]` leans to unlocking first when the unlock is close and taking the cheap match when
  the unlock is months away — give the player the cost in weeks of delay and let them choose.
- `[consensus]` Hold Golden Tower cooldown levels until Black Hole is owned, so the three can be brought to
  a common ratio together rather than re-buying around a number chosen for two.
- `plan_effective_path` does not value a UW the account does not own, so an unlock-versus-upgrade decision
  has to be argued from these references; say that it is reasoning, not calculator output.
- `[unverified]` How long a Death Wave tag lasts and whether its coin bonus needs the kill inside the GT
  window is not in the SDK oracle. Do not quote a coin gain for a GT/DW match; say the direction is right
  and the size is unknown.
- Stone income for "how many weeks until the next unlock" comes from the reward table in
  `meta-tournaments.md` § 3 (complete, from `TOURNAMENT_REWARD_ROWS`) and the weekly mission track
  (`DAILY_MISSION_WEEKLY_REWARDS`), plus the account's own league history (`readTournamentsFromSaveRoot`) —
  cross-check against lifetime stones earned ÷ account age, and give the range.

## 6. Perma targets

"Perma" is community shorthand for duration at least equal to cooldown `[mechanic]` relationship, `[consensus]` goal. It is defined only for UWs that have both stats: BH, GT, CF, PS. P + initials composes (PBHGT = both permanently up). `[mechanic]` Since v29.1 a UW with full uptime (GT, CF, BH, PS) fires immediately at run start.

- PBH (perma Black Hole) `[mechanic]` arithmetic: stones max duration 38s; the Black Hole Duration perk adds 12s; cooldown floor is 50s. So 38 + 12 = 50: perma BH needs max BH Duration (5,392), max BH Cooldown (2,040) and the perk each run, or else duration substats / Galaxy Compressor / MVN to close the gap without the perk. There is no BH duration lab. Size matters too: a permanent hole only helps if it covers where enemies die.
- Perma GT / PBHGT `[mechanic]` arithmetic: stones max duration 53s + Golden Tower Duration lab 20s = 73s against a 100s cooldown floor. GT cannot be permanent from stones and labs alone; the remaining gap is closed by cooldown reduction (Galaxy Compressor packages, GT cooldown substat, Ancestral MVN) or duration substats `[consensus]`. `[unverified]` tower-hub pages disagree with each other on the endgame cycle (73s every 100s vs an 88s cycle with 80s duration). Treat PBHGT as a late (S4–S5) module-dependent target.
- PCF (perma Chrono Field) `[mechanic]` arithmetic: stones duration up to 40s + Chrono Field Duration lab up to 30s (+5s perk) against a 60s cooldown floor. Reachable from stones and lab alone, for example cooldown 60s (1,506 stones) with stone duration 30s and a maxed lab. `[consensus]` CF does not stack on re-trigger. PCF75 / PCF90 add the slow threshold (section 7). `[consensus]` Legend "UW Durations" battle condition shortens durations, so tournament PCF needs margin.
- PPS (perma Poison Swamp) `[mechanic]`: duration 30s to 100s vs cooldown 125s to 50s; the cheapest perma of the four.
- DW has no duration stat; "perma DW" in guides means effect waves filling the whole cooldown `[consensus]`, which is a Quantity question.

Always compute: current duration (stones + lab + perk + substats) vs current cooldown (stones, modules), then price the cheapest stat that closes the gap with `uw.stoneCost`.

## 7. Quantity and threshold breakpoints

- Death Wave Quantity `[mechanic]`: 1 to 5 from stones; steps cost 200, 500, 850, 1,400 (2,950 total). +1 from the DW perk; module substat quantity floors (no partial credit). `[consensus]` DW3–DW5 are the named targets; more waves means longer tag coverage for the coin/cell bonus, and Kill Wall (DW+) does nothing with a single effect wave. `[unverified]` tower-hub quotes a total cap of 9 waves with substat and perk and gives two different stone costs on the same page; trust the chart above.
- Spotlight Quantity `[mechanic]`: 1 to 4; steps cost 375, 850, 2,500 (3,725). Angle 30 to 90 degrees per beam, so four beams at 90 degrees cover the full circle ("floodlight" `[consensus]` term). `[consensus]` Three beams at about 35–45 degrees before pushing Bonus; SL4 and wide angle are late targets because Angle is the most expensive SL stat.
- Chain Lightning Quantity `[mechanic]`: 1 to 5 for 655 stones total; the cheapest strong upgrade on any damage UW. `[consensus]` Order Quantity, then Chance, then Damage. Chance also drives Smite (CL+).
- Smart Missiles Quantity `[mechanic]`: 5 to 20 (6,966); perk adds 4. No community breakpoint found.
- ILM Quantity `[mechanic]`: 3 to 6 for 425 stones.
- Chrono Field slow `[mechanic]`: 75% is the stone maximum; 90% is the hard cap and needs other sources (substats); slow sources multiply. Targets CF60 / CF75 / PCF90 are `[consensus]`.

## 8. Trap stats and common mistakes

- `[consensus]` Off-ratio cooldown levels on GT/BH/DW (permanent desync). The single most expensive UW mistake.
- `[consensus]` Stones into SM, PS or ILM stats on a farming account before the coin UWs and CF are developed. Their damage ladders are the most expensive in the game (20K–30K each `[mechanic]`).
- `[consensus]` DW Damage beyond what the health bonus needs: DW pays through tags, not damage.
- `[consensus]` Spotlight before GT/BH/DW are developed, or before T7 W80; SL Bonus before beams/angle.
- `[consensus]` GT Bonus vs Duration: bonus levels are cheap early and should not be skipped, but uptime (duration and cooldown) is what compounds with BH; the last GT Duration levels are very expensive (final three levels cost about 4,500 `[mechanic]`).
- `[consensus]` BH Size too small for the build (enemies die outside it) or too large for a devo farm that wants a tight kill zone.
- `[consensus]` BH Damage lab and bot cooldown labs (irreversible labs that interact with UW plans); see `meta-workshop-labs.md` section 10.
- `[consensus]` CF heavy investment before the coin engine is running, on a pure farming account. Tournament-first accounts reverse this.
- `[consensus]` Buying UW+ on an undeveloped UW (GT+ scales with kills inside a long GT window; CL+ with CL Chance).

## 9. UW+ (Ultimate Weapon Enhancements)

- `[mechanic]` One per UW, unlocked and levelled with stones, separate from the three base stats. Requires all nine UWs owned `[consensus source; consistent with SDK]`. Unlock price is positional: 500, 625, 750, 975, 1,250, 1,650, 2,200, 2,900, 3,800 (14,650 for all nine), then a level ladder per ability.

| Shorthand | Ability | Effect | Stones to max levels |
|---|---|---|---|
| GT+ | Golden Combo | Combo +1 per kill while GT is active; when the window ends pays extra cash and coins, exponential in the combo count. The only UW+ that pays currency | 20,070 |
| BH+ | Consume | At the end of a BH activation deals a % of wave HP to affected enemies | 19,050 |
| DW+ | Kill Wall | Each effect-wave hit amplifies DW damage for that activation | 19,050 |
| CF+ | Chrono Loop | Enemies in the field spiral/orbit instead of approaching directly | 16,350 |
| SL+ | Light Range | Converts Damage/Meter into bonus damage for enemies in the beam | 37,050 |
| CL+ | Smite | Each zap rolls CL Chance to deal a % of wave HP; capped at 100 hits per enemy | 12,650 |
| SM+ | Cover Fire | Fires an extra missile every N seconds (13s down to 2s) | 12,650 |
| PS+ | Death Creep | Large multiplier on swamp damage per tick | 23,800 |
| ILM+ | Charged Mines | Mine damage charges per second until detonation | 18,570 |

- `[mechanic]` Golden Combo scales with kills during the GT window (density, kill speed, GT duration), not with GT Bonus; payout lands when the window ends.
- When to unlock `[consensus]`: only after all nine UWs, a working sync and decent GT uptime. Order for farmers: GT+ first, then CF+ for control; Legend-tournament guidance: GT+, CF+, then SL+ once Spotlight coverage is wide. towerstats and tower-hub (Nov 2026) put Chrono Loop (CF+) or Smite (CL+) first for an account whose goal is tournament rank. tower-hub logged Golden Combo at 46% of coins on one Legend account; that is one account, not a rate to promise. No fuller community ranking was found `[unverified]`.
- Cost discipline: the first UW+ unlock is 500 but its levels start at 300–400 each; compare each level with base-stat purchases using `uw.stoneCost`.

## 10. How labs, perks, modules and cards touch UWs

- Labs `[mechanic]`: GT Bonus +3.75 and GT Duration +20s; BH Coin Bonus x11, Extra Black Hole, BH Disable Ranged Enemies, BH Damage (trap); DW Coin Bonus x2.5, DW Cells Bonus x3, DW Health; SL Coin Bonus x3 (T7 W80), Spotlight Missiles; CF Duration +30s, CF Reduction %, CF Range (the one lab that can be switched off), CF Damage Reduction; CL Shock labs, Chain Thunder, Lightning Amplifier; Missile Amplifier/Barrage; Swamp stun/radius/rend; ILM stun/radius. No lab reduces GT/BH/DW cooldown.
- Perks `[mechanic]`: one per owned UW, quantity 1, unaffected by perk labs: GT Bonus x1.5, BH Duration +12s, +1 DW wave, CF Duration +5s, SL Damage Bonus x1.5, CL Damage x2, +4 Smart Missiles, Swamp Radius x1.5, extra set of Inner Mines. "Unlock a Random UW" grants a semi-upgraded UW for the run (its labs do not apply; substats do). Perks are per run, so a perma target that needs a perk is not perma until the perk is drawn.
- Modules `[consensus]`, values in `meta-modules-cards.md`: Multiverse Nexus (sync), Galaxy Compressor (cooldown cuts), Dimension Core (CL shock), substats for UW duration/cooldown/quantity (quantity floors `[mechanic]`), Magnetic Hook (ILMs fire at bosses and fleets `[mechanic]`), Tactical Barrage (SM). The Core module multiplier applies to all UW damage `[mechanic]`.
- Cards `[mechanic]`: Ultimate Crit card lets flat-damage UWs crit using the workshop Critical Factor; it does not affect %-health damage.
- Dissonance `[mechanic]`: a UW-off Dissonant Run earns up to x5 UW damage on that tier; Saboteur fleets temporarily reduce a UW's main stat.

## 11. What v27–v29 changed

- `[mechanic]` v27.0.6: extra UW+ levels `[unverified]` (search snippet). v28: Dissonant Runs can disable the UW tab; Bot+ unlocks cost stones; Echoing Shot affects UW projectiles. v28.3: more stone levels for Spotlight+, SM/ILM/PS Damage and Spotlight Bonus; Magnetic Hook change. v28.3.2: Kill Wall amplifier fix. v29: free presets (UWs are not part of any respec), Legend stones per rank reduced, Tactical Barrage. v29.1: full-uptime GT/CF/BH/PS fire at run start. v29.2: UW selection preview and cancel; Smite capped at 100 hits as intended.
- Older guides get wrong: "never touch BH cooldown / only 1:1:1 at 200s" (integer-ratio syncs and perma BH are now standard advice), UW+ costs and level counts, the absence of Bot+ and assist modules as stone sinks, and any stone totals for SL, SM, ILM, PS written before v28.3.
