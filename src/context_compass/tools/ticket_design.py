#!/usr/bin/env python3
"""New-ticket design helpers. Pure transitions, explicit new-file output, no hosting writes."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys

from ticket_backend import read_backend


class ContractError(ValueError):
    """Declared ticket content cannot establish the selected contract safely."""


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ContractError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _json(text):
    try:
        return json.loads(text, object_pairs_hook=_pairs)
    except (ValueError, TypeError) as exc:
        raise ContractError(f"Invalid contract JSON: {exc}") from exc


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def definition(root: pathlib.Path) -> tuple[dict, str]:
    text = (root / "templates/ticket_contract.json").read_text(encoding="utf-8")
    spec = _json(text)
    if spec.get("format_version") != 1:
        raise ContractError("Unsupported canonical contract format.")
    return spec, "sha256:" + digest(text)


def _mapping_block(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if re.match(rf"^{re.escape(key)}:", line)]
    if len(matches) > 1:
        raise ContractError(f"Duplicate YAML block: {key}")
    if not matches:
        return []
    start = matches[0]
    if re.sub(r"\s+#.*$", "", lines[start]).strip() != key + ":":
        raise ContractError(f"Use a literal block mapping for {key}.")
    end = next((i for i in range(start + 1, len(lines))
                if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", lines[i])), len(lines))
    block = lines[start + 1:end]
    if any("\t" in line[:len(line) - len(line.lstrip())] for line in block):
        raise ContractError("YAML indentation must use spaces.")
    return block


def settings(root: pathlib.Path) -> tuple[dict[str, str], int]:
    text = (root / "config/context_compass_config.yaml").read_text(encoding="utf-8-sig")
    paths = {kind: f"templates/{kind}_template.md" for kind in ("epic", "story", "task")}
    block = _mapping_block(text, "ticket_design")
    selectors = [i for i, line in enumerate(block) if re.match(r"^  templates:", line)]
    if any(re.match(r"^\s+templates:", line) and not re.match(r"^  templates:", line) for line in block):
        raise ContractError("Use the documented two-space templates selector; do not guess a design.")
    if len(selectors) > 1:
        raise ContractError("Duplicate templates selector.")
    if selectors:
        start = selectors[0]
        if block[start].split("#", 1)[0].strip() != "templates:":
            raise ContractError("Use literal template-path mappings.")
        seen = set()
        for line in block[start + 1:]:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if not line.startswith("    "):
                break
            match = re.fullmatch(r"    (epic|story|task):[ \t]+(.*)", line)
            if not match or match[1] in seen:
                raise ContractError("Unsupported or duplicate ticket template selector.")
            seen.add(match[1])
            value = re.split(r"[ \t]+#", match[2], maxsplit=1)[0].strip()
            if value.startswith('"'):
                value = _json(value)
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1].replace("''", "'")
            if not isinstance(value, str) or not value or value[0] in "&*!{|>":
                raise ContractError("Template paths must be literal relative strings.")
            paths[match[1]] = value
    workflow = "\n".join(_mapping_block(text, "workflow"))
    scores = re.findall(r"(?m)^    minimum_note_score:[ \t]+(\d+)(?:[ \t]+#.*)?$", workflow)
    if len(scores) != 1 or not 0 <= int(scores[0]) <= 10:
        raise ContractError("An explicit note-quality binding from 0 to 10 is required.")
    return paths, int(scores[0])


def template_path(root: pathlib.Path, kind: str) -> pathlib.Path:
    paths, _ = settings(root)
    if kind not in paths:
        raise ContractError("Select epic, story or task.")
    value = paths[kind].replace("\\", "/")
    if pathlib.PureWindowsPath(value).drive or pathlib.PurePosixPath(value).is_absolute():
        raise ContractError("Template paths must be context-compass-relative.")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ContractError("Template path leaves the Context Compass root.")
    if not path.is_file():
        raise ContractError(f"Template is unavailable: {value}")
    return path


def design_instructions(root: pathlib.Path) -> str:
    text = (root / "config/context_compass_config.yaml").read_text(encoding="utf-8-sig")
    block = _mapping_block(text, "ticket_design")
    matches = [i for i, line in enumerate(block) if re.match(r"^  instructions:", line)]
    if len(matches) > 1:
        raise ContractError("Duplicate design instructions.")
    if not matches:
        return ""
    start = matches[0]
    value = block[start].split(":", 1)[1].strip()
    if value in (">", "|", ">-", "|-"):
        lines = []
        for line in block[start + 1:]:
            if line.strip() and not line.startswith("    "):
                break
            lines.append(line[4:] if line.startswith("    ") else "")
        return ("\n" if value.startswith("|") else " ").join(lines).strip()
    if value.startswith('"'):
        value = _json(value)
    elif value.startswith("'") and value.endswith("'"):
        value = value[1:-1].replace("''", "'")
    if not isinstance(value, str) or value.startswith(("&", "*", "!", "{", "[")):
        raise ContractError("Use literal design instructions.")
    return value


def _known(value) -> bool:
    return (isinstance(value, str) and bool(value.strip()) and not value.startswith("<")
            and value.strip().lower() not in {"unknown", "unassigned", "none", ""})


def _named(value) -> bool:
    return _known(value) and not re.fullmatch(
        r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", value)


def _section(text: str, heading: str) -> tuple[int, int]:
    matches = list(re.finditer(rf"(?m)^## {re.escape(heading)}[ \t]*$", text))
    if len(matches) != 1:
        raise ContractError(f"Expected one complete {heading} section.")
    start = matches[0].end()
    next_heading = re.search(r"(?m)^## ", text[start:])
    return start, start + next_heading.start() if next_heading else len(text)


def _fields(text: str) -> dict[str, str]:
    pairs = re.findall(r"(?m)^[ \t]*(?:- )?([A-Z][A-Z_0-9]*):[ \t]*(.*)$", text)
    return _pairs(pairs)


def validate_note(root: pathlib.Path, note: str) -> dict[str, str]:
    spec, _ = definition(root)
    fields = _fields(note)
    if any(key not in fields for key in spec["note_fields"]):
        raise ContractError("A complete named, structured Note is required.")
    if (not _named(fields["AUTHOR"])
            or not all(_known(fields[key]) for key in ("AUTHOR_ROLE", "CLAIM", "IMPACT", "NEXT"))):
        raise ContractError("Note author, role and content must be explicit.")
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", fields["DATETIME"]):
        raise ContractError("Note DATETIME must be UTC ISO-8601.")
    try:
        datetime.datetime.fromisoformat(fields["DATETIME"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError("Note DATETIME is not a real UTC date/time.") from exc
    contract = (root / "agent_onboarding/default/general/skills/execution_contract.md").read_text(
        encoding="utf-8")
    types_section = contract.split("## 9) Type Schema Contract", 1)[1].split("## 10)", 1)[0]
    types = set(re.findall(r"(?m)^- ([A-Z_]+)$", types_section))
    if fields["TYPE"] not in types or fields["REREAD"] not in ("REQUIRED", "HELPFUL"):
        raise ContractError("Unsupported Note type or reread value.")
    score = fields["SCORE_0_TO_10"]
    if not score.isdigit() or not settings(root)[1] <= int(score) <= 10:
        raise ContractError("Note does not meet the configured quality threshold.")
    if ((fields["EVIDENCE"] and not _known(fields["EVIDENCE"]))
            or not fields["EVIDENCE"] and not re.search(r"(?m)^[ \t]+- \S", note)):
        raise ContractError("Note evidence cannot be empty.")
    return fields


def _notes(root: pathlib.Path, text: str) -> dict[str, str]:
    start, end = _section(text, "Notes")
    parts = re.split(r"(?m)(?=^- DATETIME:)", text[start:end])
    result = {}
    for note in parts:
        if not note.startswith("- DATETIME:"):
            continue
        fields = validate_note(root, note)
        key = fields.get("EVENT_ID", fields["DATETIME"])
        if key in result:
            raise ContractError("Duplicate Note/event identity.")
        result[key] = note.strip()
    return result


def _region(text: str) -> tuple[int, int]:
    begin = "<!-- BEGIN USER-DEFINED: project_fields -->"
    end = "<!-- END USER-DEFINED: project_fields -->"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ContractError("One intact project_fields region is required.")
    start, stop = text.index(begin) + len(begin), text.index(end)
    if stop < start:
        raise ContractError("Reversed project_fields markers.")
    return start, stop


def _block(text: str, name: str):
    start, end = _region(text)
    pattern = rf"(?ms)^<!-- BEGIN {name} -->\n```json\n(.*?)\n```\n<!-- END {name} -->"
    matches = list(re.finditer(pattern, text[start:end]))
    if len(matches) > 1:
        raise ContractError(f"Duplicate {name} authority.")
    markers = text[start:end].count(f"<!-- BEGIN {name} -->")
    if markers != len(matches) or text[start:end].count(f"<!-- END {name} -->") != len(matches):
        raise ContractError(f"Malformed {name} block.")
    return (_json(matches[0][1]), start + matches[0].start(), start + matches[0].end()) if matches else None


def _encoded(name: str, data: dict) -> str:
    return f"<!-- BEGIN {name} -->\n```json\n{json.dumps(data, indent=2)}\n```\n<!-- END {name} -->"


def _put(text: str, name: str, data: dict) -> str:
    current = _block(text, name)
    encoded = _encoded(name, data)
    if current:
        return text[:current[1]] + encoded + text[current[2]:]
    _, end = _region(text)
    return text[:end] + encoded + "\n" + text[end:]


def validate_attribution(root: pathlib.Path, data: dict) -> None:
    spec, _ = definition(root)
    if not isinstance(data, dict) or set(data) != {"authors", "published_by", "reviews"}:
        raise ContractError("Attribution needs authors, published_by and reviews.")
    if not isinstance(data["authors"], list) or not isinstance(data["reviews"], list):
        raise ContractError("Authors and reviews must be lists.")
    publisher = data["published_by"]
    if not isinstance(publisher, dict) or set(publisher) != set(spec["publisher_fields"]):
        raise ContractError("Publisher must have explicit service/account/receipt fields.")
    if not all(isinstance(value, str) for value in publisher.values()):
        raise ContractError("Publisher fields are strings; UNKNOWN is explicit.")
    for author in data["authors"]:
        if (not isinstance(author, dict) or set(author) != set(spec["author_fields"])
                or not all(_known(value) for key, value in author.items() if key not in ("actor", "role"))
                or not (_named(author["actor"]) or author["actor"] == "UNKNOWN")
                or not (_known(author["role"]) or author["role"] == "UNKNOWN")
                or author["kind"] not in spec["contribution_kinds"]):
            raise ContractError("Contribution authors need actor, role, kind, scope, revision and evidence.")
    for review in data["reviews"]:
        if (not isinstance(review, dict) or set(review) != set(spec["review_fields"])
                or type(review["independent"]) is not bool
                or not all(_known(value) for key, value in review.items() if key not in ("independent", "verdict"))
                or not _named(review["actor"])
                or review["verdict"] not in spec["review_verdicts"]):
            raise ContractError("Review must identify its exact actor, role, target and evidence.")
        if review["independent"] and any(
                author["actor"] in (review["actor"], "UNKNOWN") and author["scope"] == review["scope"]
                and author["revision"] == review["target_revision"] for author in data["authors"]):
            raise ContractError("An author/material editor cannot independently review that target.")


def future_status(metadata: dict) -> str:
    return " / ".join(metadata[key] for key in ("phase", "execution", "resolution"))


def _attribution_view(root: pathlib.Path, data: dict) -> str:
    labels = definition(root)[0]["attribution_labels"]
    return "\n" + "\n".join(f"- {labels[key]}: {json.dumps(data[key], sort_keys=True)}"
                              for key in ("authors", "published_by", "reviews")) + "\n\n"


def validate_ticket(root: pathlib.Path, text: str, kind: str) -> dict | None:
    canonical = (root / f"templates/{kind}_template.md").read_text(encoding="utf-8")
    for heading in re.findall(r"(?m)^## (.+)$", canonical):
        _section(text, heading)
    start, end = _section(text, "Metadata")
    header = text[start:end]
    for label in ("Owner", "Agent Name", "Agent Role", "Priority", "Created", "Updated", "Status"):
        if len(re.findall(rf"(?m)^- {label}:.*$", header)) != 1:
            raise ContractError(f"Expected one explicit {label} metadata field.")
    ids = re.findall(rf"(?m)^- {kind.title()} ID: (\S+)[ \t]*$", header)
    if len(ids) != 1 or not re.fullmatch(rf"{kind.upper()}-\d{{4}}-\d\d-\d\d-[A-Za-z0-9_-]+", ids[0]):
        raise ContractError("An immutable, type-correct ticket ID is required.")
    spec, ref = definition(root)
    attribution = _block(text, "TICKET_ATTRIBUTION")
    if attribution:
        validate_attribution(root, attribution[0])
        view_start, view_end = _section(text, "Contribution Attribution")
        if text[view_start:view_end] != _attribution_view(root, attribution[0]):
            raise ContractError("Attribution labels are derived; reconcile the conflicting readable view.")
    notes = _notes(root, text)
    if not notes:
        raise ContractError("New-format tickets need a named, complete body Note.")
    selected = _block(text, "AGILE_METADATA")
    if selected is None:
        return None
    data = selected[0]
    if not isinstance(data, dict) or not set(spec["metadata_fields"]) <= set(data):
        raise ContractError("Incomplete Agile metadata.")
    if set(data) - set(spec["metadata_fields"] + spec["optional_metadata_fields"]):
        raise ContractError("Unsupported required metadata semantics.")
    if (type(data["schema_version"]) is not int or data["schema_version"] != spec["schema_version"]
            or not isinstance(data["profile"], dict) or data["profile"] != spec["profile"]
            or type(data["profile"].get("version")) is not int
            or data["contract_ref"] != ref or data["ticket_id"] != ids[0]):
        raise ContractError("Unsupported profile/schema/source or mismatched ticket identity.")
    if type(data["revision"]) is not int or data["revision"] < 1 or not _known(data["last_event_id"]):
        raise ContractError("Revision and logical event identity must be explicit.")
    for key in ("phase", "execution", "resolution"):
        if data[key] not in spec[key + "s" if key == "phase" else key]:
            raise ContractError(f"Unsupported {key}.")
    if data["resolution"] != "unresolved" and data["execution"] != spec["terminal_execution"]:
        raise ContractError("Terminal resolution cannot be active, ready, blocked or paused.")
    if data["resolution"] == "accepted" and any(data[key] != value for key, value in spec["accepted_state"].items()):
        raise ContractError("Accepted work must be idle in acceptance phase.")
    if data["execution"] in ("ready", "active"):
        for label in ("Owner", "Agent Name", "Agent Role"):
            values = re.findall(rf"(?m)^- {label}: (.*)$", header)
            if (len(values) != 1 or not _known(values[0])
                    or label == "Agent Name" and not all(_named(value.strip()) for value in values[0].split(","))):
                raise ContractError("Ready/active needs actual accountable owner and named executor/role.")
    evidence = data["evidence_refs"]
    if not isinstance(evidence, dict) or any(not _known(value) or value not in notes for value in evidence.values()):
        raise ContractError("Evidence refs must resolve to actual complete body Notes.")
    required = (spec["evidence_requirements"]["all"]
                + spec["evidence_requirements"].get(data["execution"], [])
                + spec["evidence_requirements"].get(data["resolution"], []))
    if any(key not in evidence for key in required) or data["last_event_id"] not in notes:
        raise ContractError("The state needs its event and applicable evidence references.")
    if any(_fields(notes[evidence[key]])["TYPE"] in ("UNKNOWN", "HYPOTHESIS") for key in required):
        raise ContractError("Unresolved evidence cannot authorize a workflow state.")
    if data["resolution"] == "accepted":
        for key, required_fields in spec["accepted_note_fields"].items():
            recorded = _fields(notes[evidence[key]])
            if any(recorded.get(field) != value for field, value in required_fields.items()):
                raise ContractError("Acceptance requires explicit gate conclusions, not inferred closure or tests.")
    skipped = data.get("skipped_phases", [])
    if not isinstance(skipped, list):
        raise ContractError("Skipped phases must be explicit scoped decisions.")
    seen = set()
    for skip in skipped:
        if (not isinstance(skip, dict) or set(skip) != {"phase", "reason_ref"}
                or skip["phase"] not in spec["phases"] or skip["phase"] in seen
                or skip["phase"] == data["phase"] or not _known(skip["reason_ref"])
                or skip["reason_ref"] not in notes):
            raise ContractError("A skipped phase needs unique phase and body decision evidence.")
        seen.add(skip["phase"])
    if "extensions" in data and not isinstance(data["extensions"], dict):
        raise ContractError("Informational extensions must be an object.")
    statuses = re.findall(r"(?m)^- Status: (.*)$", header)
    if statuses != [future_status(data)]:
        raise ContractError("Status is derived from metadata; reconcile the conflicting view.")
    return data


def initial_metadata(root: pathlib.Path, ticket_id: str, event_id: str) -> dict:
    spec, ref = definition(root)
    return {"schema_version": spec["schema_version"], "profile": spec["profile"],
            "ticket_id": ticket_id, "revision": 1, "phase": "planning", "execution": "draft",
            "resolution": "unresolved", "last_event_id": event_id, "contract_ref": ref,
            "evidence_refs": {"transition": event_id}}


def render_new(root: pathlib.Path, kind: str, ticket_id: str, title: str, owner: str,
               agent_name: str, role: str, note: str, metadata: dict | None = None,
               attribution: dict | None = None) -> str:
    fields = validate_note(root, note)
    if not _known(title) or "\n" in title or "\r" in title:
        raise ContractError("A single explicit ticket title is required.")
    text = template_path(root, kind).read_text(encoding="utf-8")
    text = re.sub(rf"(?m)^# {kind.title()}:.*$", lambda _: f"# {kind.title()}: {title}", text, count=1)
    if metadata is not None and (not isinstance(metadata, dict)
            or not {"revision", "phase", "execution", "resolution"} <= set(metadata)):
        raise ContractError("Incomplete new-ticket metadata.")
    values = {kind.title() + " ID": ticket_id, "Owner": owner, "Agent Name": agent_name,
              "Agent Role": role, "Created": fields["DATETIME"], "Updated": fields["DATETIME"],
              "Status": future_status(metadata) if metadata is not None else "draft"}
    for label, value in values.items():
        text, count = re.subn(rf"(?m)^- {re.escape(label)}:.*$", lambda _: f"- {label}: {value}", text, count=1)
        if count != 1 or "\n" in value or "\r" in value:
            raise ContractError(f"Missing or invalid template field: {label}")
    start, end = _section(text, "Notes")
    text = text[:start] + "\n" + note.strip() + "\n\n" + text[end:]
    if metadata is not None:
        if not isinstance(metadata, dict) or not {"revision", "execution", "resolution"} <= set(metadata):
            raise ContractError("Incomplete new-ticket metadata.")
        if (metadata["revision"], metadata["execution"], metadata["resolution"]) != (1, "draft", "unresolved"):
            raise ContractError("New tickets start draft/unresolved at revision 1.")
        text = _put(text, "AGILE_METADATA", metadata)
        start, end = _section(text, "State Transition Event")
        text = (text[:start] + "\n- from_state: none (new ticket)\n- to_state: " + future_status(metadata)
                + "\n- transition_reason: " + metadata["last_event_id"] + "\n\n" + text[end:])
    if attribution is not None:
        text = _put(text, "TICKET_ATTRIBUTION", attribution)
        start, end = _section(text, "Contribution Attribution")
        text = text[:start] + _attribution_view(root, attribution) + text[end:]
    validate_ticket(root, text, kind)
    return text


def transition(root: pathlib.Path, text: str, kind: str, metadata: dict, note: str,
               expected_revision: int, expected_hash: str) -> str:
    current = validate_ticket(root, text, kind)
    if current is None:
        raise ContractError("This helper transitions only the explicit new Agile contract.")
    if digest(text) != expected_hash or current["revision"] != expected_revision:
        raise ContractError("Stale full-body revision/hash; reconcile the current writer's content.")
    fields = validate_note(root, note)
    event = fields.get("EVENT_ID")
    if not _known(event) or event != metadata["last_event_id"]:
        raise ContractError("Transition Note and metadata need the same logical event.")
    history = _notes(root, text)
    if event in history:
        validate_ticket(root, _put(text, "AGILE_METADATA", metadata), kind)
        if metadata == current and history[event] == note.strip():
            return text
        raise ContractError("Conflicting duplicate event payload.")
    if metadata["revision"] != expected_revision + 1 or metadata["ticket_id"] != current["ticket_id"]:
        raise ContractError("Revision must advance once; ticket identity is immutable.")
    if metadata["execution"] in ("paused", "blocked") and metadata["phase"] != current["phase"]:
        raise ContractError("Pause/block retains the current phase.")
    result = _put(text, "AGILE_METADATA", metadata)
    start, end = _section(result, "Metadata")
    header = re.sub(r"(?m)^- Status:.*$", lambda _: "- Status: " + future_status(metadata), result[start:end])
    header = re.sub(r"(?m)^- Updated:.*$", lambda _: "- Updated: " + fields["DATETIME"], header)
    result = result[:start] + header + result[end:]
    start, end = _section(result, "State Transition Event")
    event_view = (f"\n- from_state: {future_status(current)}\n- to_state: {future_status(metadata)}\n"
                  f"- transition_reason: {metadata['evidence_refs'].get('transition', 'UNKNOWN')}\n\n")
    result = result[:start] + event_view + result[end:]
    _, end = _section(result, "Notes")
    result = result[:end].rstrip() + "\n\n" + note.strip() + "\n\n" + result[end:]
    validate_ticket(root, result, kind)
    return result


def native_projection(root: pathlib.Path, text: str, kind: str, observed_state: str) -> dict[str, str]:
    metadata = validate_ticket(root, text, kind)
    if metadata is None or observed_state not in ("open", "closed"):
        raise ContractError("Projection needs a validated Agile ticket and actual open/closed state.")
    resolution = metadata["resolution"]
    if resolution == "unresolved":
        return {"state": "open", "result": "consistent" if observed_state == "open" else "discrepancy"}
    return {"state": "closed", "state_reason": "completed" if resolution == "accepted" else "not_planned",
            "result": "consistent" if observed_state == "closed" else "projection_pending"}


def bundle(root: pathlib.Path, kind: str, backend: str) -> str:
    root = root.resolve()
    if backend not in ("local", "github_codex_plugin"):
        raise ContractError("Select an explicit supported host backend.")
    sources = [root / "templates/ticket_contract.json", template_path(root, kind)]
    general = root / "agent_onboarding/default/general/skills"
    sources += [general / "ticket_design.md", general / "agent_identity.md",
                general / "execution_contract.md", general / "ticketing.md"]
    sources += ([general / "github/workflow.md", general / "github/codex_plugin.md"]
                if backend == "github_codex_plugin" else [general / "ticketing_skill_contract.md"])
    binding = {"binding_version": 1, "backend": backend, "minimum_note_score": settings(root)[1],
               "design_instructions": design_instructions(root)}
    parts = ["# Source-Derived Ticket Contract\n\nNot an onboarding receipt or publication grant.\n",
             "## Host Binding\n\n```json\n" + json.dumps(binding, indent=2) + "\n```\n"]
    for path in sources:
        content = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        parts += [f"\n<!-- SOURCE: {relative}; sha256: {digest(content)} -->\n", content, "\n"]
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate")
    check.add_argument("--kind", required=True, choices=("epic", "story", "task"))
    check.add_argument("--ticket", required=True, type=pathlib.Path)
    delivery = sub.add_parser("bundle")
    delivery.add_argument("--kind", required=True, choices=("epic", "story", "task"))
    delivery.add_argument("--backend", choices=("local", "github_codex_plugin"))
    delivery.add_argument("--out", required=True, type=pathlib.Path)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            validate_ticket(args.root, args.ticket.read_text(encoding="utf-8"), args.kind)
            print("OK: declared ticket contract validates; evidence truth/authorization remain separate.")
        else:
            text = bundle(args.root, args.kind, args.backend or read_backend(args.root / "config/context_compass_config.yaml"))
            with args.out.open("x", encoding="utf-8", newline="\n") as output:
                output.write(text)
            print(f"WROTE: {args.out}")
    except (ContractError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
