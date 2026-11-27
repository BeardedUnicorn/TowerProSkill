# Meta: Workshop and Labs

Verified against game version: v29.2.3 — 2026-11-20, updated 2026-11-25

Main sources
- SDK knowledge base (`TheTowerSDK/src/knowledge/compartments`: workshop, labs, tower, combat, survival, attack, footguns; `LAB_CATALOG`, `LAB_UNLOCKS`, `facts/v29.2.0/workshop-enhancement-caps.json`, `facts/v29.2.1/labs.json`; official patch notes to 2026-11-19). Source of every `[mechanic]`.
- `TheTowerSDK/docs/EFFECTIVE_PATHS.md` (port of the community Effective Paths sheet, ingestion v5.11.08.10) for the ROI method.
- towerstats.org guides (Nov 2026, v29, single author) and tower-hub.com (Jul–Nov 2026) for `[consensus]`.
- "Tower Build Guide" Google Doc (v23–24) and grindnstrat (Mar 2025), used only where marked `[older]`.
- Not reachable: Fandom wiki pages, Reddit, Discord. No first-hand Reddit/Discord text here.

Tag legend: `[mechanic]` verifiable rule; `[consensus]` community strategy; `[unverified]` unconfirmed or disputed; `[older]` pre-2026. Stage keys S0–S5 are defined in `account-assessment.md`.

Costs and durations: never quote from a table in this file. Compute with the MCP: `calc_run` ids `lab.coinCost`, `lab.durationDays`, `lab.maxLevel`, `lab.valueAtLevel`, `lab.coinDiscount`, `lab.speedTotal`, `workshop.statDefinitions`, `workshop.enhancementDefinitions`, `workshop.sectionDiscountPct`, `workshop.enhancementDiscountPct` (confirmed present in SDK 3.0.0; always confirm an id with `calc_list` before relying on it). A run of lab levels in one call: `lab.coinCostBetween` and `lab.durationDaysBetween` `{labKey, fromLevel, toLevel, modifiers}` (SDK 2.0.0). `form_calc lab.research` returns coins and hours for a lab level in one small answer and is the cheapest way to price a lab; its lab-speed input needs the relic `LabSpeed` total from `workshop.relicBenefitByStat` (see `data-access.md` § "Tables and calculators worth knowing"). Workshop coin levels: `calc_run workshop.upgradePrice {args: {stat, fromLevel, count, sectionDiscountPercent}}` gives what the buy button shows for 1, 5, 10 or 100 levels with the tab's discount lab applied (each level discounted and rounded, then summed), and `workshop.coinCostBetween {stat, fromLevel, toLevel}` the list price of a longer run; both cover all 48 upgrades (SDK 2.0.0). What a level gives, with its unit named: `workshop.statValue {stat, level}` — Enemy Attack and Health Level Skip are 0.05% a level, not 0.5%. On a server older than 2.0.0 the handle is `mechanics.workshopStatValue`; trust only its `coinCost`. Use `plan_effective_path` for ranked purchases.

## Contents
1. How the workshop works (what a coach must know first)
2. Workshop priorities by stage
3. What to never or rarely buy, and why
4. Workshop maxima and hard caps
5. Workshop Enhancements
6. Presets and respec
7. How labs work (slots, cost, time, switching, permanence)
8. Lab priorities by stage
9. Always-running labs, coin-starved vs time-starved queues
10. Labs to delay or treat as irreversible traps
11. Lab maxima and gates worth knowing
12. Comparing ROI instead of guessing
13. What v27–v29 changed

---

## 1. How the workshop works

