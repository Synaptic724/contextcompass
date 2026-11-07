#!/usr/bin/env python3
"""Inventory Context Compass text and explain the cost of its declared reading routes."""

from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import importlib.metadata
import itertools
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
_bytecode_setting = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    from reading_routes import (  # noqa: E402
        RouteError, TICKETS, COMMUNICATIONS, EVENTS, registry, chain,
        configured_backends, relative_path, requirements,
    )
finally:
    sys.dont_write_bytecode = _bytecode_setting

GENERATOR = "contextcompass.token_report.v1"
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".codex", ".agents"}
SENSITIVE_NAMES = {"auth.json", "credentials", "credentials.json", "id_rsa", "id_ed25519",
                   "secrets.json", "secrets.yml", "secrets.yaml"}


def generated_directory(path):
    marker = path / "report.json"
    if marker.is_symlink() or not marker.is_file():
        return False
    try:
        with marker.open("rb") as stream:
            head = stream.read(256).decode("utf-8")
        return bool(re.match(r'\s*\{\s*"generator"\s*:\s*"' + re.escape(GENERATOR) + '"', head))
    except (OSError, UnicodeError):
        return False


def tokenizer(name):
    try:
        import tiktoken
    except ImportError as exc:
        raise RouteError("Token reporting needs the optional tokenizer: pip install 'contextcompass[tokens]' "
                         "(or install tiktoken for a copied payload). Nothing was installed automatically.") from exc
    try:
        encoding = tiktoken.get_encoding(name)
    except Exception as exc:
        raise RouteError(f"Cannot load encoding {name!r}: {exc}. The public vocabulary may need caching first.") from exc
    return lambda text: len(encoding.encode_ordinary(text)), importlib.metadata.version("tiktoken")


def section(text, heading):
    match = re.search(rf"(?m)^## {re.escape(heading)}[ \t]*\r?$", text)
    if not match:
        return None
    end = re.search(r"(?m)^## ", text[match.end():])
    stop = match.end() + end.start() if end else len(text)
    return text[match.start():stop], match.start(), stop


class Inventory:
    def __init__(self, root, counter, max_bytes, output=None):
        self.root, self.counter, self.max_bytes = root.resolve(), counter, max_bytes
        self.files, self.warnings, self.scopes = {}, [], {}
        self.board_text = {}
        for directory, dirs, names in os.walk(self.root, followlinks=False,
                                               onerror=lambda exc: self.warnings.append(str(exc))):
            for name in list(dirs):
                path = pathlib.Path(directory) / name
                linked = path.is_symlink() or getattr(path, "is_junction", lambda: False)()
                if (name.casefold() in SKIP_DIRS or linked or output and path.resolve() == output.resolve()
                        or generated_directory(path)):
                    dirs.remove(name)
                    self.warnings.append(f"Excluded directory: {path.relative_to(self.root).as_posix()}")
            for name in sorted(names):
                path = pathlib.Path(directory) / name
                key = path.relative_to(self.root).as_posix()
                row = {"path": key, "tokens": None, "status": "pending"}
                self.files[key] = row
                try:
                    if path.is_symlink():
                        row["status"] = "excluded_link"
                        continue
                    row["bytes"] = path.stat().st_size
                    if (name.casefold().startswith(".env") or name.casefold() in SENSITIVE_NAMES or
                            path.suffix.lower() in (".key", ".pem", ".p12", ".pfx", ".pyc", ".pyo")):
                        row["status"] = "excluded_sensitive_or_cache"
                        continue
                    if max_bytes and row["bytes"] > max_bytes:
                        row["status"] = "over_size_limit"
                        continue
                    before = path.stat()
                    raw = path.read_bytes()
                    row["sha256"] = hashlib.sha256(raw).hexdigest()
                    if b"\0" in raw:
                        row["status"] = "binary"
                        continue
                    text = raw.decode("utf-8")
                    after = path.stat()
                    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                        row["status"] = "changed_during_read"
                        continue
                    row.update(tokens=counter(text), lines=len(text.splitlines()),
                               characters=len(text), status="measured")
                    if key in ("mailbox_board.md", "attention_board.md"):
                        self.board_text[key] = text
                except UnicodeError:
                    row["status"] = "non_utf8"
                except OSError as exc:
                    row.update(status="unreadable", error=str(exc))

    def get(self, path):
        key = relative_path(self.root, path)
        if key not in self.files:
            self.files[key] = {"path": key, "tokens": None,
                               "status": "directory_reference" if (self.root / key).is_dir() else "missing"}
        return self.files[key]

    def scope(self, path, communication):
        key = (path, communication)
        if key in self.scopes:
            return self.scopes[key]
        row = self.get(path)
        scope = {"known_tokens": row["tokens"], "scope": "full_file", "unresolved": None}
        if row["status"] == "measured" and path == "mailbox_board.md":
            roster = section(self.board_text[path], "Checked-In Agents")
            scope = {"known_tokens": self.counter(roster[0]) if roster else None,
                     "scope": "roster_plus_session_specific_text",
                     "unresolved": "Relevant session Notes" + (" and addressed Messages" if communication == "mailbox" else "")}
        elif row["status"] == "measured" and path == "attention_board.md" and communication == "codex_mcp":
            text = self.board_text[path]
            alerts = section(text, "Message Alerts")
            projected = text[:alerts[1]] + text[alerts[2]:] if alerts else text
            scope.update(known_tokens=self.counter(projected), scope="excluding_message_alerts")
        self.scopes[key] = scope
        return scope


