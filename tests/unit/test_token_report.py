"""Declared routing, accounting and read-only boundaries for token reports."""

import json
from pathlib import Path

import pytest

from conftest import PKG_ROOT, write
from reading_routes import (ENTRY, GENERAL, RouteError, chain, configured_backends, configured_reading_mode,
                            heading, manifest, registry)
from token_report import Inventory, build_report, markdown, write_report

pytestmark = pytest.mark.unit


def fake_count(text):
    return len(text.split())


@pytest.fixture
def report_root(tmp_path):
    root = tmp_path / "context_compass"
    for path in ENTRY:
        write(root / path, "Entry policy.\n")
    rows = ["## Role registry", "", "| role | skills path | extends | user-defined | selectable after onboarding | reads README |",
            "| --- | --- | --- | --- | --- | --- |"]
    for name, parent in (("general", "-"), ("engineer", "general"), ("custom_role", "engineer")):
        rows.append(f"| `{name}` | `roles/{name}/SKILLS.MD` | `{parent}` | no | yes | no |")
    write(root / "SKILLS.MD", "\n".join(rows) + "\n")
    write(root / "config/context_compass_config.yaml",
          "work_tracking:\n  backend: local\nagent_communication:\n  backend: mailbox\n")
    write(root / "roles/general/SKILLS.MD", """# General
- `INHERITS_SKILLS_FROM: none`

Shared baseline skills
- `shared.md`
- `attention_board.md`

Local backend baseline
Read these paths when selected.
- `local.md`

GitHub Codex plugin baseline
- `github.md`

Mailbox communication baseline
- `mailbox.md`

Codex MCP communication baseline
- `mcp.md`

On-demand topic skills
Read only when triggered. Not part of the baseline.
- `optional.md`
""")
    write(root / "roles/engineer/SKILLS.MD", """# Engineer
- `INHERITS_SKILLS_FROM: roles/general/SKILLS.MD`

Required baseline skills
- `shared.md`

Baseline system orientation (read every one that exists)
- `system_docs/architecture.md`

Self-directed system reading
- `system_docs/component.md`
""")
    write(root / "roles/custom_role/SKILLS.MD", """# Custom
- `INHERITS_SKILLS_FROM: roles/engineer/SKILLS.MD`

My baseline contracts
- `custom.md`
""")
    for name in ("shared", "local", "github", "mailbox", "mcp", "optional", "custom"):
        write(root / f"{name}.md", f"{name} policy.\n")
    write(root / (GENERAL + "skills/mailbox_protocol.md"), "Mailbox transport.\n")
    write(root / (GENERAL + "skills/codex_mcp.md"), "MCP transport.\n")
    write(root / (GENERAL + "skills/compaction_requirements.md"), "Recovery policy.\n")
    write(root / "system_docs/component.md", "Component reference.\n")
    write(root / "special_instructions/nested/custom.md", "Project-specific instruction.\n")
    write(root / "mailbox_board.md", "# Mailbox\n## Checked-In Agents\nRoster rows.\n"
          "## Messages\n" + "MESSAGE_PAYLOAD " * 1000 + "\n## Notes\nSESSION_NOTE.\n")
    write(root / "attention_board.md", "# Board\n## Message Alerts\n" + "ALERT " * 100 +
          "\n## Active Items\nCurrent work.\n")
    return root


def selected(report):
    return next(r for r in report["routes"] if r["id"] == report["selected_route"])


def test_all_route_choices_and_inheritance_deduplication(report_root):
    report = build_report(report_root, fake_count, role="custom_role")
    assert len(report["routes"]) == 3 * 2 * 2 * 2
    route = selected(report)
    assert route["role_chain"] == ["general", "engineer", "custom_role"]
    paths = [p["path"] for p in route["paths"]]
    assert paths.count("shared.md") == 1
    assert "special_instructions/nested/custom.md" in paths
    assert "system_docs/architecture.md" not in paths
    assert "optional.md" not in paths and "system_docs/component.md" not in paths
    assert {p["state"] for p in route["optional_paths"]} == {"on_demand", "self_directed"}