- `[mechanic]` Three tabs: Attack, Defense, Utility; 48 upgrades. Coin purchases are permanent until a respec; cash purchases during a run reset every battle. The same stat exists in both currencies.
- `[mechanic]` Upgrades unlock in chains; affordable does not mean available.
- `[mechanic]` Workshop maximum is not the stat's cap. Defense % reaches 49.5% from the workshop against a 98% hard cap; Orbs 4 of 14; labs, cards, modules, relics and vault add on top. Thorns is the exception: 99% from the workshop alone.
- `[mechanic]` Two upgrades improve downward (Shockwave Frequency, Wall Rebuild) and Knockback Force dips at level 30. "More levels = bigger number" is wrong for those three.
- `[mechanic]` Free upgrades (three separate per-wave chances, up to 49.5% each from workshop, 90.75% with card and perk) level in-run cash stats for free. This is why a build that wants a stat at 0 during a run must also zero the matching free-upgrade chance.
- `[mechanic]` Section discounts: Workshop Attack/Defense/Utility Discount labs, 99 levels each, to 49.5%. They discount upgrade levels only. The "Unlock…" buttons that open new workshop rows (the Wall at 500M, Rend Armor at 500B, and so on) are always full price. `next_unlocks` gives the next unlock on each tab, what it opens and its price beside the coin balance.
- Coaching consequence: workshop advice is always build-relative. Ask (or infer from the save) whether the player farms eHP, devo or hybrid before saying "max X".

## 2. Workshop priorities by stage

Decision rule: spend coins on the stat that the current run dies to or earns through, in the cheapest unlocked form (workshop level vs lab level vs enhancement). When several qualify, take the best gain-per-coin from `plan_effective_path` (variant `coin`).

### S0 — brand new (T1–T3, no UW)
- `[consensus]` Utility first: Cash Bonus, Cash/Wave, Coins/Kill Bonus, Coins/Wave. They compound every later run.
- `[consensus]` Defense: Defense Absolute is the T1 workhorse (enemy hits are small enough to be flat-reduced; about 50 permanent levels suffices on T1), Thorns to hit-count breakpoints, modest Health. `[unverified]` A generic 2026 emulator blog says Damage then Attack Speed first; the two specialist sources both say economy + Defense Absolute/Thorns first. Follow the specialists.
- `[consensus]` Attack: enough Damage and Attack Speed to clear early waves; do not chase crit yet.
- Why: T1 runs are short, coin income is the binding constraint, and cheap flat defense outlasts cheap damage.

### S1 — early (T2–T6, first UWs)
- `[consensus]` Defense: Health, Defense %, Health Regen/Lifesteal, Orbs, Knockback. Stop investing in Defense Absolute as the main defense once on T2+ (enemy damage outscales flat reduction; towerstats: T2 enemies are about 20x T1).
- `[consensus]` Attack: Attack Speed, Damage, Critical Chance/Factor, then Multishot, Rapid Fire, Bounce Shot in that order. Leave Super Crit until coins are plentiful.
- `[consensus]` Utility: finish Coins/Kill Bonus (x2.49) and Cash Bonus; Interest only lightly; Recovery Packages when unlocked (they also feed Galaxy Compressor later).
- Why: runs get long; eHP and sustain decide wave count, and wave count decides coins.

### S2 — early-mid (T5–T10, GT+BH+DW coming together)
- `[consensus]` Push Health and Defense % toward cap, keep Thorns climbing (about 15–20% rising toward the 34% three-hit breakpoint on devo builds).
- `[consensus]` Decide blender vs devo. Devo/orbless farms keep attack stats and all three Free Upgrades at 0 on the farm preset; blender farms max everything.
- `[consensus]` Do not raise Range for farming (kills should happen close, inside BH).
- `[mechanic]` Enemy Attack/Health Level Skip labs unlock at T11 W200; the workshop skip stats are worth early levels before that `[consensus]`.

### S3 — mid (T10–13, synced, workshop mostly maxed)
- `[consensus]` Finish the workshop: every stat the active build uses to max, including Super Crit, Rend Armor and Death Defy (30% at 75 levels `[mechanic]`).
- `[mechanic]` Workshop Enhancements open at T12 W60 (5B lab). See section 5.
- `[consensus]` Wall: only now, if hybrid; it needs Wall Health/Rebuild/Regen/Thorns labs (T8–T10 gates) and spare slots.

