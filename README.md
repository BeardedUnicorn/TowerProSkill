# Tower Pro Coach

A [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that coaches your
account in [The Tower – Idle Tower Defense](https://www.techtreegames.com/thetower) (Android, iOS, and Mac via
the iPad app).

It reads the game's official `tool_export.json` through the
[TheTowerSDK](https://github.com/BeardedUnicorn/TheTowerSDK) MCP server, works out exactly where your
account stands, and tells you the highest-value next steps — priced with real costs and ranked against the
alternatives.

## What you get

Ask Claude to review your account and you get a coaching report:

- **Account at a glance** — stage, farming tier, median coins/hour and cells/hour, and the one thing
  holding the account back
- **Do these now** — one to three moves, each with the reason, the cost, the expected effect, and a warning
  when the choice is permanent
- **Save toward** — the next target for each currency (stones, gems, coins, medals, cells, keys, bits, shards)
- **Lab queue** — what should be running in every slot
- **Stop / avoid** — where resources are being wasted
- **Run review** — what your last 30 runs show about how the tower dies and where the damage comes from
- **Since last time** — on repeat sessions, what changed and whether earlier advice paid off

Follow-up questions ("DW quantity or GT duration?", "which lab next?", "is it time to move to T11?") get a
direct, numbers-backed answer.

## How it works

1. Confirms the TheTowerSDK MCP server is connected.
2. Finds your `tool_export.json` and reads **all** of it — workshop, labs, cards, modules, ultimate weapons,
   bots, guardian, vault, relics, themes, perks, currencies, tournaments, tier records and battle history.
3. Saves a local snapshot so progress can be tracked between sessions.
4. Diagnoses the account's stage and bottleneck (economy, survival, damage or lab time).
5. Ranks candidate moves using bundled strategy references, with costs and durations computed by the SDK's
   calculators rather than quoted from memory.
6. Flags every irreversible decision (UW picks, UW stat levels, lab research, bot cooldown labs).
7. Checks your game version against the version the strategy references were verified on, and looks up
   patch notes if yours is newer.

Strategy claims are labelled as game mechanics, community consensus or unverified, and the coach keeps that
distinction in its advice.

## Requirements

- Claude with skills and MCP support (Claude Code, the Claude desktop app, or the Agent SDK)
- The **BeardedUnicorn/TheTowerSDK** MCP server — this skill does not work with other Tower servers
- Node.js 22+ (for the SDK and the optional snapshot script); Python 3 for the snapshot diff
- The Tower with External Tools Export available

## Setup

### 1. Install the TheTowerSDK MCP server

Version 1.5.0 or later is needed for unlock pricing and the coin-bonus breakdown.

**Claude desktop app:** download `thetowersdk.mcpb` from the SDK's
[latest release](https://github.com/BeardedUnicorn/TheTowerSDK/releases/latest) and open it. Nothing to build.

**From source:**

```bash
git clone https://github.com/BeardedUnicorn/TheTowerSDK.git
```

Install and build it following that repository's README, then register the server with Claude. The server
runs from the built `dist/` folder, so rebuild after every `git pull` and restart Claude — a checkout that
was pulled but not rebuilt answers with old data. For Claude
Code, copy `.mcp.json.example` to `.mcp.json` in your project (or add the entry to your user config), using your own path:

```json
{
  "mcpServers": {
    "thetowersdk": {
      "type": "stdio",
      "command": "node",
      "args": ["/absolute/path/to/TheTowerSDK/mcp/server.mjs"]
    }
  }
}
```

Restart Claude so the server connects.

### 2. Install the skill

```bash
git clone https://github.com/BeardedUnicorn/TowerProSkill.git
```

Copy the skill folder into your skills directory:

```bash
cp -r TowerProSkill/tower-pro-coach ~/.claude/skills/
```

For the Claude apps, zip the `tower-pro-coach` folder and upload it under Settings → Capabilities → Skills.

### 3. Export your save from the game

1. In The Tower, tap your **Player ID** five times to reveal the tools options.
2. Go to **Settings → Toggles → External Tools Export**.
3. Tap **Manual Export**, or turn on **Auto Export for External Tools** to keep the file current.

Where the file ends up:

| Platform | Location |
|---|---|
| Android | `Android/data/com.TechTreeGames.TheTower/files/tool_export.json` |
| Mac (iPad app) | `~/Library/Containers/<app container>/Data/Documents/tool_export.json` |
| iPhone / iPad | In the app's documents; copy it to the computer running Claude (Files, AirDrop) |

On a Mac the server finds the file by itself. Elsewhere, give the coach the path, or set the
`TOWER_TOOL_EXPORT` environment variable for the MCP server to the file's path.

The file has to be readable on the machine where Claude and the MCP server run. Only the official
`tool_export.json` is supported — the skill never touches the game's encrypted save.

## Usage

```
Coach me in The Tower — my export is at ~/Downloads/tool_export.json
```

```
Review my Tower account and tell me where my stones should go.
```

```
I exported again. What changed, and what's next?
```

```
Should I unlock Chain Lightning or keep pushing GT/BH sync?
```

## Snapshots and privacy

Everything stays on your machine. Each session can save a snapshot of the decoded export to
`~/.tower-coach/snapshots/<playerKey>/`, where `playerKey` is a short hash of your player ID, along with an
`advice-log.md` of past recommendations. Delete that folder at any time to reset history. No account data
is stored in this repository.

## Repository layout

```
tower-pro-coach/
  SKILL.md                 the coaching workflow
  references/              data access, account assessment, strategy by system, footguns, glossary, version
  scripts/snapshot.mjs     save a dated snapshot of the decoded export
  scripts/diff_snapshots.py  compare two snapshots
  evals/                   test prompts for the skill
```

## Running the evals

The cases in `tower-pro-coach/evals/` run with `claude plugin eval`. The runner works in an isolated home
folder with no MCP servers of its own, so give the skill folder a server for the run: create
`tower-pro-coach/.mcp.json` (ignored by git) with the same `thetowersdk` entry as above, plus the export's
location, because the isolated home hides the game's folder:

```json
{
  "mcpServers": {
    "thetowersdk": {
      "type": "stdio",
      "command": "node",
      "args": ["/absolute/path/to/TheTowerSDK/mcp/server.mjs"],
      "env": { "TOWER_TOOL_EXPORT": "/absolute/path/to/tool_export.json" }
    }
  }
}
```

Then run one case at a time (`--case` takes a single name or glob):

```bash
claude plugin eval tower-pro-coach --case full-account-review --mocks off --ablation none --allow-tools Bash Write Edit mcp__plugin_tower-pro-coach_thetowersdk
```

`--mocks off` starts the real server as you, outside the sandbox. Run `refuses-without-sdk-server` with
the `.mcp.json` removed and without `--mocks off`: that case checks what the coach does when the server
is missing. Results and reports contain account data; they are written under `evals/results/`, which is
ignored by git.

## Game version

The strategy references are verified against a specific game version, recorded in
[`tower-pro-coach/references/version.md`](tower-pro-coach/references/version.md). The game is patched
often; when your version is newer the coach checks patch notes before advising, and tells you what its
knowledge was verified against. Corrections and updates are welcome via issues and pull requests.

## Disclaimer

This is an unofficial fan project. It is not affiliated with, endorsed by or supported by Tech Tree Games.
The Tower – Idle Tower Defense is a trademark of its owner. Strategy advice reflects community
understanding and can be wrong or out of date — irreversible decisions are yours to make.

## License

[MIT](LICENSE)
