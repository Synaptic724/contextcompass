#!/usr/bin/env python3
"""Carry an authored graph in the retired JSON format into per-file descriptors.

Run this ONCE when a repository holds a graph written before the descriptor
format existed. After it succeeds and the document reassembles, the legacy JSON
can be deleted - everything it held now lives in the descriptors, which are the
only thing the pipeline reads.

WHY THIS EXISTS RATHER THAN "JUST RE-EXTRACT"

`extract_graph.py` rebuilds the mechanical tier and cannot invent the authored
one. `owns_lifecycle_of`, `uses` and `borrows` are the same syntax - "A holds a
reference to B" - so a fresh extraction produces a structurally perfect graph
with an empty authored layer, and nothing warns you, because an empty authored
layer is also what a brand new project looks like.

Measured on a real repository that did exactly this: 1,188 nodes recovered,
446 derived edges, and **zero** of 997 authored edges. The authored work was
still on disk in the old JSON. It simply never arrived.

The general rule, worth saying plainly: the better a repository's existing
graph, the more a naive re-extraction destroys, because a mature graph is
edge-richer than a young one.

MATCHING

Two passes, most precise first:

1. exact node id
2. `(file, label)` - catches a node whose id changed because its module moved

Anything unmatched is REPORTED, never guessed at. A node that cannot be located
keeps its authored prose in the report so you can place it by hand.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

AUTHORED_NODE_FIELDS = ("include", "role", "responsibilities", "owns_state", "phases")
AUTHORED_EDGE_FIELDS = ("from", "to", "relation", "why", "cardinality", "phase", "strength")


def load_legacy(path: pathlib.Path) -> tuple[list[dict], list[dict]]:
    d = json.loads(path.read_text(encoding="utf-8"))
    nodes = d.get("nodes") or {}
    edges = d.get("edges") or []
    nodes = list(nodes.values()) if isinstance(nodes, dict) else list(nodes)
    edges = list(edges.values()) if isinstance(edges, dict) else list(edges)
    return nodes, edges


def load_descriptors(root: pathlib.Path) -> dict[pathlib.Path, dict]:
    out = {}
    for p in sorted(root.rglob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and "source" in d and "nodes" in d:
            out[p] = d
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--legacy", required=True, type=pathlib.Path,
                    help="the retired graph JSON holding the authored tier")
    ap.add_argument("--descriptors", required=True, type=pathlib.Path,
                    help="descriptor root produced by extract_graph.py")
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    ap.add_argument("--apply", action="store_true", help="write the authored tier in")
    args = ap.parse_args()

    if not args.legacy.is_file():
        print(f"legacy graph not found: {args.legacy}", file=sys.stderr)
        return 2
    if not args.descriptors.is_dir():
        print(f"descriptor root not found: {args.descriptors}", file=sys.stderr)
        return 2
    if not args.check and not args.apply:
        print("Refusing to act without --apply. Use --check to see the plan.")
        return 2

    legacy_nodes, legacy_edges = load_legacy(args.legacy)
    descriptors = load_descriptors(args.descriptors)

    by_id: dict[str, tuple[pathlib.Path, str]] = {}
    by_file_label: dict[tuple[str, str], tuple[pathlib.Path, str]] = {}
    for path, d in descriptors.items():
        for nid, node in d.get("nodes", {}).items():
            by_id[nid] = (path, nid)
            key = (node.get("file", ""), node.get("label", ""))
            by_file_label.setdefault(key, (path, nid))

    node_edits: dict[pathlib.Path, dict[str, dict]] = {}
    matched_id = matched_fl = 0
    unmatched_nodes: list[dict] = []

    for ln in legacy_nodes:
        authored = {k: ln[k] for k in AUTHORED_NODE_FIELDS if ln.get(k)}
        if not authored:
            continue
        hit = by_id.get(ln.get("id", ""))
        if hit:
            matched_id += 1
        else:
            hit = by_file_label.get((ln.get("file", ""), ln.get("label", "")))
            if hit:
                matched_fl += 1
        if not hit:
            unmatched_nodes.append(ln)
            continue
        path, nid = hit
        node_edits.setdefault(path, {})[nid] = authored

    # An authored edge belongs to the descriptor owning its SOURCE node, which is
    # how `assemble_graph.py` renders it - under the file the edge leaves from.
    edge_edits: dict[pathlib.Path, list[dict]] = {}
    placed = 0
    unmatched_edges: list[dict] = []
    for le in legacy_edges:
        src = le.get("from", "")
        hit = by_id.get(src)
        if not hit:
            unmatched_edges.append(le)
            continue
        path, _ = hit
        edge_edits.setdefault(path, []).append(
            {k: le[k] for k in AUTHORED_EDGE_FIELDS if le.get(k) is not None})
        placed += 1

    print(f"legacy      {args.legacy}")
    print(f"descriptors {args.descriptors}  ({len(descriptors)} files, {len(by_id)} nodes)")
    print()
    print(f"  nodes with authored fields : {matched_id + matched_fl + len(unmatched_nodes)}")
    print(f"    matched by id            : {matched_id}")
    print(f"    matched by (file, label) : {matched_fl}")
    print(f"    UNMATCHED                : {len(unmatched_nodes)}")
    print(f"  authored edges             : {len(legacy_edges)}")
    print(f"    placed on a descriptor   : {placed}")
    print(f"    UNMATCHED source node    : {len(unmatched_edges)}")
    for n in unmatched_nodes[:10]:
        print(f"    unmatched node  {n.get('id')}  ({n.get('file')})")
    for e in unmatched_edges[:10]:
        print(f"    unmatched edge  {e.get('from')} -> {e.get('to')}")

    if args.check:
        print()
        print("READY" if not (unmatched_nodes or unmatched_edges)
              else "READY, with unmatched items listed above - place those by hand")
        return 0

    written = 0
    for path, d in descriptors.items():
        nodes = node_edits.get(path)
        edges = edge_edits.get(path)
        if not nodes and not edges:
            continue
        for nid, authored in (nodes or {}).items():
            d["nodes"][nid].update(authored)
        if edges:
            d["edges_authored"] = edges
        # Exactly as extract_graph.py writes it, so the next extraction rewrites nothing.
        path.write_text(json.dumps(d, indent=1) + "\n", encoding="utf-8", newline="\n")
        written += 1

    print()
    print(f"APPLIED: authored tier written into {written} descriptors")
    print("         Reassemble now: assemble_graph.py --descriptors <root> --out <system_docs>")
    print("         Verify the document shows authored rows and why lines, THEN delete the")
    print("         legacy JSON. Not before - it is the only copy until the descriptors hold it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