@pytest.mark.parametrize("ticket,transport", [("local", "mailbox"), ("local", "codex_mcp"),
                                             ("github_codex_plugin", "mailbox"), ("github_codex_plugin", "codex_mcp")])
def test_inactive_backend_documents_are_not_charged(report_root, ticket, transport):
    route = selected(build_report(report_root, fake_count, role="engineer", ticket=ticket, communication=transport))
    paths = {p["path"] for p in route["paths"]}
    assert ("local.md" in paths) == (ticket == "local")
    assert ("github.md" in paths) == (ticket == "github_codex_plugin")
    assert ("mailbox.md" in paths) == (transport == "mailbox")
    assert ("mcp.md" in paths) == (transport == "codex_mcp")


def test_partial_mailbox_and_mcp_alert_scope_are_visible(report_root):
    report = build_report(report_root, fake_count, role="engineer", communication="codex_mcp")
    route = selected(report)
    mailbox = next(p for p in route["paths"] if p["path"] == "mailbox_board.md")
    assert mailbox["known_tokens"] < mailbox["full_file_tokens"]
    assert mailbox["unresolved"] == "Relevant session Notes"
    attention = next(p for p in route["paths"] if p["path"] == "attention_board.md")
    assert attention["known_tokens"] < attention["full_file_tokens"]
    assert "MESSAGE_PAYLOAD" not in json.dumps(report)
    assert "lower bounds" in markdown(report)


def test_recovery_adds_its_entry_read_once(report_root):
    report = build_report(report_root, fake_count, role="general", event="reonboard")
    paths = [p["path"] for p in selected(report)["paths"]]
    assert paths.count(GENERAL + "skills/compaction_requirements.md") == 1


def test_lean_reads_lazy_entries_by_trigger_and_full_reads_them_up_front(report_root):
    lean = build_report(report_root, fake_count, role="general")
    assert lean["reading_mode"] == {"selected": "lean", "configured": "lean"}
    lean_route = selected(lean)
    assert "optional.md" not in {p["path"] for p in lean_route["paths"]}
    assert lean_route["lazy_tokens"] == fake_count("optional policy.\n")
    full = build_report(report_root, fake_count, role="general", reading_mode="full")
    full_route = selected(full)
    paths = {p["path"]: p for p in full_route["paths"]}
    assert any("reading.mode full" in r["reason"] for r in paths["optional.md"]["reasons"])
    assert full_route["lazy_tokens"] == 0
    assert full_route["known_tokens"] == lean_route["known_tokens"] + lean_route["lazy_tokens"]
    assert "Reading mode: `full`" in markdown(full)


@pytest.mark.parametrize("block,expected", [
    ("", "lean"),
    ("reading:\n  read_loc_max: 500\n", "lean"),
    ("reading:\n  mode: full # everything up front\n  read_loc_max: 500\n", "full"),
    ("reading:\n  mode: 'lean'\n", "lean"),
])
def test_configured_reading_mode(report_root, block, expected):
    config = report_root / "config/context_compass_config.yaml"
    config.write_text(config.read_text(encoding="utf-8") + block, encoding="utf-8")
    assert configured_reading_mode(report_root) == expected


@pytest.mark.parametrize("block", ["reading:\n  mode: eager\n", "reading:\n  mode: lean\n  mode: full\n"])
def test_invalid_reading_mode_fails_instead_of_guessing(report_root, block):
    config = report_root / "config/context_compass_config.yaml"
    config.write_text(config.read_text(encoding="utf-8") + block, encoding="utf-8")
    with pytest.raises(RouteError, match="reading.mode"):
        configured_reading_mode(report_root)


def test_missing_required_read_is_not_a_zero_cost_success(report_root):
    (report_root / "shared.md").unlink()
    route = selected(build_report(report_root, fake_count, role="engineer"))
    assert "shared.md" in route["unmeasured_paths"]
    assert next(p for p in route["paths"] if p["path"] == "shared.md")["known_tokens"] is None


