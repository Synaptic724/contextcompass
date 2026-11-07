"""Contracts for the github_issues backend: tickets and every board in GitHub Issues.

These check the shipped routing and guidance, not a live GitHub account.
"""

from __future__ import annotations

import re

import pytest

from conftest import PKG_ROOT
from reading_routes import RouteError, boards_for, configured_backends, registry, requirements
from ticket_backend import BACKENDS, ISSUE_BACKENDS, BackendConfigError, backend_from_yaml
from ticket_design import bundle

pytestmark = pytest.mark.unit

GENERAL = "agent_onboarding/default/general/"
BACKEND_SKILL = GENERAL + "skills/github/issues_backend.md"
SETUP_SKILL = GENERAL + "skills/github/issues_setup.md"
HEADER = "templates/github_issues_header.md"
MIGRATION = GENERAL + "skills/github/migration.md"
LOCAL_BOARD_READS = {
    "attention_board.md", "mailbox_board.md", "issue_board.md",
    GENERAL + "skills/mailbox_protocol.md",
    GENERAL + "skills/github/codex_plugin.md", GENERAL + "skills/github/workflow.md",
}


def read(path):
    return (PKG_ROOT / path).read_text(encoding="utf-8")


def route(role, ticket, communication, event="onboard"):
    result = requirements(PKG_ROOT, registry(PKG_ROOT), role, ticket, communication, event, [])
    eager = {item["path"] for item in result["required"]}
    lazy = {item["path"] for item in result["optional"] if item["state"] == "on_demand"}
    return result["role_chain"], eager, lazy


def test_selector_accepts_github_issues_and_still_refuses_legacy_github():
    assert BACKENDS == ("local", "github_codex_plugin", "github_issues")
    assert ISSUE_BACKENDS == ("github_codex_plugin", "github_issues")
    assert backend_from_yaml("work_tracking:\n  backend: github_issues\n") == "github_issues"
    assert backend_from_yaml("work_tracking:\n  backend: 'github_issues' # boards too\n") == "github_issues"
    with pytest.raises(BackendConfigError, match="legacy github is ambiguous"):
        backend_from_yaml("work_tracking:\n  backend: github\n")
    assert boards_for("github_issues") == "github"
    assert boards_for("local") == boards_for("github_codex_plugin") == "local"


@pytest.mark.parametrize("role", sorted(registry(PKG_ROOT)))
@pytest.mark.parametrize("event", ["onboard", "reonboard"])
def test_github_issues_reads_no_local_board_and_loads_its_baseline(role, event):
    chain, eager, _ = route(role, "github_issues", "mailbox", event)
    assert not eager & LOCAL_BOARD_READS, (role, sorted(eager & LOCAL_BOARD_READS))
    if "general" in chain:
        assert BACKEND_SKILL in eager
        assert GENERAL + "skills/agent_session_state.md" in eager


@pytest.mark.parametrize("ticket", ["local", "github_codex_plugin"])
@pytest.mark.parametrize("communication", ["mailbox", "codex_mcp", "claude_internal_communication"])
def test_local_board_backends_still_read_their_boards(ticket, communication):
    _, eager, _ = route("engineer", ticket, communication)
    assert {"attention_board.md", "mailbox_board.md"} <= eager
    assert BACKEND_SKILL not in eager
    assert (GENERAL + "skills/mailbox_protocol.md" in eager) == (communication == "mailbox")
    assert ("issue_board.md" in eager) == (ticket == "github_codex_plugin")


def test_transport_selection_inside_github_issues():
    _, mailbox, _ = route("engineer", "github_issues", "mailbox")
    _, mcp, _ = route("engineer", "github_issues", "codex_mcp")
    assert GENERAL + "skills/mailbox_protocol.md" not in mailbox | mcp
    assert GENERAL + "skills/codex_mcp.md" in mcp
    assert GENERAL + "skills/codex_mcp.md" not in mailbox
    assert mcp - mailbox == {GENERAL + "skills/codex_mcp.md"}


def test_setup_is_a_lazy_entry_with_its_own_trigger():
    _, eager, lazy = route("general", "github_issues", "mailbox")
    assert SETUP_SKILL in lazy and SETUP_SKILL not in eager
    index = read(GENERAL + "SKILLS.MD")
    entry = index.split(f"- `{SETUP_SKILL}`", 1)[1].split("\n- `", 1)[0]
    assert "Covers:" in entry and "Trigger:" in entry and "cc-header" in entry


def test_configured_backends_reads_the_new_value(tmp_path):
    (tmp_path / "config").mkdir()
    config = tmp_path / "config/context_compass_config.yaml"
    config.write_text("work_tracking:\n  backend: github_issues\n  github_issues:\n"
                      "    repository: owner/repo\nagent_communication:\n  backend: codex_mcp\n",
                      encoding="utf-8")
    assert configured_backends(tmp_path) == ("github_issues", "codex_mcp")
    config.write_text("work_tracking:\n  backend: github\n", encoding="utf-8")
    with pytest.raises(RouteError):
        configured_backends(tmp_path)


def test_shipped_config_offers_the_mode_but_stays_local():
    config = read("config/context_compass_config.yaml")
    assert "backend: local # local | github_codex_plugin | github_issues" in config
    block = config.split("  github_issues:\n", 1)[1].split("\n\n", 1)[0]
    assert 'repository: ""' in block
    assert backend_from_yaml(config) == "local"


