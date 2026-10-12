"""Contracts for the opt-in GitHub backend without touching a live account."""

from __future__ import annotations

import importlib.util
import re
import subprocess

import pytest

from conftest import PKG_ROOT
import package_manifest as manifest
from update_context_compass import conform_text, merge_config

pytestmark = pytest.mark.unit

GITHUB = PKG_ROOT / "agent_onboarding/default/general/skills/github"
SPEC = importlib.util.spec_from_file_location("cc_github_check_setup", GITHUB / "check_setup.py")
assert SPEC is not None and SPEC.loader is not None
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


def registered_roles():
    registry = (PKG_ROOT / "SKILLS.MD").read_text(encoding="utf-8")
    rows = {}
    for line in registry.splitlines():
        match = re.match(r"^\| `([^`]+)` \| `([^`]+)` \| (`[^`]+`|-) \|", line)
        if match:
            name, path, parent = match.groups()
            assert name not in rows, f"Duplicate registered role: {name}"
            rows[name] = (path, parent.strip("`"))
    assert rows, "No roles found in the canonical registry"
    return rows


def skill_paths(text):
    return set(re.findall(r"(?m)^- `(agent_onboarding/[^`]+|issue_board\.md)`$", text))


def baseline_section(text, heading):
    headings = (
        "Shared baseline skills", "Local backend baseline", "GitHub Codex plugin baseline",
        "Mailbox communication baseline", "Codex MCP communication baseline", "Note on the board paths",
    )
    tail = text.split(heading, 1)[1]
    return re.split(
        r"(?m)^(?:" + "|".join(re.escape(item) for item in headings) + r")", tail, maxsplit=1
    )[0]


def general_readsets():
    text = (PKG_ROOT / "agent_onboarding/default/general/SKILLS.MD").read_text(encoding="utf-8")
    shared = baseline_section(text, "Shared baseline skills")
    local = baseline_section(text, "Local backend baseline")
    plugin = baseline_section(text, "GitHub Codex plugin baseline")
    return skill_paths(shared), skill_paths(local), skill_paths(plugin)


@pytest.mark.parametrize("role", sorted(registered_roles()))
@pytest.mark.parametrize("backend", ["local", "github_codex_plugin"])
def test_registered_roles_inherit_exactly_one_ticket_backend(role, backend):
    rows = registered_roles()
    shared, local, plugin = general_readsets()
    active = set()
    seen = set()
    current = role
    while True:
        assert current not in seen, f"Inheritance cycle for {role}: {current}"
        seen.add(current)
        path, parent = rows[current]
        text = (PKG_ROOT / path).read_text(encoding="utf-8")
        header = re.search(r"INHERITS_SKILLS_FROM: ([^`]+)", text)
        assert header is not None, path
        expected = "none" if parent == "-" else rows[parent][0]
        assert header.group(1) == expected, f"Registry/header mismatch in {path}"
        assert not re.search(r"`general`(?:'s)?[^\n]{0,40}Active\s+skills", text), path
        if current == "general":
            active.update(shared | (local if backend == "local" else plugin))
        else:
            active.update(skill_paths(text))
        if parent == "-":
            break
        current = parent
    for path in active:
        assert (PKG_ROOT / path).is_file(), f"Missing routed skill for {role}: {path}"
    if role == "new":
        assert "general" not in seen
        entry = (PKG_ROOT / "AGENTS.MD").read_text(encoding="utf-8")
        gate = entry.split("## Onboarding Gate", 1)[1]
        assert "skills/work_tracking_backend.md" in gate
    else:
        assert "general" in seen, f"Working role {role} lost the shared backend router"
        required, inactive = (local, plugin) if backend == "local" else (plugin, local)
        assert required <= active
        assert not inactive & active, f"Inactive backend leaks into {role}: {inactive & active}"


def test_shared_and_descendant_docs_do_not_require_local_only_ticket_skills():
    _, local, _ = general_readsets()
    permitted = local | {
        "agent_onboarding/default/general/SKILLS.MD",
        "agent_onboarding/default/general/WORKFLOWS.MD",
    }
    leaks = []
    for path in (PKG_ROOT / "agent_onboarding").rglob("*"):
        if not path.is_file() or path.suffix.lower() != ".md" or path.name == "SKILLS.MD":
            continue
        relative = path.relative_to(PKG_ROOT).as_posix()
        if relative in permitted:
            continue
        references = skill_paths(path.read_text(encoding="utf-8")) & local
        if references:
            leaks.append(f"{relative}: {sorted(references)}")
    assert not leaks, "Unconditional local ticket routes:\n" + "\n".join(leaks)


