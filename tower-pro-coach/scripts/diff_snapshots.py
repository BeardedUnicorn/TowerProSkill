#!/usr/bin/env python3
"""diff_snapshots.py — what changed between two snapshots written by snapshot.mjs.

Usage
  python3 diff_snapshots.py <old.json> <new.json> [--json] [--cap N]
  python3 diff_snapshots.py --latest [--dir ~/.tower-coach/snapshots[/<playerKey>]] [--json]

--latest diffs the two most recent snapshots that come from DIFFERENT exports (two snapshots of
the same export say nothing). --dir may be one player's folder or the snapshot root; under the
root, the player whose snapshot is newest is used and the choice is printed.

The diff is generic: every reader's result is walked recursively, so a reader this script has
never heard of still gets a section. Lists of records are matched by an identity column
(guid, slug, name, tier, index ...) when one is unique, otherwise by position. Run history gets
its own section of medians, because a rolling list of runs is not usefully diffed field by field.

Standard library only.
"""
import argparse
import json
import os
import re
import statistics
import sys
from datetime import datetime

CAP_DEFAULT = 40

# Section titles and order for the readers a coach reads first. Anything else follows, by name.
SECTIONS = [
    (r'Currenc', 'Currencies'),
    (r'WorkshopUnlocks', 'Workshop unlocks'),
    (r'Workshop', 'Workshop'),
    (r'FavoriteLab', 'Favourite labs'),
    (r'Labs', 'Labs'),
    (r'UltimateWeapon', 'Ultimate weapons'),
    (r'Cards', 'Cards'),
    (r'ModuleEconomy', 'Module slots & economy'),
    (r'Modules', 'Modules'),
    (r'BotSynchronicity', 'Bot synchronicity'),
    (r'Bots', 'Bots'),
    (r'Guardian', 'Guardian'),
    (r'Vault', 'Vault'),
    (r'Relics', 'Relics'),
    (r'TierRecords', 'Tier records'),
    (r'Tournament', 'Tournaments'),
    (r'Events', 'Events'),
    (r'Milestones', 'Milestones'),
    (r'Perk', 'Perk choices'),
    (r'LifetimeBreakdown', 'Lifetime breakdown'),
    (r'Lifetime', 'Lifetime totals'),
]

# Identity columns for matching the rows of a list, most specific first. A tuple is a composite.
IDENTITY_KEYS = [
    'guid', 'slug', 'id', 'slotKey', 'key', 'name', 'label', 'displayName', 'tier', 'number',
    ('presetIndex', 'slotIndex'), ('category', 'index'), 'index', 'slotIndex', 'saveIndex',
    'recordIndex', 'equipSlot',
]
# Columns that make a matched row readable in a path.
LABEL_KEYS = ['displayName', 'mappedName', 'name', 'label', 'slug', 'id', 'slotKey', 'category']

# Paths that change constantly or say little; listed after everything else in a section.
# Clock-driven fields: they change on every export and are never a decision the player made.
TIMER_NOISE = re.compile(r'remainingSeconds|percentComplete|speedUpRemaining|RemainingSeconds', re.IGNORECASE)

LOW_PRIORITY = re.compile(
    r'preset|skin|theme|autoPick|isNew|rerollCounter|remainingSeconds|percentComplete|'
    r'completeDate|completedAt|exportedAt|ThisCycle|unknownKeys|warnings|rawWeaponLevels|\.date$',
    re.IGNORECASE,
)