def calculate_route(inventory, declarations, communication):
    paths = {}
    for entry in declarations["required"]:
        row = inventory.get(entry["path"])
        if entry["if_exists"] and row["status"] == "missing":
            continue
        value = paths.setdefault(row["path"], dict(path=row["path"], status=row["status"],
            full_file_tokens=row["tokens"], reasons=[], **inventory.scope(row["path"], communication)))
        value["reasons"].append({"reason": entry["reason"], "source": entry["source"], "line": entry["line"]})
    optional = []
    optional_keys = set()
    for entry in declarations["optional"]:
        candidates = ([p for p in list(inventory.files) if p.startswith(entry["path"]) and p not in paths]
                      if entry.get("recursive") else [entry["path"]])
        for path in candidates:
            row = inventory.get(path)
            key = (row["path"], entry["state"])
            if key not in optional_keys:
                optional_keys.add(key)
                optional.append(dict(entry, path=row["path"], tokens=row["tokens"], status=row["status"]))
    return {"role_chain": declarations["role_chain"], "paths": list(paths.values()),
            "known_tokens": sum(p["known_tokens"] or 0 for p in paths.values()),
            "full_file_reference_tokens": sum(p["full_file_tokens"] or 0 for p in paths.values()),
            "unmeasured_paths": [p["path"] for p in paths.values() if p["known_tokens"] is None],
            "session_specific_paths": [p["path"] for p in paths.values() if p["unresolved"]],
            "optional_paths": optional, "optional_sections": declarations["optional_sections"]}


def build_report(root, counter, encoding="o200k_base", version="injected", role=None,
                 ticket=None, communication=None, event="onboard", max_bytes=10 * 1024 * 1024, output=None):
    root = root.resolve()
    if not (root / "AGENTS.MD").is_file():
        raise RouteError("Select an existing Context Compass root containing AGENTS.MD")
    roles = registry(root)
    if role and role not in roles:
        raise RouteError(f"Unregistered role: {role}")
    configured_ticket, configured_communication = configured_backends(root)
    ticket, communication = ticket or configured_ticket, communication or configured_communication
    if ticket not in TICKETS or communication not in COMMUNICATIONS or event not in EVENTS:
        raise RouteError("Unsupported ticket, communication or entry-event selection")
    inventory = Inventory(root, counter, max_bytes, output)
    specials = sorted(p for p, row in inventory.files.items()
                      if p.startswith("special_instructions/") and pathlib.PurePosixPath(p).suffix.lower() == ".md")
    routes = []
    for name in roles:
        try:
            resolved, error = chain(root, roles, name), None
        except (RouteError, OSError, UnicodeError) as exc:
            resolved, error = None, str(exc)
        for tickets, transport, entry_event in itertools.product(TICKETS, COMMUNICATIONS, EVENTS):
            route = {"id": f"{name}/{tickets}/{transport}/{entry_event}", "role": name,
                     "ticket_backend": tickets, "communication_backend": transport, "event": entry_event}
            if error:
                route.update(status="unresolved", error=error, known_tokens=None)
            else:
                try:
                    declared = requirements(root, roles, name, tickets, transport, entry_event, specials, resolved)
                    route.update(calculate_route(inventory, declared, transport), status="resolved_declarations")
                except (RouteError, OSError, UnicodeError) as exc:
                    route.update(status="unresolved", error=str(exc), known_tokens=None)
            routes.append(route)
    selected = f"{role}/{ticket}/{communication}/{event}" if role else None
    for row in inventory.files.values():
        row.update(baseline_route_count=0, optional_route_count=0, read_states=set())
    for route in routes:
        for key, count_field in (("paths", "baseline_route_count"), ("optional_paths", "optional_route_count")):
            for entry in route.get(key, []):
                row = inventory.files[entry["path"]]
                row[count_field] += 1
                row["read_states"].add("baseline" if key == "paths" else entry["state"])
    for row in inventory.files.values():
        row["read_states"] = sorted(row["read_states"]) or ["not_declared_in_routes"]
    return {"generator": GENERATOR, "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "encoding": encoding, "tokenizer_version": version, "root": str(root),
            "selected_route": selected, "configured_backends": {"ticket": configured_ticket, "communication": configured_communication},
            "roles": roles, "routes": routes, "files": sorted(inventory.files.values(), key=lambda r: r["path"]),
            "warnings": inventory.warnings,
            "limits": ["Source text for the explicit encoding, not model-specific request, billing or cumulative usage.",
                       "Declared routes only: prose project overrides and additional runtime/task reads require human interpretation.",
                       "Mailbox relevant Notes/messages are session-specific; known totals are lower bounds, not full mailbox charges.",
                       "Optional full-file sizes are not mandatory reads or exact costs of topic-specific slices.",
                       "Only this Context Compass root is scanned; global harness instructions are outside scope.",
                       "Backend cost comparisons do not verify connector access, account permissions or configuration readiness.",
                       "Files are individual snapshots; concurrent changes can invalidate comparisons."]}


