# Meta: Economy (coins, cells, gems, perks, Dissonance, farming builds)

Verified against game version: v29.2.1 — written 2026-11-20

Main sources
- SDK knowledge base (`TheTowerSDK/src/knowledge/compartments`: economy, perks, dissonance, daily-missions, meta-game, labs, themes; `src/data` tables; official patch-note archive to 2026-11-19). Source of every `[mechanic]`.
- towerstats.org guide pages (single-author fan site, pages stamped Oct–Nov 2026, v29). Main 2026 source of `[consensus]`.
- tower-hub.com fan wiki (verified Jul–Nov 2026, v29.0.5–v29.1.2; compiles Reddit/Discord posts).
- the-tower.notion.site "Knowledge Hub" (2025-era, stops at v27) and the "Tower Build Guide" Google Doc (v23–24). Marked `[older]` where used.
- Not reachable during research: Fandom wiki pages, r/TheTowerGame threads, Discord pins. No first-hand Reddit/Discord text is in this file.

Tag legend: `[mechanic]` = verifiable game rule. `[consensus]` = community strategy/opinion. `[unverified]` = could not confirm or sources disagree. `[older]` = pre-2026 guidance. Stage keys S0–S5 are defined in `account-assessment.md`.

Do not quote costs from memory. Use the MCP: `calc_run` with `lab.coinCost`, `lab.durationDays`, `lab.maxLevel`, `lab.speedTotal`, `uw.stoneCost`, `uw.statValue`; `calc_list` to discover ids; `plan_effective_path` (eEcon variants `time` / `coin` / `stone`) for ranked economy purchases.

## Contents
1. How coins are actually made (the multiplier chain)
2. Which tier to farm
3. Coins per kill vs coins per wave, interest, wave skip, game speed
4. Coin bonus sources and how they stack
5. Reading the coin lines of a battle report
6. Cells and the lab-speed economy
7. Gems: what to buy, in what order
8. Packs and ads (neutral facts)
9. Perks: pick and ban priorities
10. Dissonance / Dissonant Runs
11. Daily missions, events, tournaments as currency sources
12. Farming build archetypes by stage and when to transition
13. What v27–v29 changed that older guides get wrong

---

## 1. How coins are actually made

Decision rule: treat coin income as (kills that happen inside your coin windows) x (product of multipliers). Raise whichever factor is cheapest to raise; a factor at x1 is the best target because every factor multiplies.

- `[mechanic]` All coin factors multiply. A zero factor zeroes the payout. Coin bonuses never raise cash; cash and coins share exactly one term (Golden Tower).
- `[mechanic]` Coins come from kills by enemy type, so kill volume matters: spawn ladder, spawn caps, Wave Accelerator, Enemy Balance card (about 1.8x enemies; its own multiplier is cash only, coins rise only through more kills).
- `[mechanic]` Displayed Coins/Kill = (Workshop x CPK lab + module effect) x (1 + coin enhancement) x (1 + 0.15 x coin-perk count) x (trade-off 1.8 x (1 + trade-off lab)). Tier bonus, theme/skin bonus, Golden Bot and Golden Tower multiply kill coins but do not show in that displayed number.
- `[mechanic]` Golden Tower, Black Hole, Death Wave and Spotlight each contribute a separate coin factor and their windows compound. Most apply only to enemies killed inside the window/area, which is why sync and kill placement matter more than raw stat levels.
- `[consensus]` Worked illustration (towerstats, Nov 2026): a tank killed inside BH+GT+DW is about x680; add a maxed Golden Bot and Spotlight and it is four orders of magnitude over an untagged kill. Use it as intuition for why untagged kills are nearly worthless late, not as a number to quote.

## 2. Which tier to farm

Decision rule: farm the tier with the best coins per real hour over a full run on the same build, not the highest tier you can survive. Move up only when the higher tier wins over the whole run, measured over 2–3 runs each.

