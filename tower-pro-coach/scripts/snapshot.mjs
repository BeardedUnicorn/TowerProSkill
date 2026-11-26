#!/usr/bin/env node
/**
 * snapshot.mjs — freeze one tool_export.json into a single JSON file the coach can diff later.
 *
 * Usage
 *   node snapshot.mjs [--export <path/to/tool_export.json>] [--sdk <path>] [--out <dir>]
 *   node snapshot.mjs --list [--export <path/to/tool_export.json>] [--sdk <path>] [--out <dir>]
 *
 * --export  The export to freeze. Without it: env TOWER_TOOL_EXPORT, then the TOWER_TOOL_EXPORT an
 *           MCP config gives the Tower server, then wherever the SDK finds the game's export.
 * --sdk   A TheTowerSDK checkout (built: it needs dist/) or an installed
 *         @beardedunicorn/thetowersdk package directory. Falls back to env TOWER_SDK_PATH,
 *         then to resolving the package by name, then to the checkout an MCP config starts the
 *         Tower server from (.mcp.json beside the skill or in the working directory, ~/.claude.json,
 *         the Claude desktop config).
 * --out   Snapshot root. Default: ~/.tower-coach/snapshots
 * --list  List existing snapshots. With --export: for that player. Without: every player key.
 *
 * Output: <out>/<playerKey>/<YYYY-MM-DD>T<HHMM>.json  (local time of the snapshot)
 *   { meta: {...}, readers: { <readerName>: <result> | null | { error } }, runs: [...] }
 *
 * playerKey is a short hash of the player ID. The raw ID and the user name are stripped from
 * reader output, and the script refuses to write a file in which either still appears.
 */
import { createHash } from 'node:crypto'
import fs from 'node:fs'
import { createRequire } from 'node:module'
import os from 'node:os'
import path from 'node:path'
import process from 'node:process'
import { fileURLToPath } from 'node:url'

const PACKAGE = '@beardedunicorn/thetowersdk'
const READER_NAME = /^read[A-Z].*FromSaveRoot$/

function fail(message, code = 1) {
  process.stderr.write(`snapshot: ${message}\n`)
  process.exit(code)
}

function parseArgs(argv) {
  const args = { list: false, help: false }
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]
    if (arg === '--list') args.list = true
    else if (arg === '--help' || arg === '-h') args.help = true
    else if (arg === '--export' || arg === '--sdk' || arg === '--out') {
      const value = argv[i + 1]
      if (value === undefined || value.startsWith('--')) fail(`${arg} needs a value`)
      args[arg.slice(2)] = value
      i += 1
    }
    else if (/^--(export|sdk|out)=/.test(arg)) {
      const [key, ...rest] = arg.slice(2).split('=')
      args[key] = rest.join('=')
    }
    else fail(`unknown argument "${arg}". Try --help.`)
  }
  return args
}

const HELP = `Usage:
  node snapshot.mjs [--export <tool_export.json>] [--sdk <TheTowerSDK path>] [--out <dir>]
  node snapshot.mjs --list [--export <tool_export.json>] [--out <dir>]

SDK location, first that works: --sdk, env TOWER_SDK_PATH, the installed ${PACKAGE} package,
the checkout an MCP config starts the Tower server from.
Export, first that works: --export, env TOWER_TOOL_EXPORT, the TOWER_TOOL_EXPORT in that MCP config,
the game's own folder (as the SDK finds it).
Default --out is ~/.tower-coach/snapshots.`

const expandHome = given => (/^~(?=$|[\\/])/.test(given) ? path.join(os.homedir(), given.slice(1)) : given)

// ---------------------------------------------------------------------------------------------
// SDK loading
// ---------------------------------------------------------------------------------------------

/** The directory holding save/index.js and node/index.js under a path someone gave, or null. */
function distUnder(given) {
  const base = path.resolve(expandHome(given))
  const candidates = [
    path.join(base, 'dist'),
    base,
    path.join(base, 'node_modules', ...PACKAGE.split('/'), 'dist'),
  ]
  return candidates.find(dir =>
    fs.existsSync(path.join(dir, 'save', 'index.js')) && fs.existsSync(path.join(dir, 'node', 'index.js'))) ?? null
}

