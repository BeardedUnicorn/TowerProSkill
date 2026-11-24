# Account assessment: from raw export to diagnosis

Verified against game version: v29.2.2 — 2026-11-20, updated 2026-11-24

This file is the method, not the playbook: how to turn what the readers return into (1) a stage, (2) a
dominant bottleneck, and (3) a short ranked list of moves. The stage thresholds are `[consensus]`
heuristics for orienting yourself — an account's own numbers always outrank them. Reader and field names
are in `data-access.md`.

## Contents
1. Stage ladder (S0–S5) and how to place an account
2. What matters most at each stage, and the classic mistakes
3. The account sheet: what to extract before judging
4. Reading the run history
5. Bottleneck diagnosis
6. From diagnosis to a ranked list
7. Things the export cannot tell you — ask

---

## 1. Stage ladder

The other reference files use these keys. Some use names instead: **New = S0, Early = S1, Mid = S2–S3,
Late = S4, Endgame = S5.**

| Stage | Farming tier (typical) | Ultimate weapons | Labs | Modules | Tournaments | Other signals |
|---|---|---|---|---|---|---|
| **S0** New | T1–T3 | none | 1–2 slots | none / commons | not yet or Copper | few card slots, workshop far from caps |
| **S1** Early | T2–T6 | 1–2 (first picks) | 2–4 slots | rares, first epic | Copper–Silver | Golden Tower / Black Hole / Death Wave not all owned |
| **S2** Early-mid | T5–T10 | 3–4, GT+BH+DW coming together | 4–5 slots | epics, first legendary | Silver–Gold | sync not yet achieved; workshop core stats climbing |
| **S3** Mid | T10–T13 | 5–8, GT/BH(/DW) synced | 5 slots | legendary, first mythic | Gold–Champion | workshop mostly maxed, enhancements started, masteries not yet |
| **S4** Late | T14–T18 | all nine, first UW+ | 5 slots | mythic, first ancestral | Champion–Legend | card masteries, assist modules, fleets appear (T14+) |
| **S5** Endgame | T19+ | all nine, several UW+ | 5 slots | ancestral with stars | Legend–Mythic | Vault well advanced, masteries deep, Bot+ |

Placing an account:

- Use the **farming tier actually farmed** (the modal tier of recent non-tournament runs) more than the
  highest tier ever reached. A player can have cleared T14 once and still be an S3 account that farms T11.
- Signals often disagree — that is information, not noise. Take the stage most signals agree on and name
  the outliers explicitly: "S3 economy with S1 modules" tells you where the gap is, and the lagging system
  is usually where the cheapest gains are.
- Judge modules by what they are, not the rarity label: four Legendary modules merged up from rares (no
  unique effects) are an S1 module setup, not S3. See `data-access.md` § quirks for telling them apart.
- Paying accounts run ahead on modules/cards/gems relative to labs and workshop (time-gated). Don't infer
  stage from module rarity alone. `readPurchasesFromSaveRoot` shows pack ownership; note it neutrally —
  packs multiply coin income, so absolute coins/hour comparisons against guides shift with them.
- Account age helps calibrate pace (`readLifetimeFromSaveRoot`): a young account at S2 is on a different
  trajectory from an old one.

## 2. What matters most, and classic mistakes

Each line is `[consensus]` unless tagged. Details live in the meta files named in brackets.

**S0 — New.** What matters: getting an economy at all — coin utility in the workshop, lab slots, card
slots with gems, first UW via tournaments. Farm the tier that gives the best coins/hour, not the highest
one reachable. Mistakes: spending gems on anything but lab slots/card slots; raising Range; pushing tiers
instead of farming; skipping tournaments (stones are the scarcest input for the whole game).
[meta-economy, meta-workshop-labs]

**S1 — Early.** What matters: the first UW picks (permanent — see `footguns.md`), keeping every lab slot
busy, coin-per-kill and lab speed research, joining a guild for the guardian and weekly rewards. Mistakes:
picking UWs for damage before the economy trio; idle lab slots; spreading stones thinly across stats;
unlocking the Wall early. [meta-ultimate-weapons, meta-workshop-labs, meta-bots-guardian-vault]

**S2 — Early-mid.** What matters: bringing Golden Tower, Black Hole and Death Wave into a cooldown sync and
growing their coin multipliers; filling card slots; the first good epic modules; moving the farming tier up
only when coins/hour says so. Mistakes: lowering one cooldown in isolation and breaking the path to sync
`[mechanic: cooldown levels are permanent]`; pulling modules off-banner; chasing wave records.
[meta-ultimate-weapons, meta-modules-cards, meta-economy]

