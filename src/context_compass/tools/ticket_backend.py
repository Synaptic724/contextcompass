"""Read the published work_tracking.backend YAML block without dependencies.

This is a conservative selector for local ticket-writing helpers, not a general
YAML parser. Literal block mappings and literal backend values are supported.
Aliases, merges, flow mappings, and ambiguous selectors stop the helper rather
than allowing a write under a guessed backend.
"""

from __future__ import annotations

import json
import pathlib
import re


class BackendConfigError(ValueError):
    """The helper cannot establish the configured ticket backend safely."""


_KEY = r"(?:[A-Za-z_][A-Za-z0-9_-]*|\"[A-Za-z_][A-Za-z0-9_-]*\"|'[A-Za-z_][A-Za-z0-9_-]*'|<<)"
_HEAD = re.compile(rf"^({_KEY}):(?:[ \t]+(.*)|$)")


def _head(body: str) -> tuple[str, str]:
    match = _HEAD.fullmatch(body)
    if match is None:
        raise BackendConfigError("Use literal YAML block mappings for the ticket selector.")
    key, value = match.groups()
    key = key.strip("\"'")
    if key == "<<":
        raise BackendConfigError("YAML merge keys cannot establish a literal ticket backend.")
    return key, value or ""


def backend_from_yaml(text: str) -> str:
    """Resolve local/plugin, refusing unsupported or contradictory selectors."""
    records = []
    started = finished = False
    for raw in text.lstrip("\ufeff").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[:len(raw) - len(raw.lstrip())]:
            raise BackendConfigError("YAML indentation must use spaces.")
        indent = len(raw) - len(raw.lstrip(" "))
        body = raw[indent:]
        if indent == 0 and body in ("---", "..."):
            if body == "---":
                if started or finished or records:
                    raise BackendConfigError("Use one YAML configuration document.")
                started = True
            else:
                if finished:
                    raise BackendConfigError("Use one YAML configuration document.")
                finished = True
            continue
        if finished:
            raise BackendConfigError("Content follows the YAML document end.")
        records.append((indent, body))

    roots = []
    keys = set()
    for index, (indent, body) in enumerate(records):
        if indent:
            continue
        key, value = _head(body)
        if key in keys:
            raise BackendConfigError("Duplicate top-level configuration key.")
        keys.add(key)
        roots.append((index, key, value))
    selected = next((root for root in roots if root[1] == "work_tracking"), None)
    if selected is None:
        if records and not roots:
            raise BackendConfigError("Configuration must be a top-level YAML mapping.")
        return "local"
    start, _, value = selected
    if value.strip() and not value.lstrip().startswith("#"):
        raise BackendConfigError("work_tracking must use the published YAML block format.")
    end = next((index for index, _, _ in roots if index > start), len(records))
    block = records[start + 1:end]
    if not block:
        return "local"
    child_indent = min(indent for indent, _ in block)
    values = []
    child_keys = set()
    for indent, body in block:
        if indent != child_indent:
            continue
        key, value = _head(body)
        if key in child_keys:
            raise BackendConfigError("Duplicate work_tracking key.")
        child_keys.add(key)
        if key == "backend":
            values.append(value)
    if not values:
        return "local"
    scalar = re.split(r"[ \t]+#", values[0], maxsplit=1)[0].strip()
    if scalar.startswith('"'):
        try:
            scalar = json.loads(scalar)
        except (ValueError, TypeError) as exc:
            raise BackendConfigError("backend must be a literal YAML value.") from exc
    elif scalar.startswith("'") and scalar.endswith("'") and len(scalar) >= 2:
        scalar = scalar[1:-1].replace("''", "'")
    if scalar == "files":
        return "local"
    if scalar not in ("local", "github_codex_plugin"):
        raise BackendConfigError("Select local or github_codex_plugin explicitly; legacy github is ambiguous.")
    return scalar


def read_backend(path: pathlib.Path) -> str:
    """Missing legacy config defaults local; unreadable or ambiguous config stops."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return "local"
    except (OSError, UnicodeError) as exc:
        raise BackendConfigError("Cannot read the ticket backend configuration.") from exc
    return backend_from_yaml(text)
