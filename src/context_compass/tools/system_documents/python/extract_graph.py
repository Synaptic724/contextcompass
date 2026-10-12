#!/usr/bin/env python3
"""Scaffold per-source-file graph descriptors for a Python codebase.

This is the MECHANICAL half of the system-documents graph. It walks a source
tree, parses each file with the stdlib `ast` module, and emits one descriptor
per source file mirroring the source path.

What this script produces is a SKELETON, not the graph. Measured against a
hand-authored graph of 535 nodes / 997 edges:

    node identity        98% recovered   (529 / 535)
    `specializes` edges  98% recovered   (155 / 158)  - inheritance is syntax
    `creates` edges      57% recovered, 8x over-generated - flagged as candidates
    everything else       0% recoverable - 68% of all edges

`owns_lifecycle_of`, `uses`, and `borrows` are syntactically IDENTICAL - each is
"A holds a reference to B". Which one it is, is a design fact that does not
exist in the source text. Likewise every `role`, `responsibility`, `why`,
`cardinality`, and `strength`. Those are authored, and this script must never
overwrite them.

Hence the merge contract: on re-run, mechanical fields are refreshed and
authored fields are preserved untouched. The script reports drift (nodes that
appeared, disappeared, or still lack semantics) rather than silently resolving
it.

Language-agnostic by layout: this lives under `tools/system_documents/python/`
so a sibling `tools/system_documents/<language>/` can implement the same
descriptor contract for another language.

Usage:
    python extract_graph.py --src src --out context_compass/system_docs/graph

    # report drift without writing
    python extract_graph.py --src src --out ... --check

    # fail if any source file could not be parsed (CI / unattended runs)
    python extract_graph.py --src src --out ... --strict

A file this interpreter cannot parse gets no descriptor, so every node in it
leaves the graph silently - the run still succeeds and the document is simply one
section shorter. That is correct when the file is broken and wrong when the file
is merely NEWER than the interpreter. `--strict` turns that into a non-zero exit
so an unattended run cannot publish a graph with holes in it.

    # skip __init__.py (included by default - it usually carries a package's
    # public surface, so dropping it would lose what a package exposes)
    python extract_graph.py --src src --out ... --exclude-init
"""

from __future__ import annotations

import argparse
import ast
import builtins
import hashlib
import json
import collections
import pathlib
import re
import sys
from typing import Any

SCHEMA_VERSION = 1

# Directories that never contain first-party source. Matched against path parts,
# so a nested `build/` anywhere in the tree is excluded too.
EXCLUDED_DIRS = frozenset({
    "__pycache__", ".venv", "venv", ".env", "env", "site-packages",
    "build", "dist", ".eggs", ".tox", ".nox",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".hypothesis",
    "node_modules", ".git", ".hg", ".svn", ".idea", ".vscode",
})

# Compiled/derived artifacts. Listed for documentation and for --report; the
# walk itself only ever collects `*.py`, so these cannot leak in via extension.
ARTIFACT_SUFFIXES = frozenset({".pyc", ".pyo", ".pyd", ".so", ".dylib", ".melc", ".c"})

# Fields the AST owns. Everything else in a descriptor is authored and preserved.
MECHANICAL_NODE_FIELDS = ("id", "label", "kind", "file", "lineno", "bases",
                          "markers", "public_methods", "shape")
# `include` is authored curation: whether this node belongs in the composed
# graph at all. Absent means "not yet triaged", which is distinct from false.
AUTHORED_NODE_FIELDS = ("include", "role", "responsibilities", "owns_state", "phases")


def is_excluded(path: pathlib.Path) -> bool:
    """True if any path component is an excluded directory."""
    return any(part in EXCLUDED_DIRS for part in path.parts)


def iter_source_files(src_root: pathlib.Path, include_init: bool = True):
    """Yield first-party .py files under src_root, filtered and sorted.

    `__init__.py` is INCLUDED by default. The reference codebase has almost
    none - it binds through a scanner rather than re-exports - but that is
    unusual. In most Python projects `__init__.py` carries the public surface of
    a package, so excluding it by default would silently drop the very file that
    defines what a package exposes. Opt out with --exclude-init.
    """
    for path in sorted(src_root.rglob("*.py")):
        if is_excluded(path.relative_to(src_root)):
            continue
        if not include_init and path.name == "__init__.py":
            continue
        yield path


