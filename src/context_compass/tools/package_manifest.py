#!/usr/bin/env python3
"""Emit the package manifest: what ships, who owns it, and its hash.

The manifest is the contract both `cleanup_context_compass.py` and
`update_context_compass.py` read. It answers three questions per path:

    does this file belong to the package?   -> presence in the manifest
    who is allowed to change it?            -> the ownership class
    has it changed since it shipped?        -> the sha256

WHY A GENERATED MANIFEST RATHER THAN PER-FILE VERSION STAMPS

A version header inside each document has to be bumped by hand, and nothing
enforces the bump. Miss one and the stamp lies while looking authoritative -
the same failure mode as a stale index. A manifest rebuilt from the files
themselves cannot drift, because it is derived rather than declared.

OWNERSHIP CLASSES

    PACKAGE   ships with the library and is not edited downstream.
              Cleanup restores it. Update replaces it.

    RESET     a lane the package seeds and the consuming project then fills:
              tickets, artifacts, system docs, project instructions.
              Cleanup removes files NOT in the manifest and keeps the ones that
              are. Update never touches the contents.

    INSTANCE  the project's own work, listed so both tools know to leave it
              alone. Two directories: `agent_onboarding/user_defined/` for role
              overlays, and top-level `user_defined/` for anything else. Neither
              tool restores, replaces or removes anything in either, in any mode.
              Listing them explicitly is safer than relying on absence, because a
              file missing from the manifest is indistinguishable from one that
              was never meant to be there.

              These exist so an upgrade never has to choose between the user's
              work and the new version. Package files are conformed; if you need
              something different, it lives here instead.

    LIVE      one file holding a package-owned block plus instance-owned body.
              The boards. Update swaps only the block between MANAGED markers.

    CONFIG    key-level merge, never a whole-file swap. Adding a key must not
              silently reset a value the user set.

Classes are assigned by path prefix, longest match wins, so a PACKAGE directory
can still contain a RESET subtree. That distinction is not theoretical: during
the cleanup that motivated this tool, `tools/` was package-owned and still had
five foreign files sitting in it.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import sys

MANIFEST_NAME = "MANIFEST.md"
MANIFEST_VERSION = "1.0.0"

# Manifest FORMAT majors these tools can read. Distinct from `package_version`,
# which is the content: the package moves 2.3 -> 2.5 without the format changing.
#
# Read on every load, because the alternative is the failure this file was
# written to avoid. A tool from an older release meeting a format it does not
# understand will parse SOMETHING - a subset of rows, or none - and then act on
# it: conform files it misread as package-owned, sweep paths it failed to see.
# Refusing on an unknown major turns a silent wrong action into a clear stop.
#
# Forward compatibility is one-directional and cannot be otherwise. A new tool
# reads an old manifest fine; an old tool cannot be taught a format that did not
# exist when it shipped. So bumping this major is a breaking change for every
# install still on an older package, and the error says exactly that.
SUPPORTED_MANIFEST_MAJORS = frozenset({"1"})


def manifest_version_of(text: str) -> str | None:
    """The manifest FORMAT version recorded in a manifest, if it declares one."""
    for line in text.splitlines():
        if line.startswith("| manifest_version |"):
            return line.split("|")[2].strip()
    return None


def check_manifest_compatible(text: str, source: str) -> str | None:
    """None if this manifest is readable, else a message explaining why not.

    A manifest with no `manifest_version` predates the field and is accepted:
    the format was 1.x throughout, so refusing would break installs over a
    stamp that was missing rather than wrong.
    """
    version = manifest_version_of(text)
    if version is None:
        return None
    major = version.split(".")[0]
    if major in SUPPORTED_MANIFEST_MAJORS:
        return None
    return (f"{source} declares manifest format {version}, and these tools read "
            f"format {'/'.join(sorted(SUPPORTED_MANIFEST_MAJORS))}.x only.\n"
            f"  This package is older than the manifest it was pointed at. Upgrade "
            f"the tools rather than\n  the install: an older tool cannot be taught a "
            f"newer format, and guessing would mean\n  acting on a partial reading of "
            f"what the install owns.")

# Longest matching prefix wins. Order here is for reading, not for matching.
CLASS_RULES: tuple[tuple[str, str], ...] = (
    ("", "PACKAGE"),                        # default
    ("tickets/", "RESET"),
    ("artifacts/", "RESET"),
    ("system_docs/", "RESET"),
    ("context_management/", "RESET"),
    ("special_instructions/", "RESET"),
    ("agent_onboarding/user_defined/", "INSTANCE"),
    ("user_defined/", "INSTANCE"),
    ("attention_board.md", "LIVE"),
    ("issue_board.md", "LIVE"),
    ("artifact_board.md", "LIVE"),
    ("mailbox_board.md", "LIVE"),
    ("config/context_compass_config.yaml", "CONFIG"),
)

SKIP_DIRS = {"__pycache__", ".git"}

# Lanes where the install may hold files the package does not ship. Everything
# outside them is STRICT: an upgrade sweeps whatever is not in the manifest.
#
# The asymmetry is the point. A ticket the package never heard of is the whole
# purpose of `tickets/`; a skill the package never heard of sitting in
# `agent_onboarding/default/` is a document retired versions ago that agents are
# still reading. Reporting it is not enough - it was reported for two upgrades
# and stayed, because nobody hand-deletes from a list.
#
# Observed on a real install: a `scripts/` directory left over from before the
# rename to `tools/`, a root `router.md` from the retired dual-router era, and a
# lowercase `SKILLS.md` beside the real one. All silently readable, all wrong.
PERMISSIVE_LANES: tuple[str, ...] = (
    "tickets/",
    "artifacts/",
    "system_docs/",
    "context_management/",
    "special_instructions/",
    "user_defined/",
    "agent_onboarding/user_defined/",
)


def is_permissive(rel: str) -> bool:
    """True if the install may keep unmanifested files at this path."""
    return rel.startswith(PERMISSIVE_LANES)


def classify(rel: str) -> str:
    """Ownership class for a package-relative path. Longest prefix wins."""
    best, best_len = "PACKAGE", -1
    for prefix, cls in CLASS_RULES:
        if rel == prefix or (prefix.endswith("/") and rel.startswith(prefix)):
            if len(prefix) > best_len:
                best, best_len = cls, len(prefix)
    return best


def walk(root: pathlib.Path) -> list[pathlib.Path]:
    out = []
    for p in sorted(root.rglob("*"), key=lambda x: str(x).upper()):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name == MANIFEST_NAME and p.parent == root:
            continue                      # never hash the manifest into itself
        out.append(p)
    return out


def normalize_eol(raw: bytes) -> bytes:
    """CRLF and lone CR collapsed to LF, for text only.

    The package ships LF and `.gitattributes` enforces it HERE - but that file
    does not travel into a consuming repository. A Windows checkout of a repo
    that vendored `context_compass/` converts the tree to CRLF, and a byte hash
    then reports every one of those files as locally edited. That is not a
    hypothetical: it marked 267 files in one install, and the three-hash rule
    correctly-but-uselessly answered "you edited it, keep yours" for all of them,
    silently freezing that install against every future upgrade.

    A line terminator is not a local edit. Hashing the normalized bytes makes the
    comparison mean what it was always supposed to mean: did the CONTENT change.

    Binary passes through untouched - `\\r\\n` inside a PNG is data, not a
    newline - and "binary" is decided by whether the bytes are valid UTF-8 rather
    than by extension, because an extension list is a thing you forget to update.

    Backward compatible by construction: an LF file hashes to exactly what it
    hashed to before, so every manifest already written stays valid.
    """
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha_bytes(raw: bytes) -> str:
    """Content hash, line-ending agnostic. The one definition; import it."""
    return hashlib.sha256(normalize_eol(raw)).hexdigest()


def sha(path: pathlib.Path) -> str:
    return sha_bytes(path.read_bytes())


def detect_eol(path: pathlib.Path) -> bytes:
    """The terminator a file already uses, or the platform default if it is new.

    Used on the WRITE side so an upgrade does not rewrite a Windows install's
    whole tree to LF just to deliver one changed document. Match what is there;
    if there is nothing there, follow the OS.
    """
    if path.is_file():
        try:
            head = path.read_bytes()[:65536]
        except OSError:
            head = b""
        if b"\r\n" in head:
            return b"\r\n"
        if b"\n" in head:
            return b"\n"
    return os.linesep.encode()


def apply_eol(payload: bytes, eol: bytes) -> bytes:
    """Re-terminate text `payload` with `eol`. Binary is returned untouched."""
    normalized = normalize_eol(payload)
    if normalized is payload and b"\n" not in payload:
        return payload                      # binary, or nothing to terminate
    try:
        payload.decode("utf-8")
    except UnicodeDecodeError:
        return payload
    return normalized if eol == b"\n" else normalized.replace(b"\n", eol)


def build(root: pathlib.Path, version: str) -> str:
    rows = []
    for p in walk(root):
        rel = p.relative_to(root).as_posix()
        rows.append((rel, classify(rel), sha(p)))

    counts: dict[str, int] = {}
    for _, cls, _ in rows:
        counts[cls] = counts.get(cls, 0) + 1

    out = [
        "# MANIFEST",
        "",
        "Generated by `tools/package_manifest.py`. Do not hand-edit: it is derived",
        "from the files themselves, which is the only reason it can be trusted.",
        "",
        "| field | value |",
        "| --- | --- |",
        f"| manifest_version | {MANIFEST_VERSION} |",
        f"| package_version | {version} |",
        f"| files | {len(rows)} |",
        "",
        "## Lane policy",
        "",
        "Lanes where the install may keep files the package does not ship.",
        "Everything outside them is STRICT: an upgrade sweeps what is not listed here.",
        "",
        "| lane | policy |",
        "| --- | --- |",
        *[f"| `{L}` | permissive |" for L in PERMISSIVE_LANES],
        "| everything else | strict - swept on upgrade |",
        "",
        "## Ownership classes",
        "",
        "| class | files | cleanup | update |",
        "| --- | --- | --- | --- |",
        f"| PACKAGE | {counts.get('PACKAGE', 0)} | restore | replace |",
        f"| RESET | {counts.get('RESET', 0)} | keep listed, remove unlisted | leave alone |",
        f"| INSTANCE | {counts.get('INSTANCE', 0)} | never touched | never touched |",
        f"| LIVE | {counts.get('LIVE', 0)} | reset managed block | swap managed block |",
        f"| CONFIG | {counts.get('CONFIG', 0)} | restore missing keys | merge keys |",
        "",
        "## Files",
        "",
        "| path | class | sha256 |",
        "| --- | --- | --- |",
    ]
    for rel, cls, digest in rows:
        out.append(f"| `{rel}` | {cls} | `{digest}` |")
    out.append("")
    return "\n".join(out)


def parse(text: str) -> dict[str, tuple[str, str]]:
    """Read a manifest back. Returns {path: (class, sha256)}."""
    entries: dict[str, tuple[str, str]] = {}
    in_files = False
    for line in text.splitlines():
        if line.startswith("## Files"):
            in_files = True
            continue
        if not in_files or not line.startswith("| `"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and len(cells[2]) == 64:
            entries[cells[0]] = (cells[1], cells[2])
    return entries


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, type=pathlib.Path,
                    help="package root, the directory holding AGENTS.MD")
    ap.add_argument("--version", default="0.0.0", help="package version to record")
    ap.add_argument("--check", action="store_true",
                    help="compare against the manifest on disk, write nothing")
    args = ap.parse_args()

    root: pathlib.Path = args.root
    if not (root / "AGENTS.MD").is_file():
        print(f"ERROR: {root} does not look like a package root (no AGENTS.MD)")
        return 2

    target = root / MANIFEST_NAME
    version = args.version
    if version == "0.0.0" and target.is_file():
        for line in target.read_text(encoding="utf-8").splitlines():
            if line.startswith("| package_version |"):
                version = line.split("|")[2].strip()
                break

    text = build(root, version)

    if args.check:
        if not target.is_file():
            print("MISSING: no manifest on disk")
            return 1
        current = target.read_text(encoding="utf-8")
        if current == text:
            print(f"OK: manifest is current ({len(parse(text))} files)")
            return 0
        old, new = parse(current), parse(text)
        added = sorted(set(new) - set(old))
        removed = sorted(set(old) - set(new))
        changed = sorted(p for p in set(old) & set(new) if old[p][1] != new[p][1])

        # A rename that only changes case is ONE file, not an add and a remove.
        # Reported as two it looks like unrelated churn, and the obvious repair -
        # "delete the removed one" - destroys the added one, because on a
        # case-insensitive filesystem they are the same inode. Observed three
        # times on `SKILLS.MD` in a single day, drifting to `SKILLS.md` from
        # something outside this package. Naming it is what makes it fixable.
        removed_ci = {p.lower(): p for p in removed}
        drift = [(removed_ci[p.lower()], p) for p in added if p.lower() in removed_ci]
        drifted = {a for _, a in drift} | {b for b, _ in drift}
        added = [p for p in added if p not in drifted]
        removed = [p for p in removed if p not in drifted]

        # The other half of the same disease, and the half that actually shipped.
        # Here the twin was never removed: both names exist at once. That cannot
        # happen on Windows or macOS, so it is invisible to whoever created it and
        # only ever fails on Linux - reported, before this, as a bare
        # `added SKILLS.md`, which reads like a stray file somebody forgot to
        # manifest. The repair for a stray file is "add it to the manifest", and
        # that is exactly wrong: it would enshrine a tree that cannot be checked
        # out on half the machines that use it.
        kept_ci = {p.lower(): p for p in old if p in new}
        collide = [(kept_ci[p.lower()], p) for p in added if p.lower() in kept_ci]
        added = [p for p in added if p not in {b for _, b in collide}]

        print(f"STALE: +{len(added)} -{len(removed)} ~{len(changed)}"
              + (f"  CASE DRIFT {len(drift)}" if drift else "")
              + (f"  CASE COLLISION {len(collide)}" if collide else ""))
        for was, now in drift:
            same = old.get(was, (None, None))[1] == new.get(now, (None, "x"))[1]
            print(f"  CASE     {was}  ->  {now}"
                  f"   (contents {'identical' if same else 'ALSO changed'})")
        if drift:
            print("           One file whose name changed case, not two files. Rename it")
            print("           back rather than deleting either - on a case-insensitive")
            print("           filesystem both names resolve to the same file.")
        for manifested, stray in collide:
            same = new.get(manifested, (None, None))[1] == new.get(stray, (None, "x"))[1]
            print(f"  COLLIDE  {stray}   collides with manifested {manifested}"
                  f"   (contents {'identical' if same else 'differ'})")
        if collide:
            print("           Two files whose names differ only in case, present at the")
            print("           same time. Legal on Linux, impossible on Windows and macOS.")
            print("           Delete the unmanifested one from the tree - do NOT add it to")
            print("           the manifest, and do not expect a rename on a case-insensitive")
            print("           filesystem to remove it from version control on its own.")
        for p in added[:20]:
            print(f"  added    {p}")
        for p in removed[:20]:
            print(f"  removed  {p}")
        for p in changed[:20]:
            print(f"  changed  {p}")
        return 1

    target.write_bytes(text.encode("utf-8"))
    entries = parse(text)
    counts: dict[str, int] = {}
    for cls, _ in entries.values():
        counts[cls] = counts.get(cls, 0) + 1
    print(f"WROTE: {MANIFEST_NAME}")
    print(f"  package_version {version}")
    print(f"  {len(entries)} files: " +
          ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
