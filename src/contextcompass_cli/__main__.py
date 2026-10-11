#!/usr/bin/env python3
"""The `contextcompass` command.

    contextcompass init                 put context_compass/ into this repo
    contextcompass upgrade --check      what an upgrade would change
    contextcompass upgrade --apply      do it
    contextcompass migrate-boards ...   one-time board migration
    contextcompass version              installed and on-disk versions

WHY A CLI AT ALL

Without it, adopting Context Compass means cloning a repository and copying a
directory out of it by hand, and upgrading means keeping a second checkout
around at the right version so `--new` has somewhere to point. As a command, the
installed package IS the new version, so there is nothing to keep in sync.

The subcommands delegate to the same scripts that ship inside the payload. They
are not reimplemented here: one copy of the logic, exercised by the same tests,
whether it is reached through the CLI or run directly from a repository.
"""

from __future__ import annotations

import argparse
import pathlib
import runpy
import shutil
import sys

from . import PAYLOAD, INSTALL_DIRNAME, __version__

TOOLS = PAYLOAD / "tools"


def _run_tool(script: pathlib.Path, argv: list[str]) -> int:
    """Run a payload script in-process with the argv it expects.

    `runpy` rather than a subprocess: the scripts bootstrap their own imports by
    inserting their directory on `sys.path`, and this keeps that behaviour
    identical whether they are reached through the CLI or invoked directly.
    """
    old_argv = sys.argv
    sys.argv = [str(script), *argv]
    try:
        runpy.run_path(str(script), run_name="__main__")
        return 0
    except SystemExit as exc:
        return int(exc.code or 0)
    finally:
        sys.argv = old_argv


def cmd_init(args: argparse.Namespace) -> int:
    target = args.into.resolve() / INSTALL_DIRNAME
    if target.exists():
        print(f"REFUSED: {target} already exists.")
        print("  This command creates a new install; it will not write over one.")
        print("  To bring an existing install up to date:  contextcompass upgrade --check")
        return 2

    if not PAYLOAD.is_dir():
        print(f"ERROR: payload missing from the installed package ({PAYLOAD}).")
        print("  This is a packaging fault, not a usage error - the wheel was built")
        print("  without its data files.")
        return 2

    # Importing the payload's tools compiles bytecode INTO the installed
    # package, so a pip-installed copy grows `__pycache__` directories that are
    # not part of the package. Copying those into someone's repository puts 29
    # untracked binary files in their first commit and makes the install
    # disagree with its own manifest.
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")

    if args.check:
        n = sum(1 for p in PAYLOAD.rglob("*")
                if p.is_file() and "__pycache__" not in p.parts)
        print(f"WOULD CREATE: {target}  ({n} files, version {__version__})")
        return 0

    shutil.copytree(PAYLOAD, target, ignore=ignore)
    n = sum(1 for p in target.rglob("*") if p.is_file())
    print(f"CREATED: {target}")
    print(f"  {n} files, version {__version__}")
    print()
    print("Next:")
    print(f"  1. Point your agent at {INSTALL_DIRNAME}/AGENTS.MD and ask it to onboard")
    print("     as `engineer`.")
    print("  2. If your custom instructions lack Context Compass, the agent will offer")
    print("     setup for recovery after compaction, tracking, and subagents.")
    print("  3. Commit the directory. It is your repository's memory now, and it is")
    print("     meant to be reviewed and diffed like any other source.")
    return 0


def cmd_upgrade(args: argparse.Namespace) -> int:
    install = args.install.resolve()
    if not (install / "AGENTS.MD").is_file():
        print(f"ERROR: {install} is not a Context Compass install (no AGENTS.MD).")
        print(f"  Pass --install, or run from a repo containing {INSTALL_DIRNAME}/.")
        return 2
    argv = ["--install", str(install), "--new", str(PAYLOAD)]
    argv += ["--apply"] if args.apply else ["--check"]
    for flag in ("keep_retired", "preserve_local", "seed_instance"):
        if getattr(args, flag):
            argv.append("--" + flag.replace("_", "-"))
    return _run_tool(TOOLS / "update_context_compass.py", argv)


def cmd_migrate_boards(args: argparse.Namespace) -> int:
    install = args.install.resolve()
    if not (install / "AGENTS.MD").is_file():
        print(f"ERROR: {install} is not a Context Compass install (no AGENTS.MD).")
        return 2
    argv = ["--install", str(install), "--new", str(PAYLOAD)]
    argv += ["--apply"] if args.apply else ["--check"]
    if args.diff:
        argv.append("--diff")
    return _run_tool(TOOLS / "migrate_boards.py", argv)


def cmd_version(args: argparse.Namespace) -> int:
    print(f"contextcompass {__version__}")
    manifest = PAYLOAD / "MANIFEST.md"
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if line.startswith("| package_version |"):
                print(f"  payload manifest: {line.split('|')[2].strip()}")
                break
    install = args.install.resolve() / "MANIFEST.md" if args.install else None
    if install and install.is_file():
        for line in install.read_text(encoding="utf-8").splitlines():
            if line.startswith("| package_version |"):
                print(f"  installed here  : {line.split('|')[2].strip()}")
                break
    return 0


def default_install() -> pathlib.Path:
    """`./context_compass` if it exists, else `.` - so both layouts just work."""
    here = pathlib.Path.cwd()
    nested = here / INSTALL_DIRNAME
    return nested if (nested / "AGENTS.MD").is_file() else here


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="contextcompass", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=f"contextcompass {__version__}")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help=f"create {INSTALL_DIRNAME}/ in a repository")
    p.add_argument("--into", type=pathlib.Path, default=pathlib.Path("."),
                   help="repository root (default: current directory)")
    p.add_argument("--check", action="store_true", help="report only, write nothing")
    p.set_defaults(func=cmd_init)

    # Flags are declared, not forwarded blindly. `parse_known_args` would pass a
    # typo straight through to a tool that ignores it, and the run would look
    # like it honoured a flag it never saw.
    p = sub.add_parser("upgrade", help="upgrade an install to this version")
    p.add_argument("--install", type=pathlib.Path, default=None)
    p.add_argument("--check", action="store_true",
                   help="report only, write nothing (the default)")
    p.add_argument("--apply", action="store_true", help="perform the upgrade")
    p.add_argument("--keep-retired", action="store_true",
                   help="do not sweep files the new version no longer ships")
    p.add_argument("--preserve-local", action="store_true",
                   help="do not conform package files you have edited")
    p.add_argument("--seed-instance", action="store_true",
                   help="create INSTANCE files the manifest lists but disk lacks")
    p.set_defaults(func=cmd_upgrade)

    p = sub.add_parser("migrate-boards",
                       help="one-time board migration into USER-DEFINED regions")
    p.add_argument("--install", type=pathlib.Path, default=None)
    p.add_argument("--check", action="store_true",
                   help="report only, write nothing (the default)")
    p.add_argument("--apply", action="store_true", help="rewrite the boards")
    p.add_argument("--diff", action="store_true", help="print a unified diff per board")
    p.set_defaults(func=cmd_migrate_boards)

    p = sub.add_parser("version", help="show installed and on-disk versions")
    p.add_argument("--install", type=pathlib.Path, default=None)
    p.set_defaults(func=cmd_version)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if getattr(args, "install", "missing") is None:
        args.install = default_install()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