def module_id(rel_posix: str) -> str:
    """src-relative posix path -> dotted module id."""
    return rel_posix[:-3].replace("/", ".").removesuffix(".__init__")


def base_name(node: ast.expr) -> str | None:
    """Best-effort name for a base class expression."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Subscript):  # Generic[T] -> Generic
        return base_name(node.value)
    return None


def base_dotted(node: ast.expr) -> str | None:
    """Dotted source text of a base class expression, or None."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        head = base_dotted(node.value)
        return f"{head}.{node.attr}" if head else None
    if isinstance(node, ast.Subscript):
        return base_dotted(node.value)
    return None


def snake(name: str) -> str:
    """CamelCase -> snake_case, for filename/classname comparison."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


# Bases that DECLARE what a class is rather than name a supertype in the graph.
# `class IResource(Protocol)` does not specialize anything - `Protocol` is a
# marker that makes the class an interface. Emitting an edge to it produces a
# dangling reference to a node that will never exist. Measured on the reference
# codebase: 70 of 515 extracted edges (13%) pointed at markers like these.
TYPE_MARKERS: dict[str, str] = {
    "Protocol": "interface",
    "ABC": "abstract", "ABCMeta": "abstract",
    "Enum": "enum", "IntEnum": "enum", "StrEnum": "enum", "Flag": "enum",
    "NamedTuple": "record", "TypedDict": "record", "dataclass": "record",
    "Generic": "", "object": "",  # pure noise, carry no kind
}
# stdlib supertypes that are real classes but not part of a first-party graph.
STDLIB_BASES = frozenset({"Exception", "BaseException", "RuntimeError", "ValueError",
                          "TypeError", "KeyError", "Thread", "dict", "list", "tuple",
                          "set", "str", "int", "float", "type"})


def split_bases(raw: list[str]) -> tuple[list[str], list[str]]:
    """Separate real supertypes from declaration markers and stdlib bases.

    Returns (graph_bases, markers). Only graph_bases may become edges.
    """
    graph, markers = [], []
    for b in raw:
        if b in TYPE_MARKERS or b in STDLIB_BASES:
            markers.append(b)
        else:
            graph.append(b)
    return graph, markers


def class_kind(markers: list[str]) -> str:
    """Kind implied by declaration markers, else `class`.

    This one IS syntactic, unlike curation and edge semantics. In the reference
    codebase both curated `interface` nodes are `Protocol` subclasses, and the
    extractor previously stamped them `class` because it never looked.

    ABCs are deliberately NOT interfaces here. A codebase commonly has both: an
    abstract base that subclasses actually inherit, and a Protocol mirroring the
    same public surface for structural typing. They play different roles in a
    graph - one is a supertype, the other is a contract - so only the Protocol
    is marked `interface`. See `examples/example_graph_details/src/example/core/`
    for the pair.
    """
    for m in markers:
        kind = TYPE_MARKERS.get(m)
        if kind:
            return kind
    return "class"


def import_map(tree: ast.Module, mod: str) -> dict[str, str]:
    """local name -> fully qualified id, for resolving edge targets.

    Without this an edge carries a bare `to_label` lifted from a base-class
    list, which is a name, not an address. Twenty class names are defined more
    than once in the reference codebase (`precision`, `safe_profile` and friends
    each appear three times under view/, command/ and codegen/), so a bare name
    genuinely cannot identify a node. Measured resolution rate: 99%.
    """
    out: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    out[alias.asname] = alias.name
                else:
                    top = alias.name.split(".")[0]
                    out[top] = top
            continue
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level:                                  # relative import
            base = ".".join(mod.split(".")[:-node.level])
            prefix = f"{base}.{node.module}." if node.module else f"{base}."
        elif node.module:
            prefix = f"{node.module}."
        else:
            continue
        for alias in node.names:
            out[alias.asname or alias.name] = f"{prefix}{alias.name}"
    return out


def published_aliases(tree: ast.Module, classes: set[str]) -> list[dict[str, str]]:
    """Module-level `Alias = SomeClass` bindings.

    These are invisible to a ClassDef-only walk, and they are exactly how this
    codebase publishes interface names: `ISync = Sync`, `Pack = Package`. The
    alias is the name consumers import, so dropping it loses the public
    identity while keeping the private one.
    """
    out: list[dict[str, str]] = []
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Name)
                and node.value.id in classes):
            out.append({"alias": node.targets[0].id, "target": node.value.id,
                        "lineno": node.lineno})
    return out


def shape_signals(cls: ast.ClassDef) -> dict[str, Any]:
    """Record what the class looks like. Does NOT decide whether it matters.

    Curation is authored, not inferred. This was measured, not assumed: against
    a curated graph of 535 nodes, the best syntactic significance rule tried
    here ("drop the module node when the file holds exactly one class") would
    have suppressed 419 nodes but WRONGLY dropped 63 that the curated graph
    deliberately includes. Significance is a judgment about what a reader needs,
    and it is no more derivable from syntax than `owns_lifecycle_of` is.

    So the script reports shape and lets the authored layer opt nodes in via
    `include`. Emitting inventory the author can reject is recoverable; silently
    withholding a node they wanted is not.
    """
    methods = [n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    real = [m for m in methods if not (m.name.startswith("__") and m.name.endswith("__"))]
    return {"method_count": len(real), "has_bases": bool(cls.bases),
            "trivial": not real and not cls.bases}


def span_sha(raw: bytes, node: ast.AST) -> str:
    """Hash of one definition's OWN source lines.

    Per node, not per file, and that is the whole point. A file-level hash marks
    every node in a 40-class module stale because one class changed, which is a
    census nobody can act on - the signal has to survive being useful. `ast`
    gives `end_lineno`, so a definition's own span is cheap to isolate.
    """
    start = getattr(node, "lineno", None)
    end = getattr(node, "end_lineno", None)
    if not start or not end:
        return ""
    lines = raw.decode("utf-8", errors="replace").splitlines()[start - 1:end]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def extract(path: pathlib.Path, src_root: pathlib.Path,
            skips: list[tuple[str, str]] | None = None) -> dict[str, Any] | None:
    """Parse one source file into a mechanical descriptor.

    `skips`, when given, collects `(rel_path, reason)` for every file that could
    not be parsed. The caller needs the paths, not just a count: "skipped=1" tells
    a reader something went wrong and nothing about what, and this failure is
    silent by construction - the graph simply comes out one section short.
    """
    rel = path.relative_to(src_root).as_posix()
    raw = path.read_bytes()
    try:
        tree = ast.parse(raw.decode("utf-8", errors="replace"), filename=str(path))
    except SyntaxError as exc:
        # A file the running interpreter cannot parse gets no descriptor, and
        # every node in it silently vanishes from the graph. That is correct
        # when the file is broken and badly wrong when the file is simply
        # NEWER than the interpreter - and the two look identical here.
        #
        # Real case: a PEP 701 f-string (nested quotes) parses on 3.12+ and
        # raises here on 3.10, so a graph extracted with an older Python was
        # one class short with nothing saying why. Name the version, since it
        # is the first thing to check and nothing else reports it.
        running = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f"  SKIP (syntax error) {rel}: {exc}", file=sys.stderr)
        print(f"       parsed with Python {running}. If this file uses newer "
              f"syntax it is not broken -", file=sys.stderr)
        print(f"       the interpreter is older than the code. Re-run on the "
              f"version the project targets.", file=sys.stderr)
        if skips is not None:
            skips.append((rel, f"{exc} [parsed with Python {running}]"))
        return None

    mod = module_id(rel)
    nodes: dict[str, dict[str, Any]] = {
        mod: {"id": mod, "label": mod.rsplit(".", 1)[-1], "kind": "module",
              "file": f"{src_root.name}/{rel}", "lineno": 1}
    }
    edges: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []

    for cls in [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]:
        cid = f"{mod}.{cls.name}"
        labeled: list[tuple[str, str | None]] = []
        for bnode in cls.bases:
            label = base_name(bnode)
            if not label:
                continue
            dotted = base_dotted(bnode)
            labeled.append((label, dotted))
        raw_bases = [label for label, _ in labeled]
        bases, markers = split_bases(raw_bases)
        methods = sorted(
            m.name for m in cls.body
            if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not m.name.startswith("_")
        )
        nodes[cid] = {"id": cid, "label": cls.name, "kind": class_kind(markers),
                      "file": f"{src_root.name}/{rel}", "lineno": cls.lineno,
                      "bases": bases, "markers": markers, "public_methods": methods,
                      "shape": shape_signals(cls),
                      "span_sha256": span_sha(raw, cls)}
        # relation is provisional: `implements` vs `specializes` depends on
        # whether the target is an interface, which is only knowable after every
        # file has been parsed. main() resolves it in a second pass.
        graph_dotted: list[tuple[str, str | None]] = []
        for label, dotted in labeled:
            if label in TYPE_MARKERS or label in STDLIB_BASES:
                continue
            graph_dotted.append((label, dotted))
        for label, dotted in graph_dotted:
            edge: dict[str, Any] = {"from": cid, "to_label": label, "relation": "specializes"}
            if dotted != label:
                edge["_to_dotted"] = dotted
            edges.append(edge)
        for sub in ast.walk(cls):
            if isinstance(sub, ast.Call):
                name = base_name(sub.func)
                if name and name[:1].isupper() and name not in bases:
                    candidates.append({"from": cid, "to_label": name,
                                       "relation": "creates", "confidence": "candidate"})

    seen, deduped = set(), []
    for c in candidates:
        key = (c["from"], c["to_label"])
        if key not in seen:
            seen.add(key)
            deduped.append(c)

    declared = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}
    aliases = published_aliases(tree, declared)
    imports = import_map(tree, mod)

    # When a file holds exactly one class and that class is the filename, the
    # module and the class are the same entity. The reference graph collapses
    # these to a single node - but inconsistently, sometimes keeping the class
    # name (`interfaces.IChannelLogger`) and sometimes the module path
    # (`strategies.solo_codegen_creation_discovery_strategy`). Both spellings
    # appear in the same graph, so the extractor reports the condition and lets
    # the composer apply one rule rather than guessing which spelling was meant.
    stem = mod.rsplit(".", 1)[-1]
    class_ids = [k for k, v in nodes.items() if v["kind"] in ("class", "interface")]
    collapse = None
    if len(class_ids) == 1:
        label = nodes[class_ids[0]]["label"]
        if stem in (snake(label), label.lower()):
            collapse = {"module": mod, "class": class_ids[0], "label": label}

    return {
        "schema_version": SCHEMA_VERSION,
        "source": f"{src_root.name}/{rel}",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "generator": "tools/system_documents/python/extract_graph.py",
        "nodes": nodes,
        "edges_out": edges,
        "edge_candidates": deduped,
        "published_aliases": aliases,
        "imports": imports,
        "collapse_candidate": collapse,
    }


def merge(new: dict[str, Any], old: dict[str, Any] | None) -> tuple[dict[str, Any], list[str]]:
    """Refresh mechanical fields; preserve every authored field.

    Returns the merged descriptor and a list of drift notes. Authored semantics
    are never overwritten and never silently dropped - a node that disappeared
    from source but still carries authored prose is reported, not deleted.
    """
    notes: list[str] = []
    if old is None:
        notes.append(f"NEW file with {len(new['nodes'])} node(s)")
        notes.extend(f"UNSEMANTIC node {nid}" for nid in new["nodes"])
        return new, notes

    old_nodes = old.get("nodes", {})
    retired: dict[str, dict[str, Any]] = dict(old.get("nodes_retired", {}))
    carried_over: set[str] = set()          # old ids matched to a new node

    # A rename is the common case, and treating it as a deletion discards months
    # of authored prose over a renamed class. Match by exact live id, then exact
    # retired id, then by (file, label), then by label alone. Rename fallbacks
    # use only live nodes and are reported so the match is reviewable.
    by_file_label = {(n.get("file", ""), n.get("label", "")): nid
                     for nid, n in old_nodes.items()}
    by_label: dict[str, list[str]] = {}
    for nid, n in old_nodes.items():
        by_label.setdefault(n.get("label", ""), []).append(nid)

    for nid, node in new["nodes"].items():
        prev = old_nodes.get(nid)
        if prev is not None:
            carried_over.add(nid)
        elif nid in retired:
            prev = retired[nid]
        else:
            old_id = by_file_label.get((node.get("file", ""), node.get("label", "")))
            if old_id is None:
                same_label = by_label.get(node.get("label", ""), [])
                old_id = same_label[0] if len(same_label) == 1 else None
                if old_id and any(f in old_nodes[old_id] for f in AUTHORED_NODE_FIELDS):
                    notes.append(f"RECOVERED node {nid} - matched {old_id} by label; "
                                 f"authored semantics carried over, VERIFY the match")
            elif any(f in old_nodes[old_id] for f in AUTHORED_NODE_FIELDS):
                notes.append(f"RECOVERED node {nid} - matched {old_id} by (file, label); "
                             f"authored semantics carried over")
            if old_id is None:
                notes.append(f"NEW node {nid} - needs semantics")
                continue
            prev, = (old_nodes[old_id],)
            carried_over.add(old_id)

        for field in AUTHORED_NODE_FIELDS + ("semantics_authored_against",):
            if field in prev:
                node[field] = prev[field]

    # Retain, do not drop. A node gone from source keeps its authored prose in a
    # quarantine section of the same file, so "resolve by hand" has something to
    # resolve WITH. Before this, the note said ORPHANED and the prose was written
    # out of the descriptor in the same pass - recoverable only from git, and
    # only if you noticed.
    for nid in old_nodes:
        if nid in new["nodes"] or nid in carried_over:
            continue
        authored = {f: old_nodes[nid][f] for f in AUTHORED_NODE_FIELDS
                    if f in old_nodes[nid]}
        if authored:
            entry = dict(old_nodes[nid])
            entry["retired_reason"] = "gone from source"
            retired[nid] = entry
            notes.append(f"ORPHANED node {nid} - gone from source, authored semantics "
                         f"RETAINED under nodes_retired")
        else:
            notes.append(f"REMOVED node {nid}")

    # A retired id that comes back is un-retired rather than duplicated.
    for nid in list(retired):
        if nid in new["nodes"]:
            del retired[nid]
            notes.append(f"RESTORED node {nid} - back in source, retirement lifted")
    if retired:
        new["nodes_retired"] = retired

    # Authored edges live under `edges_authored` and are owned entirely by humans/agents.
    if "edges_authored" in old:
        new["edges_authored"] = old["edges_authored"]

    for nid, node in new["nodes"].items():
        if not any(f in node for f in AUTHORED_NODE_FIELDS):
            notes.append(f"UNSEMANTIC node {nid}")
            continue
        # The state the tier contract implied and never defined: the node still
        # exists, its source moved, and its authored meaning may now be wrong.
        # Without it a graph fills up with confident descriptions of code that
        # no longer works that way, and nothing says which.
        stamp = node.get("semantics_authored_against")
        current = node.get("span_sha256", "")
        if not stamp:
            # NOT STAMPED, AND THE EXTRACTOR DOES NOT STAMP IT.
            #
            # This used to auto-stamp the node against current source so it would
            # report AUTHORED - "grandfathering". That was the extractor asserting,
            # on nobody's behalf, that prose it never read matches code it never
            # compared. It made `SEMANTICS_STALE: 0` reachable without a single node
            # having been checked, and the assumption became indistinguishable from
            # a real one the moment the run finished.
            #
            # The stamp means a human read this against this source. Only `--accept`
            # can create it. An unstamped node reports SEMANTICS_STALE, because that
            # is what it is: unverified. The first run after upgrading will show a
            # large stale count, and that count is the truth being reported for the
            # first time rather than a regression.
            notes.append(f"UNVERIFIED node {nid} - authored prose with no stamp; "
                         f"reports SEMANTICS_STALE until read and --accept'ed")
        elif current and stamp != current:
            notes.append(f"SEMANTICS_STALE node {nid} - source changed since its "
                         f"semantics were written; re-verify then re-accept")

    return new, notes


def package_candidates(src_root: pathlib.Path, include_init: bool) -> list[dict[str, Any]]:
    """Directories that read as a family of peers rather than N unrelated files.

    The reference graph carries `package` nodes pointing at directories -
    `crystals/`, `custody/`, `preflight/` - each described as a family ("the 10
    default restore preflight strategies"). All three are directories whose
    files share a naming suffix: `_crystal`, `_strategy`, `_analyzer`.

    That shared suffix is a signal, not a verdict. A directory is reported as a
    candidate; whether it deserves a package node is authored, like every other
    curation decision in this system.
    """
    out: list[dict[str, Any]] = []
    for directory in sorted({p.parent for p in iter_source_files(src_root, include_init)}):
        stems = [p.stem for p in directory.glob("*.py")
                 if include_init or p.name != "__init__.py"]
        if len(stems) < 3:
            continue
        suffixes = collections.Counter(s.rsplit("_", 1)[-1] for s in stems if "_" in s)
        if not suffixes:
            continue
        suffix, count = suffixes.most_common(1)[0]
        if count / len(stems) >= 0.6:
            rel = directory.relative_to(src_root).as_posix()
            out.append({"id": f"{src_root.name}.{rel}".replace("/", "."),
                        "kind": "package", "file": f"{src_root.name}/{rel}/",
                        "member_count": len(stems), "shared_suffix": suffix,
                        "cohesion": round(count / len(stems), 2)})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, type=pathlib.Path, help="source root, e.g. src")
    ap.add_argument("--out", required=True, type=pathlib.Path, help="descriptor output root")
    ap.add_argument("--check", action="store_true", help="report drift, write nothing")
    ap.add_argument("--exclude-init", action="store_true",
                    help="skip __init__.py (default: included)")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if any source file could not be parsed "
                         "(use in CI and unattended runs)")
    args = ap.parse_args()

    src_root: pathlib.Path = args.src.resolve()
    out_root: pathlib.Path = args.out.resolve()
    if not src_root.is_dir():
        print(f"source root not found: {src_root}", file=sys.stderr)
        return 2

    files = list(iter_source_files(src_root, (not args.exclude_init)))
    stats = {"files": 0, "nodes": 0, "edges": 0, "candidates": 0,
             "new": 0, "unsemantic": 0, "orphaned": 0, "skipped": 0,
             "interfaces": 0, "aliases": 0, "collapse": 0, "implements": 0}
    all_notes: list[str] = []

    # PASS 1 - parse everything, so interface identity is known before any edge
    # relation is decided. A class inheriting an interface IMPLEMENTS it; only
    # inheriting a concrete/abstract class is specialization. That distinction
    # cannot be made per-file, because the base may be defined anywhere.
    parsed: list[tuple[pathlib.Path, dict[str, Any]]] = []
    skipped: list[tuple[str, str]] = []
    stats_resolved = [0, 0]   # [resolved, unresolved]
    for path in files:
        desc = extract(path, src_root, skipped)
        if desc is None:
            stats["skipped"] += 1
            continue
        parsed.append((path, desc))

    interface_ids = {nid for _, d in parsed for nid, n in d["nodes"].items()
                     if n.get("kind") == "interface"}
    # every class id defined anywhere, for same-module resolution
    local_defs = {(d["nodes"][nid]["file"], d["nodes"][nid]["label"]): nid
                  for _, d in parsed for nid in d["nodes"]
                  if d["nodes"][nid]["kind"] != "module"}
    for _, d in parsed:
        imports = d.get("imports", {})
        for e in d["edges_out"]:
            label = e["to_label"]
            qualified = "_to_dotted" in e
            dotted = e.pop("_to_dotted", None)
            target = None
            # An unsupported qualified expression must not become a bare-name guess.
            if qualified:
                if dotted is not None and "." in dotted:
                    head, _, rest = dotted.partition(".")
                    if head in imports:
                        target = f"{imports[head]}.{rest}"
            else:
                target = imports.get(label) or local_defs.get((d["source"], label))
                if not target and label in builtins.__dict__:
                    obj = builtins.__dict__[label]
                    if isinstance(obj, type):
                        target = f"builtins.{label}"
            if target:
                e["to"] = target
                stats_resolved[0] += 1
            else:
                stats_resolved[1] += 1
            if target in interface_ids:
                e["relation"] = "implements"

    # PASS 2 - merge with any authored descriptor and write
    for path, desc in parsed:
        rel = path.relative_to(src_root).with_suffix(".json")
        target = out_root / rel
        prev = None
        if target.exists():
            try:
                prev = json.loads(target.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                all_notes.append(f"UNREADABLE existing descriptor {rel}, treating as new")
        merged, notes = merge(desc, prev)

        stats["files"] += 1
        stats["nodes"] += len(merged["nodes"])
        stats["edges"] += len(merged["edges_out"])
        stats["candidates"] += len(merged["edge_candidates"])
        stats["interfaces"] += sum(1 for n in merged["nodes"].values() if n["kind"] == "interface")
        stats["aliases"] += len(merged.get("published_aliases", []))
        stats["collapse"] += 1 if merged.get("collapse_candidate") else 0
        stats["implements"] += sum(1 for e in merged["edges_out"] if e["relation"] == "implements")
        stats["new"] += sum(1 for n in notes if n.startswith("NEW"))
        stats["unsemantic"] += sum(1 for n in notes if n.startswith("UNSEMANTIC"))
        stats["orphaned"] += sum(1 for n in notes if n.startswith("ORPHANED"))
        all_notes.extend(f"{rel}: {n}" for n in notes)

        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(merged, indent=1) + "\n",
                              encoding="utf-8", newline="\n")

    packages = package_candidates(src_root, (not args.exclude_init))
    if not args.check and packages:
        out_root.mkdir(parents=True, exist_ok=True)
        (out_root / "_package_candidates.json").write_text(
            json.dumps({"schema_version": SCHEMA_VERSION, "candidates": packages},
                       indent=1) + "\n", encoding="utf-8", newline="\n")

    mode = "CHECK (no writes)" if args.check else "WROTE"
    print(f"{mode}: {stats['files']} descriptors under {out_root}")
    print(f"  nodes={stats['nodes']}  specializes={stats['edges']}  "
          f"creates-candidates={stats['candidates']}")
    print(f"  needing semantics={stats['unsemantic']}  new={stats['new']}  "
          f"orphaned={stats['orphaned']}  skipped={stats['skipped']}")
    print(f"  interfaces={stats['interfaces']}  aliases={stats['aliases']}  "
          f"collapse-candidates={stats['collapse']}  package-candidates={len(packages)}")
    print(f"  specializes={stats['edges']-stats['implements']}  implements={stats['implements']}")
    tot = stats_resolved[0] + stats_resolved[1]
    if tot:
        print(f"  edge targets resolved to ids: {stats_resolved[0]}/{tot} "
              f"({100 * stats_resolved[0] // tot}%)")
    # Every state that needs a human gets surfaced. A note only in the returned
    # list is a note nobody reads.
    for marker, heading in (
        ("SEMANTICS_STALE",
         "SEMANTICS_STALE - source changed under authored semantics; re-verify"),
        ("ORPHANED",
         "ORPHANED - gone from source; semantics RETAINED under nodes_retired"),
        ("RECOVERED",
         "RECOVERED - matched an older id; semantics carried over"),
        ("RESTORED",
         "RESTORED - back in source; retirement lifted"),
        ("UNVERIFIED",
         "UNVERIFIED - authored prose nobody has checked against source"),
    ):
        hits = [n for n in all_notes if n.startswith(marker) or f" {marker} " in n]
        if not hits:
            continue
        print(f"\n  {heading}: {len(hits)}")
        for n in hits[:15]:
            print(f"    {n}")
        if len(hits) > 15:
            print(f"    ... +{len(hits) - 15} more")

    # SKIPPED is surfaced last and loudest, because it is the only failure here
    # that makes the graph WRONG rather than merely incomplete. Drift is visible -
    # a node marked new or orphaned says so. A skipped file leaves no trace at all:
    # its section is simply absent, every citation into it stops resolving, and the
    # run still prints a clean summary. It cannot be counted in `census` for the
    # same reason - the census describes nodes that exist, and these do not.
    if skipped:
        print(f"\n  SKIPPED - NOT IN THE GRAPH: {len(skipped)}")
        for rel, reason in skipped[:15]:
            print(f"    {rel}: {reason}")
        if len(skipped) > 15:
            print(f"    ... +{len(skipped) - 15} more")
        print("  Every node in these files is missing from the graph and any")
        print("  Key Files citation into them will not resolve. If the reason is")
        print("  a syntax error on a file the project considers valid, re-run on")
        print("  the interpreter the project targets. Use --strict to fail on this.")

    stale = sum(1 for n in all_notes if "SEMANTICS_STALE" in n)
    print(f"\n  census: {stats['unsemantic']} unsemantic, {stale} stale, "
          f"{stats['orphaned']} orphaned")
    print("  staleness is tracked per NODE, so one changed class does not")
    print("  invalidate its whole module. Full report: graph_walker.py --report")

    # Two independent reasons to fail. Drift only fails under --check, because a
    # write run is how drift gets resolved and failing on it would make the normal
    # path exit non-zero. A skip fails whenever --strict is set, in either mode:
    # writing a knowingly incomplete graph is the case worth stopping.
    drift = bool(args.check and (stats["new"] or stats["orphaned"] or stale))
    unparsed = bool(args.strict and skipped)
    return 1 if (drift or unparsed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
