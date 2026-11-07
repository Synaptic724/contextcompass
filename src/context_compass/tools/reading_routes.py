"""Read the existing role dialect for reporting, not for agent authorization."""

from __future__ import annotations

import pathlib
import re
import json

from ticket_backend import BACKENDS, backend_from_yaml, BackendConfigError


class RouteError(ValueError):
    """A declaration cannot safely establish a reading route."""


GENERAL = "agent_onboarding/default/general/"
ENTRY = (
    "AGENTS.MD", "SKILLS.MD", "config/context_compass_config.yaml",
    GENERAL + "skills/execution_contract.md",
    GENERAL + "skills/work_tracking_backend.md",
    GENERAL + "skills/agent_communication_backend.md",
    GENERAL + "skills/agent_session_state.md",
    GENERAL + "skills/harness_custom_instructions.md",
)
TICKETS = BACKENDS
COMMUNICATIONS = ("mailbox", "codex_mcp")
EVENTS = ("onboard", "reonboard")
READING_MODES = ("lean", "full")
# Each heading prefix maps to every (dimension, value) pair that must hold.
# `boards` is derived from the ticket backend: only github_issues keeps the
# boards on GitHub; every other backend uses the local board files.
CONDITIONS = {
    "local backend": (("ticket", "local"),),
    "github codex plugin": (("ticket", "github_codex_plugin"),),
    "github issues backend": (("ticket", "github_issues"),),
    "local boards": (("boards", "local"),),
    "mailbox communication": (("communication", "mailbox"), ("boards", "local")),
    "codex mcp communication": (("communication", "codex_mcp"),),
}


def boards_for(ticket: str) -> str:
    """Where the boards live for a ticket backend: `github` or `local`."""
    return "github" if ticket == "github_issues" else "local"


def relative_path(root: pathlib.Path, value: str) -> str:
    value = value.replace("\\", "/")
    if (pathlib.PureWindowsPath(value).drive or value.startswith("/")
            or any(char in value for char in "*?[]")):
        raise RouteError(f"Use a literal Context Compass-relative path: {value}")
    target = (root / value).resolve()
    if not target.is_relative_to(root.resolve()):
        raise RouteError(f"Path leaves the selected Context Compass root: {value}")
    return target.relative_to(root.resolve()).as_posix()


def read_text(root: pathlib.Path, path: str) -> str:
    target = root / relative_path(root, path)
    if target.stat().st_size > 2 * 1024 * 1024:
        raise RouteError(f"Routing declaration exceeds the 2 MiB safety limit: {path}")
    return target.read_text(encoding="utf-8-sig")


def registry(root: pathlib.Path) -> dict:
    text = read_text(root, "SKILLS.MD")
    section = re.search(r"(?ms)^## Role registry\s*\n(.*?)(?=^## |\Z)", text)
    if not section:
        raise RouteError("SKILLS.MD has no Role registry section")
    result, paths = {}, set()
    first_line = text[:section.start(1)].count("\n") + 1
    for number, line in enumerate(section[1].splitlines(), first_line):
        if not re.match(r"^\|\s*`[^`]+`\s*\|", line):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            raise RouteError("Expected the six-column role registry contract")
        name, path, parent, user_defined, selectable, readme = cells
        path = relative_path(root, path)
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name) or name.casefold() in {x.casefold() for x in result}:
            raise RouteError(f"Invalid or duplicate registered role: {name}")
        if path.casefold() in paths:
            raise RouteError(f"Roles share an ambiguous skills entrypoint: {path}")
        if any(value not in ("yes", "no") for value in (user_defined, selectable, readme)):
            raise RouteError(f"Invalid registry flags for {name}")
        paths.add(path.casefold())
        result[name] = {"path": path, "parent": None if parent == "-" else parent,
                        "reads_readme": readme == "yes", "user_defined": user_defined == "yes",
                        "selectable_after_onboarding": selectable == "yes", "line": number}
    if not result:
        raise RouteError("The role registry is empty")
    return result


def heading(line: str):
    if not line or line.startswith(("-", " ", "|", "```")) or "`" in line:
        return None
    label = re.sub(r"^[# ]+", "", line).strip().strip("*").rstrip(":")
    explicit = line.startswith("#") or line.startswith("**") and line.endswith("**")
    if not explicit and any(mark in label for mark in ".,;"):
        return None
    lower = label.lower()
    state = None
    if lower.startswith("on-demand"):
        state = "on_demand"
    elif lower.startswith("self-directed"):
        state = "self_directed"
    elif len(label) < 120 and ("baseline" in lower or lower == "active skills"):
        state = "baseline"
    if state is None:
        return None
    condition = next((value for prefix, value in CONDITIONS.items() if lower.startswith(prefix)), None)
    if_exists = state == "baseline" and bool(re.search(
        r"\b(?:that exists|if present|when present|if available|when available)\b", lower))
    if state == "baseline" and condition is None and re.search(r"\b(backend|communication)\b", lower):
        raise RouteError(f"Unsupported conditional baseline: {label}")
    if state == "baseline" and condition is None and not if_exists and re.search(r"\b(if|when|unless)\b", lower):
        raise RouteError(f"Unsupported conditional baseline: {label}")
    return {"label": label, "state": state, "condition": condition,
            "if_exists": if_exists}


