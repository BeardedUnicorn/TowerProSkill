# Version pin and freshness protocol

Verified against game version: **v29.2.3** (build 1301; patch note dated 2026-11-24)
Reference files written: 2026-11-20, updated 2026-11-25
Verified against SDK: `@beardedunicorn/thetowersdk` **1.7.2**

Main sources
- SDK knowledge base (`TheTowerSDK`): `facts/v29.0.0`, `facts/v29.2.0`, `facts/v29.2.1`, `facts/v29.2.2` (286 on-screen readings of the live game, 2026-11-24, and the Milestones screen for tiers 1–15), compartments, and the patch-note archive (261 notes, 2021-07-15 to 2026-11-24, ingested from the official announcement channel). SDK 1.7.2 checked a build-1301 export (2026-11-25) field by field and re-read the vault, card, daily-mission and bot tables from that build; no screen was re-read, so the newest on-screen check is still the v29.2.2 one.
- techtreegames.com blog: v29.2 preview (Nov 13), v29.2.1 notes (Nov 19), Tower Tea Oct 26, Nov 9 and Nov 23, 2026, 2026 Black Friday sale post (Nov 23).
- Store listings read 2026-11-25: Google Play (version 29.2.3, updated Nov 23) and the App Store version history (29.2.3, Nov 24).
- Community strategy re-read 2026-11-24: towerstats.org guides (pages updated 18–19 Nov 2026), tower-hub.com (pages verified Jul–Nov 2026), and one Legend player's notes (hiro29 on note.com, Aug–Sep 2026; single author). Re-checked 2026-11-25: no new towerstats posts after Nov 21, and tower-hub's relic tier list had not yet rated the Howling Wolf event.
- Fandom wiki: reachable in a browser on 2026-11-25, but its Version History stops at 29.1.2. Pages re-read by the SDK on 2026-11-18 (Modules, Tournaments, The Vault, Guardian, Currency).
- Not reachable: r/TheTowerGame (blocked for the browser on 2026-11-25), the official Discord, YouTube. No first-hand Reddit or Discord text is in these files.

## Contents
1. What the pin means
2. v29.0 → v29.2.3 changelog (strategy-relevant only)
3. Things older guides get wrong after v29
4. Known upcoming changes (not yet live at the pin)
5. Freshness protocol
6. How to phrase advice when knowledge may be stale

---

## 1. What the pin means

Every file in `references/` describes the game **as of v29.2.3**. Tags used across the files:
- `[mechanic]` – a verifiable game rule, checked against SDK game data or a patch note.
- `[consensus]` – community strategy or opinion. Usually sourced from guides written for v27–v28; still the best available, but not a rule.
- `[unverified]` – sources disagree, or the claim could not be confirmed at the pin.

Community strategy lags the game. At the pin, almost no published guide covers v29's slot levels, Mythic league, the Vault rework or the four new modules. Treat `[consensus]` about those areas as thin.

## 2. v29.0 → v29.2.3 changelog (strategy-relevant only)

### v29.0 (notes 2026-08-25, rollout late August)
- **Presets lab** replaces the Card Preset lab. Level 1 Card presets (350K coins), 2 Workshop (35M), 3 Bot (3.5B), 4 Module (350B), 5 Guardian (35T). Each unlocks two presets; switching is free; a respec still costs gems. `[mechanic]`
- **Global Presets** lab at Tier 11 Wave 60: two named bundles of presets (farm / tournament), more via the Vault. `[mechanic]`
- **Module levels moved from the module to the slot.** Spent coins and shards were refunded. Swapping modules no longer loses or transfers levels. Substats stay on the module. `[mechanic]`
- **Vault rework.** Harmony (by category), Power (Workshop-like categories) and a new Enemy tree. All keys refunded; no tree order, each category unlocked once with keys; some upgrades cost more than before. `[mechanic]`
- **Mythic league** added above Legend, difficulty T23+. `[mechanic]`
- **Tournament rewards changed**: Platinum more gems for ranks 1–24; Champion rank 1 gems down, others up; Legend fewer stones at every rank, plus 1 key for ranks 16–24. Developer statement: across the two weekly tournaments you never earn fewer stones, gems or keys by performing better. `[mechanic]`
- **Wave Speed Up**: unlimited Intro Sprint Mastery applied in tournaments (the card is not needed). The preview said all leagues; 29.0.2 and 29.1 describe it as "Gold and up". `[mechanic, scope per the later notes]`
- **Fleet waves** (leagues with fleets, Legend and up): fleets spawn at the start of their wave, the wave only ends when every fleet is dead, other enemies keep spawning; ties on a fleet wave break on % fleet health left. `[mechanic]`
- **New card: Cells** (Rare, unlocked at Tier 4 Wave 40; +2 → +14 cells; mastery ×1.05 → ×1.32 cells). `[mechanic]`
- **Four new epic modules** on featured banners: Sentry Protocol (Armor, from Aug 31), Gilded Sniper (Cannon, from Sep 14), Tactical Barrage (Core), Infinity Threshold (Generator); all four featured together Oct 26 – Nov 9 at 12.5% of epics each. `[mechanic]`
- **Gems**: daily claim 15 → 20; ad gem 5 → 6; ad gems capped at 60 claims/day (360 gems). `[mechanic]`
- New fleet labs (Overcharge Exponent Reducer, Commander Radius, Saboteur Attack Speed); Titan Shock scales continuously with mass; Bot+ can be previewed before unlock.