def test_local_and_plugin_readsets_resolve_one_ticket_source():
    config = (PKG_ROOT / "config/context_compass_config.yaml").read_text(encoding="utf-8")
    skills = (PKG_ROOT / "agent_onboarding/default/general/SKILLS.MD").read_text(encoding="utf-8")
    assert "backend: local" in config
    assert "github_codex_plugin:" in config
    assert "issues_repository:" in config and "project_url:" in config
    assert "Shared baseline skills" in skills
    assert "Local backend baseline" in skills
    assert "GitHub Codex plugin baseline" in skills
    assert "github/workflow.md" in skills and "issue_board.md" in skills
    shared = baseline_section(skills, "Shared baseline skills")
    local = baseline_section(skills, "Local backend baseline")
    plugin = baseline_section(skills, "GitHub Codex plugin baseline")
    assert "skills/role_local_workflows.md" in shared
    assert "general/WORKFLOWS.MD" in shared
    macros = {
        "agent_onboarding/default/general/workflows/cleanup_context_compass.md",
        "agent_onboarding/default/general/workflows/start_context_compass_work.md",
        "agent_onboarding/default/general/workflows/turn_in_selected_tickets.md",
        "agent_onboarding/default/general/workflows/sync_attention_board.md",
    }
    assert macros <= skill_paths(shared)
    assert not macros & skill_paths(local)
    entries = lambda text: set(re.findall(r"(?m)^- `([^`]+)`$", text))
    local_paths, plugin_paths = entries(local), entries(plugin)
    assert not local_paths & plugin_paths
    assert "agent_onboarding/default/general/skills/workflow.md" in local_paths
    assert "agent_onboarding/default/general/skills/ticket_closure_attention_sync.md" in local_paths
    assert "agent_onboarding/default/general/skills/github/codex_plugin.md" in plugin_paths
    assert "agent_onboarding/default/general/skills/github/workflow.md" in plugin_paths
    assert "issue_board.md" in plugin_paths
    assert not any(path.endswith((".py", ".ps1", ".sh", "commands.md")) for path in plugin_paths)
    for path in local_paths | plugin_paths:
        assert (PKG_ROOT / path).is_file(), path


def test_existing_macros_keep_scope_and_selection_in_both_backends():
    root = PKG_ROOT / "agent_onboarding/default/general/workflows"
    for name in ("start_context_compass_work", "cleanup_context_compass",
                 "turn_in_selected_tickets", "sync_attention_board"):
        text = (root / f"{name}.md").read_text(encoding="utf-8")
        assert "skills/work_tracking_backend.md" in text
        assert "## Backend Routing" in text
        assert "plugin" in text.lower()
    cleanup = (root / "cleanup_context_compass.md").read_text(encoding="utf-8")
    assert "my assets" in cleanup and "everything" in cleanup
    assert "not" in cleanup and "every Issue" in cleanup
    turn_in = (root / "turn_in_selected_tickets.md").read_text(encoding="utf-8")
    assert "displayed candidate set" in turn_in
    assert "never every Issue" in turn_in


def test_plugin_connection_nickname_is_blank_and_required_only_for_plugin():
    config = (PKG_ROOT / "config/context_compass_config.yaml").read_text(encoding="utf-8")
    routing = (PKG_ROOT / "agent_onboarding/default/general/skills/work_tracking_backend.md").read_text(
        encoding="utf-8"
    )
    assert 'connection_nickname: ""' in config
    assert "backend: local" in config
    assert "connection_nickname" in routing
    assert "Local mode ignores" in routing


def test_plugin_nickname_selection_is_exact_and_fail_closed():
    operations = (GITHUB / "codex_plugin.md").read_text(encoding="utf-8")
    assert "## Resolve the connection nickname" in operations
    assert "exact match" in operations
    assert "link_name" in operations and "link_id" in operations
    assert "profile_nickname" in operations and "profile_id" in operations
    assert "Missing" in operations and "multiple" in operations
    assert "single connected account" in operations
    assert "Before any plugin read or write" in operations
    assert "recovery" in operations and "credentials" in operations
    assert "do not fall back" in operations


@pytest.mark.parametrize("path", [
    GITHUB / "README.md",
    PKG_ROOT.parents[1] / "README.md",
])
def test_plugin_setup_examples_include_a_generic_nickname(path):
    text = path.read_text(encoding="utf-8")
    assert 'connection_nickname: "Work account"' in text
    assert "issues_repository: YOUR_OWNER/YOUR_REPO" in text


def test_plugin_migration_resolves_connection_before_publishing():
    migration = (GITHUB / "migration.md").read_text(encoding="utf-8")
    assert "connection_nickname" in migration
    assert "codex_plugin.md" in migration
    assert migration.index("connection_nickname") < migration.index("After the owner approves")


def test_upgrade_preserves_chosen_connection_nickname():
    incoming = (PKG_ROOT / "config/context_compass_config.yaml").read_text(encoding="utf-8")
    current = (
        "work_tracking:\n  backend: github_codex_plugin\n  github_codex_plugin:\n"
        '    connection_nickname: "My project account"\n'
        '    issues_repository: "team/existing"\n    project_url: "keep-this-link"\n'
    )
    merged, added, _ = merge_config(current, incoming)
    assert current.rstrip() in merged
    assert "work_tracking" not in added


