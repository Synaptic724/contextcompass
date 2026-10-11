#!/usr/bin/env python3
"""Prove the suite fails when the tools are broken.

A green suite means nothing on its own - it is equally consistent with "the code
is correct" and "the tests assert nothing". This applies a set of deliberate
one-line defects, each one a plausible mistake or an inversion of a rule the
tools document, and requires that at least one test fails for every single one.

A mutation that SURVIVES is the interesting result: it names a behaviour the
suite claims to protect and does not.

Not run by pytest - it rewrites source files. It copies the repo to a scratch
directory first and never mutates the working tree.

    python tests/mutation_check.py
"""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent

# (label, file relative to src/context_compass, find, replace)
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "classify: first match wins instead of longest prefix",
        "tools/package_manifest.py",
        "            if len(prefix) > best_len:\n                best, best_len = cls, len(prefix)",
        "            if best_len < 0:\n                best, best_len = cls, len(prefix)",
    ),
    (
        "is_permissive: every lane becomes permissive, nothing is ever swept",
        "tools/package_manifest.py",
        "    return rel.startswith(PERMISSIVE_LANES)",
        "    return True",
    ),
    (
        "is_permissive: no lane is permissive, tickets get swept",
        "tools/package_manifest.py",
        "    return rel.startswith(PERMISSIVE_LANES)",
        "    return False",
    ),
    (
        "manifest: hash the path instead of the contents",
        "tools/package_manifest.py",
        "    return hashlib.sha256(path.read_bytes()).hexdigest()",
        "    return hashlib.sha256(str(path).encode()).hexdigest()",
    ),
    (
        "index: section end is off by one",
        "tools/system_documents/index_document.py",
        "                end = nxt_start - 1",
        "                end = nxt_start",
    ),
    (
        "index: headings inside code fences are counted",
        "tools/system_documents/index_document.py",
        "        if in_fence:\n            continue\n        m = HEADING.match(line)",
        "        if False:\n            continue\n        m = HEADING.match(line)",
    ),
    (
        "index: the document title is indexed as a section",
        "tools/system_documents/index_document.py",
        "        if lone_title and level == min_level:\n            continue",
        "        if False:\n            continue",
    ),
    (
        "index: slice stops verifying the on-disk staleness proof",
        "tools/system_documents/index_document.py",
        "        if (not want_hash or want_hash.group(1) != live\n"
        "                or not want_count or int(want_count.group(1)) != len(lines)):",
        "        if False:",
    ),
    (
        "index: wrapped-heading warning removed",
        "tools/system_documents/index_document.py",
        "            if title.count(opener) > title.count(closer):",
        "            if False:",
    ),
    (
        "index: agrees to index an assembled graph",
        "tools/system_documents/index_document.py",
        '    if "<!-- BEGIN FILE:" in doc.read_text(encoding="utf-8", errors="ignore"):',
        "    if False:",
    ),
    (
        "cleanup: managed blocks swapped front-to-back, corrupting offsets",
        "tools/cleanup_context_compass.py",
        "    for name, s, e in sorted(managed_blocks(current), key=lambda b: -b[1]):",
        "    for name, s, e in sorted(managed_blocks(current), key=lambda b: b[1]):",
    ),
    (
        "cleanup: unterminated managed block is silently tolerated",
        "tools/cleanup_context_compass.py",
        '            raise ValueError(f"unterminated managed block {name!r}")',
        "            continue",
    ),
    (
        "cleanup: purge sweeps the top-level free space too",
        "tools/cleanup_context_compass.py",
        "        if rel.startswith(ROLE_OVERLAY_ROOT):",
        "        if any(rel.startswith(r) for r in instance_roots):",
    ),
    (
        "cleanup: reset stops protecting INSTANCE files",
        "tools/cleanup_context_compass.py",
        '        if cls == "INSTANCE":\n            continue',
        '        if False:\n            continue',
    ),
    (
        "update: config merge overwrites a value the user set",
        "tools/update_context_compass.py",
        "        if key not in cur_keys:",
        "        if True:",
    ),
    (
        "update: the case-twin guard is removed",
        "tools/update_context_compass.py",
        "        if rel.lower() in incoming_ci:\n            case_twins.append(rel)\n            continue",
        "        if False:\n            case_twins.append(rel)\n            continue",
    ),
    (
        "update: RESET and INSTANCE lanes are no longer skipped",
        "tools/update_context_compass.py",
        '        if cls in ("RESET", "INSTANCE"):\n            continue',
        "        if False:\n            continue",
    ),
    (
        "update: a locally edited file is replaced instead of kept",
        "tools/update_context_compass.py",
        "        elif new_sha == old_sha:\n            keep.append(rel)",
        "        elif new_sha == old_sha:\n            replace.append(rel)",
    ),
    (
        "assemble: index counts only derived edges",
        "tools/system_documents/python/assemble_graph.py",
        '            "edges": len(desc.get("edges_out", [])) + len(desc.get("edges_authored", [])),',
        '            "edges": len(desc.get("edges_out", [])),',
    ),
    (
        "assemble: range verification is skipped",
        "tools/system_documents/python/assemble_graph.py",
        '        if head != HEADER.format(source=s["source"]):',
        "        if False:",
    ),
    (
        "assemble: authored why lines are dropped",
        "tools/system_documents/python/assemble_graph.py",
        '        whys = [(e.get("from", "?"), e.get("to", "?"), e["why"])\n'
        '                for e in authored if e.get("why")]',
        "        whys = []",
    ),
    (
        "assemble: fmt_cell renders empty instead of a dash",
        "tools/system_documents/python/assemble_graph.py",
        '        return "-"',
        '        return ""',
    ),
    (
        "extract: Protocol is treated as a real supertype",
        "tools/system_documents/python/extract_graph.py",
        "        if b in TYPE_MARKERS or b in STDLIB_BASES:",
        "        if b in STDLIB_BASES:",
    ),
    (
        "extract: authored fields are dropped on re-extraction",
        "tools/system_documents/python/extract_graph.py",
        "AUTHORED_NODE_FIELDS = (\"include\", \"role\", \"responsibilities\", \"owns_state\", \"phases\")",
        "AUTHORED_NODE_FIELDS = ()",
    ),
    (
        "regions: user content is not carried across an upgrade",
        "tools/cleanup_context_compass.py",
        "        if name in mine and incoming[s:e] != mine[name]:",
        "        if False:",
    ),
    (
        "regions: carried front-to-back, corrupting later offsets",
        "tools/cleanup_context_compass.py",
        "    for name, s, e in sorted(user_regions(incoming), key=lambda r: -r[1]):",
        "    for name, s, e in sorted(user_regions(incoming), key=lambda r: r[1]):",
    ),
    (
        "regions: a region the new version dropped is reattached anyway",
        "tools/cleanup_context_compass.py",
        "        if name in mine and incoming[s:e] != mine[name]:",
        "        if mine and incoming[s:e] != list(mine.values())[0]:",
    ),
    (
        "regions: an unterminated region is silently tolerated",
        "tools/cleanup_context_compass.py",
        '            raise ValueError(f"unterminated user-defined region '
        '{name or \'(unnamed)\'!r}")',
        "            continue",
    ),
    (
        "live: a board with no user region is conformed anyway, deleting rows",
        "tools/update_context_compass.py",
        "                migrated = bool(user_regions(p.read_text(encoding=\"utf-8\")))",
        "                migrated = True",
    ),
    (
        "instance: seeding resurrects a file the user deliberately deleted",
        "tools/update_context_compass.py",
        "            if not p.exists() and rel not in shipped:",
        "            if not p.exists():",
    ),
    (
        "instance: a new lane never arrives (the original bug)",
        "tools/update_context_compass.py",
        "            if not p.exists() and rel not in shipped:\n                added.append(rel)",
        "            if False:\n                added.append(rel)",
    ),
    (
        "migrate_boards: table separators are carried as if they were rows",
        "tools/migrate_boards.py",
        "    if SEPARATOR.match(line):\n        return False",
        "    if False:\n        return False",
    ),
    (
        "graph: orphaned authored prose is dropped instead of retained",
        "tools/system_documents/python/extract_graph.py",
        "            retired[nid] = entry",
        "            pass",
    ),
    (
        "graph: staleness uses the whole file, not the node's own span",
        "tools/system_documents/python/extract_graph.py",
        '                      "span_sha256": span_sha(raw, cls)}',
        '                      "span_sha256": hashlib.sha256(raw).hexdigest()}',
    ),
    (
        "graph: a changed span no longer flags SEMANTICS_STALE",
        "tools/system_documents/python/extract_graph.py",
        "        elif current and stamp != current:",
        "        elif False:",
    ),
    (
        "graph: every authored node is flagged stale on first run",
        "tools/system_documents/python/extract_graph.py",
        "        if not stamp:",
        "        if False:",
    ),
    (
        "walker: a stale node reports as AUTHORED",
        "tools/system_documents/python/graph_walker.py",
        "    if stamp and current and stamp != current:\n        return \"SEMANTICS_STALE\"",
        "    if False:\n        return \"SEMANTICS_STALE\"",
    ),
    (
        "walker: accept writes without --apply",
        "tools/system_documents/python/graph_walker.py",
        "    if not apply:",
        "    if False:",
    ),
    (
        "walker: a possible move is applied instead of suggested",
        "tools/system_documents/python/graph_walker.py",
        "                if candidate != nid:",
        "                if False:",
    ),
    (
        "reconcile: deletes without confirmation",
        "tools/system_documents/python/graph_walker.py",
        "    if not confirm(f\"Delete {len(victims)} retired node(s)?\", assume_yes):",
        "    if False:",
    ),
    (
        "reconcile: assumes yes when there is no terminal",
        "tools/system_documents/python/graph_walker.py",
        "    if not sys.stdin.isatty():",
        "    if False:",
    ),
    (
        "tickets: --create writes without asking",
        "tools/system_documents/python/graph_semantics_tickets.py",
        "    if not confirm(f\"Write 1 epic and {len(plan)} story/stories into {args.tickets}?\",\n                   args.yes):",
        "    if False:",
    ),
    (
        "tickets: an existing ticket is not found, so every run duplicates",
        "tools/system_documents/python/graph_semantics_tickets.py",
        "        if pattern.search(p.read_text(encoding=\"utf-8\", errors=\"replace\")):",
        "        if False:",
    ),
    (
        "tickets: nested package slugs match by substring again",
        "tools/system_documents/python/graph_semantics_tickets.py",
        'pattern = re.compile(re.escape(marker) + r"(?![0-9A-Za-z-])")',
        'pattern = re.compile(re.escape(marker))',
    ),
    (
        "manifest: case drift reported as an unrelated add and remove",
        "tools/package_manifest.py",
        "        drift = [(removed_ci[p.lower()], p) for p in added if p.lower() in removed_ci]",
        "        drift = []",
    ),
    (
        "extract: a syntax error no longer names the interpreter version",
        "tools/system_documents/python/extract_graph.py",
        '        print(f"       parsed with Python {running}. If this file uses newer "',
        '        print(f"" or (f"       parsed with Python {running}. If this file uses newer "',
    ),
    (
        "manifest: an unreadable future format is accepted anyway",
        "tools/package_manifest.py",
        "    if major in SUPPORTED_MANIFEST_MAJORS:\n        return None",
        "    return None\n    if major in SUPPORTED_MANIFEST_MAJORS:\n        return None",
    ),
    (
        "manifest: a manifest with no version field is refused",
        "tools/package_manifest.py",
        "    if version is None:\n        return None",
        "    if version is None:\n        return 'no version'",
    ),
    (
        "migrate: unmatched nodes are silently attached to the first descriptor",
        "tools/system_documents/python/migrate_authored_graph.py",
        "        if not hit:\n            unmatched_nodes.append(ln)\n            continue",
        "        if not hit:\n            continue",
    ),
]