### S4–S5 — late and endgame (T14+)
- `[consensus]` Coins go to enhancements and module levels, not base workshop. Build one preset per job (farm, tournament, each dissonant type) and keep them current.
- `[mechanic]` Tier battle conditions from T14 resist orbs, thorns, knockback, plasma cannon and death ray; re-check which stats still do anything on the farm tier before spending.

## 3. What to never or rarely buy, and why

| Item | Verdict | Why | Tag |
|---|---|---|---|
| Defense Absolute after T1 | Rarely | Flat reduction is outscaled by enemy damage; fine as cheap filler and for the enhancement later | `[consensus]` |
| Range (workshop and lab) | Keep low for farming | Enemies should die near the tower inside BH/GT; the wiki says one "range" lab can be turned off, but which one (tower Range or Chrono Field Range) is `[unverified]` — see `footguns.md` | `[consensus]` |
| Interest | Lightly, early only | Pays cash, not coins; capped by Max Interest lab; dead once GT supplies cash | `[consensus]` |
| Coins/Wave | Early only | Flat and independent of kills; negligible on long runs | `[consensus]` |
| Free Upgrades | Build-dependent | Good on blender/eHP; zero on devo/orbless because they level the stats you want at 0. `[older]` doc calls them good except low-range BH builds | `[consensus]` |
| Land Mines | Low priority | Minor damage source; old doc: only for events or once coins are abundant | `[older]` |
| Knockback | Useful early, fades | Weakens at high waves; resisted from T14 battle conditions `[mechanic]` | `[consensus]` |
| Health Regen early | Low | `[older]` doc calls regen useless early; it becomes real with labs, cards and the wall | `[consensus]` |
| Super Crit early | Wait | Expensive unlock chain; value arrives with a developed crit chain | `[consensus]` |
| Enemy Level Skips | Not "never" | Cheap early levels are good value; `[consensus]` tournaments scale skip chance down by league, and Utility Dissonant runs disable them. `[mechanic]` v29 tournaments apply no ELS-subtract condition; campaign tiers 14+ do | mixed |
| Wall (unlock) early | Avoid before S3 | Expensive, pulls lab slots, can hurt pure health builds | `[consensus]` |
| Rapid Fire / Bounce Shot | Normal priority after core attack | Not traps; they come after Attack Speed, Damage, Crit, Multishot | `[consensus]` |

General reason behind most "don't": a workshop coin spent on a stat the farm build never uses is a coin not compounding in Coins/Kill, labs or enhancements. Respec exists, so the cost of a mistake is 150 gems, not permanent.

## 4. Workshop maxima and hard caps

`[mechanic]` from the SDK tables (verify bounds with `workshop.statDefinitions`):
- Health, Damage, Health Regen: 6000 levels each. Attack Speed 99 levels to 5.95. Critical Chance 79 levels to 80% (100% with other sources). Critical Factor 150 levels to x16.2. Super Crit Mult 120 levels to x13.2. Lifesteal 80 levels to 4.46%.
- Defense %: 49.5% from workshop; hard cap 98% across all sources. Thorns 99% (49.5% vs bosses). Death Defy 30%. Knockback Chance 80%. Shockwave Frequency 14s from workshop (hard floor 7s). Wall Health 20% to 200% of tower health over 1800 levels; Wall Rebuild hard floor 150s.
- Coins/Kill Bonus and Cash Bonus x2.49 (149 levels). Interest 5.94% (99 levels). Coins/Wave 150. Orbs 4 from workshop of 14 total (11 clockwise + 3 extra).
- Formulas that explain priorities: eHP = (Health + Defense Absolute) / (1 - Defense %); damage taken = damage x (1 - Def%) - Def Abs; each enemy hit that lands multiplies that enemy's damage by x1.04 (heat-up). Near the 98% cap, each Defense % point is worth far more than the previous one; flat defense matters only while hits are small.

