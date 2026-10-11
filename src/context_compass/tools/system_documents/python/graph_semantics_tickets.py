#!/usr/bin/env python3
"""Turn unauthored graph areas into tickets. On demand, prompted, idempotent.

    graph_semantics_tickets.py --descriptors <dir> --tickets <dir>            # dry run
    graph_semantics_tickets.py --descriptors <dir> --tickets <dir> --create

OFF BY DEFAULT, AND IT HAS TO BE

A library that writes tickets into somebody's board without being asked is doing
something hostile. Nothing here runs as part of extraction or assembly; this is a
separate command, dry-run by default, and it asks before writing.

The install's `config/context_compass_config.yaml`, beside the `tickets/` lane,
selects the backend. Local `--create` is refused for github_codex_plugin. Its
dry run reports the graph census only and never reads inactive local tickets.

AGGREGATED AT THE PACKAGE, WHICH IS THE WHOLE DESIGN CONSTRAINT

On a real codebase the census is ~1,188 unsemantic nodes across ~575 files.

    one ticket per node   1,188 tickets   destroys the board
    one ticket per file     575 tickets   destroys the board
    one story per package    ~33 stories  usable

The attention board is a routing surface carrying roughly a dozen active rows.
Any design emitting per-node or per-file work is unusable on the first real
repository it meets. A package is also the unit an agent actually works in - a
subsystem at a time - so it is the natural granularity as well as the survivable
one.

    1 epic       "Author graph semantics"        the backlog as a whole
      N stories  one per package needing work    only where there is work

**Tasks are deliberately not generated.** Task granularity is the working
agent's judgement, and pre-generating it presumes an approach to work nobody has
started yet.

IDEMPOTENCY IS NOT OPTIONAL

Ticket ids derive from the package path, so re-running updates rather than
duplicates. A scan that doubles the board every run gets switched off within a
day and never switched back on. Equally, a package whose semantics get authored
has its story reported as SATISFIED rather than left open forever - the loop has
to close in both directions or it is just a different kind of noise.
"""

from __future__ import annotations

import argparse
import collections
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from graph_walker import census, load, confirm  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from ticket_backend import BackendConfigError, read_backend  # noqa: E402

STORY_MARKER = "GRAPH-SEM"
EPIC_SLUG = "author-graph-semantics"


