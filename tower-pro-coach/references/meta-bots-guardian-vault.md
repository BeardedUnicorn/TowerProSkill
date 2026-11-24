# Bots, medals, Guardian, Vault, relics, themes, guild and daily missions

Verified against game version: v29.2.2 — 2026-11-20, updated 2026-11-24

Main sources
- SDK: `compartments/bots.ts`, `guardian.ts`, `guild.ts`, `vault.ts`, `themes.ts`, `daily-missions.ts`, `progression.ts` (relics), `meta-game.ts` (events), `footguns.ts`; `facts/v29.2.1/vault-upgrades.json`; `src/data/bots`, `guild`, `themes`.
- Patch notes v28.0 (Bot Bot, Bot+, Synchronicity), v29.0–v29.2.
- Fandom wiki: "Medals Guide", "Footguns", "Guardian", "The Vault" (read 2026-11-18/20). The Medals Guide predates Bot Bot and Bot+.

Tags: `[mechanic]` game rule · `[consensus]` community view · `[unverified]` unconfirmed or disputed.
Stages: New · Early · Mid · Late · Endgame (as in the other reference files).

## Contents
1. Decision rules at a glance
2. Medals and the event shop
3. Bots
4. Guild basics
5. Guardian
6. Daily missions
7. Relics
8. Themes, skins and songs
9. The Vault
10. Tools

---

## 1. Decision rules at a glance

| Stage | Medals | Guild / Guardian | Vault |
|---|---|---|---|
| New | Events open at Tier 1 Wave 70. Buy lab-speed or coin relics if offered, then themes. | Join an active guild as soon as guilds unlock (Tier 3 Wave 10). It is free weekly income. | Not visible. |
| Early | Themes and relics each event; unlock Golden Bot and level Range and Bonus. | Unlock the Guardian (200 bits); buy the first shop chip. | — |
| Mid | Golden Bot first, then Amplify Bot. No cooldown levels until the UW sync target is known. | Second and third chip slots; level the chips you equip. | — |
| Late | Remaining bots; bring cooldowns to the sync; consider Bot+ once all five are owned. | Chip tracks, guild-shop relics and skins. | Opens on promotion to Legend. Start with Harmony quality-of-life that changes play. |
| Endgame | Bot+ levels, Synchronicity. | Presets for farm and tournament. | Card slots, automations, then Power categories by ROI; Enemy tree in Mythic. |

Why: medals and bits are calendar-paced, not skill-paced. A weekly or fortnightly allowance spent on the wrong thing cannot be re-earned by playing more. `[mechanic]`

## 2. Medals and the event shop

**Mechanics** `[mechanic]`
- Medals come from events (two-week cycles, unlocked at Tier 1 Wave 70) and from the weekly daily-mission track (135 a week at 35 missions). New missions appear for the first 8 days of an event; all stay open to the end.
- Each mission has three tiers of requirement. Some auto-complete when the underlying system is maxed.
- The event shop sells bots and bot levels, Bot+ levels, themes, songs, relics, stone and gem packs.
- A gem-priced relic section (since v28) rotates weekly: two Rare (600 gems) and two Epic (1,200 gems) older event relics.
- Event-store medal relics return only on event re-runs.
- `readEventShopFromSaveRoot` keeps two relic lists apart, and they are different relics. `earnTrack` is what the running event **awards**: four relics, given when the medals earned in the event reach `medals` (350 and 700 free; 550 and 1,100 need the paid event pass, `needsEventPass`). `relics` is what the shop **sells**: older relics from a past event (`fromEvent`), at `price` medals (Rare 200, Epic 500). Compare `medalsCurrentEvent` with the earn-track thresholds to say which awards are still in reach, and only count pass rows for a player who has the pass. Rotating relics are priced in gems and the save does not say which are on the shelf. The reader also lists themes and songs with their coin bonus.
- v29.2 warns when a medal purchase would leave another bot preset in deficit.

**Spending order** `[consensus, wiki Medals Guide]`
1. High-value past relics when offered (`relics[]` rows with `owned: false`): lab speed and coin relics first. The event's own relics (`earnTrack`) cost nothing; they come from earning medals, so finishing missions is what secures them.
2. Themes and songs each event (about 400 medals an event for both): small permanent coin bonuses that add up.
3. Stone packs: at most one or two; the price escalates. Many players skip them to fund bots.
4. Gem packs: only while lab slots are still locked.
5. Bots (section 3).

