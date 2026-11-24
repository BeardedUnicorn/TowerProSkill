# Footguns: irreversible decisions and classic traps

Verified against game version: v29.2.2 — 2026-11-20, updated 2026-11-24

Main sources
- SDK: `compartments/footguns.ts` (permanence rules kept apart from opinion), `modules.ts`, `bots.ts`, `vault.ts`, `guardian.ts`, `masteries.ts`; `facts/v29.2.1/vault-upgrades.json`.
- Fandom wiki "Footguns" (Category:Guides; mixes rules and advice), "Medals Guide", "Gem Guide", "Guardian".
- Patch notes v29.0–v29.2. Community guides by Evan (Legend, v28) and DrAudacious (glass cannon, Jan 2026).

## Contents
1. How to use this file
2. List A — objective permanence facts
3. What can be respecced, and how
4. List B — community-opinion traps
5. Warning templates
6. Pre-recommendation checklist

---

## 1. How to use this file

Two lists, kept separate on purpose.

- **List A** is `[mechanic]`: what the game will not let a player undo. State these as facts.
- **List B** is `[consensus]`: things experienced players regret. State these as community judgement, with the reasoning, and let the player choose.

Mixing them causes two errors: presenting an opinion as a rule ("never level BH cooldown"), or dropping a rule because it arrived wrapped in advice. Reversibility belongs to the **source** of a number, not the stat: the same bot cooldown is undoable if it came from medals and permanent if it came from a lab.

A footgun is different from a slow choice. Unlocking lab slots late or skipping a tournament costs time; a footgun costs options.

Before recommending any upgrade to a real account, call the MCP `oracle_footguns` and check the account's current levels in the save readers (`data-access.md`).

## 2. List A — objective permanence facts

### A1. Ultimate weapon picks are permanent `[mechanic]`
- What: each UW unlock is final. The price depends on how many are already owned: 5, 50, 150, 300, 800, 1,250, 1,750, 2,400, 3,000 stones.
- Why it hurts: a weak early pick is paid for by a later, much more expensive unlock. It self-corrects only by owning all nine (9,705 stones).
- v29.2 added a preview and a cancel option to the selection flow, so a mis-tap is less likely. The pick itself is still final.
- Wording: "This choice cannot be changed, and your next unlock will cost N stones. Let's check what each option does for your build before you confirm."

### A2. Ultimate weapon stat levels are permanent, cooldown included `[mechanic]`
- What: every stone spent on a UW stat stays there. There is no UW respec.
- Why it hurts: damage, bonus and duration levels are only ever "more". **Cooldown is the exception in effect**: a lower cooldown can break a sync with another UW or a bot, and it cannot be raised again.
- Floors at maximum: Black Hole 50 s, Death Wave 50 s, Golden Tower 100 s (2:1 against bots at 50 s).
- Wording: "Cooldown levels cannot be undone. Before you buy this one, here is what your GT, BH and DW cooldowns become and whether they still line up."

### A3. Lab research is permanent `[mechanic]`
- What: a completed lab level cannot be removed.
- Exception stated by the wiki: "range" can be turned off. The SDK records this as the one lab exception but its own notes disagree on whether that means the tower Range lab or Chrono Field Range `[unverified]`. Several labs have in-game sliders (v27.3 added a "Slider" filter to the research list); check the lab in game before telling a player a level can be dialled back.
- Why it hurts: almost every lab is harmless to over-level. The known exceptions are below (A4) and anything that enlarges the play field (List B1).

### A4. Bot cooldown labs are permanent; bot medal levels are not `[mechanic]`
- What: each bot's Cooldown lab removes 1 s per level (25 levels). Medal cooldown levels remove 3 s each (15 levels) and return on a bot respec.
- Why it hurts: bots are synced to the UW cooldowns at 2:1 or 1:1. Lab levels past the target leave a bot that cannot be matched by respeccing medals. The wiki's example: a 69 s Multiverse Nexus sync cannot be matched by a maxed Golden Bot.
- Only recovery: Vault ▸ Harmony ▸ Bots ▸ Bot Cooldown Sliders (15 keys, after the 10-key category unlock). That needs Legend league.
- Wording: "Medal cooldown levels come back if you respec. Lab cooldown levels never do. What cooldown are GT and BH heading for? We should stop the lab at half of that."

### A5. Merging destroys the fodder `[mechanic]`
- What: in a merge the **first** module selected keeps its substats. Every other module is consumed with its substats.
- Why it hurts: merging a well-rolled copy into a poorly rolled one deletes the good rolls; no cost model shows the loss.
- An Unmerge Module lab exists; what it returns is `[unverified]`. Treat merges as final.
- Since v29 levels are on the slot, so a merge no longer risks levels.

### A6. Reroll shards, gems on pulls and stones are never refunded `[mechanic]`
- Rerolls: shards are spent whatever comes out. Cost climbs with locks (40 → 3,000).
- Pulls: gems are deducted before the roll.
- Stones spent on masteries, UW+, assist slots, assist efficiency, Bot+ unlocks and Synchronicity have no respec. (A Bot+ unlock survives a bot respec; only its medals return.)