/**
 * What the MCP configs on this machine say about the Tower server: the checkouts it is started
 * from (an argument ending in mcp/server.mjs) and the export it is pointed at. A coach that reads
 * the save through the server has both, but only the config knows where they are on disk.
 */
function mcpConfigHints() {
  const here = path.dirname(fileURLToPath(import.meta.url))
  const files = [
    path.join(here, '..', '.mcp.json'),
    path.join(here, '..', '..', '.mcp.json'),
    path.join(process.cwd(), '.mcp.json'),
    path.join(os.homedir(), '.claude.json'),
    path.join(os.homedir(), 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json'),
    path.join(os.homedir(), 'AppData', 'Roaming', 'Claude', 'claude_desktop_config.json'),
    path.join(os.homedir(), '.config', 'Claude', 'claude_desktop_config.json'),
  ]
  const sdkRoots = []
  const exports = []
  const walk = (value, file, depth) => {
    if (depth > 8 || value === null || typeof value !== 'object') return
    if (Array.isArray(value.args)) {
      const server = value.args.find(arg => typeof arg === 'string' && /[\\/]mcp[\\/]server\.mjs$/.test(arg))
      if (server) {
        sdkRoots.push({ root: path.dirname(path.dirname(path.resolve(expandHome(server)))), file })
        const named = value.env?.TOWER_TOOL_EXPORT
        if (typeof named === 'string' && named.trim()) exports.push({ path: named.trim(), file })
      }
    }
    for (const child of Object.values(value)) walk(child, file, depth + 1)
  }
  for (const file of [...new Set(files.map(candidate => path.resolve(candidate)))]) {
    try {
      walk(JSON.parse(fs.readFileSync(file, 'utf8')), file, 0)
    }
    catch { /* absent, unreadable or not JSON: not a source */ }
  }
  return { sdkRoots, exports }
}

function versionNear(dist) {
  for (const dir of [path.dirname(dist), dist]) {
    try {
      const pkg = JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8'))
      if (pkg.name === PACKAGE && typeof pkg.version === 'string') return pkg.version
    }
    catch { /* keep looking */ }
  }
  return null
}

function loadFromDist(dist, origin) {
  const require = createRequire(path.join(dist, 'index.js'))
  return {
    save: require(path.join(dist, 'save', 'index.js')),
    node: require(path.join(dist, 'node', 'index.js')),
    version: versionNear(dist),
    origin,
  }
}

async function loadSdk(sdkArg) {
  const tried = []
  for (const [label, given] of [['--sdk', sdkArg], ['TOWER_SDK_PATH', process.env.TOWER_SDK_PATH]]) {
    if (!given) continue
    const dist = distUnder(given)
    if (dist) return loadFromDist(dist, label)
    const base = path.resolve(expandHome(given))
    const hint = fs.existsSync(path.join(base, 'package.json')) && !fs.existsSync(path.join(base, 'dist'))
      ? ' (a checkout without dist/ — run `pnpm install && pnpm build` in it first)'
      : ''
    tried.push(`${label}=${given}: no dist/save/index.js and dist/node/index.js there${hint}`)
  }

  // By package name: from this script's location, then from the working directory.
  const requires = [createRequire(import.meta.url), createRequire(path.join(process.cwd(), 'noop.js'))]
  for (const require of requires) {
    try {
      const main = require.resolve(PACKAGE)
      const dist = path.dirname(main)
      if (fs.existsSync(path.join(dist, 'save', 'index.js'))) return loadFromDist(dist, 'installed package')
    }
    catch { /* not resolvable from here */ }
  }
  try {
    const [save, node] = await Promise.all([import(`${PACKAGE}/save`), import(`${PACKAGE}/node`)])
    return { save: save.default ?? save, node: node.default ?? node, version: null, origin: 'installed package' }
  }
  catch {
    tried.push(`import('${PACKAGE}'): not installed where this script or the working directory can resolve it`)
  }

  for (const { root, file } of mcpConfigHints().sdkRoots) {
    const dist = distUnder(root)
    if (dist) return loadFromDist(dist, `MCP config ${file}`)
    tried.push(`${root} (the Tower server in ${file}): no built dist/ there`)
  }

  fail(
    `could not find the Tower SDK.\n  ${tried.join('\n  ')}\n`
    + 'Pass its location one of these ways:\n'
    + '  --sdk /path/to/TheTowerSDK          a built checkout of github.com/BeardedUnicorn/TheTowerSDK\n'
    + `  --sdk /path/to/node_modules/${PACKAGE}\n`
    + '  TOWER_SDK_PATH=/path/to/TheTowerSDK  the same, as an environment variable\n'
    + `  npm install ${PACKAGE}              next to this script or in the working directory`,
  )
  return null
}

// ---------------------------------------------------------------------------------------------
// Serialisation
// ---------------------------------------------------------------------------------------------

/** Anything a reader can return, as plain JSON. BigInt, Map, Set, Date, functions and cycles included. */
function toPlain(value, seen = new WeakSet()) {
  if (value === null || value === undefined) return null
  switch (typeof value) {
    case 'number': return Number.isFinite(value) ? value : String(value)
    case 'bigint': {
      const asNumber = Number(value)
      return Number.isSafeInteger(asNumber) ? asNumber : value.toString()
    }
    case 'string':
    case 'boolean': return value
    case 'function':
    case 'symbol': return undefined
    default: break
  }
  if (value instanceof Date) return Number.isNaN(value.getTime()) ? null : value.toISOString()
  if (seen.has(value)) return '[Circular]'
  seen.add(value)
  let plain
  if (Array.isArray(value)) plain = value.map(item => toPlain(item, seen) ?? null)
  else if (ArrayBuffer.isView(value)) plain = Array.from(value, item => toPlain(item, seen))
  else if (value instanceof Set) plain = [...value].map(item => toPlain(item, seen) ?? null)
  else {
    const entries = value instanceof Map ? [...value.entries()] : Object.entries(value)
    plain = {}
    for (const [key, item] of entries) {
      const converted = toPlain(item, seen)
      if (converted !== undefined) plain[String(key)] = converted
    }
  }
  seen.delete(value)
  return plain
}

/** Whether any string value in a plain JSON tree is exactly `wanted`. */
function hasStringValue(value, wanted) {
  if (typeof value === 'string') return value === wanted
  if (Array.isArray(value)) return value.some(item => hasStringValue(item, wanted))
  if (value && typeof value === 'object') return Object.values(value).some(item => hasStringValue(item, wanted))
  return false
}

/** A copy of a plain JSON tree with every string that is, or contains, a `secrets` entry replaced. */
function redact(value, secrets) {
  if (typeof value === 'string') {
    if (secrets.exact.includes(value)) return '[redacted]'
    return secrets.anywhere.reduce((text, secret) => text.split(secret).join('[redacted]'), value)
  }
  if (Array.isArray(value)) return value.map(item => redact(item, secrets))
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, redact(item, secrets)]))
  }
  return value
}