def run_suite(root: pathlib.Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no"],
        cwd=root, capture_output=True, text=True, timeout=600,
    )
    return proc.returncode == 0, proc.stdout.strip().split("\n")[-1]


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--start", type=int, default=0, help="first mutation index")
    ap.add_argument("--count", type=int, default=len(MUTATIONS),
                    help="how many to run (for splitting a long run into batches)")
    ap.add_argument("--list", action="store_true", help="list mutations and exit")
    ap.add_argument("--keep", action="store_true", help="do not delete the scratch copy")
    args = ap.parse_args()

    if args.list:
        for i, (label, rel, _, _) in enumerate(MUTATIONS):
            print(f"  {i:>2}  {rel:<52}  {label}")
        return 0

    batch = MUTATIONS[args.start:args.start + args.count]

    scratch = pathlib.Path(tempfile.mkdtemp(prefix="ccmut-"))
    work = scratch / "repo"
    work.mkdir()
    # pyproject.toml carries the pytest config, so the scratch copy needs it or
    # markers and testpaths are lost and every mutation "passes" against an
    # empty collection.
    for item in ("src", "tests", "contributor", "pyproject.toml", "README.md"):
        s = REPO / item
        if not s.exists():
            continue
        (shutil.copytree if s.is_dir() else shutil.copy2)(s, work / item)

    pkg = work / "src" / "context_compass"

    ok, line = run_suite(work)
    print(f"baseline: {'PASS' if ok else 'FAIL'}  {line}")
    if not ok:
        print("ERROR: baseline must pass before mutating. Nothing was tested.")
        shutil.rmtree(scratch, ignore_errors=True)
        return 2

    caught, survived, skipped = 0, [], []
    print(f"\napplying {len(batch)} mutations "
          f"[{args.start}..{args.start + len(batch) - 1}]\n")
    for label, rel, find, replace in batch:
        target = pkg / rel
        original = target.read_text(encoding="utf-8")
        if find not in original:
            skipped.append(label)
            print(f"  SKIP     {label}\n           (anchor not found in {rel})")
            continue
        target.write_text(original.replace(find, replace, 1), encoding="utf-8")
        try:
            passed, summary = run_suite(work)
        finally:
            target.write_text(original, encoding="utf-8")

        if passed:
            survived.append(label)
            print(f"  SURVIVED {label}")
        else:
            caught += 1
            print(f"  caught   {label}")

    print(f"\ncaught {caught}/{len(batch) - len(skipped)}"
          f"{f', {len(skipped)} skipped' if skipped else ''}")
    if survived:
        print("\nSURVIVING MUTATIONS - the suite does not protect these:")
        for s in survived:
            print(f"  - {s}")
    if args.keep:
        print(f"\nscratch kept at {work}")
    else:
        shutil.rmtree(scratch, ignore_errors=True)
    return 1 if survived or skipped else 0


if __name__ == "__main__":
    raise SystemExit(main())