towerstats (Oct–Nov 2026) `[consensus]`: medals do not expire, so a balance can wait for a re-run relic; do not spend them on gem, stone or shard packs; on bots, buy Range and Bonus before Cooldown (cooldown interacts with sync, section 3).

Adjustments for the current game `[consensus]`
- The guide was written with four bots. Bot Bot multiplies other bots, so it is worth little until the others are strong.
- Once bots and Bot+ are deep, relics and themes still come first each event because they are time-limited; bot levels can always be bought later.

## 3. Bots

**The five bots** `[mechanic]`
| Bot | Upgradable stats | What it does |
|---|---|---|
| Golden Bot (coin bot) | Duration, Cooldown, Bonus, Range | Multiplies coins from kills in its radius; Bonus ×2.0 rising 0.2 per level to ×8.0. |
| Amplify Bot | Duration, Cooldown, Bonus, Range | Multiplies tower damage against enemies in its radius. |
| Thunder Bot | Duration, Cooldown, Linger, Range | Stuns; Linger is how long the effect stays after the bot leaves. |
| Flame Bot | Damage Reduction, Cooldown, Damage, Range | Burns; the only bot with Damage Reduction. Fixed 3 s duration, base cooldown 75 s. |
| Bot Bot (v28) | Duration, Cooldown, Bonus, Range | Amplifies the other bots' effects inside its radius. |

- Bought and levelled with medals. Unlock price depends on how many bots you already own (positional ladder; look up with `oracle_get`).
- Level cost: 100 medals for the first level of a stat, +40 for each level after. Each stat has its own maximum: Cooldown 15 on every bot; Duration and Bonus 30 on Golden and Amplify; Range 15–20 by bot; Bot Bot Bonus 19; Flame Bot Damage 30. Never assume one "bot level".
- Tower range amplifies bot range. Relics and the Vault add more.
- Bots can be switched off individually.

**Cooldowns and why they are a trap** `[mechanic]`
- Base 120 s. Medal levels remove 3 s each for 15 levels (floor 75 s). The Cooldown lab removes 1 s per level for 25 levels (floor 50 s). Flame Bot is the exception: it starts at 75 s, its ladder ends at 30 s and the lab takes it to 5 s.
- **Medal levels can be respecced. Lab levels cannot.** Respec is limited to once per event unless the Vault's Bot Presets upgrade is owned.
- At maximum: every bot except Flame at 50 s, Black Hole and Death Wave at 50 s, Golden Tower at 100 s, a clean 2:1.
- The Vault's Bot Cooldown Sliders (Harmony ▸ Bots, 15 keys) let a Legend-league player dial a cooldown back up. Below Legend there is no undo for the lab.

**Sync recipe** `[consensus, wiki Footguns]`
- Target: bot cooldown = half the GT/DW sync cooldown, so the bot is up for every second activation at worst and every activation at best.
- Step 1: 6 medal levels + 2 lab levels → 100 s.
- Then move in 5 s steps (1 medal + 2 labs) or 10 s steps (3 medals + 1 lab) toward half the UW sync cooldown.
- Do not research bot cooldown labs "because they are cheap". Ask what the UW sync cooldown is first. Example from the wiki: a 69 s Multiverse Nexus sync cannot be matched by a maxed Golden Bot.

**Medal priority within bots** `[consensus, wiki Medals Guide; pre-v28]`
1. Golden Bot: Range a couple of levels ahead of Bonus; no Cooldown until syncing. Move on when both are well up.
2. Amplify Bot: Range first (so bosses pass through it), then Bonus.
3. Thunder Bot: needs to be near max to help; low levels can disrupt some builds.
4. Flame Bot: last.
5. Bot Bot: after the others carry real values `[consensus, inferred from its mechanic]`.
- Unlock one bot and level it; do not unlock all five and leave them at level 0. (Exception: Bot+ requires all five owned.)
- Duration matters with Bonus: value is roughly Bonus × Duration ÷ Cooldown inside the radius.

**Bot+** `[mechanic]`
- Available once all five bots are unlocked. Each ability costs 1,250 stones to unlock, then medals to level. A bot respec returns the medals; the stone unlock is kept.
- Wildfire (Flame): burned enemies also take ×1.5 and up extra damage.
- Titan Shock (Thunder): struck enemies permanently attack 5–25% slower, multiplied by the digits of their mass (continuous since v29).
- Bonus Cells (Golden): elites killed **inside Golden Bot range** give ×1.25 and up cells (range restriction since 29.1.1).
- Echoing Shot (Amplify): bullets in range count as several; UW projectiles get one third of the boost. Different, steeper medal ladder (9 levels).
- Maximum Power (Bot Bot): boosts the other bots' Bot+ abilities.

