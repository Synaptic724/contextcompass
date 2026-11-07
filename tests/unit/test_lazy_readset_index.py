"""Lazy readset contracts: every On-demand entry is indexed and never loads eagerly."""

from __future__ import annotations

import pytest

from conftest import PKG_ROOT
from reading_routes import configured_reading_mode, manifest, registry, requirements

pytestmark = pytest.mark.unit

GENERAL = "agent_onboarding/default/general/"
TICKETS = ("local", "github_codex_plugin")
COMMUNICATIONS = ("mailbox", "codex_mcp")


def lazy_entries():
    """Yield (role, entry, lines) for every On-demand entry in a registered manifest."""
    for role, row in sorted(registry(PKG_ROOT).items()):
        lines = (PKG_ROOT / row["path"]).read_text(encoding="utf-8-sig").splitlines()
        for entry in manifest(PKG_ROOT, row["path"])["entries"]:
            if entry["state"] == "on_demand":
                yield role, entry, lines


def sub_items(lines, entry_line):
    """Indented lines directly under a 1-based entry line, stripped."""
    items = []
    for line in lines[entry_line:]:
        if not line.startswith("  "):
            break
        items.append(line.strip())
    return items


def eager_and_lazy(role, ticket, communication):
    route = requirements(PKG_ROOT, registry(PKG_ROOT), role, ticket, communication, "onboard", [])
    eager = {item["path"] for item in route["required"]}
    lazy = {item["path"] for item in route["optional"] if item["state"] == "on_demand"}
    return eager, lazy


def test_shipped_config_defaults_to_lean_and_full_adds_every_lazy_entry():
    assert configured_reading_mode(PKG_ROOT) == "lean"
    roles = registry(PKG_ROOT)
    lean = requirements(PKG_ROOT, roles, "engineer", "local", "mailbox", "onboard", [])
    full = requirements(PKG_ROOT, roles, "engineer", "local", "mailbox", "onboard", [], reading_mode="full")
    lazy = {item["path"] for item in lean["optional"] if item["state"] == "on_demand"}
    assert lazy and lazy <= {item["path"] for item in full["required"]}
    assert not any(item["state"] == "on_demand" for item in full["optional"])


def test_every_lazy_entry_says_what_it_covers_and_what_loads_it():
    found = list(lazy_entries())
    assert found, "no lazy entries found"
    for role, entry, lines in found:
        items = sub_items(lines, entry["line"])
        assert any(item.startswith("- Covers:") for item in items), (role, entry["path"])
        assert any(item.startswith("- Trigger:") for item in items), (role, entry["path"])
        assert (PKG_ROOT / entry["path"]).exists(), (role, entry["path"])


@pytest.mark.parametrize("ticket", TICKETS)
@pytest.mark.parametrize("communication", COMMUNICATIONS)
def test_lazy_paths_never_load_eagerly(ticket, communication):
    for role in registry(PKG_ROOT):
        eager, lazy = eager_and_lazy(role, ticket, communication)
        assert not eager & lazy, (role, sorted(eager & lazy))


def test_general_keeps_the_loop_eager_and_procedures_lazy():
    eager, lazy = eager_and_lazy("general", "local", "mailbox")
    moved = {
        GENERAL + "skills/ticket_closure_attention_sync.md",
        GENERAL + "workflows/start_context_compass_work.md",
        GENERAL + "workflows/turn_in_selected_tickets.md",
        GENERAL + "workflows/cleanup_context_compass.md",
        GENERAL + "workflows/sync_attention_board.md",
        GENERAL + "skills/package_upgrade.md",
        GENERAL + "skills/context_management.md",
        GENERAL + "skills/harness_custom_instructions_setup.md",
        "artifact_board.md",
        "context_management/context_board.md",
    }
    assert moved <= lazy
    assert not moved & eager
    loop = (
        GENERAL + "skills/ticketing.md",
        GENERAL + "skills/workflow.md",
        GENERAL + "skills/ticket_microcycle.md",
        GENERAL + "skills/active_pointerboard.md",
        GENERAL + "skills/active_documentation.md",
        GENERAL + "skills/compaction_requirements.md",
        GENERAL + "skills/harness_custom_instructions.md",
        "attention_board.md",
    )
    for path in loop:
        assert path in eager, path


def test_design_engineer_loads_document_and_patch_authoring_lazily():
    design = "agent_onboarding/default/design_engineer/"
    eager, lazy = eager_and_lazy("design_engineer", "local", "mailbox")
    moved = {design + "skills/" + name for name in (
        "src_architecture_instructions.md", "src_components_instructions.md",
        "tests_architecture_instructions.md", "tests_components_instructions.md",
        "patch_framework_design.md", "architecture_patch_contracts.md",
        "component_patch_contracts.md", "code_description_patch_contracts.md")}
    moved.add(design + "policies/system_document_quality_rubric.md")
    assert moved <= lazy
    assert not moved & eager
    for name in ("skills/system_design_method.md", "skills/design_engineer_execution.md",
                 "skills/architecture_tradeoffs.md", "policies/design_review_policy.md"):
        assert design + name in eager, name


def test_engineer_loads_system_doc_guides_and_procedures_lazily():
    engineer = "agent_onboarding/default/engineer/"
    eager, lazy = eager_and_lazy("engineer", "local", "mailbox")
    moved = {
        engineer + "skills/context_protocol.md",
        engineer + "skills/src_graph_usage.md",
        engineer + "skills/system_document_build.md",
        engineer + "skills/src_graph_generation.md",
        engineer + "policies/ctx_autonomy_rubric.md",
        engineer + "policies/ctx_autonomy_policy.md",
        engineer + "skills/patch_framework_gating.md",
        engineer + "skills/patch_artifact_consumption.md",
        engineer + "skills/system_orientation.md",
        engineer + "examples/artifact_workflow.md",
        engineer + "skills/package_maintenance.md",
    }
    assert moved <= lazy
    assert not moved & eager
    core = (
        engineer + "AGENTS.MD",
        engineer + "skills/engineer_execution.md",
        engineer + "skills/technical_expertise.md",
        engineer + "skills/documentation_standards.md",
        engineer + "skills/staleness_protocol.md",
        engineer + "behavioral_guidelines/task_execution_and_validation.md",
        "system_docs/system_docs_read_first.md",
    )
    for path in core:
        assert path in eager, path
    assert GENERAL + "skills/ticketing.md" in eager