How to tell:
- `[consensus]` Compare coins/hour (and cells/hour if cell-starved) from the battle report across tiers; only compare runs with the same build, perks policy and game speed. Change one thing at a time.
- `[mechanic]` Tier coin bonus is a table, not a formula: T1 x1.0, T2 x1.8, T3 x2.6, T4 x3.4, T5 x4.2, T6 x5.0, T7 x5.8, T8 x6.6, T9 x7.5, T10 x8.7, T11 x10.3, T12 x12.2, T13 x14.7, T14 x17.6, T15 x21.3, T16 x25.2, T17 x29.1, T18 x33, T19 x40, T20 x48, T21 x60, T22 x72, T23 x86, T24 x103. The step between adjacent tiers is roughly 10–25%, so a higher tier only wins if you lose less than that to earlier death, slower kills, or kills outside GT/BH.
- `[consensus]` Run-length heuristics: income per wave keeps rising deep into a run (spawn rate rises until about wave 6,500 `[older]`), so long runs on a lower tier usually beat short runs on a higher one. 2025 guidance: move up from T2–T10 when you consistently reach about 5,000+ waves with the coin trade-off perk `[older]`. 2026 guidance drops the fixed wave rule in favour of the measured comparison.
- `[consensus]` If you routinely reach Overheat on a tier, you have outgrown it. `[mechanic]` Overheat (v28) appears after clearing wave 4500 on a tier and applies Enemy Skip Decay from a defined later wave on normal tiers.
- `[mechanic]` From Tier 14 up, tiers carry static battle conditions (orb/thorns/knockback/plasma/death-ray resistance, armored enemies, ELS reduction, more bosses). A build that farms T13 can collapse at T14 because the thing it relies on is resisted. Check the tier's conditions before recommending a move (`facts/v29.2.1/tier-battle-conditions.json` via the SDK).
- `[mechanic]` Elite cells: T1–13 drop 1..tier per elite; T14+ raises the minimum (T14 avg 10.5, T15 13, T16 14, T19 17, T21 18, T24 19.5). T13 to T14 is a +50% cell step, the largest on the ladder. For a cell-starved account that can swing the farm-tier choice.
- `[mechanic]` The Utility Dissonance coin boost is earned per tier (section 10). `[consensus]` A new farm tier without its Utility boost can start well behind the old one; budget a Dissonant Run on the new tier into the comparison.
- `[consensus]` Death cause as a signal: dying early to one boss hit means the tier is too high for the eHP; dying late to accumulated heat-up is normal and fine for farming. End or abandon a run when the coin rate falls below the run average and keeps falling.

Units trap: `[mechanic]` coins/minute or coins/hour is only meaningful with the clock stated; real time and game time diverge with game speed. Never compare a per-run figure with a per-hour figure.

## 3. Coins per kill vs coins per wave, interest, wave skip, game speed

- Coins/Kill Bonus `[mechanic]`: workshop 149 levels to x2.49; lab 99 levels to x2.98; multiplicative with everything. `[consensus]` Core buy at every stage; always worth finishing.
- Coins/Wave `[mechanic]`: flat award per wave (workshop base 1 to 150), raised by the All Coins perk and tier multiplier, independent of kills. `[consensus]` Useful only very early; guides put the crossover where kill coins dominate at a few hundred waves but explicitly say it is not a constant. Lab is worth only its cheap early levels (about 20 `[consensus]`).
- Interest `[mechanic]`: % of cash held at end of wave, workshop to 5.94%, applied after cash/wave; Cash Bonus does not raise the rate. Interest is cash, not coins. `[consensus]` Buy lightly early; the Max Interest lab (T2 W80) gates its value; irrelevant once GT supplies cash. Interest perk is a ban candidate.
- Wave Skip card `[mechanic]`: chance to skip a wave and collect x1.1 of the previous wave's coins, cash and cells; consecutive skips compound (1.1^n); double skip is a separate roll; time is not skipped; skipped boss waves still roll shards/modules. `[consensus]` Minor coin source, larger effect on run length per hour.
- Game speed `[mechanic]`: lab 7 levels to x5.0; +1 from the perk scaled by Standard Perk Bonus reaches x6.25. Accelerates everything timer-driven. `[consensus]` Game Speed lab is the first lab to max on any account; the perk is a top farming pick. `[unverified]` The SDK notes the displayed multiplier overstates real speed (x5.0 behaves closer to x4.0).
- Enemy Balance, Wave Accelerator, Intro Sprint `[mechanic]`: change enemy count and time per wave, not coin multipliers. v29 made the Intro Sprint mastery unlimited in tournaments.

## 4. Coin bonus sources and how they stack

Rule: everything below multiplies. Order purchases by (increase in the factor) / cost, which the eEcon path computes; the table tells the coach what exists and its ceiling.

