# Tournaments: leagues, rewards, builds and v29 changes

Verified against game version: v29.2.1 — 2026-11-20

Main sources
- SDK: `compartments/meta-game.ts`, `survival.ts`; `src/data/tournaments/data.ts` (leagues, rewards, heat profiles); `facts/v29.2.0/tournament-prizes.json`, `facts/v29.2.1/tier-battle-conditions.json`.
- Patch notes: v27.3 (Skip Decay, Skip Reduction – Multiply), v28.0 (Overheat), v29.0, v29.0.2, v29.1, v29.2.
- Fandom wiki "Tournaments" (rewards match the SDK; its battle-condition text is pre-v27.3).
- Community guides: Evan, "Small guide for new Legend tournament players (v28)"; DrAudacious, "Glass Cannon without Chrono Field" (Jan 2026). Both predate v29's tournament changes.

Tags: `[mechanic]` game rule · `[consensus]` community view · `[unverified]` unconfirmed or disputed.
Stages: New · Early · Mid · Late · Endgame.

## Contents
1. Decision rules at a glance
2. How tournaments work
3. Leagues, difficulty and rewards
4. Stones: why tournaments drive progression
5. Tournament vs farming priority by stage
6. Building for tournaments
7. Battle conditions and how to adapt
8. v29.x tournament changes
9. Common mistakes by league
10. Tools

---

## 1. Decision rules at a glance

- **Play every tournament, at every stage.** Two a week, one free ticket each. Power stones come almost entirely from here; keys come only from here. `[mechanic]`
- Placement is **highest wave reached** in the run. Coins, damage and time do not count. Build for wave, not income. `[mechanic]`
- Use a separate preset. A farm build leaves waves on the table; since v29 the Presets lab and Global Presets make switching free. `[mechanic + consensus]`
- Aim to stay out of the bottom six from Platinum up (ranks 25–30 demote and pay far less). Promotion is worth taking whenever you can hold mid-table above. `[mechanic-derived]`
- Read the Heat panel before starting. Adjust cards, target priority and survival cards to that day's conditions. `[consensus]`

## 2. How tournaments work