Which first `[consensus, thin]`: Bonus Cells for lab speed if cells are the bottleneck and Golden Bot range covers the kill zone; Echoing Shot for damage-limited tournament players. No tested v29 ranking was found. `[unverified]`

**Synchronicity** `[mechanic]` Unlocked for stones (1,500) after all five Bot+ abilities are owned. Gives two slots for bots that then share a path; each further slot costs 1,500 stones. It is an Endgame stone sink; weigh it against UW+ and assists with `calc_run`.

## 4. Guild basics

`[mechanic]`
- Guilds unlock at the Tier 3 Wave 10 milestone. A guild changes nothing inside a run except enabling the Guardian.
- **Weekly guild box**: four chests at 100 / 250 / 500 / 750 guild contribution, cumulative. All four pay 60 gems, 150 guild tokens and 185 bits, plus coins as a multiplier of the tier-based coin value.
- Contribution is weekly. Unclaimed chests are mailed (v29.2 hardened this).
- **Guild shop** (tokens): Guardian chips (200 each), Guardian skins and menu themes, season relics (75 tokens Rare, 150 Epic in documented seasons), bits and other items. Seasons rotate; a missed season relic is gone unless it re-runs.
- Bits exist only through guilds. No guild, no Guardian progress.
- Leaving a guild keeps the Guardian and chips but they stop working until you join another (v29.1).

`[consensus]`
- Any active guild that reaches the 750 chest weekly is enough; guild "level" matters less than everyone contributing.
- Token priority: chips you will equip → season relics (time-limited) → skins and menu themes (+0.6% coins each, permanent) → bits.
- `[consensus]` Spend tokens before the season ends: towerstats (currencies page, 7 Oct 2026) reports leftovers converting at 5 tokens to 1 gem. Check the season end in game before leaving a balance.
- Do not hop guilds mid-week; contribution and chest claims are per week.

## 5. Guardian

**Mechanics** `[mechanic]`
- Unlock: 200 bits, one chip slot, two chips (Ally, Attack). Second slot 200 bits, third 300. A fourth is listed as unavailable.
- Shop chips, 200 tokens each: Bounty, Fetch, Summon (season 5), Scout (season 7).
- Each chip has three separately levelled tracks (cooldown plus two stats), each with its own maximum. Level 1 is free. Maxing one chip costs roughly 13,000–14,500 bits.
- Chips cannot be changed during a run. It only fights with at least one chip equipped and while in a guild.
- Respec: 150 gems, once a week, refunds chip and slot bits (not the 200 unlock). The Vault lowers the price and, with Guardian Presets, removes the limit.
- Presets: Presets lab level 5 (35T coins) gives two; the Vault adds three. Switching presets costs or refunds the bit difference.

| Chip | Effect (base values) | Used for |
|---|---|---|
| Ally | Turns the nearest enemy into a recovery package that can heal past max recovery (120 s) | Health builds |
| Attack | Hits the most damaged enemies for a % of health already lost, half on bosses (120 s) | Damage, tournaments |
| Bounty | Marks non-common enemies to pay more coins (120 s) | Coins |
| Fetch | Finds loot: coins, gems, medals, shards, modules (120 s) | Steady side income |
| Summon | Spawns enemies twice a second while active and applies a cash bonus (140 s) | Coins when timed with GT/BH |
| Scout | All enemies count as farther away for damage (105 s) | Damage / meter builds, tournaments |

**Which chips first** `[consensus, thin; no tested v29 guide found]`
- Farming: Fetch (it pays in currencies nothing else farms: gems, medals, shards) and Bounty or Summon for coins. Summon is strongest when its cooldown is synced to Golden Tower and Black Hole, so it belongs with a synced farm; the GC guide lists "synced GT/BH/DW/GB/Summon".
- Tournament preset: Attack and Scout; Ally for health builds.
- Bit priority: slots 2 and 3 first (unlock plus both slots is 700 bits, about four weeks of full guild boxes), then cooldown and headline tracks of the chips actually equipped.
- Summon's cooldown is a sync value. Treat levelling it like a UW cooldown: decide the target first. `[consensus]`