| Source | Ceiling / shape | Tag |
|---|---|---|
| Tier coin bonus | table in section 2 | `[mechanic]` |
| Workshop Coins/Kill | x2.49 | `[mechanic]` |
| Coins/Kill lab | x2.98 | `[mechanic]` |
| Coin Bonus enhancement (T12 W60+) | +0.01x per level, counted in both tier bonus and CPK (effectively squared, documented behaviour). Cap is 300 levels in v29.2.0 game data; older wiki text says 200 levels / x3. Final multiplier at 300 not confirmed | `[mechanic]` cap, `[unverified]` max value |
| Golden Tower | stones x5 to x21, lab +3.75 (25 lv), perk x1.5; active window only | `[mechanic]` |
| GT+ Golden Combo | pays at window end, exponential in kills during the window; the only UW+ that pays currency | `[mechanic]` |
| Black Hole Coin Bonus lab | x1 to x11 (20 lv, T5 W150); kills inside BH only; Extra Black Hole lab (T5 W500, 15B) | `[mechanic]` |
| Death Wave Coin Bonus lab | x1.5 to x2.5 (20 lv, T3 W250); tagged enemies | `[mechanic]` |
| Spotlight Coin Bonus lab | x1 to x3 (20 lv, T7 W80); enemies in the beam | `[mechanic]` |
| Golden Bot | x2.0 to x8.0 on kills in range while active; medals | `[mechanic]` |
| Coins card (must be equipped) + Coins mastery | card up to about x1.45 `[consensus]`; unequipped gives nothing | `[mechanic]` |
| All Coin Bonuses perk | x1.15 each, up to 5, scaled by Standard Perk Bonus | `[mechanic]` |
| Coin trade-off perk | x1.80 coins, -70% max health; Improve Trade-off lab raises the benefit only | `[mechanic]` |
| Utility Dissonance boost | up to x3 per tier, plus echo | `[mechanic]` |
| Relics | additive with each other, multiplicative with the rest; owned = active (equipping is cosmetic) | `[mechanic]` |
| Themes | passive coin % for owning, not equipping (0.4% / 0.8% each `[older]`) | `[mechanic]` |
| Modules | generator/cannon effects and substats add into the stat before multipliers. Named ones: Black Hole Digestor (CPK per free upgrade), Galaxy Compressor (recovery packages cut UW cooldowns), Multiverse Nexus (forces GT/BH/DW to one cooldown), Gilded Sniper (v29 cannon: chance on kill to apply all active coin bonuses even out of range) | `[mechanic]` existence; values via SDK |
| Guardian | Bounty chip feeds coins; Fetch brings coins/items (fetched coins bypass the ad bonus). Scout is a damage chip | `[mechanic]` |
| Critical Coin card | chance on basic enemies killed by crits; tiny share of late-run coins | `[mechanic]` |
| Packs / ad bonus | starter x2, epic x3 (stack to x6), ad bonus x1.5 (also granted permanently by ad removal) | `[mechanic]` |

`[consensus]` Ranking of what moves the needle, in the order accounts usually reach them: GT+BH owned and synced, their coin labs, DW with its coin lab, Golden Bot, second Black Hole, Spotlight with coin lab, coin enhancement, GT+. `[older]` Notion hub calls the second Black Hole "the final major coin jump" and wants GT duration about BH duration + 12s so GT covers the BH perk extension.

## 5. Reading the coin lines of a battle report

- `[mechanic]` The ~10 per-source coin counters are attributions, not a partition. The same coin is credited to GT, BH, DW, etc. They do not sum to the total and routinely exceed it. Never build a percentage breakdown by summing them.
- `[mechanic]` Ad bonus counter = total / 3 (it holds the bonus part of x1.5), applies to non-fetched coins only. Guardian-fetched coins are already inside the round total.
- `[mechanic]` Coverage is not income: Death Wave can tag ~89% of kills and be credited under 2% of coins; Critical Coin at 15% chance produced ~0.12% in the SDK fixture.
- `[consensus]` Diagnostic use: if GT's and BH's attributed coins are a small fraction of the total, kills are happening outside the windows (a build/sync problem, not a stat problem). A healthy synced farm has both close to the total.
- `[unverified]` Negative BH/Golden Bot/Spotlight coin lines are reported as a display bug (towerstats FAQ).

## 6. Cells and the lab-speed economy

Decision rule: cells exist to buy lab time. Spread cheap boosts across every running lab before buying a higher multiplier on one.