def markdown(report):
    measured = [row for row in report["files"] if row["status"] == "measured"]
    out = ["# Context Compass Token Report", "", f"Generated: {report['generated_at']}", "",
           f"Tokenizer: tiktoken {report['tokenizer_version']}; explicit encoding: `{report['encoding']}`.",
           f"Inventory: {len(report['files'])} paths; {len(measured)} measured; {len(report['roles'])} registered roles.", "",
           "This is a map of declared reading choices, not a change to agent instructions.", "",
           "## How To Read This Report", ""]
    out += ["- " + value for value in report["limits"]]
    out += ["", "## Registered Roles", "",
            "These flags come from the existing registry, not from token size. Entry-only roles are not steady-state alternatives.", "",
            "| Role | Parent | Steady-state selection | User-defined | Role README |",
            "| --- | --- | --- | --- | --- |"]
    for name, role in report["roles"].items():
        out.append(f"| {name} | {role['parent'] or '-'} | {'yes' if role['selectable_after_onboarding'] else 'entry-only'} | {'yes' if role['user_defined'] else 'no'} | {'yes' if role['reads_readme'] else 'no'} |")
    out += ["", "## All Route Choices", "",
            "Each role is expanded across both ticket backends, both communication modes and onboarding/recovery.",
            "Known tokens deduplicate shared paths. Session-specific text is additional and unknown.", "",
            "| Role | Ticket backend | Messages | Entry | Known tokens | Unmeasured paths | Session-specific paths |",
            "| --- | --- | --- | --- | ---: | ---: | ---: |"]
    for route in report["routes"]:
        if route["status"] == "unresolved":
            out.append(f"| {route['role']} | {route['ticket_backend']} | {route['communication_backend']} | {route['event']} | UNKNOWN | declaration error | - |")
        else:
            out.append(f"| {route['role']} | {route['ticket_backend']} | {route['communication_backend']} | {route['event']} | {route['known_tokens']:,}+ | {len(route['unmeasured_paths'])} | {len(route['session_specific_paths'])} |")
    out += ["", "## Selected Route And Inherited Paths", ""]
    selected = next((r for r in report["routes"] if r["id"] == report["selected_route"]), None)
    if selected and selected["status"] != "unresolved":
        out += [f"`{selected['id']}`", "", "Inheritance: " + " -> ".join(selected["role_chain"]), "",
                "| Path | Known tokens | Full-file reference size | Read scope | Why included |",
                "| --- | ---: | ---: | --- | --- |"]
        for row in selected["paths"]:
            why = "; ".join(dict.fromkeys(x["reason"] for x in row["reasons"]))
            out.append(f"| `{row['path']}` | {row['known_tokens'] if row['known_tokens'] is not None else 'UNKNOWN'} | {row['full_file_tokens'] if row['full_file_tokens'] is not None else 'UNKNOWN'} | {row['scope']} | {why} |")
        out += ["", "### Conditional And Self-Directed Choices", "",
                "These are not added to the baseline. Their listed sizes refer to full files; actual triggers/slices are a separate choice.", "",
                "| Path | State | Full-file tokens | Declaration |", "| --- | --- | ---: | --- |"]
        for row in selected["optional_paths"]:
            out.append(f"| `{row['path']}` | {row['state']} | {row['tokens'] if row['tokens'] is not None else 'UNKNOWN'} | `{row['source']}:{row['line']}` |")
        for value in selected["optional_sections"]:
            if not value["paths"]:
                out.append(f"\n- `{value['source']}:{value['line']}` declares **{value['label']}** without explicit paths; read its stated conditions rather than assuming zero extra work.")
    elif selected:
        out.append("Selected route is unresolved: " + selected["error"])
    else:
        out.append("No role was assumed. Use `--role <registered-name>` for an inherited per-path explanation; all route choices are shown above.")
    out += ["", "## Every Path By Source Size", "",
            "This inventory includes tools, examples, inactive roles and user state. Its total is NOT one onboarding readset.", "",
            "| Path | Full-file tokens | Lines | Read states | Baseline routes | Status |", "| --- | ---: | ---: | --- | ---: | --- |"]
    for row in sorted(report["files"], key=lambda r: (-(r.get("tokens") or 0), r["path"])):
        out.append(f"| `{row['path']}` | {row['tokens'] if row['tokens'] is not None else 'UNKNOWN'} | {row.get('lines', '-')} | {', '.join(row['read_states'])} | {row['baseline_route_count']} | {row['status']} |")
    errors = sorted({r["error"] for r in report["routes"] if r["status"] == "unresolved"})
    out += ["", "## Diagnostics", ""]
    out += ["- " + value for value in errors + report["warnings"]] or ["- No declaration or scan errors."]
    out += ["", "JSON contains the full per-route path/reason maps, including source declaration lines. CSV contains every inventory path.",
            "Keep generated reports local when they include private path metadata."]
    return "\n".join(out) + "\n"