// ---------------------------------------------------------------------------------------------
// Snapshot
// ---------------------------------------------------------------------------------------------

function playerIdentity(root) {
  const find = (wanted) => {
    const key = Object.keys(root).find(name => name.toLowerCase() === wanted)
    const value = key === undefined ? null : root[key]
    return typeof value === 'string' || typeof value === 'number' ? String(value).trim() : ''
  }
  return { playerId: find('playerid'), userName: find('username') }
}

const playerKeyOf = playerId => createHash('sha256').update(`tower-coach:${playerId}`).digest('hex').slice(0, 12)

function localStamp(date) {
  const two = number => String(number).padStart(2, '0')
  return `${date.getFullYear()}-${two(date.getMonth() + 1)}-${two(date.getDate())}T${two(date.getHours())}${two(date.getMinutes())}`
}

function listSnapshots(dir) {
  if (!fs.existsSync(dir)) return []
  return fs.readdirSync(dir)
    .filter(name => /^\d{4}-\d{2}-\d{2}T\d{4}\.json$/.test(name))
    .sort()
    .map((name) => {
      const file = path.join(dir, name)
      let meta = {}
      try {
        meta = JSON.parse(fs.readFileSync(file, 'utf8')).meta ?? {}
      }
      catch { /* listed anyway, as unreadable */ }
      return { file, name, meta }
    })
}