def slug(package: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", package.lower()).strip("-") or "root"


def today() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def find_existing(lane: pathlib.Path, marker: str) -> pathlib.Path | None:
    """Any ticket carrying this id, in ANY lane - active, backlog or completed.

    Completed lanes are searched too. Missing them is how a scan re-creates a
    story somebody already finished, which is the fastest way to lose trust in
    generated work.

    Matched on a WORD BOUNDARY, not as a substring. Package slugs nest:
    `GRAPH-SEM-src-example` is a prefix of `GRAPH-SEM-src-example-core`, so a
    substring search made the root package find the core package's story and
    overwrite it. Sorted iteration keeps the answer stable when a marker somehow
    appears in two files.
    """
    if not lane.is_dir():
        return None
    pattern = re.compile(re.escape(marker) + r"(?![0-9A-Za-z-])")
    for p in sorted(lane.rglob("*.md")):
        try:
            if pattern.search(p.read_text(encoding="utf-8", errors="replace")):
                return p
        except OSError:
            continue
    return None


def story_body(package: str, story_id: str, epic_id: str,
               unsemantic: list[str], stale: list[str]) -> str:
    total = len(unsemantic) + len(stale)
    return f"""

# Story: Author graph semantics for `{package}`

## Metadata
- Story ID: {story_id}
- Epic: {epic_id}
- Status: draft
- Owner:
- Agent Name:
- Priority: p2
- Created: {stamp()}
- Updated: {stamp()}

## User Narrative
As an agent reading the source graph, I want `{package}` to carry authored
semantics, so that I can tell what its objects are FOR without re-deriving it
from the code every time.

## Value / MRP Alignment
The mechanical tier already says what exists. Without the authored tier the graph
cannot say what anything means, and every reader pays the same rediscovery cost.

## Ticket Contract
- ENTRY_GATE: active board row exists and the graph is current (`extract_graph.py --check`).
- EXECUTION_BOUNDARY: descriptors under `{package}` only. Do not author neighbouring packages.
- DEPENDENCIES: {epic_id}
- EXIT_GATE: every node below carries `role` and `responsibilities`; `graph_walker.py --report` shows 0 unsemantic and 0 stale for this package; graph reassembled.
- FAILURE_ESCALATION: raise DECISION_REQUEST if a node's purpose cannot be established from source.

## Requirements (Functional)
- Author `role` and `responsibilities` for each node listed below.
- Author `owns_state` and `phases` where the source supports them.
- Author `edges_authored` for relationships this package owns or borrows.

## Requirements (Non-Functional)
- **Semantics must be authored by READING THE CODE.** Never inferred from names.
- `owns_lifecycle_of`, `uses` and `borrows` are syntactically identical - `self._x = x`
  in all three cases. The difference is design intent that appears nowhere in the
  source text. Measured on a labelled corpus, a cleanup-contract heuristic
  discriminated at 21% vs 21% - no signal at all. Invented semantics are worse
  than none, because they read as verified.

## Scope Boundaries
- IN: authored tier for `{package}`.
- OUT: mechanical fields, other packages, refactoring the source.

## State Transition Event
- draft -> ready when an agent claims it on the attention board.

## Dependencies / Related Work
- Epic: {epic_id}

## Tasks (Implementation Checklist)
- [ ] Read the source for each node below.
- [ ] Author the semantic fields in the descriptors.
- [ ] Reassemble the graph and verify ranges.
- [ ] `graph_walker.py --report` shows this package clean.

## Acceptance Criteria
- {total} node(s) below carry authored semantics grounded in the source.
- No node authored from its name alone.

## Validation / Test Plan
```bash
python context_compass/tools/system_documents/python/graph_walker.py \\
    --descriptors <descriptors> --report --by package
```

## Nodes To Author

Unsemantic ({len(unsemantic)}):
{chr(10).join(f"- `{n}`" for n in unsemantic) or "- none"}

Semantics stale ({len(stale)}) - source changed under existing prose, re-verify then
`graph_walker.py --accept <id> --apply`:
{chr(10).join(f"- `{n}`" for n in stale) or "- none"}

## Open Questions
- (none recorded)

## Decision Log
- {stamp()}: generated by `graph_semantics_tickets.py` from the graph census.

## Notes
- Generated. Re-running the scan UPDATES this ticket rather than creating another.
- The `{STORY_MARKER}` id above is what makes that work; do not remove it.

## Context / Handoff Summary
Author the semantic tier for `{package}`. The node list is the scope. Read the
code; do not infer from names.
"""


def epic_table(packages: list[tuple[str, int, int]]) -> str:
    """The generated Stories table, and nothing else.

    Split out from `epic_body` so an existing epic can have JUST this block
    refreshed. Everything else in that file may be authored, and authored
    content is not this tool's to rewrite.
    """
    # Header and separator are not decoration. Without them this is not a Markdown
    # table at all - it renders as literal pipe-delimited text - and the two integer
    # columns are unlabelled, so a reader cannot tell which one is stale and which
    # is unsemantic. They are different kinds of work: unsemantic means nobody has
    # written it, stale means somebody did and the source moved underneath it.
    return "\n".join(
        ["| package | unsemantic | stale |", "| --- | --- | --- |"]
        + [f"| `{p}` | {u} | {s} |" for p, u, s in packages]
    )


EPIC_ID_RE = re.compile(r"^- Epic ID: (\S+)\s*$", re.M)
EPIC_TABLE_RE = re.compile(
    r"(## Stories \(Required to Complete\)\n).*?(Total nodes needing work: \d+)", re.S)


def existing_epic_id(path: pathlib.Path | None) -> str | None:
    """The epic id already on disk, if there is one.

    Minting `EPIC-{today}-...` on every run silently renamed the epic each time
    the tool ran, and every story got a `- Epic:` pointing at the NEW id. Any
    story the run skipped - a SATISFIED one, i.e. finished work - kept the old
    id and was orphaned by the rename. The id is the join key; it has to be
    stable or the join is decorative.
    """
    if path is None or not path.exists():
        return None
    m = EPIC_ID_RE.search(path.read_text(encoding="utf-8", errors="replace"))
    return m.group(1) if m else None


def refresh_epic_table(text: str, packages: list[tuple[str, int, int]]) -> str | None:
    """Replace only the generated table inside an existing epic.

    Returns None if the block is not found, in which case the caller should not
    guess - better to leave the file alone and say so than to overwrite prose.
    """
    total = sum(u + s for _, u, s in packages)
    table = epic_table(packages)
    if not EPIC_TABLE_RE.search(text):
        return None
    return EPIC_TABLE_RE.sub(
        lambda m: f"{m.group(1)}{table}\n\nTotal nodes needing work: {total}", text)


def epic_body(epic_id: str, packages: list[tuple[str, int, int]]) -> str:
    total = sum(u + s for _, u, s in packages)
    rows = epic_table(packages)
    return f"""

# Epic: Author graph semantics

## Metadata
- Epic ID: {epic_id}
- Status: draft
- Owner:
- Agent Name:
- Priority: p2
- Created: {stamp()}
- Updated: {stamp()}

## Problem / Opportunity
The source graph's mechanical tier self-heals on every extraction. The authored
tier does not exist until somebody writes it, and until then the graph can say
what exists but not what any of it is for.

## MRP Alignment (Most Reasonable Product)
Authoring semantics per package, in the order the work is actually done, rather
than attempting the whole graph at once.

## Ticket Contract
- ENTRY_GATE: the graph is current.
- EXECUTION_BOUNDARY: descriptors only. No source changes.
- DEPENDENCIES: none.
- EXIT_GATE: every story below closed; `graph_walker.py --report` shows 0 stale.
- FAILURE_ESCALATION: DECISION_REQUEST when a node's purpose is not establishable.

## Goals (Outcomes)
- Every graph node carries authored meaning, or is explicitly recorded as not
  worth authoring.

## Non-Goals (Explicit Exclusions)
- Generating semantics automatically. It was tested against a labelled corpus and
  the most valuable fields are not derivable; see the story requirements.
- Refactoring source to make it more derivable.

## Success Metrics
- `graph_walker.py --report`: UNSEMANTIC and SEMANTICS_STALE both at 0.

## Stories (Required to Complete)
{rows}

Total nodes needing work: {total}

## Notes
- Generated by `graph_semantics_tickets.py`. Re-running updates rather than duplicates.
- The `{STORY_MARKER}` id above is what makes that work; do not remove it.

## Context / Handoff Summary
One story per package with unauthored or stale semantics. Work a subsystem at a
time; the stories are ordered by how much is outstanding.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--descriptors", required=True, type=pathlib.Path)
    ap.add_argument("--tickets", required=True, type=pathlib.Path,
                    help="the tickets/ lane root of the install")
    ap.add_argument("--create", action="store_true",
                    help="write the tickets (default is a dry run)")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    ap.add_argument("--min-nodes", type=int, default=1,
                    help="skip packages with fewer than this many nodes needing work")
    ap.add_argument("--depth", type=int, default=0,
                    help="group at this path depth instead of the containing "
                         "directory, e.g. 3 turns src/a/b/c/d into src/a/b. Use it "
                         "when the directory-level count is too many stories")
    args = ap.parse_args()

    config_path = args.tickets.parent / "config" / "context_compass_config.yaml"
    try:
        backend = read_backend(config_path)
    except BackendConfigError as exc:
        print(f"ERROR: {config_path}: {exc}")
        return 2
    if args.create and backend == "github_codex_plugin":
        print("REFUSED: github_codex_plugin uses Issues; local --create is disabled.")
        print("Use the dry-run census and compose tickets through the connected plugin.")
        return 1

    if not args.descriptors.is_dir():
        print(f"ERROR: descriptor root not found: {args.descriptors}")
        return 2
    if backend == "local" and not args.tickets.is_dir():
        print(f"ERROR: tickets lane not found: {args.tickets}")
        return 2

    rows = census(load(args.descriptors))
    if not rows:
        print("no nodes found - is --descriptors an extractor output tree?")
        return 2

    # Every package gets an entry, including ones with nothing outstanding.
    # Populating only the packages with work meant a package that got fully
    # authored simply vanished from the map, so it could never be compared
    # against and its story was never reported SATISFIED - the loop closed in
    # one direction only, which is how generated tickets become permanent noise.
    def group_of(package: str) -> str:
        if args.depth and args.depth > 0:
            return "/".join(package.split("/")[:args.depth])
        return package

    by_pkg: dict[str, dict[str, list[str]]] = collections.defaultdict(
        lambda: {"UNSEMANTIC": [], "SEMANTICS_STALE": []})
    for r in rows:
        entry = by_pkg[group_of(r["package"])]
        if r["state"] in ("UNSEMANTIC", "SEMANTICS_STALE"):
            entry[r["state"]].append(r["id"])

    needing = {p: v for p, v in by_pkg.items()
               if len(v["UNSEMANTIC"]) + len(v["SEMANTICS_STALE"]) >= args.min_nodes}

    if backend == "github_codex_plugin":
        print("  backend: github_codex_plugin")
        print("  DRY RUN: graph census only; local ticket history is inactive.")
        for package, states in sorted(needing.items()):
            print(f"    {package}: {len(states['UNSEMANTIC'])} unsemantic, "
                  f"{len(states['SEMANTICS_STALE'])} stale")
        print("  Read existing Issues through the plugin before composing or updating tickets.")
        return 0

    stories_lane = args.tickets / "stories"
    epics_lane = args.tickets / "epics"
    epic_existing = find_existing(epics_lane, EPIC_SLUG)
    epic_id = existing_epic_id(epic_existing) or f"EPIC-{today()}-{EPIC_SLUG}"

    # Both directions of the loop: what needs a ticket, and what no longer does.
    satisfied = []
    for package in sorted(set(by_pkg) - set(needing)):
        marker = f"{STORY_MARKER}-{slug(package)}"
        existing = find_existing(stories_lane, marker)
        if existing:
            satisfied.append((package, existing))

    print(f"  packages with work : {len(needing)}")
    print(f"  nodes to author    : "
          f"{sum(len(v['UNSEMANTIC']) + len(v['SEMANTICS_STALE']) for v in needing.values())}")
    print(f"  epic               : {epic_id}")

    # Guidance, not a refusal. The directory-level count is right for a small
    # package and far too many for a deep one - measured on a real 575-file tree
    # it was 146 stories, where the design target was a board carrying about a
    # dozen active rows. Show the levers rather than silently emitting 146.
    LOUD = 50
    if len(needing) > LOUD and not args.depth:
        depths = {d: len({"/".join(p.split("/")[:d]) for p in needing})
                  for d in (3, 4, 5)}
        print()
        print(f"  {len(needing)} stories is a lot for a routing board. Two levers:")
        for d, n in depths.items():
            if n < len(needing):
                print(f"    --depth {d}      ->  {n:>3} stories  "
                      f"(group at src/a/b{'/c' * (d - 3)})")
        sizes = sorted(len(v["UNSEMANTIC"]) + len(v["SEMANTICS_STALE"])
                       for v in needing.values())
        for m in (3, 5, 10):
            n = sum(1 for s in sizes if s >= m)
            if n < len(needing):
                print(f"    --min-nodes {m:<3} ->  {n:>3} stories  "
                      f"(skip packages with fewer than {m} nodes)")
        print("  Neither loses work - the nodes are still in the census either way.")
    print()

    plan: list[tuple[str, str, pathlib.Path | None]] = []
    for package, states in sorted(
            needing.items(),
            key=lambda kv: -(len(kv[1]["UNSEMANTIC"]) + len(kv[1]["SEMANTICS_STALE"]))):
        marker = f"{STORY_MARKER}-{slug(package)}"
        existing = find_existing(stories_lane, marker)
        verb = "UPDATE" if existing else "CREATE"
        n = len(states["UNSEMANTIC"]) + len(states["SEMANTICS_STALE"])
        print(f"    {verb:<6} {package}  ({n} node(s))"
              + (f"  -> {existing.name}" if existing else ""))
        plan.append((verb, package, existing))

    for package, path in satisfied:
        print(f"    SATISFIED {package}  -> {path.name}")
        print(f"              nothing left unauthored; close it by hand")

    if not plan:
        # Nothing left to author is exactly when the epic's table is MOST wrong: it still
        # lists whatever was outstanding on the last run that had work. Returning here
        # without refreshing left a completed epic advertising N nodes still needing
        # work - the table contradicting the thing it summarises. Empty the table so the
        # finished state is legible, but only with --create, because a dry run must not write.
        print("\n  nothing to do")
        if args.create and epic_existing:
            prior = epic_existing.read_text(encoding="utf-8", errors="replace")
            spliced = refresh_epic_table(prior, [])
            if spliced is not None and spliced != prior:
                epic_existing.write_text(spliced, encoding="utf-8")
                print(f"  Refreshed the Stories table in {epic_existing.name}: 0 outstanding.")
        return 0

    if not args.create:
        print(f"\n  DRY RUN. {len(plan)} story/stories and 1 epic would be written to")
        print(f"  {stories_lane} and {epics_lane}.")
        print("  Re-run with --create to write them.")
        return 0

    if not confirm(f"Write 1 epic and {len(plan)} story/stories into {args.tickets}?",
                   args.yes):
        print("  nothing written")
        return 1

    stories_lane.mkdir(parents=True, exist_ok=True)
    epics_lane.mkdir(parents=True, exist_ok=True)

    written = 0
    epic_rows = []
    for verb, package, existing in plan:
        states = needing[package]
        marker = f"{STORY_MARKER}-{slug(package)}"
        story_id = f"STORY-{today()}-{marker}"
        target = existing or (stories_lane / f"{today()}_{slug(package)}_graph_semantics_story.md")
        target.write_text(
            story_body(package, story_id, epic_id,
                       sorted(states["UNSEMANTIC"]), sorted(states["SEMANTICS_STALE"])),
            encoding="utf-8")
        written += 1
        epic_rows.append((package, len(states["UNSEMANTIC"]), len(states["SEMANTICS_STALE"])))

    epic_path = epic_existing or (epics_lane / f"{today()}_{EPIC_SLUG}_epic.md")
    if epic_existing:
        # An epic that already exists is a document somebody has been working in:
        # status, owner, decision log, notes. Rewriting the whole body to refresh
        # a generated table destroys all of it. Refresh the table in place.
        prior = epic_path.read_text(encoding="utf-8", errors="replace")
        spliced = refresh_epic_table(prior, epic_rows)
        if spliced is None:
            print(f"\n  SKIPPED epic {epic_path.name}: no generated Stories block found.")
            print("  Refusing to overwrite - the file has been restructured by hand.")
        else:
            epic_path.write_text(spliced, encoding="utf-8")
    else:
        epic_path.write_text(epic_body(epic_id, epic_rows), encoding="utf-8")

    print(f"\n  WROTE: {written} story/stories, 1 epic")
    print(f"    epic    {epic_path}")
    print(f"    stories {stories_lane}")
    print("\n  These are DRAFTS. Route them through the attention board as normal;")
    print("  nothing here touches the board, because a generated ticket claiming an")
    print("  active row is a ticket nobody agreed to take.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