### A7. Mastery lab time `[mechanic]`
- A mastery lab level occupies a research slot for 20.8 days (level 1) up to 104.2 days (level 9) before lab speed, and that slot researches nothing else meanwhile.
- A mastery bought during a run does not apply to that run (v29.1).

### A8. Time-limited items `[mechanic]`
- Event-store medal relics return only on event re-runs; guild season relics only if the season re-runs.
- Guild chests are per week; an unclaimed week is mailed (hardened in v29.2), but a week with no contribution is lost.
- Featured banners end on a date.

### A9. Guardian needs guild membership `[mechanic]`
- Since v29.1 chips do nothing while the player is not in a guild. Leaving a guild before a tournament or farm run silently removes Bounty, Summon, Scout and the rest.

### A10. Vault purchases `[mechanic]`
- Keys were refunded once at v29 and one optional free respec exists per account (v29.0.2). Do not assume any further respec. Some upgrades require a card or mastery the player may not own (Elite Balance Toggle needs the Enemy Balance mastery; Spawn Accelerator Toggle needs the Wave Accelerator mastery).

## 3. What can be respecced, and how

| Thing | Undo | Limits / cost `[mechanic]` |
|---|---|---|
| Workshop coin upgrades | Workshop respec | Costs gems (Vault discount 33/66/100%). Since v29, Workshop presets (Presets lab level 2, 35M coins) switch for free. |
| Bot medal levels (including Bot+ medal levels) | Bot respec | Once per event (enforced since 29.0.2); Vault Bot Presets removes the limit; Vault discount on gem cost. Bot presets from Presets lab level 3 (3.5B coins). |
| Guardian chip levels and slots | Guardian respec | 150 gems, once a week; refunds bits except the 200 unlock. Vault lowers the cost and, with Guardian Presets, removes the limit. Presets from lab level 5. |
| Module choice per slot | Swap freely | Free since v29; module presets from lab level 4 (350B coins). |
| Module substats | Reroll | Shards not refunded; locked substats stay. |
| Cards equipped | Card presets | Free; cards lock while a boss or fleet is alive. |
| Perk bans, target priority, toggles, sliders | Change any time between runs | — |
| Bot cooldown from **labs** | Only via Vault Bot Cooldown Sliders | Legend-gated. |
| Vault | One free respec | Per account. |
| UW picks, UW stats, lab levels, stones spent, merges | **None** | — |

Exact gem prices for respecs: read in game or `oracle_get`; do not quote from memory.

## 4. List B — community-opinion traps

All `[consensus]`. Each entry: what, why it hurts, how to word it.

### B1. Range and zoom-out effects
- What: anything that enlarges the field (Chrono Field Range lab, more tower Range) zooms the camera out; enemies spawn farther away and take longer to arrive and die. Farm builds that place orbs on the range line (the classic 69.5 m set-up) depend on a specific range.
- Why it hurts: coins per hour drop slightly; an orb-line farm stops working if range moves.
- The mechanical effect is `[mechanic]`. The verdict is opinion: the wiki argues the CPH loss from CF Range is small and outweighed by tournament value, and recommends maxing it anyway. Glass cannon guides hold Range low for farming and raise it for tournaments through presets.
- Wording: "More range zooms the view out and can lower farm income a little. Most experienced players still take CF Range for tournaments. Your farm build uses the range line, so let's check your orb set-up before changing range."

### B2. Breaking a sync by over-levelling one cooldown
- What: levelling Black Hole cooldown while Golden Tower lags, or the reverse. Also any cooldown bought "for uptime" without checking the pair.
- Why it hurts: the coin bonus is largest when GT and BH overlap fully. A BH cooldown ahead of GT makes the 1:1 match more expensive to reach. It self-corrects only when GT catches up or both are maxed (BH 50 s, GT 100 s, 2:1).
- The wiki's advice: head for natural sync, at least 3:20 on both, and keep dropping stones into it even while using Multiverse Nexus. Core-module cooldown substats shift the same numbers.
- Other UWs matter too: some strategies need Smart Missiles or Death Wave on a specific timing.
- Wording: "Lower is not always better here, and it is permanent. With this level your BH would fire every X s and GT every Y s, so they overlap only every Z. The usual advice is to bring them level first."

### B3. Multiverse Nexus as "training wheels"
- What: MVN forces GT, BH and DW to fire together at their average cooldown plus an offset: +20 s Epic, +10 s Legendary, +1 s Mythic, −10 s Ancestral. `[mechanic]`
- Why it hurts: below Mythic it adds seconds, so total uptime is lower than a natural sync; players lean on it and stop investing in real sync, then cannot leave the Core slot.
- Opinion, not measurement: the wiki calls it a minor footgun until Mythic and tells players to use it while still working toward natural sync. For a specific account, compute both cases instead of repeating the slogan.
- Wording: "MVN gets you a sync today, at a cost of N seconds per cycle at your rarity. The common view is to use it as a bridge and keep levelling GT and BH toward a natural match."