def manifest(root: pathlib.Path, path: str) -> dict:
    text = read_text(root, path)
    parents = re.findall(r"(?m)^- `INHERITS_SKILLS_FROM: ([^`]+)`\s*$", text)
    if len(parents) != 1:
        raise RouteError(f"Expected one inheritance header in {path}")
    entries, sections, current = [], [], None
    lines, fenced = text.splitlines(), False
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        boundary = (number == 1 or not lines[number - 2].strip() or line.startswith("#")
                    or line.startswith("**") and line.endswith("**")
                    or number < len(lines) and lines[number].startswith("- `"))
        new = heading(line) if boundary else None
        if new:
            current = dict(new, line=number, paths=[])
            sections.append(current)
            continue
        if current and current["state"] == "self_directed" and line.startswith("Every system document"):
            entries.append({"path": "system_docs/", "recursive": True, "source": path,
                            "line": number, "state": "self_directed", "section": current["label"],
                            "condition": None, "if_exists": True})
        if line.startswith("## "):
            current = None
        match = re.match(r"^- `([^`]+)`(?:\s.*)?$", line)
        if not match or match[1].startswith("INHERITS_SKILLS_FROM:"):
            continue
        value = match[1]
        if "/" not in value and "." not in value:
            continue
        if current is None:
            raise RouteError(f"Unclassified skill entry at {path}:{number}: {value}")
        entry = {"path": relative_path(root, value), "source": path, "line": number,
                 "state": current["state"], "section": current["label"],
                 "condition": current["condition"], "if_exists": current["if_exists"]}
        entries.append(entry)
        current["paths"].append(entry["path"])
    return {"parent": None if parents[0] == "none" else relative_path(root, parents[0]),
            "entries": entries, "sections": sections}


def chain(root: pathlib.Path, roles: dict, name: str) -> tuple[list[str], dict]:
    order, manifests, visiting = [], {}, set()

    def visit(role):
        if role not in roles:
            raise RouteError(f"Unregistered parent role: {role}")
        if role in visiting:
            raise RouteError(f"Role inheritance cycle at {role}")
        visiting.add(role)
        row = roles[role]
        value = manifest(root, row["path"])
        parent = row["parent"]
        expected = roles[parent]["path"] if parent in roles else None
        if parent and parent not in roles or value["parent"] != expected:
            raise RouteError(f"Registry and inheritance header disagree for {role}")
        if parent:
            visit(parent)
        visiting.remove(role)
        manifests[role] = value
        order.append(role)

    visit(name)
    return order, manifests


def configured_backends(root: pathlib.Path) -> tuple[str, str]:
    text = read_text(root, "config/context_compass_config.yaml")
    try:
        ticket = backend_from_yaml(text)
    except BackendConfigError as exc:
        raise RouteError(f"Cannot resolve configured backends: {exc}") from exc
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if re.match(
        r"^(?:agent_communication|'agent_communication'|\"agent_communication\"):", line)), None)
    if start is None:
        return ticket, "mailbox"
    if not re.fullmatch(r"(?:agent_communication|'agent_communication'|\"agent_communication\"):\s*(?:#.*)?", lines[start]):
        raise RouteError("agent_communication must use a literal block mapping")
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].strip() and not lines[i][0].isspace() and not lines[i].startswith("#")), len(lines))
    block = [line for line in lines[start + 1:end] if line.strip() and not line.lstrip().startswith("#")]
    if any("\t" in line[:len(line) - len(line.lstrip())] or line.lstrip().startswith("<<:") for line in block):
        raise RouteError("Unsupported communication mapping indentation or YAML merge")
    indent = min((len(line) - len(line.lstrip()) for line in block), default=0)
    selectors = []
    for line in block:
        if len(line) - len(line.lstrip()) == indent:
            match = re.fullmatch(r"\s*(?:backend|'backend'|\"backend\"):\s*(.*?)\s*", line)
            if match:
                selectors.append(re.split(r"\s+#", match[1], maxsplit=1)[0].strip())
    if len(selectors) > 1:
        raise RouteError("Duplicate agent_communication.backend selector")
    value = selectors[0] if selectors else "mailbox"
    if value.startswith('"'):
        try:
            value = json.loads(value)
        except ValueError as exc:
            raise RouteError("Communication backend must be a literal string") from exc
    elif value.startswith("'") and value.endswith("'"):
        value = value[1:-1].replace("''", "'")
    if value not in COMMUNICATIONS:
        raise RouteError("Select mailbox or codex_mcp explicitly")
    return ticket, value