## 6. Daily missions

`[mechanic]`
- Each completed mission: 3 gems, plus coins and module shards scaled to the **highest tier unlocked** (not the tier played). Tier 1 pays no shards.
- Weekly track, cumulative at 5 / 10 / 15 / 20 / 25 / 30 / 35 missions. A full week pays 185 gems, 135 medals, 45 stones, 35 guild tokens, and coins worth ×64 the tier coin value. Stones start at the 25-mission bracket.
- Reroll Daily Mission lab unlocks rerolls at 5 gems each; a reroll costs more than a mission pays, so it is only for reaching a bracket. Vault ▸ Harmony ▸ Modules: Free Mission Reroll (15 keys) and Daily Mission Shard Type (10 keys, choose the shard pool).
- Daily Mission Shards lab raises the shard reward.
- v29.2: new accounts start with 4 missions instead of 2.

`[consensus]` Finish 35 a week at every stage. It is the largest income that needs no run, and unlocking a higher tier raises the payout even if you farm a lower one.

## 7. Relics

`[mechanic]`
- A relic is a permanent account-wide bonus once **unlocked** (claimed). Equipping or displaying a relic does nothing to stats. A relic still in the mail pays nothing.
- **Stacking: relics of the same stat add together; the total multiplies with every other source.** Ten 2% damage relics are +20%, not ×1.219.
- 27 possible relic stats, including Lab Speed, Coin Bonus, Damage, Health, Defense %, Ultimate Damage, Enemy Attack/Health Skip, free upgrades and Bot Range (metres, additive).
- Relics count toward hard caps (Defense % 98).
- Sources: milestones (wave 4500 on a tier), tournament placement, event completion and event store, guild seasons, years played, gifts.
- Rarities: Rare, Epic, Legendary.

`[consensus]`
- Value order: **Lab Speed** (compounds over the whole account) → **Coin Bonus** → the stat your build is short of. Because same-stat relics add, each new one is worth less in relative terms as the pile grows; a first relic in a new stat can beat a tenth in an old one.
- Never skip a time-limited lab-speed or coin relic for a bot level.
- Gem relics (600 / 1,200) compete with modules and cards. Mid-game and later, a lab-speed or coin relic is usually worth it; cosmetic-stat relics are not.
- Published community totals for relic bonuses disagree with the game's own relic list; use the save readers (`run_extractor` / `read_save_field`, see `data-access.md`) for what an account really has.

## 8. Themes, skins and songs

`[mechanic]`
- Every **owned** theme pays a permanent coin bonus whether or not it is displayed. Per item: Tower theme +0.4%, Background +0.8%, Menu +0.6%, Guardian skin +0.6%. Milestone tower themes (wave 2500 of each tier) count as tower themes.
- The categories add together into one coin multiplier.
- Default themes pay nothing.
- Songs and profile banners pay +0.6% each. The game's stores print the bonus beside each one and the Themes screen total only matches with them counted (checked on screen, v29.2.2). They are inside the `themes` row of `coin_bonus`.

`[consensus]` Buy the event theme (and song) every event from Early onward. Each is small; a year of them is a large multiplier that never needs upkeep. Background themes pay the most per item.

## 9. The Vault

**Access and currency** `[mechanic]`
- Visible only after promotion to **Legend**. Everything costs keys. Keys come only from Legend (1–25 by rank; none for ranks 25–30) and Mythic (8–50) tournaments, twice a week.
- v29 rebuilt it into three tabs. A category is unlocked once with keys; upgrades inside can be bought in any order, except chained steps.
- One optional free respec exists per account (v29.0.2).