### v29.0.1 – v29.0.6 (Aug 27 – Oct 6)
- 29.0.1: Intro Sprint card ending early fixed; Platinum/Champion stone display corrected.
- 29.0.2: **Damage Decay and Health Decay removed from Legend and Mythic**; one-time free Vault respec; bot and guardian respec limits now actually enforced; slot level shows orange when above the equipped module's rarity cap. `[mechanic]`
- 29.0.3: card slots no longer stay unlocked after a Vault respec.
- 29.0.5 / 29.0.6: save fix; offer wall and creator codes removed on iOS.

### v29.1 (2026-10-13/15) and 29.1.1 – 29.1.4
- **Tournament-only death-save limits**: Demon Mode, Second Wind and Viking Funeral end after a maximum number of waves or a time limit, whichever comes first. The exact limits are not in the notes. `[mechanic, numbers unverified]`
- **Viking Funeral (Berserker mastery)** now triggers on every death save (Demon Mode, Nuke, Death Defy, Second Wind). `[mechanic]`
- **Energy Shield and Wall need at least two waves to charge** in tournaments (shown as 99% until then). `[mechanic]`
- Wave Speed Up (Gold and up) only ends once all shields are used (Smart Demon Mode, Smart Nuke, Energy Shield, Second Wind). `[mechanic]`
- **Full-uptime UWs fire at run start** (Golden Tower, Chrono Field, Black Hole, Poison Swamp). `[mechanic]`
- **Primary Module Bonus labs** (Cannon / Armor / Generator / Core): 30 levels, +1% to +30% on the primary module's main effect. `[mechanic]`
- Module inventory cap 300 → 350; quick "level slot to next sub-stat effect" button; card drop-rate info button.
- **Guardian chips stop working while not in a guild.** `[mechanic]`
- Card masteries unlocked mid-run no longer apply to that run. `[mechanic]`
- 29.1.1: **Golden Bot+ (Bonus Cells) now respects Golden Bot range** (was all elites). May lower cells/hour. `[mechanic]`
- 29.1.4: Elite Balance toggle added to Vault ▸ Harmony ▸ Cards (20 keys, needs the Enemy Balance mastery); tower skin changeable while paused.

### v29.2 (2026-11-16) and v29.2.1 (2026-11-19)
- New-player changes: no Ranged enemies on Tier 1 waves 1–20; 4 starting daily missions; a pseudo-tournament tutorial; login calendar. `[mechanic]`
- **Defense % perk no longer offered once Defense reaches 98%.** `[mechanic]`
- Scatter splits 1 → 1/2 → 1/4 → 1/8 health (was 1/4, 1/8, 1/16), so Scatters are tankier. `[mechanic]`
- CL+ (Smite) capped at 100. `[mechanic]`
- Event missions: "hit the same enemy with Smart Missiles" removed; six added (AoE kills, crowd control, hit elites with a named UW, kill elites before they deal damage), in the pool from the event starting 2026-11-24. `[mechanic]`
- UW selection now has a preview and a cancel option; warning pop-ups when spending medals would leave another preset in deficit; Relics page no longer capped at 250.
- Vault Max Recovery no longer skips its 60% step (values 20/40/60/80/100%). `[mechanic]`
- 29.2.1: ads fixed for EU; Workshop tutorial soft-lock fixed. No balance change.