def test_registry_cycles_parent_mismatches_and_unknown_sections(report_root):
    roles = registry(report_root)
    roles["general"]["parent"] = "engineer"
    write(report_root / "roles/general/SKILLS.MD", "- `INHERITS_SKILLS_FROM: roles/engineer/SKILLS.MD`\n")
    with pytest.raises(RouteError, match="cycle"):
        chain(report_root, roles, "engineer")
    write(report_root / "roles/general/SKILLS.MD", "- `INHERITS_SKILLS_FROM: none`\n")
    with pytest.raises(RouteError, match="disagree"):
        chain(report_root, roles, "engineer")
    write(report_root / "roles/general/SKILLS.MD", "- `INHERITS_SKILLS_FROM: none`\n## Mystery\n- `shared.md`\n")
    with pytest.raises(RouteError, match="Unclassified"):
        manifest(report_root, "roles/general/SKILLS.MD")


@pytest.mark.parametrize("value", ["'codex_mcp'", '"codex_mcp"', "codex_mcp # selected"])
def test_quoted_communication_selector(report_root, value):
    write(report_root / "config/context_compass_config.yaml", f"agent_communication:\n  backend: {value}\n")
    assert configured_backends(report_root) == ("local", "codex_mcp")


@pytest.mark.parametrize("block", ["  backend: invalid", "  backend: mailbox\n  backend: codex_mcp",
                                    "  <<: *other", "  backend: *other"])
def test_ambiguous_selectors_are_rejected(report_root, block):
    write(report_root / "config/context_compass_config.yaml", "agent_communication:\n" + block + "\n")
    with pytest.raises(RouteError):
        configured_backends(report_root)


def test_inventory_binary_limit_sensitive_files_and_output_exclusion(report_root):
    (report_root / "binary.dat").write_bytes(b"\0\xff")
    (report_root / "large.txt").write_bytes(b"x" * 1001)
    write(report_root / ".env", "not to be read")
    output = report_root / "generated_reports"
    write(output / "old.md", "Previous output")
    inventory = Inventory(report_root, fake_count, 1000, output)
    assert inventory.files["binary.dat"]["status"] == "binary"
    assert inventory.files["large.txt"]["status"] == "over_size_limit"
    assert inventory.files[".env"]["status"] == "excluded_sensitive_or_cache"
    assert "generated_reports/old.md" not in inventory.files


def test_report_writes_only_owned_outputs_and_never_input(report_root, tmp_path):
    before = {p: p.read_bytes() for p in report_root.rglob("*") if p.is_file()}
    report = build_report(report_root, fake_count, role="engineer")
    out = tmp_path / "report"
    write_report(report, out)
    assert json.loads((out / "report.json").read_text())["generator"].startswith("contextcompass.")
    write_report(report, out)
    assert {p: p.read_bytes() for p in report_root.rglob("*") if p.is_file()} == before
    with pytest.raises(RouteError):
        write_report(report, report_root)
    unrelated = tmp_path / "unrelated"
    write(unrelated / "report.md", "Keep this file.")
    with pytest.raises(RouteError):
        write_report(report, unrelated)
    assert (unrelated / "report.md").read_text() == "Keep this file."


def test_unsafe_skill_path_cannot_escape_root(report_root):
    write(report_root / "roles/general/SKILLS.MD", "- `INHERITS_SKILLS_FROM: none`\nActive skills\n- `../secret.md`\n")
    report = build_report(report_root, fake_count)
    assert all(r["status"] == "unresolved" for r in report["routes"])
    assert any("leaves" in r["error"] for r in report["routes"])


def test_every_shipped_role_and_conditional_section_is_parsed():
    report = build_report(PKG_ROOT, fake_count, role="engineer")
    assert len(report["routes"]) == len(registry(PKG_ROOT)) * 8
    assert all(r["status"] == "resolved_declarations" for r in report["routes"])
    route = selected(report)
    assert GENERAL + "skills/llm_full_usage.md" not in {p["path"] for p in route["paths"]}
    assert GENERAL + "skills/llm_full_usage.md" in {p["path"] for p in route["optional_paths"]}
    assert report["roles"]["new"]["selectable_after_onboarding"] is False
    assert "entry-only" in markdown(report)