def write_report(report, output):
    output = output.resolve()
    root = pathlib.Path(report["root"])
    if output == root or root.is_relative_to(output):
        raise RouteError("Report output must not replace the input root or one of its ancestors")
    for name in ("report.json", "report.md", "files.csv"):
        if (output / name).is_symlink():
            raise RouteError("Report destinations must not be symbolic links")
    if output.exists() and any(output.iterdir()):
        if not generated_directory(output):
            raise RouteError("Select an empty output directory or one already owned by this report generator")
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(markdown(report), encoding="utf-8")
    with (output / "files.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, ["path", "tokens", "lines", "bytes", "status", "sha256", "baseline_route_count", "optional_route_count", "read_states"], extrasaction="ignore")
        writer.writeheader()
        for row in report["files"]:
            record = dict(row, read_states=";".join(row["read_states"]))
            if record["path"].startswith(("=", "+", "-", "@", "\t", "\r")):
                record["path"] = "'" + record["path"]
            writer.writerow(record)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, required=True)
    parser.add_argument("--role", help="registered role for the detailed explanation; no role is assumed")
    parser.add_argument("--ticket-backend", choices=TICKETS)
    parser.add_argument("--communication-backend", choices=COMMUNICATIONS)
    parser.add_argument("--event", choices=EVENTS, default="onboard")
    parser.add_argument("--encoding", default="o200k_base")
    parser.add_argument("--max-file-bytes", type=int, default=10 * 1024 * 1024,
                        help="larger files stay visible as unmeasured; 0 means unlimited")
    parser.add_argument("--out-dir", type=pathlib.Path, help="write Markdown, JSON and CSV; otherwise print Markdown")
    args = parser.parse_args(argv)
    try:
        if args.max_file_bytes < 0:
            raise RouteError("--max-file-bytes cannot be negative")
        count, version = tokenizer(args.encoding)
        report = build_report(args.root, count, args.encoding, version, args.role,
                              args.ticket_backend, args.communication_backend, args.event,
                              args.max_file_bytes, args.out_dir)
        if args.out_dir:
            write_report(report, args.out_dir)
            print(f"REPORT: {args.out_dir.resolve() / 'report.md'}")
            print(f"  {len(report['files'])} paths; {len(report['routes'])} route choices; encoding {args.encoding}")
        else:
            print(markdown(report), end="")
        return int(any(r["status"] == "unresolved" for r in report["routes"]))
    except (RouteError, OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