def configured_reading_mode(root: pathlib.Path) -> str:
    """Return `reading.mode` from config: `lean` (also when absent) or `full`."""
    lines = read_text(root, "config/context_compass_config.yaml").splitlines()
    start = next((i for i, line in enumerate(lines)
                  if re.match(r"^(?:reading|'reading'|\"reading\"):", line)), None)
    if start is None:
        return "lean"
    if not re.fullmatch(r"(?:reading|'reading'|\"reading\"):\s*(?:#.*)?", lines[start]):
        raise RouteError("reading must use a literal block mapping")
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].strip() and not lines[i][0].isspace() and not lines[i].startswith("#")), len(lines))
    block = [line for line in lines[start + 1:end] if line.strip() and not line.lstrip().startswith("#")]
    indent = min((len(line) - len(line.lstrip()) for line in block), default=0)
    values = []
    for line in block:
        match = re.fullmatch(r"\s*(?:mode|'mode'|\"mode\"):\s*(.*?)\s*", line)
        if match and len(line) - len(line.lstrip()) == indent:
            values.append(re.split(r"\s+#", match[1], maxsplit=1)[0].strip().strip("'\""))
    if len(values) > 1:
        raise RouteError("Duplicate reading.mode selector")
    value = values[0] if values else "lean"
    if value not in READING_MODES:
        raise RouteError("Select reading.mode lean or full explicitly")
    return value


def requirements(root, roles, name, ticket, communication, event, special_paths, resolved=None,
                 reading_mode="lean"):
    if reading_mode not in READING_MODES:
        raise RouteError(f"Unsupported reading mode: {reading_mode}")
    order, manifests = resolved or chain(root, roles, name)
    entry_text = read_text(root, "AGENTS.MD")
    def locate(label):
        return next((i for i, line in enumerate(entry_text.splitlines(), 1) if line.startswith(label)), None)
    required = [{"path": path, "reason": "Runtime entrypoint", "source": "AGENTS.MD",
                 "line": locate("## Onboarding Gate"), "state": "baseline", "if_exists": False} for path in ENTRY]
    if event == "reonboard":
        required.append({"path": GENERAL + "skills/compaction_requirements.md",
                         "reason": "Recovery entrypoint", "source": "AGENTS.MD", "line": locate("## Compaction Directive"),
                         "state": "baseline", "if_exists": False})
    required += [{"path": path, "reason": "Project special instructions", "source": "AGENTS.MD",
                  "line": locate("## Project Instructions Bootstrap"), "state": "baseline", "if_exists": False} for path in special_paths]
    boards = boards_for(ticket)
    if boards == "local":
        required.append({"path": "mailbox_board.md", "reason": "Shared session state; relevant Notes/messages remain session-specific",
                         "source": GENERAL + "skills/agent_session_state.md", "line": 9,
                         "state": "baseline", "if_exists": False})
    selected = {"ticket": ticket, "communication": communication, "boards": boards}
    optional, sections = [], []
    for role in order:
        row, value = roles[role], manifests[role]
        required.append({"path": row["path"], "reason": f"Role manifest: {role}",
                         "source": "SKILLS.MD", "line": row["line"], "state": "baseline", "if_exists": False})
        if row["reads_readme"]:
            required.append({"path": str(pathlib.PurePosixPath(row["path"]).parent / "README.md"),
                             "reason": f"Registry README policy: {role}", "source": "SKILLS.MD",
                             "line": row["line"], "state": "baseline", "if_exists": False})
        sections += [dict(section, source=row["path"]) for section in value["sections"]
                     if section["state"] != "baseline"]
        for entry in value["entries"]:
            condition = entry.get("condition")
            if condition and any(selected[dimension] != value for dimension, value in condition):
                continue
            entry = dict(entry, reason=f"{role}: {entry['section']}")
            eager = entry["state"] == "baseline" or (reading_mode == "full" and entry["state"] == "on_demand")
            if eager and entry["state"] == "on_demand":
                entry["reason"] += " (reading.mode full)"
            (required if eager else optional).append(entry)
    return {"role_chain": order, "required": required, "optional": optional,
            "optional_sections": sections}