### v29.2.2 (build 1296, note dated 2026-11-21)
- A fix to tournament reward validation. No balance change. `[mechanic]`

### v29.2.3 (build 1301, note dated 2026-11-24)
- Fixed new players (and players returning after a very long absence) being shown the login screen instead of starting their first game. The note says it should not affect existing players. No balance change. `[mechanic]`
- A build-1301 export has the same 456 fields at data version 35 as build 1296, and every save reader returns as before (SDK 1.7.2).

### Corrections from reading the live game (SDK 1.3.0–1.7.1, 2026-11-24)
These are not game changes. They are things earlier SDK data, the wiki or guides had wrong, now checked on screen. `[mechanic]`
- The Battle tab's **Total Coin Bonus** includes the selected tier's coin bonus and every row multiplies. Read it with `coin_bonus`.
- Songs and profile banners pay a coin bonus (+0.6% each), like themes.
- Workshop "Unlock…" buttons are never discounted by the workshop discount labs.
- The Labs Speed lab speeds up its own research.
- The gem price on a lab's Rush button is the list price divided by (1 + 0.015 × fully researched labs).
- Milestone lab unlocks: the wiki listed six labs at milestones the game does not gate them at, and used placeholder names. The gates quoted in these files were re-checked against the corrected table on 2026-11-24 and all match.
- The relics an event shop sells are not the relics the event awards. An event gives four relics of its own at 350 / 700 medals earned (550 / 1,100 with the event pass); its shop sells older relics from a past event for 200 (Rare) or 500 (Epic) medals. An event that returns brings new relics. Read both lists from `readEventShopFromSaveRoot` (`earnTrack`, `relics`).
- A card that is maxed leaves the draw pool; six cards cannot be drawn until their milestone is claimed.
- Still unexplained by the SDK (do not compute these, read them in game): Chain Lightning Quantity, Spotlight Bonus and Knockback Force as displayed.

## 3. Things older guides get wrong after v29

| Old advice (pre-v29) | True at the pin |
|---|---|
| "Keep levels on your best module / transfer levels when swapping" | Levels are on the slot. Swap modules freely; only substats and rarity belong to the module. `[mechanic]` |
| "Legend is the top league" | Mythic sits above it (T23+ scaling, 6 random conditions, boss every 4 waves). `[mechanic]` |
| "Workshop/Bot presets come from the Vault" | They come from the Presets lab (coins); the Vault only adds three more of each. `[mechanic]` |
| "Vault trees unlock bottom-up; Power nodes cost 1×/2×/4×" | No tree order. Category unlock, then per-level key costs. Old key totals do not buy the same things. `[mechanic]` |
| "Gold–Legend tournaments have ELS reduction 10/20/30/50%" (the wiki still says so) | Removed from tournaments in v27.3. Replaced by Skip Decay and Skip Reduction – Multiply. `[mechanic]` |
| "Drop a league on purpose for better rewards" | v29 reward tables were rebuilt so better placement never pays less across the week. `[mechanic]` |
| "Intro Sprint card/mastery is needed for fast tournaments" | Wave Speed Up is built in (Gold and up). `[mechanic]` |
| "Stack Demon Mode / Second Wind to ride out the end of a tournament" | Both now expire after a wave or time limit in tournaments. `[mechanic]` |
| "Golden Bot+ pays cells on every elite" | Only elites killed inside Golden Bot range since 29.1.1. `[mechanic]` |
| "Ad gems are unlimited if you run 24/7" | 60 claims a day. `[mechanic]` |
| "Guardian keeps working if you leave the guild" | Chips are inactive outside a guild since 29.1. `[mechanic]` |
| "31 cards / 31 masteries" | 32 with Cells. `[mechanic]` |
| "Assist multiplier efficiency caps at 100%" | 130% including labs since v28.3. `[mechanic]` |

## 4. Known upcoming changes (not live at the pin)

### Time-limited: 2026 Black Friday sale (Nov 25 15:00 UTC – Dec 1 15:00 UTC)
From the developer's blog post of 2026-11-23. Delete this block after Dec 1.
- In game: a $29.99 bundle with 200 gems, 300 medals and 400 stones (3 per player). Gem packs carry +50% for the first 5 purchases.
- Web store: $49.99 (440 gems, 500 medals, 700 stones; 3 per player) and $99.99 (900 gems, 1,100 medals, 1,400 stones; 5 per player) bundles, each with an exclusive **Turkey relic**. The post says the relic joins the Rotating Relics shelf, for gems, in about six months.
- Coaching use: state these as facts only if the player asks about buying stones or gems, or about the Turkey relic. Never suggest a purchase. A player worried about missing the relic can be told it returns for gems later.