### B4. Wasting gems
- What: gems on lab rushing early, extra tournament tickets, daily-mission rerolls for their own sake (5 gems to earn 3), card slots with no card to fill them, module pulls before lab slot 5, event-shop gem packs bought with medals after labs are unlocked.
- Why it hurts: gem income is capped by real time (20 daily, 6 per ad gem up to 60 a day, missions, tournaments). Lab slots and the first card slots are worth more than anything else early.
- Wording: "Gems are time-limited. At your stage the community order is lab slots, then the core cards and slots. This purchase would delay lab slot N by about M days."

### B5. Banner chasing
- What: emptying gems into a featured banner for a module the build cannot use yet (a Core whose UW is not owned), or, for accounts with most old epics at 5★, chasing each new module on its own banner.
- Why it hurts: 2.5% epic rate; duplicates are needed for rarity. SDK estimate for maxed accounts: about 51% more gems than waiting for the standard pool.
- Wording: "This module needs UW X, which you do not own. I would keep pulling at your normal rate. If you do want it, here are your real odds from the drop-rate panel."

### B6. Levelling the wrong thing on modules
- What: rerolling substats on Epic-rarity modules; locking mediocre rolls early; shattering natural epics or rares still needed as fodder; assuming a merged-to-epic rare has a unique.
- Wording: "Substat quality is capped by the module's rarity, so heavy rerolling now buys rolls you will replace. Light rerolls only, until this one is Legendary or better."

### B7. Bots
- What: unlocking every bot before levelling any; medals into cooldown before a sync target exists; levelling Thunder Bot halfway (it can disrupt builds at low level); skipping time-limited relics for bot levels.
- Wording: "Bots are weak at level 0. The usual order is Golden Bot range and bonus first. I would leave cooldown alone until we know your GT/BH target."

### B8. Unlocking workshop features too early
- What: the Wall on a health build (older guides say it actively hurts health builds), Land Mines (adds perks to the pool), Rend Armor and Super Crit before they are affordable. Each unlock also adds upgrade lines and perk options.
- Status: `[consensus, older guides, v23–v27]`; re-check for the player's build. A workshop respec undoes the coin cost but not the unlock's side effects in every case `[unverified]`.
- Wording: "Some unlocks change your perk pool or defence behaviour. For your build the older advice is to wait on X. Let's check that it still applies."

### B9. Stone sinks in the wrong order
- What: CL damage instead of CL quantity/chance; SL+ beyond +5; Chrono Field before damage masteries and ILM are ready (Legend guide); stone packs for medals at escalating prices; Synchronicity or assist efficiency while UW sync is unfinished.
- Wording: "Every stone here is permanent. Let me price the alternatives so you can see what this delays."

### B10. Tournament habits made obsolete by v29
- Sandbagging for rewards; buying Intro Sprint for tournaments; planning runs around long Demon Mode / Second Wind chains. See `meta-tournaments.md`.

### B11. Leaving farm on autopilot
- What: farming the highest tier reachable instead of the best coins per hour; no Auto Restart or presets when available; ignoring daily missions and the guild box; letting guild tokens sit past the season end; leaving a row of the Total Coin Bonus at x1 that is cheap to raise (`coin_bonus` shows the rows).
- Not irreversible, but it compounds. Raise it as an efficiency note, not a warning.

## 5. Warning templates

Match tone to permanence.

- **Permanent and about to happen (List A)** — direct, one sentence of fact, one of consequence, one check:
  "That cannot be undone. [What changes.] Before you do it, can we check [the paired value]?"
- **Opinion trap (List B)** — attribute it and give the reason:
  "Most experienced players avoid this because [reason]. It is a judgement, not a rule; in your case [what the numbers say]."
- **Already done** — no blame, state the way out:
  "That is locked in. It is recoverable: [GT catching up / the Vault slider / owning all nine UWs]. Here is the cheapest route."
- **Uncertain or newer than the pin** — say so:
  "My notes are from v29.2.2 and I could not confirm this for your version. Please check the in-game description before spending."

Do not stack warnings. One footgun per recommendation, the one that applies. Never invent a number in a warning; compute it (`calc_run`) or leave it out.

## 6. Pre-recommendation checklist

1. Does the recommendation spend stones, a UW pick, a lab level on a bot cooldown or range, or a merge? → List A applies; add the fact and the check.
2. Does it change any cooldown (UW stat, core substat, bot, Summon chip)? → compute the resulting pair with `uw.statValue` and state the sync before and after.
3. Is the source respeccable (section 3)? → say so; a respeccable choice needs no warning.
4. Is the claim opinion (List B)? → attribute it and explain why.
5. Is the export newer than v29.2.2? → follow `version.md` before asserting permanence rules that a patch may have changed.