function printList(dir, label) {
  const found = listSnapshots(dir)
  process.stdout.write(`${label}: ${found.length} snapshot${found.length === 1 ? '' : 's'} in ${dir}\n`)
  for (const { file, meta } of found) {
    process.stdout.write(`  ${file}  exported ${meta.exportedAt ?? '?'}  ${meta.gameVersion ?? '?'}  runs ${meta.runCount ?? '?'}\n`)
  }
}

async function decodeExport(sdk, exportPath) {
  let stats
  try {
    stats = fs.statSync(exportPath)
  }
  catch {
    fail(`no file at ${exportPath}`)
  }
  if (stats.isDirectory()) fail(`${exportPath} is a directory. Point at the tool_export.json inside it.`)
  const bytes = fs.readFileSync(exportPath)
  if (bytes.length === 0) fail(`${exportPath} is empty. Export again from the game.`)
  try {
    return await sdk.node.decodePlayerInfoSaveBytesAsync(bytes)
  }
  catch (error) {
    const issues = Array.isArray(error?.issues) ? [...new Set(error.issues.map(issue => String(issue?.message)))].join('; ') : null
    fail(`${exportPath} is not an official tool_export.json: ${issues ?? error?.message ?? error}`)
  }
  return null
}

async function main() {
  const args = parseArgs(process.argv.slice(2))
  if (args.help) {
    process.stdout.write(`${HELP}\n`)
    return
  }
  const outRoot = path.resolve(expandHome(args.out ?? path.join('~', '.tower-coach', 'snapshots')))

  if (args.list && !args.export) {
    if (!fs.existsSync(outRoot)) {
      process.stdout.write(`no snapshots yet: ${outRoot} does not exist\n`)
      return
    }
    const players = fs.readdirSync(outRoot, { withFileTypes: true }).filter(entry => entry.isDirectory())
    if (players.length === 0) process.stdout.write(`no snapshots yet in ${outRoot}\n`)
    for (const player of players) printList(path.join(outRoot, player.name), `player ${player.name}`)
    return
  }
  const sdk = await loadSdk(args.sdk)
  let exportGiven = args.export
  if (!exportGiven) {
    const configured = mcpConfigHints().exports.find(found => fs.existsSync(expandHome(found.path)))
    const found = process.env.TOWER_TOOL_EXPORT?.trim()
      || configured?.path
      || (typeof sdk.node.findToolExport === 'function' ? sdk.node.findToolExport().path : null)
    if (!found) fail(`no export found. Pass --export <path/to/tool_export.json>.\n${HELP}`)
    exportGiven = found
    process.stdout.write(`export: ${found}\n`)
  }
  const exportPath = path.resolve(expandHome(exportGiven))
  const { parsedRoot } = await decodeExport(sdk, exportPath)

  const { playerId, userName } = playerIdentity(parsedRoot)
  if (!playerId) fail('the export carries no player ID, so its snapshots cannot be kept apart from another account\'s.')
  const playerKey = playerKeyOf(playerId)
  const playerDir = path.join(outRoot, playerKey)

  // An agent's sandbox may hide the home folder. Say so in words, before any work is done, with
  // the way round it: a traceback here reads as "the script is broken", and it is not.
  try {
    if (fs.existsSync(outRoot)) fs.readdirSync(outRoot)
    if (!args.list) fs.mkdirSync(playerDir, { recursive: true })
  }
  catch (error) {
    fail(
      `cannot ${args.list ? 'read' : 'write'} the snapshot folder ${outRoot}: ${error?.code ?? error?.message ?? error}.\n`
      + 'Snapshots already saved there cannot be seen from this session.\n'
      + 'Pass --out <a folder this session can write>, for example --out ./tower-coach-snapshots, '
      + 'and give the same folder to diff_snapshots.py as --dir.',
    )
  }

  if (args.list) {
    printList(playerDir, `player ${playerKey}`)
    return
  }

  const readerNames = Object.keys(sdk.save).filter(name => READER_NAME.test(name) && typeof sdk.save[name] === 'function').sort()
  if (readerNames.length === 0) fail('the SDK\'s save entry exports no read*FromSaveRoot readers — is this the BeardedUnicorn SDK?')

  const readers = {}
  const failed = []
  const absent = []
  for (const name of readerNames) {
    try {
      const result = sdk.save[name](parsedRoot)
      readers[name] = result === null || result === undefined ? null : toPlain(result)
      if (readers[name] === null) absent.push(name)
    }
    catch (error) {
      readers[name] = { error: error instanceof Error ? error.message : String(error) }
      failed.push(name)
    }
  }

  let runs = []
  let runsError = null
  try {
    const killedByName = typeof sdk.save.getKilledByFromSave === 'function' ? sdk.save.getKilledByFromSave : null
    runs = (sdk.save.listImportableBattleRuns?.(parsedRoot) ?? []).map((run) => {
      const plain = toPlain(run)
      if (killedByName && plain && typeof plain === 'object') plain.killedByName = killedByName(run.killedBy)
      return plain
    })
  }
  catch (error) {
    runsError = error instanceof Error ? error.message : String(error)
  }

  const info = readers.readExportInfoFromSaveRoot && !readers.readExportInfoFromSaveRoot.error ? readers.readExportInfoFromSaveRoot : {}
  const checked = sdk.save.NEWEST_CHECKED_EXPORT
  const build = info.versionNumber ?? null
  const gameVersion = build === null
    ? null
    : (checked && checked.versionNumber === build ? `${checked.gameVersion} (build ${build})` : `build ${build}`)

  const now = new Date()
  const snapshot = {
    meta: {
      snapshotAt: now.toISOString(),
      exportedAt: info.exportedAt ?? null,
      gameVersion,
      gameBuild: build,
      dataVersion: info.dataVersion ?? null,
      sdkVersion: sdk.version,
      exportPath: path.basename(exportPath),
      playerKey,
      readerCount: readerNames.length,
      readersFailed: failed,
      readersAbsent: absent,
      runCount: runs.length,
      ...(runsError ? { runsError } : {}),
    },
    // Readers such as readProfileFromSaveRoot return the player ID and user name. Strip them: the
    // ID wherever it appears, the name only where a value IS the name (it can be an ordinary word).
    readers: redact(readers, { exact: userName ? [userName] : [], anywhere: playerId.length >= 6 ? [playerId] : [] }),
    runs: redact(runs, { exact: userName ? [userName] : [], anywhere: playerId.length >= 6 ? [playerId] : [] }),
  }

  const json = `${JSON.stringify(snapshot, null, 1)}\n`
  // The ID is distinctive, so any occurrence counts. A user name can be an ordinary word that a
  // card or module is also called, so only a value that IS the name counts.
  if (playerId.length >= 6 && json.includes(playerId)) {
    fail('refusing to write: a reader\'s output contains the raw player ID. Nothing was saved.')
  }
  if (userName && hasStringValue(snapshot, userName)) {
    fail('refusing to write: a reader\'s output contains the account\'s user name. Nothing was saved.')
  }

  const previous = listSnapshots(playerDir).at(-1)
  fs.mkdirSync(playerDir, { recursive: true })
  const outFile = path.join(playerDir, `${localStamp(now)}.json`)
  fs.writeFileSync(outFile, json)

  const problems = [
    failed.length > 0 ? `${failed.length} failed (${failed.join(', ')})` : null,
    absent.length > 0 ? `${absent.length} absent (${absent.join(', ')})` : null,
    runsError ? `runs failed (${runsError})` : null,
  ].filter(Boolean)
  process.stdout.write(
    `snapshot ok: player ${playerKey}, exported ${snapshot.meta.exportedAt ?? '?'}, ${gameVersion ?? 'unknown build'}, `
    + `${readerNames.length - failed.length}/${readerNames.length} readers, ${runs.length} runs`
    + `${problems.length > 0 ? `; ${problems.join('; ')}` : ''}\n`,
  )
  if (previous && previous.file !== outFile && previous.meta.exportedAt && previous.meta.exportedAt === snapshot.meta.exportedAt) {
    process.stdout.write(`note: same export as the previous snapshot (${previous.name}) — re-export in game for fresh data.\n`)
  }
  process.stdout.write(`${outFile}\n`)
}

const isDirectRun = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)
if (isDirectRun) {
  main().catch(error => fail(error instanceof Error ? error.stack ?? error.message : String(error)))
}