**Harmony (quality of life)** — category unlock in brackets `[mechanic]`
- Gameplay [0]: Auto Restart Run 20 · Ad Gem Stack 10/20/40/60 · Damage Cap Slider 25 · +3 Global Presets 20.
- Cards [5]: Additional Card Slot ×6 at 5/10/20/40/60/80 · Charge Berserker 5 · Demon Mode Automation 10, Smart 25 · Nuke Automation 10, Smart 25 · Death Ray Toggle 15 · Spawn Accelerator Toggle 20 (needs WA mastery) · Elite Balance Toggle 20 (needs EB mastery) · Life Saving Ordering 50 · Energy Shield Restriction 50.
- Ultimate Weapons [5]: Missile Barrage Automation 10, Smart 25 · Black Hole Size Slider 25 · Swamp Range Slider 25.
- Modules [5]: Auto Shatter Rare 5 · Daily Mission Shard Type 10 · Free Mission Reroll 15 · Module Reroll Discount ×8 (5 → 40 keys, 2.5% each) · +3 Module Presets 20.
- Bots [10]: Respec Discount 5/10/15 · Bot Presets 20 (+3 presets, removes respec limit) · Bot Range +2 m ×4 at 10/20/30/40 · Bot Cooldown Sliders 15.
- Workshop [10]: Respec Discount 5/10/15 · +3 Workshop Presets 20 · Enhancements Discount ×9 (2 → 18 keys, 2.5% each) · Workshop Orb Adjuster 15.
- Guardian [10]: Respec Discount 5/10/15 · +3 Guardian Presets 20.

**Power (tower stats)** `[mechanic]`
- Four categories, 25 keys each to open: Attack, Defense, Utility, Ultimate Weapons.
- Standard upgrade: five levels at 10/20/40/70/110 keys (250 total) for +5% per level on a multiplier stat.
- Notable exceptions: Ultimate Damage (all UWs) at 5/10/20/35/55; Defense % three levels at 20/40/70 for +0.5% each; Death Defy and Wall Rebuild at 20/40/80/140/220; Orbs +1/+2 at 20/40; Shockwave Frequency −1/−2 s at 20/40; Enemy Attack/Health Skip +0.5% ×3 at 20/40/80; Coins / Kill +5% per level; Golden Tower Bonus +1% per level; Max Recovery 20/40/60/80/100%.

**Enemy (Mythic)** `[mechanic]`
- Categories: Simple (0 keys), Advanced (50), Elites (100), Fleets (150). Game data requires Mythic as highest league reached for every Enemy category.
- Each enemy has three 30-level tracks (attack, health, a special), costing 25 keys rising to 103 per level: about 1% reduction per level. Basic enemies have a Coins/Kill special (+0.01 per level).

**Harmony or Power first?** `[consensus, reasoned from v29 costs; no published v29 key guide found]`
- Rule: buy what changes how you play before what adds a few percent.
- Typical first purchases, in rough order: Auto Restart (AFK farming) → Cards category and the first Additional Card Slots (5, 10, 20 keys: each is a whole extra card) → Demon Mode Automation and Smart Demon Mode, Smart Nuke (extra death saves that tournaments count as shields) → Damage Cap Slider for scaled-damage farming → Workshop Orb Adjuster → Bot Cooldown Sliders if bot labs overshot a sync → Module Reroll Discount and Enhancements Discount early levels (cheap, permanent).
- Power: open the category that matches the bottleneck. Ultimate Damage is the cheapest ladder (125 keys for +25% to all UWs). Coins / Kill in Utility pays back through every later purchase. The 110-key fifth levels are poor value next to first levels elsewhere.
- Later card slots (40/60/80 keys) and the 50-key toggles are Endgame.
- Presets from the Vault only add to presets the Presets lab already opened; research the lab first.
- towerstats' Vault page (19 Nov 2026) names the same openers: the extra card slots (215 keys for all six, and the only way past 22 slots), Auto Restart (20) and Smart Demon Mode / Smart Nuke (25 each).
- Because the first respec is free and later ones are not confirmed, plan the first 100 keys before spending. Compare options with `oracle_get` on the Vault entries.

Ranks 16–24 in Legend earn one key per tournament, about two a week. At that rate the Vault is slow; say so, and tie Vault plans to the player's realistic rank.

## 10. Tools

- Bot stat ceilings and names: `calc_run` `bot.statMaxLevel`, `bot.statNames`, `bot.findByName`.
- Guardian tracks and bounds: `guardian.definitions`, `guardian.statBounds`.
- Relics an event awards, by event name: `calc_run` `event.relicSet` `{name}`. The set spans every run of that event; a single event awards one edition only, so for the running event read `earnTrack` instead.
- Vault upgrade costs and values, relic lists, theme catalog: `oracle_get` / `oracle_map`.
- What the account owns (bots, chips, relics, themes, keys, medals, bits): the save readers (`run_extractor` / `read_save_field`, see `data-access.md`).
- UW cooldowns for sync targets: `uw.statValue` with stat "Cooldown".
- Irreversibility check before any cooldown advice: `oracle_footguns`.
