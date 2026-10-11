#!/usr/bin/env python3
"""Read-only standalone GitHub CLI Project preflight (legacy helper).

Verifies, without changing anything: the gh CLI is installed and recent
enough, the user is authenticated (via gh's own credential store), the
repository resolves with Issues enabled, and the required project resolves
and carries the expected Status field. Exits nonzero with a clear message on
the first failure.

This script never asks for, prints, or stores tokens. Authentication is
established separately by a human running setup.ps1/setup.sh, which uses
``gh auth login --web`` interactively. It performs no Issue or Project
mutation and writes no configuration files. See
``agent_onboarding/default/general/skills/security_and_secrets.md``: no path
in the repository may hold a secret, and secrets are never printed.

The github_codex_plugin backend does not require or invoke this CLI helper.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys

PROJECT_URL_RE = re.compile(
    r"^https://github\.com/(?P<kind>orgs|users)/(?P<owner>[^/]+)/"
    r"projects/(?P<number>\d+)(?:/.*)?$"
)
OWNER_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")
VERSION_RE = re.compile(r"^gh version (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)")

DEFAULT_MIN_VERSION = "2.83.2"
DEFAULT_STATUS_FIELD = "Status"


class PreflightError(Exception):
    """A failed check with a human-actionable message (never a secret)."""


def run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a read-only gh subcommand. No stdin, no secrets, bounded time."""
    try:
        return subprocess.run(
            argv,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=60,
            check=False,
        )
    except FileNotFoundError as exc:
        raise PreflightError(
            "gh CLI not found on PATH. Install it from https://cli.github.com, "
            "then re-run this script."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise PreflightError(
            f"Timed out running `{' '.join(argv)}`. Check network access to "
            "github.com and retry."
        ) from exc


def parse_version(text: str) -> tuple[int, int, int]:
    match = VERSION_RE.match(text.strip().splitlines()[0] if text.strip() else "")
    if not match:
        raise PreflightError(
            "Could not parse `gh --version` output. Reinstall gh from "
            "https://cli.github.com and retry."
        )
    return (int(match["major"]), int(match["minor"]), int(match["patch"]))


def parse_min_version(text: str) -> tuple[int, int, int]:
    parts = text.strip().split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise PreflightError(
            f"Invalid --min-version {text!r}; expected MAJOR.MINOR.PATCH."
        )
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def check_gh(min_version: tuple[int, int, int]) -> tuple[int, int, int]:
    if shutil.which("gh") is None:
        raise PreflightError(
            "gh CLI not found on PATH. Install it from https://cli.github.com, "
            "then re-run this script."
        )
    result = run(["gh", "--version"])
    if result.returncode != 0:
        raise PreflightError("`gh --version` failed; reinstall gh and retry.")
    found = parse_version(result.stdout)
    if found < min_version:
        want = ".".join(str(p) for p in min_version)
        have = ".".join(str(p) for p in found)
        raise PreflightError(
            f"gh {have} is older than the supported floor gh {want}. Upgrade "
            "gh, or pass --min-version explicitly to acknowledge the older "
            "version (some checks may then behave unexpectedly)."
        )
    return found


def check_auth() -> None:
    result = run(["gh", "auth", "status"])
    if result.returncode != 0:
        raise PreflightError(
            "gh is not authenticated. Run setup.ps1 (Windows) or setup.sh "
            "(macOS/Linux) and complete `gh auth login --web` interactively. "
            "Never paste a token into chat; gh stores it in its own "
            "credential store."
        )


def validate_slug(owner: str, repo: str) -> str:
    """Reject malformed owner/name inputs before any gh call is made."""
    if not OWNER_RE.match(owner):
        raise PreflightError(
            f"Repository owner {owner!r} is not a valid GitHub owner name "
            "(letters, digits, hyphens; at most 39 characters)."
        )
    if not REPO_RE.match(repo) or repo.startswith(".") or repo.endswith("."):
        raise PreflightError(
            f"Repository name {repo!r} is not a valid GitHub repository name."
        )
    return f"{owner}/{repo}"


def check_repo(owner: str, repo: str) -> str:
    slug = validate_slug(owner, repo)
    result = run(["gh", "repo", "view", slug, "--json", "nameWithOwner,hasIssuesEnabled"])
    if result.returncode != 0:
        raise PreflightError(
            f"Repository {slug!r} did not resolve (gh exit "
            f"{result.returncode}). Check the owner/name spelling and that "
            "the authenticated account may read it."
        )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise PreflightError(
            f"Could not parse `gh repo view` output for {slug!r}."
        ) from exc
    resolved = str(data.get("nameWithOwner", ""))
    if resolved.lower() != slug.lower():
        raise PreflightError(
            f"Repository resolved as {resolved!r}, not {slug!r}."
        )
    if data.get("hasIssuesEnabled") is not True:
        raise PreflightError(
            f"Repository {resolved!r} does not have Issues enabled. GitHub "
            "mode tracks work in Issues; enable them under the repository "
            "Settings, then re-run this preflight."
        )
    return resolved


def parse_project_url(url: str) -> tuple[str, int]:
    match = PROJECT_URL_RE.match(url.strip())
    if not match:
        raise PreflightError(
            f"Project URL {url!r} is not a github.com org/user project URL "
            "(expected https://github.com/<orgs|users>/<owner>/projects/<n>). "
            "Enterprise hosts are not supported by this preflight."
        )
    return match["owner"], int(match["number"])


def check_project(owner: str, number: int) -> str:
    if not OWNER_RE.match(owner):
        raise PreflightError(
            f"Project owner {owner!r} is not a valid GitHub owner name "
            "(letters, digits, hyphens; at most 39 characters)."
        )
    result = run(
        ["gh", "project", "view", str(number), "--owner", owner, "--format", "json"]
    )
    if result.returncode != 0:
        raise PreflightError(
            f"Project #{number} under {owner!r} did not resolve (gh exit "
            f"{result.returncode}). Check the URL and that the account holds "
            "the project scope for the requested standalone CLI Project work."
        )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise PreflightError(
            f"Could not parse `gh project view` output for #{number}."
        ) from exc
    try:
        returned = int(data.get("number", number))
    except (TypeError, ValueError) as exc:
        raise PreflightError(
            f"Could not parse project number from `gh project view` output "
            f"for #{number}."
        ) from exc
    if returned != number:
        raise PreflightError(
            f"Project URL points to #{number} but gh returned #{returned}; "
            "check the URL and re-run."
        )
    title = str(data.get("title", ""))
    return f"#{returned} {title}".strip()


def check_status_field(owner: str, number: int, field: str) -> list[str]:
    result = run(
        ["gh", "project", "field-list", str(number), "--owner", owner,
         "--format", "json", "--limit", "100"]
    )
    if result.returncode != 0:
        raise PreflightError(
            f"Could not list fields of project #{number} (gh exit "
            f"{result.returncode}). The account may lack the project scope; "
            "re-run setup to refresh scopes."
        )
    try:
        fields = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise PreflightError(
            f"Could not parse `gh project field-list` output for #{number}."
        ) from exc
    if isinstance(fields, dict):
        # gh shapes vary by version: a bare list, or an object carrying the
        # list under "fields" (or "data"). Anything else fails clearly below.
        for key in ("fields", "data"):
            if isinstance(fields.get(key), list):
                fields = fields[key]
                break
    items = fields if isinstance(fields, list) else []
    names = [str(item.get("name", "")) for item in items]
    match = next((item for item in items
                  if str(item.get("name", "")).lower() == field.lower()), None)
    if match is None:
        seen = ", ".join(names) if names else "(no fields listed)"
        raise PreflightError(
            f"Project #{number} has no field named {field!r} (fields seen: "
            f"{seen}). Add a Status single-select field to the project, or "
            "pass --status-field to check a different field name."
        )
    if str(match.get("dataType", "")).lower() != "single_select":
        raise PreflightError(
            f"Project #{number} field {field!r} is not single-select "
            f"(dataType {match.get('dataType', '?')!r}). This helper checks "
            "single-select Status options; change the field type "
            "or pass --status-field for a single-select field."
        )
    options = [str(opt.get("name", "")) for opt in match.get("options", []) or []]
    if not options:
        raise PreflightError(
            f"Project #{number} field {field!r} lists no options yet; add the "
            "desired Project Status options, then re-run this standalone helper."
        )
    return options


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only standalone GitHub CLI Project preflight. "
                    "Changes nothing; exits nonzero with guidance on failure."
    )
    parser.add_argument("--owner", required=True, help="Repository owner (org or user).")
    parser.add_argument("--repo", required=True, help="Repository name.")
    parser.add_argument("--project-url", required=True,
                        help="GitHub Project URL (orgs/... or users/...). "
                             "Required for this standalone Project helper.")
    parser.add_argument("--hostname", default="github.com",
                        help="GitHub host. Only github.com is supported.")
    parser.add_argument("--min-version", default=DEFAULT_MIN_VERSION,
                        help="Minimum supported gh version "
                             f"(default {DEFAULT_MIN_VERSION}).")
    parser.add_argument("--status-field", default=DEFAULT_STATUS_FIELD,
                        help=f"Project field to require (default {DEFAULT_STATUS_FIELD}).")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.hostname != "github.com":
        print(f"Only github.com is supported, not {args.hostname!r}.",
              file=sys.stderr)
        return 1
    try:
        floor = parse_min_version(args.min_version)
        found = check_gh(floor)
        print(f"[ok] gh {'.'.join(str(p) for p in found)} on PATH")
        check_auth()
        print("[ok] gh authenticated (credential store untouched, nothing printed)")
        resolved = check_repo(args.owner, args.repo)
        print(f"[ok] repository resolves: {resolved}")
        project_owner, number = parse_project_url(args.project_url)
        summary = check_project(project_owner, number)
        print(f"[ok] project resolves: {summary}")
        options = check_status_field(project_owner, number, args.status_field)
        print(f"[ok] project field present: {args.status_field} (single-select)")
        print(f"[ok] status options: {', '.join(options)}")
    except PreflightError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 2
    print("Preflight passed. Nothing was created, modified, or stored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