**S3 — Mid.** What matters: finishing the workshop and starting enhancements, perma/sync targets, a real
farming build (devo or blender by how attended the play is), Dissonant Runs as free compounding, module
substats and legendary+ merges, climbing leagues for stones. Mistakes: staying on a comfortable tier after
the economy has outgrown it; ignoring Dissonance; rerolling substats on modules about to be replaced; no
separate tournament preset. [meta-economy, meta-modules-cards, meta-tournaments]

**S4 — Late.** What matters: the transition away from orb-carried farming as orb resistance sets in from
T14 `[mechanic: battle condition]`, the remaining UWs and first UW+, card masteries (stones), assist
modules, Vault keys, fleet handling. Mistakes: spending stones on masteries with little effect on the
actual build; neglecting damage until tournaments stall; unfocused key spending.
[meta-ultimate-weapons, meta-modules-cards, meta-bots-guardian-vault, meta-tournaments]

**S5 — Endgame.** What matters: marginal-return comparison across very expensive options (UW+ levels,
masteries, ancestral stars, enhancement caps, Bot+), tournament placement in Legend/Mythic, long lab
chains. Mistakes: not pricing options against each other; guides written before the current patch.
Lean hardest on the calculators here — intuition is weakest when every option costs weeks.

## 3. The account sheet

Fill this in before forming an opinion. If a line can't be filled, it goes under "gaps".

| Area | Extract | Reader(s) |
|---|---|---|
| Identity | game build/version, export time, account age | ExportInfo, Lifetime |
| Progress | best wave per tier, highest tier, milestones claimed | TierRecords, Milestones, EffectivePathsSettings |
| Currencies | coins, gems, stones, medals, cells, keys, bits/tokens, shards by type, reroll shards | Currencies, Modules, Vault |
| What each balance can open | next workshop unlock per tab (coins), next UW and UW+ (stones), Rush price of each running lab (gems), and whether the balance covers it | `next_unlocks` |
| Coin multiplier | Total Coin Bonus rows at the farming tier; which rows sit at x1; the same at a candidate tier | `coin_bonus` (and `coin_bonus {tier}`) |
| Workshop | levels vs caps for attack/defense/utility, enhancements, which presets exist and what they are for | Workshop, WorkshopUnlocks, GlobalPresets |
| Labs | slots unlocked, **what is running in each and time left, any empty slot**, levels of the high-value labs, lab speed, total researched/maxed | Labs |
| Ultimate weapons | which are owned, each stat level, cooldown and duration per UW, UW+ unlocked/levels | UltimateWeapons |
| Cards | slots unlocked, card levels, equipped set per preset, masteries, what the next card purchase can draw | Cards, CardDrawOdds |
| Modules | equipped per slot with rarity and substats, slot levels, inventory worth merging, assist slots, pity counters, bans | Modules, ModuleEconomy |
| Bots | owned, levels, cooldowns (medals vs labs), Bot+, synchronicity | Bots, BotSynchronicity |
| Guardian | unlocked, in a guild or not, chips and levels, equipped | Guardians |
| Vault | keys held/earned, nodes unlocked and levelled | Vault |
| Relics / themes | count unlocked, notable missing ones, themes owned (passive coin bonus) | Relics, Themes, CollectedThemeNames |
| Perks | bans, first-perk choice, auto-pick order | PerkChoices |
| Tournaments / events | current and highest league, recent results, event medals, what the event shop sells now | Tournaments, Events, EventShop |
| Dissonance | which boosts are earned and at what wave, whether Dissonant Runs are being done at all | `calc_run save.readDissonanceBoostWavesByType` (savePath), run `dissonanceType` |
| Runs | the last 30 runs, in full | battle history |
| Settings | target priority, range selection, orb distances, life-saving order | RuntimeControls |

Compute UW sync yourself rather than eyeballing: take each UW's current cooldown and duration (stat levels
→ `calc_run uw.statValue`, plus lab/module/perk modifiers the account has), then check (a) the ratio
between GT, BH and DW cooldowns — integer ratios keep activations aligned — and (b) duration ≥ cooldown for
perma. Perma is only defined for UWs that have both stats (`glossary.md`).

## 4. Reading the run history

Split runs into farming, tournament and Dissonant (`isTournament`, `dissonanceType`) before any statistic;
mixing them makes every median meaningless. Then, per group and per tier:

- **Income**: coins/hour and cells/hour per run = earned ÷ **real** time (the player's actual clock).
  Report the **median** over recent runs and the spread. `battle_history`'s own `coinsPerHour` is a mean of
  the three best runs — a peak, useful as "what the build can do", not as income.
- **Tier comparison**: if runs exist on more than one tier, compare median coins/hour and cells/hour
  across them. That comparison — not the highest wave — decides the farming tier. If only one tier
  appears, say that the comparison can't be made and suggest a test run one tier up or down.
  `coin_bonus {tier}` tells you the multiplier a neighbouring tier would give before the test run: use
  it to say how much shorter the run may get and still come out ahead.
- **How runs end**: tabulate `killedBy` and the death wave. A consistent killer at a consistent wave is a
  wall you can name and address; scattered causes suggest a build that simply runs out of scaling.
- **Uptime**: the share of the clock the tower is actually in a run. Sum real run time over the window the
  30 runs span and divide by that window; also count runs per day. Daily income = coins/hour × hours in a
  run, so an account that is in a run a third of the day has a bigger lever in "start another run" than in
  any upgrade. This is often the largest single finding — compute it every time.
- **Run length**: real hours per run vs how the player plays (overnight, attended). A run that ends after
  3 hours wastes an 8-hour night; a 14-hour run wastes the time between restarts if nobody is there.
- **Coin sources**: share of coins from GT, BH, DW, Spotlight, wave skip, coin upgrades, bots, guardian.
  Low share from a UW the account has invested in means the kills aren't happening inside it (range, sync
  or uptime problem). See meta-economy § reading the coin lines.
- **Damage and kill mix**: which sources actually kill (orbs, projectiles, thorns, land mines, chain
  lightning, UWs). This tells you the real build archetype regardless of what the workshop looks like.
- **Survival lines**: damage taken, what blocked it (defense %, absolute, shield, wall), regen and
  lifesteal, death defy/second wind use. A health build whose mitigation lines are small relative to
  damage taken is under-defended; a damage build taking almost nothing is fine.
- **Trend**: are wave and income rising across the 30 runs? Flat for weeks with coins banking up means
  spending is the problem, not the build.

## 5. Bottleneck diagnosis

Pick the one that best fits; it becomes the report's headline.

| Bottleneck | Looks like | Usual direction |
|---|---|---|
| **Economy-limited** | Runs are long and stable, labs/workshop upgrades wait on coins, coins/hour flat, coin UWs under-levelled or out of sync, coin labs/cards/perks behind, not using Dissonance | Raise coin multipliers before anything else; check farming tier; fix sync. |
| **Survival-limited** | Runs end early on the farmed tier at a repeatable wave to a repeatable killer; income per hour is fine while alive but runs are short; moving up a tier collapses income | Defense/health/regen/wall labs and workshop, the right defensive cards and module, or drop a tier if that earns more per hour. |
| **Damage-limited** | Bosses or fleets leak, runs end by being overrun late rather than burst down; tournament placement stalls while farming is fine; kill mix leans on a source that stops scaling (orbs at T14+) | Damage labs, attack workshop/enhancements, damage UWs and their sync, cannon module, tournament preset. |
| **Time/lab-limited** | Coins pile up unspent, workshop near caps, every useful lab is days-to-weeks long; or slots sit idle / run cheap filler | Lab speed, slot count, queue discipline, cells for speed-ups on the long chains; choose labs by value per day, not per coin. |
| **Stone-limited** | Clear UW targets exist but stone income (league results) can't fund them | Tournament performance is the lever: preset, cards, league strategy. |
| **Attention-limited** | Unclaimed missions/events, missed tournaments, idle slots, banked gems/medals with obvious uses, stale export | Routine fixes first — they are free. |

Check which lab slots are **empty right now** before anything else. An empty slot is the most common and
cheapest fix there is.

Sanity-check the diagnosis against the bank balances: an account that is "economy-limited" while holding a
huge coin balance isn't — it is undecided or time-limited.

## 6. From diagnosis to a ranked list

1. List candidates that relieve the bottleneck (from the matching meta file), plus any free fixes.
2. Price each one for this account (`calc_run`), and convert to time at the account's median income: coins
   ÷ coins/hour, stones ÷ stones per week from the current league, lab days at current lab speed.
3. Estimate the payoff in the unit of the bottleneck (income multiplier, waves survived, damage
   multiplier, days saved). `plan_effective_path` can order economy/damage/health/regen purchases; check
   its starting levels and read what it left out. Where the payoff can't be quantified, say so and rank by
   reasoning.
4. Rank by payoff per unit of the constrained resource. Different currencies don't compete — coins, stones,
   gems, medals, keys and cells each get their own best use — so "do now" can hold one move per currency.
5. Apply the permanence filter (`oracle_footguns`, `footguns.md`): when two options are close, prefer the
   reversible one, and state clearly when a recommended move is permanent.
6. Keep one to three "do now" moves. Everything else is "save toward" or "ignore for now" — naming what to
   ignore is half the value.

## 7. What the export cannot tell you

Ask once, briefly, when the answer would change the advice:

- Goal: maximise farming income, push tiers/milestones, or climb tournament leagues?
- Play pattern: how long do runs go unattended, how many runs a day, is the device left on overnight?
- Spending: free-to-play or not, and whether upcoming purchases should be assumed (never suggest any).
- Which preset each recent run used, if presets aren't labelled in a way that makes it obvious.
- Anything only visible on screen: current banner, event shop stock, guild status details.