`[mechanic]`
- Unlock: Tier 1 Wave 60 milestone. Start Wednesday and Saturday 00:00 UTC. Brackets of 30 players.
- One free ticket per tournament; further tickets by watching an ad or with gems (10 for the first bought, +10 each after).
- A tournament **cannot be joined during an active run** at the pin. (v30 is planned to allow pausing a tier run; see `version.md`.) Plan farm runs to end before you want to enter.
- Ties: everyone tied receives the reward of the lowest rank in the tied group.
- Top 4 promote. From Platinum up, ranks 25–30 demote. Copper and Silver cannot be re-entered once left; Gold can (Platinum's bottom six drop into it).
- Tournaments are version-locked after each update; an outdated client cannot enter.
- Whether a second ticket replaces your score only if it is higher is `[unverified]`; the usual understanding is that the best run counts.

## 3. Leagues, difficulty and rewards

The table below lists selected rank bands, not every rank. For a band it skips, interpolate between its neighbours, say that it is an estimate, and cross-check against the account's own stone history.

`[mechanic]` Difficulty is "tier+": enemy stats (health, attack, mass, speed pressure) scale faster than the campaign tier of the same number.

| League | Tier+ base | Boss every | Random conditions | Always on |
|---|---|---|---|---|
| Copper | T1+ | 10 waves | 0 (no heat) | — |
| Silver | T3+ | 9 | 1 | — |
| Gold | T5+ | 8 | 2 | Skip Decay, Skip Multiply ×0.9, Wave Speed Up |
| Platinum | T8+ | 7 | 3 | + Death Defy Down **or** Energy Shields Down |
| Champion | T12+ | 6 | 4 | same; Skip Multiply ×0.6 |
| Legend | T17+ | 5 | 5 | same; ×0.45; fleet waves; keys |
| Mythic (v29) | T23+ | 4 | 6 | same; fleet waves; keys; Enemy vault tree |

Stones (and keys) by rank `[mechanic]`
| League | 1 | 3–4 | 5–6 | 9–10 | 13–15 | 16–22/24 | bottom |
|---|---|---|---|---|---|---|---|
| Copper | 20 | 16 | 12 | 9 | 7 | 6 | 5 |
| Silver | 40 | 30 | 20 | 18 | 16 | 14 | 12 |
| Gold | 80 | 60 | 40 | 28 | 24 | 22 | 20 |
| Platinum | 180 | 140 | 80 | 60 | 53 | 50 | 20 |
| Champion | 300 | 260 | 180 | 160 | 125 | 100 | 20 |
| Legend | 375 (25 keys) | 325 (15) | 275 (10) | 245 (6) | 215 (2) | 200 (1) | 100 (0) |
| Mythic | 475 (50) | 425 (40) | 400 (37) | 370 (31) | 340 (25) | 325 (20) | 225 (8) |

- "Bottom" is ranks 23–30 up to Gold and 25–30 from Platinum. Gems also rise with league (Copper 10–100, Mythic 335–900). Full tables: `oracle_get`.
- Reading the table: a safe mid-table finish one league up beats a podium below it (Platinum 16–24 pays 50, Gold 5–6 pays 40; Champion 16–24 pays 100, Platinum 5–6 pays 80; Legend 16–24 pays 200 plus a key, Champion 5–6 pays 180). The bottom six from Platinum to Champion pay 20, so yo-yoing between leagues roughly breaks even at best. v29 rebuilt the tables so deliberate demotion does not pay. `[mechanic-derived]`

## 4. Stones: why tournaments drive progression

`[mechanic]`
- UW unlocks cost 5 / 50 / 150 / 300 / 800 / 1,250 / 1,750 / 2,400 / 3,000 stones in the order bought (9,705 for all nine). UW stat levels, cooldowns included, cost stones and are permanent.
- Later stone sinks: UW+ unlocks (500 rising to 3,800; 14,650 for nine), card masteries (500–1,250 each; 28,500 total), assist modules (1,000 per slot to open; about 20,700 per slot type to finish), Bot+ (1,250 each), Synchronicity (1,500 per step).
- Other stone income is small: 45 a week from the daily-mission weekly track, event-shop packs for medals, milestones.
- So stone income ≈ league × rank × 2 per week. Moving from Gold mid-table (≈25) to Platinum mid-table (≈55) more than doubles it.

`[consensus]` Stones are the scarcest currency for most of the game. Every stone plan should say what it delays. Use `calc_run` `uw.stoneCost` for the real price of a UW target.

## 5. Tournament vs farming priority by stage

| Stage | Rule | Why |
|---|---|---|
| New | Enter with your normal build; no special investment. | Copper is decided by raw workshop levels. Coins spent on economy raise tournament waves too. |
| Early | Economy first. Make one cheap tournament card preset (swap economy cards for damage/survival). | Coin growth still lifts everything; stones needed are small (first UWs cost 5–300). |
| Mid | Start a real tournament preset: workshop preset if owned, modules, perks. Spend labs on tournament-relevant counters when stones become the bottleneck for syncing GT/BH/DW. | From the fifth UW each unlock costs 800+ stones and sync needs cooldown levels; league position now sets the pace. |
| Late | Split investment. Damage masteries, tournament modules and assist cores pay back in stones and, in Legend, keys. | The Legend guide warns serious Legend preparation can mean pausing economy growth for a while. Say this trade-off out loud. |
| Endgame | Tournament strength is the main goal; farming funds it. | Keys gate the Vault; Mythic roughly doubles keys. |

How to decide for one account `[consensus]`: list what is blocked. Blocked by coins (labs unaffordable, workshop not maxed) → farm. Blocked by stones (UW levels, masteries, assists waiting) → tournament. Compare the stones gained from the next rank band against the weeks of economy it costs.

## 6. Building for tournaments

**What changes from a farm build** `[consensus]`
- Cards: remove pure-economy cards (Coins, Critical Coin, Enemy Balance, Wave Accelerator, Cells). Keep Cash and Free Upgrades at the start; late in the run swap them for Land Mine Stun and Extra Orb. Add Damage, Attack Speed, Critical Chance, Range, Slow Aura, Plasma Cannon, Energy Net, Super Tower, Ultimate Crit, Berserker, Demon Mode, Energy Shield, Second Wind; Death Ray or Nuke fill spare slots. Health builds keep Health, Health Regen, Extra Defense early.
- Workshop: max everything reachable, including Range and Bounce Shot Range that farm builds hold down. Economy stats do nothing here except Cash (and cash only matters through in-run upgrades and Project Funding).
- Damage is not capped. Farm builds scale damage down to protect coin multipliers; tournaments want all of it.
- Modules (detail in `meta-modules-cards.md`): Amplifying Strike or Astral Deliverance · Anti-Cube Portal or Space Displacer · Project Funding · Dimension Core; assists Om Chip, Restorative Bonus.
- UWs: damage and control matter (Chain Lightning, Spotlight, Chrono Field, Inner Land Mines, Black Hole size/uptime, Poison Swamp). Golden Tower only helps through cash. Since v29.1 full-uptime GT/CF/BH/PS fire at run start.
- Perks: Perk Wave Requirement first on long runs; a flat Damage first perk on very short ones. Ban the 50/50-style and knockback trade-offs; avoid trade-offs that cut survival. `[consensus, GC guide]`
- Target priority in upper leagues: Ranged > Fast > Closest (Tank's Ultimate is common). `[consensus, GC guide]`
- Game speed: lower it late in the run and never open menus unpaused; fast enemies reach the tower during lag. `[consensus]`

**Death saves** `[mechanic]`
- Order consumed: Death Defy → Energy Shield → Second Wind → Demon Mode (needs Smart Demon Mode Automation from the Vault) → Nuke (needs Smart Nuke Automation). The Vault's Life Saving Ordering (50 keys) lets you reorder.
- Death Defy rolls before a shield charge is spent. If health is so high that nothing one-shots you, or Death Defy chance is low, shields carry the run instead. `[mechanic + consensus]`
- From Platinum one of Death Defy Down / Energy Shields Down is always active; which one varies. Do not build a run on only one of them.

**By stage** `[consensus]`
- New–Early (Copper–Gold): health build with thorns and orbs; biggest gains are workshop levels, Defense %, health labs and the right cards.
- Mid (Gold–Platinum): hybrid, health to survive plus enough damage to kill bosses arriving every 7–8 waves. Enemy speed and mass scale, so Slow Aura, knockback and Chrono Field gain value.
- Late (Champion–Legend): damage builds take over; glass cannon with Space Displacer, Energy Shield and Second Wind, or hybrid until the pieces exist. Reference targets from the v28 Legend guide: CL 6–9 quantity and 20–35% chance, SL 3 quantity at 45–55° with ×15–25 bonus, ILM 6–9 quantity at 2:30 cooldown; do not overspend on CL damage; Chrono Field only after attack speed, damage masteries and ILM are in place. `[consensus, v28]`
- Endgame (Legend–Mythic): CF 90% slow, SL+ (stop at +3 to +5), assists, fleet handling. Fleet waves do not time out since v29, so fleet kill speed is a hard gate.

## 7. Battle conditions and how to adapt

`[mechanic]`
- Copper has none. Above it, **heat** ramps with wave: your resistance to a condition is 95% effective at wave 0 and falls to 5% by wave 1000, so conditions bite hardest late. Silver uses a gentler ramp column than Gold and up.
- **More Bosses** is fixed by league (table above), no ramp.
- **Skip Decay** (v27.3, Gold up, fixed by league): enemy level skip chances lose 1% every 80 / 60 / 40 / 20 waves in Gold / Platinum / Champion / Legend.
- **Skip Reduction – Multiply** (v27.3): ELS chances × 0.9 / 0.75 / 0.6 / 0.45 in Gold / Platinum / Champion / Legend, reduced by the Skip Reduction lab and the general Battle Condition Reduction lab. Mythic's value: look up. `[unverified here]`
- **Skip Reduction – Subtract** (the old "ELS reduction 10/20/30/50%") is **not** in tournaments since v27.3. The wiki's Tournaments page and some guides still state it.
- Overheat conditions that can appear in tournaments (v28): More Fleets, More Elites, Damage Decay, Health Decay. Damage and Health Decay were removed from Legend and Mythic in 29.0.2.
- Legend guide note: UW Durations is a possible condition; Chrono Field duration at the higher breakpoint is described as making it immune. `[consensus, numbers in the guide]`
- Condition pool (game names): Orb, Death Ray, Thorns, Knockback and Plasma Cannon Resistance; Enemy Speed; Enemy Attack Speed; Armored Enemies; More Enemies; One Enemy Type; Wave Jumps; Mass Enforcement; Ultimate Weapon Durations; the enemy Ultimates (Basic's, Fast's, Tank's, Ranged, Boss's, Protector's, Elite's, Ray's, Scatter's, Vampire's, and the fleet ones). Which are in the random pool per league: check the Heat button; do not assume.

**Adapting** `[consensus]`
| Condition | Adjustment |
|---|---|
| Thorns Resistance | Thorn-reliant boss kills fail; lean on damage cards and Plasma Cannon. |
| Orb Resistance | Blender/orb defence leaks; add knockback, Slow Aura, Land Mine Stun. |
| Knockback Resistance / Mass Enforcement | Knockback builds weaken; rely on slow, stuns and raw damage. |
| Plasma Cannon / Death Ray Resistance | Drop that card for another damage or survival card. |
| Enemy Speed / Enemy Attack Speed | Slow Aura, Chrono Field, more range; health builds need more regen/defense. |
| Armored Enemies | Hit count matters; attack speed, multishot, bounce. |
| Ultimate Weapon Durations | Perma targets (pBH, pCF) may break; check uptime before relying on them. |
| Death Defy Down | Lean on Energy Shield and Second Wind. |
| Energy Shields Down | Lean on Death Defy (module substat, labs) and Second Wind. |
| Basic's Ultimate | Amplifying Strike gains over Astral Deliverance (Legend guide). |
| Tank's Ultimate | Target Ranged > Fast > Closest; keep tanks out of mine range. |
| Skip Decay / Multiply | Do not spend tournament cash on ELS if your chance is mostly cancelled. |

Long-term counters: the per-condition reduction labs and Battle Condition Reduction. They cost lab time, so rank them against economy labs by stage (Late onward for most accounts). `[consensus]`

## 8. v29.x tournament changes

`[mechanic]` unless marked.
- **Mythic league** above Legend (T23+). Legend promotes top 4 into it; Mythic's bottom six return to Legend.
- **Rewards rebuilt** (section 3). Legend stones per rank went down; Legend ranks 16–24 now earn 1 key.
- **Wave Speed Up**: unlimited Intro Sprint Mastery in tournaments without the card. Notes after release describe it for Gold and up. Waves keep skipping until the tower takes its first destroying hit; since 29.1 it only ends once all shields are used (Smart Demon Mode, Smart Nuke, Energy Shield, Second Wind). Effect: runs are shorter and the early game is skipped, so **permanent** power (workshop, labs, modules) matters more than cash built in-run. `[mechanic + consensus]`
- **Fleet waves** (Legend up): fleets spawn at wave start; the wave lasts until all fleets die; other enemies keep spawning; ties break on fleet health remaining.
- **Death-save limits (29.1, tournaments only)**: Demon Mode, Second Wind and Viking Funeral end after a maximum number of waves or a time limit, whichever comes first. Exact limits were not published. `[numbers unverified]`
- **Viking Funeral** (Berserker mastery) triggers on every death save.
- **Energy Shield and Wall take at least two waves to recharge** in tournaments.
- **Decay conditions** removed from Legend and Mythic (29.0.2).
- **Presets**: Global Presets can bind a tournament loadout (cards, workshop, bots, modules, guardian).
- **Full-uptime UWs fire at run start** (29.1).
- **29.2**: Defense % perk no longer offered at 98%; Scatter splits are tankier; CL+ Smite capped at 100; a practice pseudo-tournament for new players.
- Ban waves and anti-cheat work in 29.1 changed some leaderboards.

What this means for old advice `[consensus]`
- Chaining Demon Mode and Second Wind to coast for hundreds of waves no longer works in tournaments. Count each save as a short window.
- The Intro Sprint card and mastery are not tournament purchases any more.
- Tanking through fleet waves on a timer is over; without the damage to kill fleets the run stops there.
- Sandbagging for rewards is dead.

## 9. Common mistakes by league

`[consensus]`
- **Copper–Silver (New)**: skipping tournaments; entering mid-farm-run and losing the entry window; running Coins/Enemy Balance/Wave Accelerator; buying extra tickets with gems needed for lab slots.
- **Gold (Early)**: no tournament preset; ignoring the Heat panel; holding back to avoid promotion (Platinum ranks 16–24 pay 50 stones, more than Gold ranks 5–6 at 40); spending in-run cash on ELS that Skip Multiply cancels.
- **Platinum (Mid)**: relying on a single death save while the matching "Down" condition is active; health-only builds that cannot kill bosses every 7 waves; UW cooldown levels bought for tournaments that break the farm sync (see `footguns.md`).
- **Champion (Late)**: staying on eHP too long; over-investing stones in CL damage instead of quantity/chance and Spotlight; no Battle Condition labs; finishing 25–30 repeatedly (20 stones) instead of fixing the build.
- **Legend (Late–Endgame)**: buying Chrono Field levels before damage masteries, attack speed and ILM are ready; SL+ beyond +5; expecting Vault progress from ranks 16–24 (two keys a week); fleet waves ending runs.
- **Mythic (Endgame)**: applying Legend key maths (Mythic pays 8–50 keys); ignoring the Enemy vault tree; assuming death saves last as long as before 29.1.
- **Any league**: comparing wave counts across leagues or patches; copying a top player's build without their labs; changing UW cooldowns for one tournament.

## 10. Tools

- League, rank history and tickets for the account: the save readers (`run_extractor` / `read_save_field`, see `data-access.md`).
- Reward rows, heat profiles, battle-condition definitions: `oracle_get` / `oracle_map` (system "tournament").
- Enemy scaling at a wave: `calc_run` `enemy.healthWave100Multiplier`, `enemy.damageWave100Multiplier` (with the tournament flag), `enemy.bossWaveInterval`.
- Stone prices for targets: `uw.stoneCost`, `uw.statValue`, `uw.maxLevel`.
- Patch changes since the pin: `patch_notes` (see `version.md`).