def test_backend_skill_describes_mechanics_not_tools():
    text = read(BACKEND_SKILL)
    flat = " ".join(text.split())
    for phrase in ("raise the gap to your owner", "no write lock", "last-edited time",
                   "edit history", "one at a time", "65,536", "80 a minute",
                   "earliest `primary` claim", "cc-promoted-through", "<!-- cc-card: <AGENT_NAME> -->",
                   "<!-- cc-event: <type> <AGENT_NAME> -->", "Check out", "stale", "`cc-active`",
                   "agent_session_state.md", "github/issues_setup.md"):
        assert phrase in flat, phrase
    assert not re.search(r"\bgh\b|github_update_issue|github_create_issue|curl|GraphQL|REST", text)


@pytest.mark.parametrize("board", ["attention_board.md", "issue_board.md", "mailbox_board.md",
                                   "artifact_board.md", "context_management/context_board.md"])
def test_every_local_board_has_a_github_form(board):
    table = read(BACKEND_SKILL).split("## The boards in this mode", 1)[1].split("\n## ", 1)[0]
    assert f"| `{board}`" in table
    if board == "issue_board.md":
        assert "active only when `work_tracking.backend: github_codex_plugin`" in read(board)
    else:
        assert "Unused in `github_issues` mode" in read(board)


def test_header_template_keeps_managed_rules_and_owner_notes_apart():
    text = read(HEADER)
    assert text.startswith("<!-- cc-header-version: <VERSION> -->\n")
    assert "<REPOSITORY>" in text
    managed = text.split("<!-- BEGIN MANAGED: header -->", 1)[1].split("<!-- END MANAGED: header -->", 1)[0]
    assert "earliest `primary` claim" in " ".join(managed.split())
    notes = text.split("<!-- BEGIN USER-DEFINED: notes -->", 1)[1].split("<!-- END USER-DEFINED: notes -->", 1)[0]
    assert notes == "\n"
    assert text.index("<!-- END MANAGED: header -->") < text.index("<!-- BEGIN USER-DEFINED: notes -->")


def test_root_policy_routes_github_issues_through_the_backend_skill():
    policy = " ".join(read("AGENTS.MD").split())
    assert "In `github_issues` mode, tickets and every board live in GitHub Issues" in policy
    assert BACKEND_SKILL in policy
    assert "resolve `local`, `github_codex_plugin` or `github_issues` before reading ticket state" in policy


def test_backend_skill_states_body_and_comment_size_limits():
    """Creating an issue over 65,536 characters fails while an edit reaches 262,144."""
    flat = " ".join(read(BACKEND_SKILL).split())
    rule = flat.split("**Size.**", 1)[1].split("## Claims", 1)[0]
    for phrase in ("comment holds up to 65,536", "refuses to create an issue", "262,144",
                   "short body that carries its ID", "first edit", "promotes any pending comments",
                   "verbatim and in order", "moves the promotion stamp past those comments"):
        assert phrase in rule, phrase


def test_moving_boards_labels_ticket_issues_and_marks_retired_boards():
    flat = " ".join(read(SETUP_SKILL).split())
    section = flat.split("## Moving from local boards", 1)[1]
    for phrase in ("Every ticket Issue carries `cc-epic`", "skip empty regions and bare headings",
                   "lists Issue URLs, not file paths", "unless the section already lists it",
                   "own setup notes", "moved to GitHub Issues", "header issue's link"):
        assert phrase in section, phrase
    assert section.index("Show the owner the result") < section.index("Leave the local board files in place")


def test_migration_moves_local_and_plugin_tickets_into_github_issues():
    text = read(MIGRATION)
    local = " ".join(text.split("## Moving local tickets into github_issues", 1)[1].split("\n## ", 1)[0].split())
    for phrase in ("owner requests the move", "changes last", "outside `completed/` and `archive/`",
                   "parents before children", "Search for each ID first", "65,536",
                   "(`issues_backend.md`, Size)", "ID-to-URL", "(#12)", "`path:12-34` unchanged",
                   "every line present in order", "`issues_setup.md`", "first line linking its Issue"):
        assert phrase in local, phrase
    assert local.index("set the backend") < local.index("first line linking its Issue")
    plugin = " ".join(text.split("## Moving from github_codex_plugin to github_issues", 1)[1]
                      .split("\n## ", 1)[0].split())
    for phrase in ("`issues_repository`", "`cc-task`", "Ticket bodies stay as they are"):
        assert phrase in plugin, phrase
    entry = read(GENERAL + "SKILLS.MD").split(f"- `{MIGRATION}`", 1)[1].split("\n- `", 1)[0]
    assert "`github_issues`" in entry and "Covers:" in entry and "Trigger:" in entry


def test_ticket_design_bundle_uses_the_issues_backend_guidance():
    text = bundle(PKG_ROOT, "task", "github_issues")
    sources = set(re.findall(r"<!-- SOURCE: ([^;]+);", text))
    assert BACKEND_SKILL in sources
    assert GENERAL + "skills/github/codex_plugin.md" not in sources
    assert GENERAL + "skills/ticketing_skill_contract.md" not in sources
    assert '"backend": "github_issues"' in text