### Announced, not yet released
From Tower Tea, 2026-11-09 and 2026-11-23 (developer plans, may slip):
- **Next major update targeted for "around the beginning of December" 2026** (Nov 9 post): pause a Tier run to start a Tournament run; Perk Presets in the Presets lab. The post calls these "some of the items", so the list is not complete.
- **A tenth Ultimate Weapon, "The Dome"** (Nov 23 post): a defensive UW, in development and about to enter testing, aimed at "our major update at the end of the year". No unlock method, price or numbers were given, and the post says descriptions and values may change. `[unverified beyond the announcement]`
- **Type-exclusive module banners planned for January 2027**; more banner types later in 2027.
- Scatter's Ultimate spawning behaviour is a known issue to be fixed.

What this means for advice given before the update `[consensus, the coach's own reasoning]`:
- When a player is about to commit a large stone balance to a UW unlock or a long stat ladder, mention once that a new UW has been announced and that nothing is known about its cost or where it will rank. Do not tell them to hoard stones for it: stones spent on GT/BH/DW sync pay back every day, and an unreleased weapon cannot be valued.
- How a tenth weapon fits the "all nine owned" rule for UW+ is unknown. Do not guess.

If the export shows v30 or later, assume the "cannot join a tournament during a run" rule, the perk advice, the UW unlock ladder and every "nine UWs" statement in these files may be out of date.

## 5. Freshness protocol

Run this at the start of every coaching session.

1. Read the game build from the export (`readExportInfoFromSaveRoot` → `versionNumber`; the snapshot's `meta.gameVersion` names it when the SDK knows the build). Compare with the pin, **v29.2.3** (build 1301; 1296 is v29.2.2, 1294 is v29.2.1, 1286 is v29.2.0). A build-1301 export that reads `checked: false` with "newer than 1296" means the SDK is older than 1.7.2 or was not rebuilt — see `data-access.md` § preflight, not this protocol.
2. **Same version** → use the references as written.
3. **Export is older** → the player has not updated. Tournaments are version-locked, so tell them to update before the next one. Advice here may describe features they do not have yet.
4. **Export is newer** → before giving advice in any affected area:
   1. Call the MCP `patch_notes` tool for every version after v29.2.3 (one question per call). Read the notes themselves; a note that mentions a mechanic is not proof the mechanic changed.
   2. If the archive stops before the export's version, check the official blog (techtreegames.com/blog), which carries patch notes and Tower Tea posts.
   3. For numbers, check the Fandom wiki (the-tower-idle-tower-defense.fandom.com) via `wiki_search` / `wiki_page`. The wiki can lag by weeks; the Tournaments page still showed pre-v27.3 conditions at the pin.
   4. For community reaction to a new patch, r/TheTowerGame and the official Discord. Treat as `[consensus]` at best.
   5. Prefer SDK game data (`oracle_get`, `calc_run`, `get_export`) over any prose source when a number matters.
5. Classify the gap:
   - **Patch only (29.2.x)** → almost always bug fixes. Proceed, mention the version difference once.
   - **Minor (29.3, 29.4 …)** → re-check tournaments, modules/banners and anything the notes name.
   - **Major (v30+)** → treat every `[consensus]` claim as provisional and every `[mechanic]` claim in a system the notes touch as unverified until re-checked.
6. `whenIntroduced`-style lookups returning nothing means "not in the archive", not "never happened".

## 6. How to phrase advice when knowledge may be stale

- State the pin once, plainly: "My strategy notes are pinned to v29.2.3; your save is v30.0. I checked the patch notes for the versions in between."
- Separate rule from opinion in the sentence itself: "The game refunds nothing if you reroll (rule). Most strong players wait for Mythic rarity before rerolling seriously (community view, written for v28)."
- When a system changed after the pin and no guide covers it yet, say so and fall back to mechanics: "No one has published tested advice on this module yet. Here is what it does and how that interacts with your build."
- Never quote a cost from memory for a newer version. Compute it (`calc_run`) or look it up (`oracle_get`), or tell the player where to read it in game.
- For irreversible actions (see `footguns.md`), a stale reference is a reason to slow down: recommend the player confirm the in-game description before spending.