- `[mechanic]` Only elites drop cells. Multipliers: Death Wave Cells Bonus lab (20 lv, to x3), Cells/Kill enhancement (300-level cap), Cells card (v29, rare, T4 W40, +2 to +14 applied last; mastery multiplier), Golden Bot's Bonus Cells Bot+, Wave Skip (x1.1 of previous wave).
- `[mechanic]` Boosts are 1.5x up to 8x, sold for 1, 8 or 24 hours, and only tick while a lab is slotted. Each lab already boosted adds 20% of base price to the next (all five cost 7x one, not 5x). Cost grows far faster than the multiplier: 1.5x to 2x is 33% more speed for about 6.7x the cells.
- `[unverified]` Exact prices: sources and the SDK's own table disagree (prices come from remote config). Community figures per lab-hour: 1.5x = 15, 2x = 100, 3x = 840, 4x = 3,360. No calculator prices boosts; tell the player to confirm the price in game.
- `[consensus]` Policy: 1.5x on all running labs, then 2x on all, and go higher only when cell income refills it. An account banking cells with unboosted labs is time-limited by choice.
- `[mechanic]` Labs Speed lab: 99 levels to x2.98 (T1 W150). Relics and milestones add lab speed. `[consensus]` Keep it running almost continuously to about level 60; payback lengthens toward 3 years near 99. `[older]` Early accounts may pause it for econ UW labs.
- `[mechanic]` Gem rush skips the whole remaining time only; longer labs are discounted per unit time (0% at 1 hour to 61% at 360 days). `[consensus]` Rush only long labs, preferably when an event mission rewards research time; never short labs.

## 7. Gems: what to buy, in what order

Decision rule: buy permanent capacity (lab slots, card slots) before content (cards, modules), and content before conveniences.

- `[mechanic]` Income is bounded by real time: daily claim 20 (v29, was 15), ad gem 6 (was 5) capped at 60 claims/day, floating gem 2 (max 10 per run), daily missions 3 each plus weekly track (185 gems for a full week), tournaments, events, milestones.
- `[mechanic]` Sinks: lab slots 2–5 cost 100 / 400 / 1,400 / 3,000 (4,900 total; 5 is the cap). Cards 20 gems each; a card to 7 stars is 80 copies / 1,600 gems. Card slots: 22 buyable for 58,400 total; 23–28 need Vault keys. Tournament tickets after the free one cost 10, 20, 30... Workshop respec 150 gems `[consensus]`. Daily mission reroll 5 gems (more than a mission pays).
- `[consensus]` Order (towerstats, Nov 2026): lab slot 2, card slots 2–3, lab slot 3, card slots 4–5, lab slot 4, card slots 6–8, lab slot 5. Then one epic module of each type, then cards (do the event "buy cards" mission each event), then modules as the long-term sink. `[older]` Notion hub: about 5 card slots, then all 5 lab slots ("lab slots are the main bottleneck"), then cards to 10+ slots, then modules.
- By stage: S0–S1 slots only. S2 finish lab slots, cards to fill slots, first epic modules. S3 modules (featured banners) and card copies. S4–S5 modules for ancestral merges, relic store only for lab-speed/coin relics.
- `[consensus]` Do not buy: short lab rushes, card slots you cannot fill, extra tournament tickets, repeated respecs, gem relics early.
- `[unverified]` Whether to hold a gem buffer for banners: 2025 advice says keep a few thousand; 2026 advice says banners are announced with dates so no blind saving.

## 8. Packs and ads (neutral facts)

State these as facts and let the player decide; never push spending.
- `[mechanic]` Starter pack x2 coins and epic pack x3 coins are permanent and stack (x6). The ad coin bonus is x1.5 while active and is granted permanently when ads are bypassed (ad-free purchase).
- Consequence: absolute coin figures are not comparable between accounts without knowing these three flags. Calibrate advice to the account's own coins/hour, not to benchmark numbers from guides. Premium milestone track gives extra resources but zero feature unlocks.

## 9. Perks: pick and ban priorities

Rule: for farming, pick perks that shorten the time to more perks and raise coins; ban perks whose benefit you never use and trade-offs whose penalty hits the stat your build survives on.

