#!/usr/bin/env python3
"""Reconcile the graph's authored tier against source. Read-only by default.

    graph_walker.py --descriptors <dir> --report
    graph_walker.py --descriptors <dir> --report --by package
    graph_walker.py --descriptors <dir> --accept app.mod.Alpha --apply

WHAT THIS ANSWERS

The mechanical tier self-heals: re-run the extractor and classes, bases and line
numbers are correct again. The authored tier does not. It is written once, and
nothing has ever said which parts are still true. Over months that produces a
graph full of confident descriptions of code that no longer works that way, and
no way to tell those from the accurate ones.

FOUR STATES

    UNSEMANTIC        no authored fields. The extractor refusing to guess.
    AUTHORED          authored, and the source has not moved since.
    SEMANTICS_STALE   authored, but its source changed underneath it.
    RETIRED           gone from source; prose retained under `nodes_retired`.

`UNSEMANTIC` is a state, not a defect. A brand new project is entirely
unsemantic and that is correct.

WHY IT IS READ-ONLY

Everything here except `--accept` reports. Deleting authored prose is reserved
for an explicit act, because the failure this subsystem exists to prevent is a
regeneration quietly discarding human work - and a walker that tidies up on its
own would be that failure wearing a different hat.

`--accept` is the one write, and it is narrow: it re-stamps a node whose
semantics you have RE-READ and confirmed. It changes no prose. Accepting without
reading is how a graph becomes confidently wrong, so the stamp records the
source it was accepted against, not the fact that someone ran a command.
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

AUTHORED_NODE_FIELDS = ("include", "role", "responsibilities", "owns_state", "phases")
STAMP = "semantics_authored_against"


def load(root: pathlib.Path) -> dict[pathlib.Path, dict]:
    out: dict[pathlib.Path, dict] = {}
    for p in sorted(root.rglob("*.json")):
        if p.name == "_package_candidates.json":
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"  SKIP (bad json) {p}: {exc}", file=sys.stderr)
            continue
        if isinstance(d, dict) and "source" in d and "nodes" in d:
            out[p] = d
    return out


def write_descriptor(path: pathlib.Path, d: dict) -> None:
    """Write a descriptor exactly as extract_graph.py does: `indent=1`, LF.

    The extractor owns these files and rewrites every one on each run. Written
    any other way, a one-line stamp becomes a whole-file diff, and the next
    extraction reverses it line by line.
    """
    path.write_text(json.dumps(d, indent=1) + "\n", encoding="utf-8", newline="\n")


def stranded_descriptors(descriptors: dict[pathlib.Path, dict],
                         src_root: pathlib.Path) -> list[tuple[pathlib.Path, str, int]]:
    """Descriptors whose source file no longer exists.

    A blind spot the extractor cannot have: it walks SOURCE files and merges each
    into its descriptor, so a file deleted from source is never visited, its
    descriptor is never opened, and every node in it keeps counting as live and
    AUTHORED forever. Deleting one class gets reported; deleting the file holding
    it is silent.

    Only a pass that starts from the DESCRIPTORS and looks back at source can
    see it, which is this tool.
    """
    out = []
    for path, d in descriptors.items():
        source = d.get("source", "")
        # `source` is `<src_root.name>/<rel>`; strip the root name to rejoin.
        rel = source.split("/", 1)[1] if "/" in source else source
        if not (src_root / rel).is_file():
            authored = sum(1 for n in d.get("nodes", {}).values()
                           if any(f in n for f in AUTHORED_NODE_FIELDS))
            out.append((path, source, authored))
    return out


def state_of(node: dict) -> str:
    if not any(f in node for f in AUTHORED_NODE_FIELDS):
        return "UNSEMANTIC"
    stamp, current = node.get(STAMP), node.get("span_sha256", "")
    # NO STAMP MEANS NOT VERIFIED, AND THAT IS SEMANTICS_STALE.
    #
    # `AUTHORED` claims one specific thing: someone read this prose against this
    # source. A node with no stamp has never had that done, so returning AUTHORED
    # for it is a false claim - and it was the actual defect here. Nothing was
    # wrong with the state machine; the extractor was papering over the gap by
    # stamping unverified nodes "current" so they would land in AUTHORED.
    #
    # Yes, this means an existing graph reports a large stale count on the first
    # run after upgrading. That number is correct. It is the count of nodes nobody
    # has checked, which is the question this tool exists to answer, and hiding it
    # to make day one look tidy is how the census stopped meaning anything.
    # Test for the KEY, not for a truthy value. A node with no `span_sha256` -
    # module nodes, which describe a whole file rather than a span - is accepted
    # with an empty stamp, and that is a legitimate acceptance: there is nothing
    # to hash, so "" is the correct record of what it was accepted against.
    # Checking truthiness instead made those nodes permanently stale, unable to
    # leave the state no matter how many times a human read and accepted them.
    if STAMP not in node:
        return "SEMANTICS_STALE"
    if current and stamp != current:
        return "SEMANTICS_STALE"
    return "AUTHORED"


def census(descriptors: dict[pathlib.Path, dict]) -> list[dict]:
    """One row per node, with the state and where it lives."""
    rows = []
    for path, d in descriptors.items():
        source = d.get("source", str(path))
        package = source.rsplit("/", 1)[0] if "/" in source else source
        for nid, node in d.get("nodes", {}).items():
            rows.append({"id": nid, "state": state_of(node), "source": source,
                         "package": package, "descriptor": path})
        for nid, node in d.get("nodes_retired", {}).items():
            rows.append({"id": nid, "state": "RETIRED", "source": source,
                         "package": package, "descriptor": path})
    return rows


def find_rename_candidates(descriptors: dict[pathlib.Path, dict]) -> list[tuple[str, str, str]]:
    """Retired nodes whose label reappears elsewhere - a probable cross-file move.

    The extractor works one file at a time, so it cannot see that a class it
    just retired turned up in a different descriptor. Only a whole-graph pass
    can, which is the main reason this tool exists rather than being folded into
    extraction.

    SUGGESTED, never applied. A same-label match is evidence, not proof, and
    moving someone's authored prose onto the wrong class is worse than leaving
    it retired where they can see it.
    """
    live_by_label: dict[str, list[str]] = collections.defaultdict(list)
    for d in descriptors.values():
        for nid, node in d.get("nodes", {}).items():
            live_by_label[node.get("label", "")].append(nid)

    out = []
    for d in descriptors.values():
        for nid, node in d.get("nodes_retired", {}).items():
            for candidate in live_by_label.get(node.get("label", ""), []):
                if candidate != nid:
                    out.append((nid, candidate, node.get("label", "")))
    return out


def report(descriptors: dict[pathlib.Path, dict], group_by: str,
           src_root: pathlib.Path | None) -> int:
    rows = census(descriptors)
    if not rows:
        print("no nodes found - is --descriptors pointing at an extractor output tree?")
        return 2

    counts = collections.Counter(r["state"] for r in rows)
    total = len(rows)
    print(f"  {len(descriptors)} descriptors, {total} nodes\n")
    print(f"  {'state':<18} {'count':>6}   share")
    print(f"  {'-' * 18} {'-' * 6}   -----")
    for state in ("AUTHORED", "SEMANTICS_STALE", "UNSEMANTIC", "RETIRED"):
        n = counts.get(state, 0)
        print(f"  {state:<18} {n:>6}   {100 * n / total:5.1f}%")

    stale = [r for r in rows if r["state"] == "SEMANTICS_STALE"]
    retired = [r for r in rows if r["state"] == "RETIRED"]

    if stale:
        print(f"\n  SEMANTICS_STALE - re-read the source, then --accept:")
        for r in stale[:20]:
            print(f"    {r['id']}  ({r['source']})")
        if len(stale) > 20:
            print(f"    ... +{len(stale) - 20} more")

    if retired:
        print(f"\n  RETIRED - prose retained, gone from source:")
        for r in retired[:20]:
            print(f"    {r['id']}  (was in {r['source']})")
        if len(retired) > 20:
            print(f"    ... +{len(retired) - 20} more")

    stranded = stranded_descriptors(descriptors, src_root) if src_root else []
    if stranded:
        print(f"\n  STRANDED DESCRIPTORS - their source file is gone: {len(stranded)}")
        for path, source, authored in stranded[:15]:
            note = f"{authored} authored node(s)" if authored else "no authored content"
            print(f"    {source}  ->  {note}")
        print("    The extractor walks SOURCE, so it never opens these and their nodes")
        print("    keep counting as live. Move any authored prose you want to keep,")
        print("    then delete the descriptor by hand.")
    elif src_root is None:
        print("\n  (pass --src to also detect descriptors whose source file is gone)")

    renames = find_rename_candidates(descriptors)
    if renames:
        print(f"\n  POSSIBLE MOVES - a retired label that exists elsewhere now:")
        for old, new, label in renames[:10]:
            print(f"    {old}\n      -> {new}   (both labelled `{label}`)")
        print("    Suggested only. Verify, then copy the authored fields across by")
        print("    hand - a same-label match is evidence, not proof.")

    # Aggregated at the unit an agent actually works in: a subsystem at a time.
    # Per-node output on a real codebase is thousands of lines nobody reads.
    key = "package" if group_by == "package" else "source"
    grouped: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for r in rows:
        grouped[r[key]][r["state"]] += 1

    needs_work = {k: c for k, c in grouped.items()
                  if c["UNSEMANTIC"] or c["SEMANTICS_STALE"]}
    if needs_work:
        print(f"\n  BY {key.upper()} - where the work is ({len(needs_work)} with any):\n")
        print(f"  {'unsem':>6} {'stale':>6} {'auth':>6}   {key}")
        for k, c in sorted(needs_work.items(),
                           key=lambda kv: -(kv[1]['UNSEMANTIC'] + kv[1]['SEMANTICS_STALE'])):
            print(f"  {c['UNSEMANTIC']:>6} {c['SEMANTICS_STALE']:>6} "
                  f"{c['AUTHORED']:>6}   {k}")

    print(f"\n  Nothing was written. Semantics must be AUTHORED BY READING THE CODE -")
    print(f"  `owns_lifecycle_of`, `uses` and `borrows` are the same syntax, so a")
    print(f"  name-based guess is worse than leaving a node unsemantic.")
    return 1 if (counts.get("SEMANTICS_STALE") or counts.get("RETIRED")) else 0


def accept(descriptors: dict[pathlib.Path, dict], ids: list[str], apply: bool) -> int:
    """Re-stamp nodes whose semantics have been re-verified against source."""
    wanted = set(ids)
    hits: list[tuple[pathlib.Path, str, str]] = []
    for path, d in descriptors.items():
        for nid, node in d.get("nodes", {}).items():
            if nid in wanted:
                hits.append((path, nid, state_of(node)))

    missing = wanted - {nid for _, nid, _ in hits}
    for nid in sorted(missing):
        print(f"  NOT FOUND: {nid}")

    for path, nid, state in hits:
        if state == "UNSEMANTIC":
            print(f"  SKIP {nid} - unsemantic; there is nothing to accept. Author it first.")
            continue
        print(f"  {'ACCEPT' if apply else 'WOULD ACCEPT'} {nid}  (was {state})")

    if not apply:
        print("\n  Nothing written. Re-run with --apply once you have RE-READ each one.")
        return 0

    written = 0
    for path, d in descriptors.items():
        touched = False
        for nid, node in d.get("nodes", {}).items():
            if nid in wanted and state_of(node) != "UNSEMANTIC":
                node[STAMP] = node.get("span_sha256", "")
                touched = True
        if touched:
            write_descriptor(path, d)
            written += 1
    print(f"\n  ACCEPTED into {written} descriptor(s). Reassemble to refresh the document.")
    return 0 if not missing else 1


def confirm(question: str, assume_yes: bool) -> bool:
    """Ask before doing something irreversible.

    Refuses rather than assuming when there is no terminal to ask at. A prompt
    that silently self-answers in CI is not a prompt, and the one verb this
    guards is the only one that destroys authored work.
    """
    if assume_yes:
        print(f"  {question}  [--yes]")
        return True
    if not sys.stdin.isatty():
        print(f"  {question}")
        print("  REFUSED: not a terminal, so there is nobody to ask. Pass --yes if you")
        print("           mean it, having read the list above.")
        return False
    try:
        answer = input(f"  {question} [y/N] ").strip().lower()
    except EOFError:
        # `isatty()` said yes and then there was nothing to read. Some CI
        # harnesses hand a process a stdin that claims to be a terminal but
        # closes on first read, so this is the same situation as no terminal
        # at all - and it gets the same answer and the same wording, rather
        # than a softer one that reads like the user chose to cancel.
        print("\n  REFUSED: stdin closed before answering, so nobody confirmed.")
        print("           Pass --yes if you mean it, having read the list above.")
        return False
    except KeyboardInterrupt:
        print("\n  cancelled")
        return False
    return answer in ("y", "yes")


def reconcile(descriptors: dict[pathlib.Path, dict], assume_yes: bool) -> int:
    """Delete retired nodes. The only sanctioned path for structural deletion.

    A node reaches `nodes_retired` because it left source. Clearing it is the
    act that says "that removal was real and its semantics are not coming back"
    - which is a judgement, not a derivation, so it is asked rather than
    inferred. Everything else in this tool reports.
    """
    victims: list[tuple[pathlib.Path, str, dict]] = []
    for path, d in descriptors.items():
        for nid, node in d.get("nodes_retired", {}).items():
            victims.append((path, nid, node))

    if not victims:
        print("  nothing retired - nothing to reconcile")
        return 0

    print(f"  {len(victims)} retired node(s) would be DELETED, with their authored prose:\n")
    for path, nid, node in victims[:25]:
        role = str(node.get("role", "")).strip()
        summary = (role[:72] + "...") if len(role) > 72 else (role or "(no role)")
        fields = [f for f in AUTHORED_NODE_FIELDS if f in node]
        print(f"    {nid}")
        print(f"      was in : {node.get('file', '?')}")
        print(f"      fields : {', '.join(fields)}")
        print(f"      role   : {summary}")
    if len(victims) > 25:
        print(f"    ... +{len(victims) - 25} more")

    print("\n  This is not recoverable from the descriptor afterwards - only from")
    print("  version control. If any of these is a MOVE rather than a deletion,")
    print("  copy its authored fields onto the new node first (--report lists")
    print("  possible moves).")

    if not confirm(f"Delete {len(victims)} retired node(s)?", assume_yes):
        print("  nothing written")
        return 1

    written = 0
    for path, d in descriptors.items():
        if d.pop("nodes_retired", None):
            write_descriptor(path, d)
            written += 1
    print(f"\n  RECONCILED: cleared retired nodes from {written} descriptor(s).")
    print("  Reassemble to refresh the document.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--descriptors", required=True, type=pathlib.Path)
    ap.add_argument("--src", type=pathlib.Path, default=None,
                    help="source root; enables detection of descriptors whose "
                         "source file no longer exists")
    ap.add_argument("--report", action="store_true", help="four-state census (default)")
    ap.add_argument("--by", choices=("package", "file"), default="package",
                    help="aggregate the work table by package or by file")
    ap.add_argument("--accept", metavar="NODE_ID", action="append", default=[],
                    help="re-stamp a node whose semantics you have re-verified; repeatable")
    ap.add_argument("--reconcile", action="store_true",
                    help="DELETE retired nodes and their authored prose. Prompts first; "
                         "the only sanctioned path for structural deletion")
    ap.add_argument("--yes", action="store_true",
                    help="answer the confirmation prompt yes (for automation)")
    ap.add_argument("--apply", action="store_true", help="write the accepted stamps")
    args = ap.parse_args()

    if not args.descriptors.is_dir():
        print(f"ERROR: descriptor root not found: {args.descriptors}")
        return 2

    descriptors = load(args.descriptors)
    if not descriptors:
        print(f"ERROR: no descriptors under {args.descriptors}")
        return 2

    if args.src is not None and not args.src.is_dir():
        print(f"ERROR: source root not found: {args.src}")
        return 2

    if args.accept:
        return accept(descriptors, args.accept, args.apply)
    if args.reconcile:
        return reconcile(descriptors, args.yes)
    return report(descriptors, args.by, args.src)


if __name__ == "__main__":
    raise SystemExit(main())