def test_unknown_role_is_not_silently_replaced(report_root):
    with pytest.raises(RouteError, match="Unregistered"):
        build_report(report_root, fake_count, role="made_up")


def test_per_path_route_membership_is_explained(report_root):
    report = build_report(report_root, fake_count, role="engineer")
    shared = next(r for r in report["files"] if r["path"] == "shared.md")
    optional = next(r for r in report["files"] if r["path"] == "optional.md")
    assert shared["baseline_route_count"] == 24
    assert optional["baseline_route_count"] == 0
    assert optional["read_states"] == ["on_demand"]


def test_output_file_symlink_cannot_overwrite_an_input(report_root, tmp_path):
    report = build_report(report_root, fake_count)
    out = tmp_path / "output"
    write_report(report, out)
    (out / "report.md").unlink()
    try:
        (out / "report.md").symlink_to(report_root / "AGENTS.MD")
    except OSError:
        pytest.skip("This host cannot create file symlinks")
    before = (report_root / "AGENTS.MD").read_bytes()
    with pytest.raises(RouteError, match="symbolic links"):
        write_report(report, out)
    assert (report_root / "AGENTS.MD").read_bytes() == before


def test_csv_path_cannot_become_a_spreadsheet_formula(report_root, tmp_path):
    write(report_root / "=1+1.md", "Example text")
    report = build_report(report_root, fake_count)
    out = tmp_path / "output"
    write_report(report, out)
    import csv
    with (out / "files.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert any(row["path"] == "'=1+1.md" for row in rows)


def test_previous_generated_reports_are_not_recursively_counted(report_root):
    report = build_report(report_root, fake_count)
    previous = report_root / "previous_report"
    write_report(report, previous)
    next_report = build_report(report_root, fake_count)
    assert not any(row["path"].startswith("previous_report/") for row in next_report["files"])


def test_unlisted_system_document_is_self_directed_not_baseline(report_root):
    role = report_root / "roles/engineer/SKILLS.MD"
    role.write_text(role.read_text() + "\nSelf-directed system reading\nEvery system document not listed above.\n", encoding="utf-8")
    write(report_root / "system_docs/another_topic.md", "A separate topic.")
    route = selected(build_report(report_root, fake_count, role="engineer"))
    assert "system_docs/another_topic.md" not in {row["path"] for row in route["paths"]}
    assert "system_docs/another_topic.md" in {row["path"] for row in route["optional_paths"]}


def test_baseline_label_does_not_turn_existing_or_orientation_into_optional():
    assert not heading("Existing baseline contracts")["if_exists"]
    assert not heading("Baseline orientation")["if_exists"]
    assert heading("Baseline system orientation (read every one that exists)")["if_exists"]
    assert heading("## My baseline: interfaces, checks.")["state"] == "baseline"


def test_explicit_startup_read_paths_remain_covered_by_entry_model():
    import re
    text = (PKG_ROOT / "AGENTS.MD").read_text(encoding="utf-8")
    gate = text.split("## Onboarding Gate (Required)", 1)[1].split("## Communication Style", 1)[0]
    paths = re.findall(r"(?m)^- Read `([^`]+)`", gate)
    for path in paths:
        if path.startswith("context_compass/"):
            path = path[len("context_compass/"):]
        if (PKG_ROOT / path).is_file():
            assert path in ENTRY, path


@pytest.mark.parametrize("condition", ["if a feature is enabled", "when a workflow runs", "unless disabled"])
def test_unknown_baseline_condition_is_not_guessed(condition):
    with pytest.raises(RouteError, match="Unsupported conditional"):
        heading("## Custom baseline " + condition)


@pytest.mark.parametrize("marker", ["[]", "null", '{"generator":"someone_else"}'])
def test_unrelated_output_marker_is_rejected_without_a_crash(report_root, tmp_path, marker):
    out = tmp_path / "not_our_report"
    write(out / "report.json", marker)
    report = build_report(report_root, fake_count)
    with pytest.raises(RouteError, match="empty output directory"):
        write_report(report, out)
    assert (out / "report.json").read_text() == marker