Mechanics `[mechanic]`
- Unlock Perks lab at T2 W150. Pool draw: 65% standard, 20% UW, 15% trade-off. Quantity caps: 5 for most standard, 3 for Bounce Shot and Perk Wave Requirement, 2 for Orbs, 1 for UW and trade-off perks.
- Waves between perks = trunc((base - Waves Required lab) x (1 - PWR)); base 200, rising to 250/300/350 after 20/30/40 perks. PWR is -20% each (the wiki table's -25% is contradicted by its own example).
- Standard Perk Bonus lab (25 lv) scales standard perks; Improve Trade-off lab (10 lv) raises trade-off benefits only, never the penalty. Bounce Shot, Orbs and every UW perk ignore both labs.
- Perk labs: First Perk Choice (T2 W250), Improve Trade-off (T2 W400), Auto Pick (T4 W50), Perk Option Quantity (T4 W80, 2 lv), Ban Perks (T5 W40, 8 lv), Auto Pick Ranking (T6 W10).
- Perks are disabled in tournaments `[consensus source, towerstats]`; v29.2 stops offering Defense % once 98% is reached.

Farming picks `[consensus]`
1. Perk Wave Requirement every time (set First Perk Choice to it).
2. Game Speed; Free Upgrade Chance (unless a devo build keeps stats at 0, then ban it).
3. All Coin Bonuses; GT Bonus x1.5; Black Hole Duration +12s (this perk is what completes perma BH); +1 Death Wave.
4. Coin trade-off x1.80 / -70% max health if the farm does not survive on health; ban it for eHP builds.
5. Then survivability the build uses (Max Health, Defense %, Orbs).

Pushing / milestone picks `[consensus]`: Defense %, Max Health, Damage, UW perks for damage UWs, PWR still first. Skip coin perks and the coin trade-off.

Ban candidates `[consensus]`: Interest, Land Mine Damage, Defense Absolute and Health Regen past early game, Unlock Random UW once it stops helping, UW perks for UWs you keep off, and by dependency: boss 8x health, regen/lifesteal -90% (regen/lifesteal builds), tower damage -50% (damage builds), enemy damage x2.5, no kill cash (cash-dependent in-run builds), knockback -70%. For unattended (auto-pick) runs ban every trade-off that can end a run.

`[consensus]` Lab value: Perk Option Quantity is cheap and high impact; Ban Perks levels are cheap early; Auto-pick only matters for AFK play.

## 10. Dissonance / Dissonant Runs

Rule: a Dissonant Run is an investment run that buys a permanent per-tier multiplier. Do the Utility-off run on your farm tier first, push it to wave 5,000, then decide on others by which stat limits the account.

- `[mechanic]` Unlocks at T4 W90. Before a run you disable one whole workshop tab (Attack, Defense, Utility or Ultimate Weapons). Reward by tab disabled: Attack-off boosts damage, Defense-off boosts health, Utility-off boosts coins, UW-off boosts UW damage.
- `[mechanic]` Max boosts: Attack x5, Defense x5, UW x5, Utility x3 (v28.0.2–v28.0.3 changes). Boost on a tier = 1 + (max - 1) x (min(best dissonant wave, 5000) / 5000)^1.75, per tier and per type. Convex: wave 3,365 is about half, wave 4,500 about 83%; nothing is gained past 5,000.
- `[mechanic]` Dissonant Echo labs (four, T17 W60, 21 levels, 0.5% at level 0 to 10.5%) add a share of every other tier's boost-minus-one to the current tier, including tiers above, and the echo reaches tournaments. `[consensus]` Only the echo applies in tournaments.
- `[mechanic]` Workshop presets (Presets lab level 2, 35M coins) make the swap free; respeccing a preset still costs gems. A Utility-off run turns off enemy level skips, free upgrades, recovery packages and all coin/cash workshop stats.
- When it pays off `[consensus]`: as soon as the run can reach a few thousand waves with the tab off, because the Utility boost multiplies every later farm run on that tier. A full run costs about 4–7 hours of reduced income. Remove coin-only gear in non-coin runs. Stopping at 4,500 leaves 17% on the table.
- `[unverified]` Order of the other three types: towerstats says Utility first and calls low-tier echo sweeps debatable before Echo labs; tower-hub recommends Attack, UW, Health, then Utility starting at T1 and climbing. Resolve by bottleneck: damage-limited accounts want Attack/UW, survival-limited want Defense.
- `[unverified]` SDK notes tier index 25+ returns no boost; irrelevant while max tier is 24.

## 11. Daily missions, events, tournaments as currency sources

- Daily missions `[mechanic]`: 3 gems + coins + module shards each, scaled to highest tier unlocked (not the tier played). Weekly brackets at 5..35 missions are cumulative: a full week pays x64 of the tier coin figure, 185 gems, 135 medals, 45 stones, 35 guild tokens. Stones only start at the 25-mission bracket. Daily Mission Shards lab at T4 W70.
- Events `[mechanic]`: 14-day cycle, missions released over the first 8 days, unlocked at T1 W70. Medals come only from events (plus the mission weekly track) and buy bots, Bot+ upgrades, relics, themes. Event-store relics return only on reruns.
- Tournaments `[mechanic]`: Wednesday and Saturday, 30 players, 7 leagues (Copper to Mythic), only highest wave counts. Main stone source; keys only from Legend (ranks 1–24) and Mythic. v29 reduced Legend stones per rank. Unlock at T1 W60.
- Guild `[mechanic]`: bits and tokens only from guilds; Guardian costs 200 bits; chips cost guild tokens.
- `[consensus]` Never skip a tournament ticket or the weekly mission track; these are the binding inputs for stones and medals at every stage.

## 12. Farming build archetypes by stage

Two independent axes `[consensus]`: (a) how you survive: eHP (health/defense/regen/wall) vs hybrid vs glass cannon (kill before contact); (b) how you place kills: blender (everything maxed, AFK-friendly) vs devo ("devolved": some workshop stats left at 0 and some UWs off so enemies die inside BH/GT at minimum range).

| Stage | Typical farm build | Why | Transition trigger |
|---|---|---|---|
| S0 | "Turtle" on T1: Defense Absolute, Thorns breakpoints, cash/coin utility | T1 damage is flat-reducible; economy first | T2 enemies outscale Defense Absolute |
| S1 | eHP: Health, Defense %, regen/lifesteal, orbs, knockback | Survive long runs cheaply while UWs come online | GT+BH owned |
| S2 | eHP blender with orbs + BH; start devo once GT and BH are synced | Kills inside GT+BH are worth far more than extra kills outside | Sync achieved, BH about 38–50m covers kill zone |
| S3 | Orb devo on T10–13 (attack stats at 0, kills by orbs inside BH), finish the run as blender; hybrid with Wall where health still holds | Maximises tagged kills; `[consensus]` health scales poorly after about T9, hybrid to T11–12 with a strong Wall | Orb resistance at T14+ (`[mechanic]` battle condition) |
| S4 | Orbless / hybrid on T14+: high GT/BH uptime, 3-beam Spotlight, long runs | Orbs are resisted from T14 and nearly nullified by T19 `[consensus]` | Damage and UW+ let you kill before contact |
| S5 | Hybrid or glass cannon; tower-hub: hybrid "is where most accounts end up" | Enemy scaling outpaces eHP | — |

- `[consensus]` Devo generally out-earns blender but needs monitoring; blender is the correct recommendation for players who run unattended.
- `[consensus]` Orbless prerequisites (towerstats): GT about x16+, Spotlight 3 beams at about 40 degrees and x20+, runs of 7,000+ waves.
- `[unverified]` No 2026 written source covers glass-cannon farming or the exact eHP-to-GC timing. Old (v23–24) stone/coin thresholds for GC exist but predate UW+, fleets and tiers 19–24; do not quote them.
- `[consensus]` Wall: unlocking it early is a recognised mistake (costly labs, wants spare lab slots); it becomes core for hybrid in S3–S4.

## 13. What v27–v29 changed that older guides get wrong

- `[mechanic]` v28 (2026-04-07): Dissonance changes farm-tier maths; Overheat after wave 4500; Bot+ and Synchronicity add stone and medal sinks; battle report now shows cells/hour.
- `[mechanic]` v28.3 (2026-06-29): tiers 22–24, fleet rebalance, higher workshop-enhancement caps.
- `[mechanic]` v29 (2026-08-25): free preset switching (Workshop/Bot/Module/Guardian) and Global Presets (T11 W60) make farm/tournament/dissonant builds cheap to swap; module levels live on the slot; Vault rebuilt (Harmony/Power/Enemy, keys refunded); Mythic league; Cells card; gem income raised; Legend stones per rank reduced.
- `[mechanic]` v29.1 (2026-10-13): full-uptime GT/CF/BH/PS fire at run start; Primary Module Bonus labs.
- Any guide quoting Defense % cap 90%, 21 or fewer tiers, "respec to swap builds", key income only for Legend top 15, or a x5 Utility Dissonance boost is out of date.