## 5. Workshop Enhancements

Rule: enhancements are a late coin sink with a brutal curve. Open them when the core stat of your build is maxed in the workshop, then follow gain-per-coin, starting with Coin Bonus on a farming account.

- `[mechanic]` Unlock: T12 W60 milestone plus the Workshop Enhancements lab (5B coins). 18 enhancements, 6 per tab, multiplicative over the base stat. First level of any enhancement costs 5B. `[consensus]` First enhancement per tab is available immediately; later ones unlock by cumulative spend in that tab (50B, 500B, 5T, 50T, 500T).
- `[mechanic]` Caps (v29.2.0 game data): 600 levels for Damage, Rend Armor, Critical Factor, Damage/Meter, Super Crit Mult, Health, Health Regen, Defense Absolute, Land Mine Damage, Wall Health, Cash Bonus, Recovery Package; Coin Bonus 300; Cells/Kill 300; Orb Size 250; Free Upgrades 150; Attack Speed 100; Enemy Level Skips 60. Wiki and older guides show the pre-v28.3 caps.
- `[mechanic]` Cost curve: all start at 5B, step sharply at level 17, steepen again in the low 200s. Twelve of the eighteen share one identical ladder. A shorter ladder is not cheaper (Free Upgrades' last level costs more than Damage's).
- `[mechanic]` Discounts are separate from workshop discounts: Enhancement Attack/Defense/Utility Coin Discount labs (T21 W60, 100 levels, to 30%) and a Vault discount (to 25%).
- `[mechanic]` Coin Bonus enhancement counts twice (tier bonus and Coins/Kill). `[unverified]` its value at the new 300-level cap; older text says +0.01x per level and x3 at 200.
- Priority `[consensus]`: no ranked 2026 list was found. What sources agree on: Coin Bonus first for farmers (squared effect); Cells/Kill when lab-time-limited; then the enhancement of the stat your build survives or kills with (Health / Wall Health for eHP-hybrid, Damage and crit chain for damage builds). `[older]` v23–24 advice: do not open enhancements until you can max your core stat mid-run.
- Method: `plan_effective_path` prices enhancement levels against lab levels and stones in the same currency of benefit; use it rather than a fixed order.

## 6. Presets and respec