def test_upgrade_adds_backend_default_without_changing_existing_choice():
    incoming = (PKG_ROOT / "config/context_compass_config.yaml").read_text(encoding="utf-8")
    current = "version: 2\n\nsystem_of_record:\n  enforce: false\n"
    merged, added, _ = merge_config(current, incoming)
    assert "work_tracking" in added
    assert "backend: local" in merged
    assert "enforce: false" in merged


@pytest.mark.parametrize("backend", ["local", "files", "github", "github_codex_plugin"])
def test_upgrade_preserves_existing_backend_and_repository(backend):
    incoming = (PKG_ROOT / "config/context_compass_config.yaml").read_text(encoding="utf-8")
    current = (
        f"work_tracking:\n  backend: {backend}\n  github:\n"
        '    issues_repository: "team/existing"\n    project_url: "keep-this-link"\n'
    )
    merged, added, _ = merge_config(current, incoming)
    assert current.rstrip() in merged
    assert "work_tracking" not in added


def test_recovery_resolves_yaml_before_backend_and_ticket_reads():
    text = (PKG_ROOT / "agent_onboarding/default/general/skills/compaction_requirements.md").read_text(
        encoding="utf-8"
    )
    sequence = text.split("Required post-compaction sequence (REONBOARD)", 1)[1]
    config_read = sequence.index("config/context_compass_config.yaml")
    assert config_read < sequence.index("registry table")
    assert config_read < sequence.index("attention_board.md")
    assert "Issue-body Status/Notes" in sequence


def test_plugin_notes_and_updates_are_preserved_in_the_issue_body():
    workflow = (GITHUB / "workflow.md").read_text(encoding="utf-8")
    operations = (GITHUB / "codex_plugin.md").read_text(encoding="utf-8")
    assert "## Notes" in workflow and "Issue body" in workflow
    assert "github_update_issue" in operations
    assert "preserve every unrelated section and historical note" in operations
    assert "Never send a note alone" in operations
    assert "add_comment_to_issue" in operations and "pr_number" in operations
    assert "compare-and-swap" in operations
    assert "optional context" in workflow


def test_issue_board_is_live_and_upgrade_carries_claims(tmp_path):
    assert manifest.classify("issue_board.md") == "LIVE"
    incoming = (PKG_ROOT / "issue_board.md").read_bytes()
    current = incoming.decode("utf-8").replace(
        "<!-- BEGIN USER-DEFINED: active_claims -->\n",
        "<!-- BEGIN USER-DEFINED: active_claims -->\n"
        "| https://github.com/team/app/issues/7 | primary | team | agent_0 | build | none | 2026-10-03T00:00:00Z |\n",
    ).replace("This board is active only", "Old managed copy: active only")
    installed = tmp_path / "issue_board.md"
    installed.write_text(current, encoding="utf-8")
    merged, carried, orphaned = conform_text(incoming, installed)
    text = merged.decode("utf-8")
    assert "https://github.com/team/app/issues/7" in text
    assert "Old managed copy" not in text
    assert "active_claims" in carried
    assert orphaned == []


def test_preflight_repo_check_requests_issues_field(monkeypatch):
    calls = []

    def fake_run(argv):
        calls.append(argv)
        return subprocess.CompletedProcess(
            argv, 0, '{"nameWithOwner":"team/app","hasIssuesEnabled":true}', ""
        )

    monkeypatch.setattr(preflight, "run", fake_run)
    assert preflight.check_repo("team", "app") == "team/app"
    assert "hasIssuesEnabled" in calls[0][-1]


def test_preflight_reads_status_options_from_gh_object(monkeypatch):
    payload = (
        '{"fields":[{"name":"Status","dataType":"SINGLE_SELECT",'
        '"options":[{"name":"Ready"},{"name":"Working"},'
        '{"name":"Blocked"},{"name":"Review"},{"name":"Done"}]}]}'
    )
    monkeypatch.setattr(
        preflight, "run",
        lambda argv: subprocess.CompletedProcess(argv, 0, payload, ""),
    )
    assert preflight.check_status_field("team", 1, "Status") == [
        "Ready", "Working", "Blocked", "Review", "Done"
    ]


def test_preflight_rejects_bad_target_and_empty_status(monkeypatch):
    with pytest.raises(preflight.PreflightError):
        preflight.check_project("not valid", 1)
    with pytest.raises(preflight.PreflightError):
        preflight.validate_slug("team", "../app")
    payload = '{"fields":[{"name":"Status","dataType":"SINGLE_SELECT","options":[]}]}'
    monkeypatch.setattr(
        preflight, "run",
        lambda argv: subprocess.CompletedProcess(argv, 0, payload, ""),
    )
    with pytest.raises(preflight.PreflightError):
        preflight.check_status_field("team", 1, "Status")


def test_standalone_cli_helpers_keep_their_existing_setup_behavior():
    ps = (GITHUB / "setup.ps1").read_text(encoding="utf-8")
    sh = (GITHUB / "setup.sh").read_text(encoding="utf-8")
    for script in (ps, sh):
        assert "gh auth login --web" in script
        assert "gh auth refresh" in script
        assert "-s project" in script
        assert "Project URL" in script
        assert "gh auth token" not in script