SUFFIXES = [(1e33, 'D'), (1e30, 'N'), (1e27, 'O'), (1e24, 'S'), (1e21, 's'), (1e18, 'Q'),
            (1e15, 'q'), (1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')]


def fmt_num(value):
    """A number in the game's notation (q = 1e15, Q = 1e18: case matters)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return fmt_val(value)
    magnitude = abs(value)
    if magnitude >= 1e36:
        return '%.3g' % value
    if magnitude >= 1e4:
        for size, suffix in SUFFIXES:
            if magnitude >= size:
                return ('%.2f' % (value / size)).rstrip('0').rstrip('.') + suffix
    if isinstance(value, int) or float(value).is_integer():
        return str(int(value))
    return ('%.4g' % value)


def fmt_val(value):
    if value is None:
        return 'none'
    if isinstance(value, bool):
        return 'yes' if value else 'no'
    if isinstance(value, (int, float)):
        return fmt_num(value)
    if isinstance(value, str):
        return value if len(value) <= 60 else value[:57] + '...'
    if isinstance(value, list):
        return '[%d items]' % len(value)
    if isinstance(value, dict):
        label = row_label(value)
        return label if label else '{%d fields}' % len(value)
    return str(value)


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def row_label(row):
    for key in LABEL_KEYS:
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def identity_of(old_rows, new_rows):
    """The column (or columns) that names every row uniquely on both sides, or None."""
    for candidate in IDENTITY_KEYS:
        keys = candidate if isinstance(candidate, tuple) else (candidate,)
        ok = True
        for rows in (old_rows, new_rows):
            seen = set()
            for row in rows:
                ident = tuple(row.get(key) for key in keys)
                if any(part is None or isinstance(part, (dict, list)) for part in ident) or ident in seen:
                    ok = False
                    break
                seen.add(ident)
            if not ok:
                break
        if ok:
            return keys
    return None


def step_name(row, keys):
    ident = tuple(row.get(key) for key in keys)
    label = row_label(row)
    if label and len(keys) == 1 and str(ident[0]) != label and keys[0] not in LABEL_KEYS:
        return '%s #%s' % (label, ident[0])
    if label and len(keys) == 1:
        return label
    text = ','.join('%s=%s' % (key, part) for key, part in zip(keys, ident))
    return '%s (%s)' % (label, text) if label else text


def walk(old, new, path, out):
    """Append one change per differing leaf. A change is a dict with path, kind, old, new."""
    if old == new:
        return
    if isinstance(old, dict) and isinstance(new, dict):
        for key in list(old.keys()) + [key for key in new.keys() if key not in old]:
            child = '%s.%s' % (path, key) if path else str(key)
            if key not in new:
                out.append({'path': child, 'kind': 'removed', 'old': summarise(old[key]), 'new': None})
            elif key not in old:
                out.append({'path': child, 'kind': 'added', 'old': None, 'new': summarise(new[key])})
            else:
                walk(old[key], new[key], child, out)
        return
    if isinstance(old, list) and isinstance(new, list):
        records = lambda rows: len(rows) > 0 and all(isinstance(row, dict) for row in rows)
        if (records(old) or not old) and (records(new) or not new) and (old or new):
            keys = identity_of(old, new)
            if keys:
                old_by = {tuple(row.get(key) for key in keys): row for row in old}
                new_by = {tuple(row.get(key) for key in keys): row for row in new}
                for ident, row in old_by.items():
                    child = '%s[%s]' % (path, step_name(row, keys))
                    if ident in new_by:
                        walk(row, new_by[ident], child, out)
                    else:
                        out.append({'path': child, 'kind': 'removed', 'old': summarise(row), 'new': None})
                for ident, row in new_by.items():
                    if ident not in old_by:
                        out.append({'path': '%s[%s]' % (path, step_name(row, keys)), 'kind': 'added',
                                    'old': None, 'new': summarise(row)})
                return
        # Positional: the shared prefix is compared, the tail is reported as a count.
        shared = min(len(old), len(new))
        for index in range(shared):
            walk(old[index], new[index], '%s[%d]' % (path, index), out)
        if len(new) > shared:
            out.append({'path': path, 'kind': 'grew', 'old': len(old), 'new': len(new),
                        'sample': [summarise(item) for item in new[shared:shared + 3]]})
        elif len(old) > shared:
            out.append({'path': path, 'kind': 'shrank', 'old': len(old), 'new': len(new)})
        return
    out.append({'path': path, 'kind': 'changed', 'old': summarise(old), 'new': summarise(new)})


def summarise(value):
    """A leaf as it is; a container as something short enough to print or serialise."""
    if isinstance(value, dict):
        label = row_label(value)
        small = {key: item for key, item in value.items() if not isinstance(item, (dict, list))}
        if label and len(small) > 6:
            keep = ('level', 'rarityLabel', 'unlocked', 'active', 'count')
            return {'label': label, **{key: small[key] for key in keep if key in small}}
        return small if len(small) <= 8 else {'fields': len(value)}
    if isinstance(value, list):
        return value if len(value) <= 6 and not any(isinstance(item, (dict, list)) for item in value) \
            else '[%d items]' % len(value)
    return value


def describe(change):
    kind, old, new = change['kind'], change['old'], change['new']
    path = change['path']
    if kind == 'added':
        return '+ %s  (new: %s)' % (path, show(new))
    if kind == 'removed':
        return '- %s  (was: %s)' % (path, show(old))
    if kind == 'grew':
        sample = ', '.join(show(item) for item in change.get('sample', []))
        return '+ %s  %d -> %d items (+%d)%s' % (path, old, new, new - old, ': ' + sample if sample else '')
    if kind == 'shrank':
        return '- %s  %d -> %d items (%d)' % (path, old, new, new - old)
    if is_number(old) and is_number(new):
        delta = new - old
        pct = ''
        if old not in (0, 0.0) and abs(delta / old) >= 0.0005:
            pct = ', %+.1f%%' % (100.0 * delta / abs(old))
        sign = '+' if delta >= 0 else '-'
        return '  %s  %s -> %s  (%s%s%s)' % (path, fmt_num(old), fmt_num(new), sign, fmt_num(abs(delta)), pct)
    return '  %s  %s -> %s' % (path, show(old), show(new))


def show(value):
    if isinstance(value, dict):
        if 'label' in value:
            rest = ', '.join('%s %s' % (key, fmt_val(item)) for key, item in value.items() if key != 'label')
            return '%s%s' % (value['label'], ' (%s)' % rest if rest else '')
        return ', '.join('%s=%s' % (key, fmt_val(item)) for key, item in value.items()) or '{}'
    if isinstance(value, list):
        return '[%s]' % ', '.join(fmt_val(item) for item in value)
    return fmt_val(value)


def section_title(reader):
    for pattern, title in SECTIONS:
        if re.search(pattern, reader):
            return title
    core = re.sub(r'^read|FromSaveRoot$', '', reader)
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', core).capitalize() or reader


def section_rank(reader):
    for rank, (pattern, _title) in enumerate(SECTIONS):
        if re.search(pattern, reader):
            return (rank, reader)
    return (len(SECTIONS), reader)


def ordered(changes):
    """Unlocks and level changes first, noise last; original order otherwise."""
    return [change for _rank, _index, change in sorted(
        ((1 if LOW_PRIORITY.search(change['path']) else 0, index, change) for index, change in enumerate(changes)),
        key=lambda item: (item[0], item[1]),
    )]


# --------------------------------------------------------------------------------------------
# Runs
# --------------------------------------------------------------------------------------------

def median(values):
    values = [value for value in values if is_number(value)]
    return statistics.median(values) if values else None


def per_hour(run, field):
    """Per REAL hour: `realTime` is wall-clock seconds, `gameTime` is sped-up in-game seconds."""
    amount, seconds = run.get(field), run.get('realTime')
    if not is_number(amount) or not is_number(seconds) or seconds <= 0:
        return None
    return amount / (seconds / 3600.0)


def run_stats(runs):
    normal = [run for run in runs if isinstance(run, dict) and run.get('isTournament') is not True
              and not run.get('dissonanceType')]
    # "Full" farming runs only: drop aborted runs (well under half the typical length), so the
    # median matches what the coach reports as income. Dissonant runs are excluded above.
    typical = median([run['realTime'] for run in normal if is_number(run.get('realTime'))])
    farming = [run for run in normal
               if typical is None or not is_number(run.get('realTime')) or run['realTime'] >= 0.5 * typical]
    tournament = [run for run in runs if isinstance(run, dict) and run.get('isTournament') is True]

    def block(rows):
        return {
            'runs': len(rows),
            'medianCoinsPerHour': median([per_hour(run, 'coinsEarned') for run in rows]),
            'medianCellsPerHour': median([per_hour(run, 'cellsEarned') for run in rows]),
            'medianWave': median([run.get('wave') for run in rows]),
            'medianRealHours': median([run['realTime'] / 3600.0 for run in rows if is_number(run.get('realTime'))]),
        }

    tiers = {}
    for run in farming:
        tiers.setdefault(run.get('tier'), []).append(run)
    dates = sorted(run.get('battleDate') for run in runs if isinstance(run, dict) and isinstance(run.get('battleDate'), str))
    return {
        'total': len(runs),
        'farming': block(farming),
        'farmingByTier': {str(tier): block(rows) for tier, rows in sorted(tiers.items(), key=lambda item: (item[0] is None, item[0]))},
        'tournament': {'runs': len(tournament), 'medianWave': median([run.get('wave') for run in tournament])},
        'newest': dates[-1] if dates else None,
        'oldest': dates[0] if dates else None,
    }


def runs_report(old_runs, new_runs):
    old_stats, new_stats = run_stats(old_runs), run_stats(new_runs)
    cutoff = old_stats['newest']
    fresh = [run for run in new_runs
             if isinstance(run, dict) and isinstance(run.get('battleDate'), str) and (cutoff is None or run['battleDate'] > cutoff)]
    return {'old': old_stats, 'new': new_stats, 'sinceOld': run_stats(fresh), 'newRunCount': len(fresh)}


def delta_text(old, new, unit=''):
    if old is None and new is None:
        return 'n/a'
    if old is None:
        return '%s%s (no earlier figure)' % (fmt_num(new), unit)
    if new is None:
        return '%s%s -> n/a' % (fmt_num(old), unit)
    if old == new:
        return '%s%s (unchanged)' % (fmt_num(new), unit)
    pct = ' (%+.1f%%)' % (100.0 * (new - old) / abs(old)) if old else ''
    return '%s%s -> %s%s%s' % (fmt_num(old), unit, fmt_num(new), unit, pct)


def runs_lines(report):
    old, new, since = report['old'], report['new'], report['sinceOld']
    lines = [
        'History holds %d runs (was %d); %d played since the older snapshot.' % (new['total'], old['total'], report['newRunCount']),
        'Rates are per REAL hour (coinsEarned / realTime). Medians over full normal farming runs',
        '(tournament, Dissonant and aborted runs excluded) that each snapshot holds.',
        '  farming coins/hr   %s' % delta_text(old['farming']['medianCoinsPerHour'], new['farming']['medianCoinsPerHour']),
        '  farming cells/hr   %s' % delta_text(old['farming']['medianCellsPerHour'], new['farming']['medianCellsPerHour']),
        '  farming wave       %s' % delta_text(old['farming']['medianWave'], new['farming']['medianWave']),
        '  farming run length %s' % delta_text(old['farming']['medianRealHours'], new['farming']['medianRealHours'], 'h'),
    ]
    tiers = sorted(set(old['farmingByTier']) | set(new['farmingByTier']), key=lambda tier: (not tier.isdigit(), int(tier) if tier.isdigit() else 0))
    for tier in tiers:
        before = old['farmingByTier'].get(tier, {})
        after = new['farmingByTier'].get(tier, {})
        lines.append('  tier %s (%d -> %d runs): wave %s | coins/hr %s | cells/hr %s' % (
            tier, before.get('runs', 0), after.get('runs', 0),
            delta_text(before.get('medianWave'), after.get('medianWave')),
            delta_text(before.get('medianCoinsPerHour'), after.get('medianCoinsPerHour')),
            delta_text(before.get('medianCellsPerHour'), after.get('medianCellsPerHour')),
        ))
    if old['tournament']['runs'] or new['tournament']['runs']:
        lines.append('  tournament (%d -> %d runs): wave %s' % (
            old['tournament']['runs'], new['tournament']['runs'],
            delta_text(old['tournament']['medianWave'], new['tournament']['medianWave'])))
    if report['newRunCount']:
        farming = since['farming']
        lines.append('  only the %d new runs (%d farming): coins/hr %s, cells/hr %s, wave %s' % (
            report['newRunCount'], farming['runs'], fmt_val(farming['medianCoinsPerHour']),
            fmt_val(farming['medianCellsPerHour']), fmt_val(farming['medianWave'])))
    return lines


# --------------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------------

SNAPSHOT_NAME = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{4}\.json$')


def load(path):
    try:
        with open(path, encoding='utf-8') as handle:
            data = json.load(handle)
    except OSError as error:
        sys.exit('diff_snapshots: cannot read %s: %s' % (path, error.strerror or error))
    except ValueError as error:
        sys.exit('diff_snapshots: %s is not JSON: %s' % (path, error))
    if not isinstance(data, dict) or not isinstance(data.get('readers'), dict):
        sys.exit('diff_snapshots: %s is not a snapshot (no "readers"). Make one with snapshot.mjs.' % path)
    data.setdefault('meta', {})
    data.setdefault('runs', [])
    return data


def snapshots_in(folder):
    return sorted(os.path.join(folder, name) for name in os.listdir(folder) if SNAPSHOT_NAME.match(name))


def latest_pair(folder):
    folder = os.path.expanduser(folder)
    if not os.path.isdir(folder):
        sys.exit('diff_snapshots: no snapshot folder at %s. Take a snapshot with snapshot.mjs first.' % folder)
    files = snapshots_in(folder)
    notes = []
    if not files:
        players = [os.path.join(folder, name) for name in sorted(os.listdir(folder)) if os.path.isdir(os.path.join(folder, name))]
        players = [(snapshots_in(player), player) for player in players]
        players = [(found, player) for found, player in players if found]
        if not players:
            sys.exit('diff_snapshots: no snapshots under %s.' % folder)
        players.sort(key=lambda item: os.path.basename(item[0][-1]))
        files, chosen = players[-1]
        if len(players) > 1:
            notes.append('%d players have snapshots; using %s (newest). Pass --dir <root>/<playerKey> for another.'
                         % (len(players), os.path.basename(chosen)))
    newest = files[-1]
    newest_export = load(newest)['meta'].get('exportedAt')
    skipped = 0
    for candidate in reversed(files[:-1]):
        if newest_export is not None and load(candidate)['meta'].get('exportedAt') == newest_export:
            skipped += 1
            continue
        if skipped:
            notes.append('Skipped %d older snapshot(s) of the same export as the newest.' % skipped)
        return candidate, newest, notes
    reason = 'only one snapshot' if len(files) == 1 else 'every snapshot is of the same export'
    sys.exit('diff_snapshots: nothing to compare in %s: %s. Re-export in game and snapshot again.'
             % (os.path.dirname(newest), reason))


def parse_time(text):
    if not isinstance(text, str):
        return None
    try:
        return datetime.fromisoformat(re.sub(r'(\.\d{6})\d+', r'\1', text.replace('Z', '+00:00')))
    except ValueError:
        return None


def elapsed_text(old_meta, new_meta):
    for field in ('exportedAt', 'snapshotAt'):
        before, after = parse_time(old_meta.get(field)), parse_time(new_meta.get(field))
        if before and after:
            try:
                hours = (after - before).total_seconds() / 3600.0
            except TypeError:
                continue
            span = '%.1f days' % (hours / 24.0) if abs(hours) >= 48 else '%.1f hours' % hours
            return '%s between exports' % span if field == 'exportedAt' else '%s between snapshots' % span
    return None


# --------------------------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------------------------

def build(old, new):
    sections = []
    names = sorted(set(old['readers']) | set(new['readers']), key=section_rank)
    for reader in names:
        before, after = old['readers'].get(reader), new['readers'].get(reader)
        changes = []
        state = lambda value: 'error' if isinstance(value, dict) and set(value) == {'error'} else ('absent' if value is None else 'ok')
        if reader not in old['readers']:
            changes.append({'path': '(reader)', 'kind': 'added', 'old': None, 'new': 'new reader in this SDK'})
        elif reader not in new['readers']:
            changes.append({'path': '(reader)', 'kind': 'removed', 'old': 'reader no longer in this SDK', 'new': None})
        elif state(before) != state(after) or state(after) == 'error':
            if before != after:
                changes.append({'path': '(reader)', 'kind': 'changed',
                                'old': before.get('error') if state(before) == 'error' else state(before),
                                'new': after.get('error') if state(after) == 'error' else state(after)})
        else:
            walk(before, after, '', changes)
            changes = [change for change in changes if not TIMER_NOISE.search(str(change.get('path', '')))]
        if changes:
            sections.append({'reader': reader, 'title': section_title(reader), 'total': len(changes), 'changes': ordered(changes)})
    changed = {section['reader'] for section in sections}
    return {
        'unchanged': [reader for reader in names if reader not in changed],
        'old': old['meta'],
        'new': new['meta'],
        'elapsed': elapsed_text(old['meta'], new['meta']),
        'sections': sections,
        'runs': runs_report(old['runs'], new['runs']),
    }


def render(report, cap, notes, old_path, new_path):
    old, new = report['old'], report['new']
    lines = ['# Snapshot diff', '']
    lines.append('old: %s  (exported %s, %s)' % (os.path.basename(old_path), old.get('exportedAt') or '?', old.get('gameVersion') or '?'))
    lines.append('new: %s  (exported %s, %s)' % (os.path.basename(new_path), new.get('exportedAt') or '?', new.get('gameVersion') or '?'))
    if report['elapsed']:
        lines.append(report['elapsed'])
    for note in notes:
        lines.append('note: %s' % note)
    if old.get('exportedAt') and old.get('exportedAt') == new.get('exportedAt'):
        lines.append('note: both snapshots are of the SAME export — differences below are not game progress.')
    if old.get('playerKey') and new.get('playerKey') and old['playerKey'] != new['playerKey']:
        lines.append('WARNING: these snapshots are from two different accounts.')
    for field, label in (('gameVersion', 'game version'), ('sdkVersion', 'SDK version')):
        if old.get(field) != new.get(field):
            lines.append('%s changed: %s -> %s (some differences may be reader changes, not progress)'
                         % (label, old.get(field) or '?', new.get(field) or '?'))
    for field in ('readersFailed', 'readersAbsent'):
        if new.get(field):
            lines.append('new snapshot %s: %s' % ('readers that threw' if field == 'readersFailed' else 'readers with no data', ', '.join(new[field])))

    if not report['sections']:
        lines += ['', 'No reader output changed.']
    for section in report['sections']:
        lines += ['', '## %s  [%s] — %d change%s' % (section['title'], section['reader'], section['total'], '' if section['total'] == 1 else 's')]
        for change in section['changes'][:cap]:
            lines.append(describe(change))
        if section['total'] > cap:
            lines.append('  ... and %d more (use --cap N or --json for all)' % (section['total'] - cap))

    if report.get('unchanged') and report['sections']:
        lines += ['', 'Unchanged since the old snapshot (nothing was spent or changed here): '
                  + ', '.join(name.replace('read', '', 1).replace('FromSaveRoot', '') for name in report['unchanged'])]

    lines += ['', '## Run history']
    lines += runs_lines(report['runs'])
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description='Diff two tower-coach snapshots.')
    parser.add_argument('old', nargs='?', help='older snapshot JSON')
    parser.add_argument('new', nargs='?', help='newer snapshot JSON')
    parser.add_argument('--latest', action='store_true', help='diff the two most recent snapshots in --dir')
    parser.add_argument('--dir', default=os.path.join('~', '.tower-coach', 'snapshots'),
                        help='snapshot root or one player folder (default ~/.tower-coach/snapshots)')
    parser.add_argument('--json', action='store_true', help='machine-readable output, uncapped')
    parser.add_argument('--cap', type=int, default=CAP_DEFAULT, help='changes shown per section (default %d)' % CAP_DEFAULT)
    args = parser.parse_args()

    notes = []
    if args.latest:
        if args.old or args.new:
            parser.error('--latest takes no snapshot paths')
        old_path, new_path, notes = latest_pair(args.dir)
    elif args.old and args.new:
        old_path, new_path = os.path.expanduser(args.old), os.path.expanduser(args.new)
    else:
        parser.error('give <old.json> <new.json>, or --latest')

    old, new = load(old_path), load(new_path)
    old_at, new_at = old['meta'].get('exportedAt'), new['meta'].get('exportedAt')
    if isinstance(old_at, str) and isinstance(new_at, str) and old_at > new_at:
        notes.append('The first snapshot is the NEWER export; arrows read old-argument -> new-argument regardless.')

    report = build(old, new)
    if args.json:
        json.dump({'oldFile': os.path.basename(old_path), 'newFile': os.path.basename(new_path), 'notes': notes, **report},
                  sys.stdout, indent=1, default=str)
        sys.stdout.write('\n')
    else:
        sys.stdout.write(render(report, max(1, args.cap), notes, old_path, new_path))


if __name__ == '__main__':
    main()