- `[mechanic]` Workshop Respec lab: one level, T4 W30, 3M coins. Respec refunds coin upgrades. `[consensus]` Respec costs 150 gems, refunds the undiscounted price, and does not touch UWs; the Vault can discount it.
- `[mechanic]` v29 Presets lab (renamed from Card Presets; T1 W400): level 1 Card presets 350K, level 2 Workshop presets 35M, level 3 Bot presets 3.5B, level 4 Module presets 350B, level 5 Guardian presets 35T. Two slots each on unlock, more through the Vault. Switching presets is free; respeccing a preset still costs gems.
- `[mechanic]` Global Presets lab: T11 W60, one level, 100T coins, long research. Binds a set of presets to a battle type (farm, tournament).
- Use `[consensus]`: a Farm preset and a Tournament/Push preset at minimum; one preset per Dissonant type once the player runs them (a preset with the disabled tab's spend moved elsewhere is not required, but a devo farm preset and a full-stat push preset are). Recommend a gem respec only to fix a preset that is structurally wrong (for example attack stats bought on a devo farm, or an early Wall); never as a routine swap, since switching is now free.

## 7. How labs work

- `[mechanic]` Labs cost coins and real time, are permanent, and cannot be turned off (the wiki states "range" as the one exception; which Range lab is `[unverified]`, see `footguns.md`). Most must be unlocked by a milestone: of 236 named labs only 58 are open from the start; gates run T1–T23. A recommended lab must be checked against the account's per-tier best waves (`LAB_UNLOCKS`, SDK `isLabUnlockedAt`).
- `[mechanic]` Slots: first free at T1 W30; slots 2–5 cost 100 / 400 / 1,400 / 3,000 gems; five is the maximum.
- `[mechanic]` Stopping a lab refunds the coins in full and keeps accrued progress; resuming charges the full cost again. Switching labs therefore costs slot time, not coins. A coin-starved player can pull coins out of a long lab temporarily.
- `[mechanic]` Cost and time mostly rise together; three labs are cheap but slow (Chain Lightning Shock, Missile Barrage, Common Drop Chance); none is expensive and fast. 22 labs are one-shot unlocks (Unlock Perks, Workshop Respec, Auto Pick Perks, First Perk Choice, Package After Boss...).
- `[mechanic]` Labs Coin Discount: 99 levels x 0.3% = 29.7%. Labs Speed: 99 levels to x2.98, plus relic and milestone lab speed. Labs Speed applies to its own research, so its next level takes about half the time a model without that would say at level 54 (239.75 h on screen against 498.68 h). For a running lab quote `activeQueue[].remainingSecondsWithSpeedUp`, which also counts the slot's cell boost. Cell boosts 1.5x–8x (see `meta-economy.md` section 6). Gem rush skips the whole remainder only; gold-boxing (maxing) a lab improves rush efficiency by 0.015x each.

## 8. Lab priorities by stage

Decision rule: never leave a slot empty; in each slot run the lab with the best benefit per day (if time-limited) or per coin (if coin-limited) among unlocked labs that the build uses. `[mechanic]` Labs are limited by slot time, not coins: a lab that costs a million coins can hold a slot for two hundred hours, so never rank labs and coin buys in one list. `plan_spending` (SDK 3.0.0) does this for the coin labs: `labQueue` by coins per day gained per slot-hour, `labSchedule` for what starts in which slot and when. Check each row's `paybackDays`; the stage lists below still decide the labs it cannot price (Labs Speed, discounts, damage and survival labs).

### S0 (1–2 slots)
- `[consensus]` Game Speed to max first (7 levels, cheap, multiplies everything). Then Coins/Kill Bonus, Labs Speed, Damage, Health, Defense Absolute, Attack Speed in rotation. `[unverified]` tower-hub says hold Labs Speed on T1 and run Game Speed > Coins/Wave > Defense Absolute; towerstats wants Labs Speed almost always on. With one slot, Game Speed and Coins/Kill first is common ground.
- `[consensus]` Cheap levels of Labs Coin Discount and the Workshop Discount labs whenever coins are tight.

### S1 (2–4 slots)
- `[consensus]` Unlock Perks the day T2 W150 is reached; then Standard Perks Bonus, Perk Option Quantity (T4 W80), Ban Perks, First Perk Choice, Waves Required.
- `[consensus]` One slot on Labs Speed, one on a coin lab (Coins/Kill), the rest cycling Health, Damage, Defense %, Regen, Attack Speed, Crit Factor.
- `[consensus]` Presets level 1; Workshop Respec; Daily Mission Shards and Reroll Shards (T4 W70) once modules exist.
- `[mechanic]` UW coin labs unlock early and are cheap at first: DW Coin Bonus and DW Health (T3 W250), GT Bonus and GT Duration (T4 W200), BH Coin Bonus (T5 W150).

### S2 (4–5 slots)
- `[consensus]` Max the econ UW labs: Black Hole Coin Bonus (20), Golden Tower Bonus (25), Golden Tower Duration (20), Death Wave Coin Bonus (20), Extra Black Hole (T5 W500), then Spotlight Coin Bonus (T7 W80) if owned.
- `[consensus]` Module Shard Cost (30), Common/Rare Drop Chance, Death Wave Cells Bonus, Golden Bot Duration, Super Crit labs, Recovery Package labs (T6 W150), Orbs labs, Garlic Thorns (T2 W1000).
- `[consensus]` Presets level 2 (Workshop presets) before starting Dissonant Runs.

### S3 (5 slots)
- `[consensus]` Enemy Attack/Health Level Skip (T11 W200), Workshop Enhancements (T12 W60), Wall labs if hybrid (Wall Health/Rebuild T8 W10, Wall Regen/Thorns T10 W70, Wall Invincibility T12 W10), Module Coin Cost and effect-ban labs (T10 W40), Global Presets (T11 W60), Chrono Field labs if owned, Max Rend Armor (T13 W10).
- `[consensus]` Keep Labs Speed running; finish Standard Perks Bonus and Improve Trade-off.

### S4 (5 slots, T14–T18)
- `[consensus]` Recharge Second Wind / Demon Mode / Nuke (T14 W60), Wall Fortification (T14 W40), Shatter Shards (T16 W40), Chain Thunder and Lightning Amplifier (T16 W60), Swamp Rend labs, Card Mastery labs (T16 W100 with 30 maxed cards; very long), Dissonant Echo (T17 W60, Utility echo first for farmers `[consensus]`), Battle Condition Reduction (T18 W1000).
- `[unverified]` A "start masteries at about 700T coins/day" rule was attributed to tower-hub in a search snippet but not confirmed.

### S5 (T19+)
- `[mechanic]` Elite/resistance/battle-condition labs (T19–T21), Assist Module labs (T19 W50), Enhancement Coin Discount (T21 W60), fleet labs (T22–T24), Primary Module Bonus labs (T23 W500, 30 levels to +30%, added v29.1). These run to hundreds of days per level; ROI comparison is mandatory.

## 9. Always-running labs; coin-starved vs time-starved

Always running `[consensus]`: Game Speed until maxed; Labs Speed (to roughly level 60, then reassess payback); one coin lab at all times (Coins/Kill early, UW coin labs mid, coin-relevant enhancement-discount/echo labs late).

Coin-starved (coins are spent the moment they arrive; slots would sit idle on the labs you "should" run):
- Queue cheap-but-long labs so no slot is empty: Labs Speed, Labs Coin Discount, Workshop Discounts, low levels of secondary stats, the three cheap-and-slow labs.
- Prioritise coin labs and Labs Coin Discount ahead of combat labs; pull coins from a long expensive lab by pausing it only if a clearly better purchase is waiting (full refund, progress kept).
- Fix the economy first (farm tier, sync, Dissonance Utility run); labs are a symptom here.

Time-starved (coins pile up, every slot busy):
- Buy the fifth slot if missing; spend cells on 1.5x across all labs then 2x; keep Labs Speed running; pick up lab-speed relics.
- Prefer high-cost, high-impact labs (benefit per day); dump surplus coins into workshop/enhancements/modules rather than hoarding.
- Rush with gems only long labs and only when gems have no better permanent use.

How to tell which: compare coins on hand and daily income with the summed cost of the next level of each running lab. If the next levels cost several days of income, coin-starved; if minutes to hours, time-starved.

## 10. Labs to delay or treat as traps

- `[mechanic]` Bot cooldown labs are irreversible (bot medal upgrades are respeccable, the labs are not). Four bots floor at 50s with the lab (75s without); Flame Bot floors at 5s. `[consensus]` Do not research bot cooldown labs until the UW/bot sync target is decided; a Golden Bot cooldown that does not divide the GT/BH cycle loses overlap.
- `[consensus]` Black Hole Damage lab: kills enemies BH is supposed to hold for tagged kills, undermines devo/perma-BH farms, cannot be undone. Delay until the BH plan is fixed.
- `[consensus]` Chrono Field Range: zooms the view out and lowers coins/hour slightly. The wiki argues to max it anyway for tournaments; it is opinion both ways.
- `[consensus]` Defense % lab past the level where the account already reaches 98% from all sources is wasted (towerstats: around level 23 for many accounts; depends on cards/relics/modules, so compute).
- `[consensus]` Low value past early levels: Starting Cash, Cash/Wave, Coins/Wave, Interest, Range, enemy-research labs unless a slot is spare, Flame Bot Burn Stack, DW Damage Amplifier and DW Armor Stripping for farmers.
- `[consensus]` Deep-levelling one lab while others sit at 0 is a classic mistake: early levels of many labs beat late levels of one.

## 11. Lab maxima and gates worth knowing

`[mechanic]` (levels; use `lab.maxLevel` to confirm, `lab.valueAtLevel` for values)
- Game Speed 7 (x5.0). Labs Speed 99 (x2.98). Labs Coin Discount 99 (29.7%). Workshop discounts 99 each (49.5%).
- Damage, Health, Health Regen, Defense Absolute 100; Attack Speed, Critical Factor, Coins/Kill, Cash Bonus 99; Defense % 50 (+10%); Super Crit Chance 50, Super Crit Mult 40; Range 80.
- Perks: Standard Perks Bonus 25, Waves Required 100, Improve Trade-off 10, Ban Perks 8, Perk Option Quantity 2, Auto Pick Ranking 32.
- UW labs: GT Bonus 25 (+3.75), GT Duration 20 (+20s), BH Coin Bonus 20 (x11), DW Coin Bonus 20 (x2.5), DW Cells Bonus 20 (x3), SL Coin Bonus 20 (x3), CF Duration 30 (+30s), CF Reduction % 30, CF Range 20, Missile Amplifier 25, Spotlight Missiles 18.
- Modules: Module Shard Cost 30, Module Coin Cost 30, Reroll Shards 100, Daily Mission Shards 50, Shatter Shards 5.
- Late: Dissonant Echo 21 each, Enhancement discounts 100 each, Assist Module labs 30 each, Primary Module Bonus 30 each, Card Mastery labs 9 per card.

## 12. Comparing ROI instead of guessing

1. List candidate labs that are unlocked and not maxed.
2. For each, get next-level `lab.coinCost` (after `lab.coinDiscount`) and `lab.durationDays` (after `lab.speedTotal` and any boost), and the value change from `lab.valueAtLevel`.
3. Convert the value change to the account-level metric it feeds: coins/hour (economy), eHP or eRegen (survival), eDamage (damage). The Effective Paths method does exactly this: one number per account per model, candidate scored by change in that number divided by cost.
4. For coin-earning candidates `plan_spending` does steps 1–4 in one call, in coins per day (SDK 3.0.0), and `survival_rank` scores survival workshop levels in waves gained per billion coins from a model fitted to the account's runs; steps 1–3 by hand remain the method for everything they leave in `notRanked`. Rank by gain per coin when coin-starved and gain per research-day when time-starved. The same candidates rank differently under the two; that is the point (`plan_effective_path` variants `lab-coins` vs `lab-time`).
5. Caveats `[mechanic]`: the planner is greedy, so it can miss an upgrade whose payoff arrives levels later (breakpoints such as perma targets, quantity, thorns hit counts — compute those with `calc_run` `mechanics.thornsHitsToKill` `{percentOfMaxHealth, isBoss}`); an empty plan with `issues` populated means bad inputs, not a finished account; do not double-fill `lab` and `coin` level bands.
6. Payback check for speed/discount labs: (time or coins saved per day across all running labs) vs (days the slot is occupied). Labs Speed pays back faster the more slots are running.

## 13. What v27–v29 changed

- `[mechanic]` v27: fleets from T14, assist modules, enhancement coin-discount labs. v28: Dissonant Echo labs, Bot+ (stones + medals), Overheat. v28.3: tiers 22–24, fleet labs, enhancement caps raised (600/300/250/150/100/60). v29: Presets lab with Workshop/Bot/Module/Guardian presets and free switching, Global Presets lab, Wall Regen shown on Wall Health, module levels moved to slots (old coin/shard spend refunded), Vault rework, three new fleet labs. v29.1: Primary Module Bonus labs. v29.2: Defense % perk hidden at 98%; no ranged enemies on T1 waves 1–20.
- Older guides that say "respec to change build", "enhancements cap at 200/400", "Defense % caps at 90%", or that omit presets and Dissonance are out of date.
