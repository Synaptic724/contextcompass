"""Message routing contracts, not a claim of live agent or MCP behavior."""

from __future__ import annotations

import re

import pytest

from conftest import PKG_ROOT
from cleanup_context_compass import user_regions
from update_context_compass import conform_text, merge_config
from test_github_work_backend import baseline_section, registered_roles, skill_paths

pytestmark = pytest.mark.unit
GENERAL = "agent_onboarding/default/general/"


def read(path):
    return (PKG_ROOT / path).read_text(encoding="utf-8")


def normalized(text):
    return " ".join(text.replace("`", "").split())


def readsets():
    text = read(GENERAL + "SKILLS.MD")
    return {
        key: skill_paths(baseline_section(text, heading))
        for key, heading in (
            ("shared", "Shared baseline skills"), ("local", "Local backend baseline"),
            ("github_codex_plugin", "GitHub Codex plugin baseline"),
            ("mailbox", "Mailbox communication baseline"),
            ("codex_mcp", "Codex MCP communication baseline"),
        )
    }


@pytest.mark.parametrize("role", sorted(registered_roles()))
@pytest.mark.parametrize("ticket_backend", ["local", "github_codex_plugin"])
@pytest.mark.parametrize("communication", ["mailbox", "codex_mcp"])
def test_every_role_resolves_independent_ticket_and_message_baselines(role, ticket_backend, communication):
    rows, sets = registered_roles(), readsets()
    active, seen, current = set(), set(), role
    while True:
        assert current not in seen
        seen.add(current)
        path, parent = rows[current]
        text = read(path)
        active.update(
            sets["shared"] | sets[ticket_backend] | sets[communication]
            if current == "general" else skill_paths(text)
        )
        if parent == "-":
            break
        current = parent
    if role == "new":
        gate = read("AGENTS.MD").split("## Onboarding Gate", 1)[1]
        assert "skills/agent_communication_backend.md" in gate
        assert "agent_session_state.md" in gate
    else:
        assert sets[communication] <= active
        inactive = "mailbox" if communication == "codex_mcp" else "codex_mcp"
        assert not sets[inactive] & active
        inactive_ticket = "local" if ticket_backend == "github_codex_plugin" else "github_codex_plugin"
        assert not sets[inactive_ticket] & active
        assert GENERAL + "skills/agent_session_state.md" in active
        assert GENERAL + "skills/request_tracking.md" in active
        assert GENERAL + "skills/harness_custom_instructions.md" in active
    for path in active:
        assert (PKG_ROOT / path).is_file(), (role, path)


def test_default_and_message_only_boundary():
    config = read("config/context_compass_config.yaml")
    assert re.search(r"(?m)^agent_communication:\n  backend: mailbox", config)
    selector = normalized(read(GENERAL + "skills/agent_communication_backend.md"))
    assert "absent backend key means mailbox" in selector
    assert "independent selectors" in selector
    assert "blank value" in selector and "unknown value" in selector
    sets = readsets()
    assert sets["mailbox"] == {GENERAL + "skills/mailbox_protocol.md"}
    assert sets["codex_mcp"] == {GENERAL + "skills/codex_mcp.md"}
    assert not sets["mailbox"] & sets["shared"]
    assert not sets["codex_mcp"] & sets["shared"]


def test_mcp_keeps_state_but_skips_mailbox_messages_and_alerts():
    mcp = normalized(read(GENERAL + "skills/codex_mcp.md"))
    state = normalized(read(GENERAL + "skills/agent_session_state.md"))
    for heading in ("Checked-In Agents", "Request Tracking", "Notes"):
        assert heading in state and heading in mcp
    assert "effective onboarding authorization" in state
    assert "must never be guessed" in state
    assert "message alerts" in mcp and "## Messages" in mcp
    assert "Never write mailbox messages or alerts" in mcp
    assert "No silent transport fallback" in mcp
    assert "Selecting" in read(GENERAL + "skills/agent_communication_backend.md")
    assert "prompt_id" in read(GENERAL + "skills/request_tracking.md")


def test_mcp_names_real_tools_and_separates_delivery_from_completion():
    text = normalized(read(GENERAL + "skills/codex_mcp.md"))
    for name in ("list_threads", "send_message_to_thread", "read_thread", "wait_threads"):
        assert name in text
    assert "threadId" in text and "hostId" in text
    assert "cursor" in text
    assert "delivery" in text and "completion" in text
    assert "human-authorized" in text
    assert "pauses" in text and "pending approvals" in text


def test_shared_registration_retains_original_roster_and_authorization_semantics():
    state = normalized(read(GENERAL + "skills/agent_session_state.md"))
    assert "| <agent_name> | <owner> | <checked_in_at> | <last_checked> | active |" in state
    assert "first check in for the session" in state
    assert "every time you read the message section" in state
    assert "active rows older than one day" in state
    assert "departed" in state
    assert "no pre-authorization write exception" in state
    assert "Communication protocol references are conditional" in state


def test_custom_instruction_clauses_follow_configured_transport():
    text = normalized(read(GENERAL + "skills/harness_custom_instructions.md"))
    assert "through its boards and mailbox" not in text
    assert "use Context Compass's boards and mailbox" not in text
    assert "configured agent_communication.backend" in text
    assert "setup-outcome store is independent" in text


def test_mcp_does_not_disable_non_message_attention_flags():
    board = normalized(read("attention_board.md"))
    mcp = normalized(read(GENERAL + "skills/codex_mcp.md"))
    assert "Non-mailbox blockers and cross-agent flags" in board
    assert "remain active in both modes" in board
    assert "skipping mailbox notices does not deactivate" in mcp


@pytest.mark.parametrize("path", ["mailbox_board.md", "attention_board.md", "issue_board.md"])
def test_transport_changes_preserve_every_original_user_region(path, tmp_path):
    incoming = (PKG_ROOT / path).read_bytes()
    text = incoming.decode("utf-8")
    old = text
    for name, start, end in sorted(user_regions(text), key=lambda item: -item[1]):
        old = old[:start] + f"\nORIGINAL {name}: durable state or unread message\n" + old[end:]
    installed = tmp_path / path
    installed.write_text(old, encoding="utf-8")
    merged, _, orphaned = conform_text(incoming, installed)
    result = merged.decode("utf-8")
    original = {name: old[start:end] for name, start, end in user_regions(old)}
    retained = {name: result[start:end] for name, start, end in user_regions(result)}
    assert original == retained
    assert not orphaned


@pytest.mark.parametrize("ticket_backend", ["local", "github_codex_plugin"])
@pytest.mark.parametrize("communication", ["mailbox", "codex_mcp"])
def test_upgrade_never_changes_selected_modes(ticket_backend, communication):
    current = (
        f"work_tracking:\n  backend: {ticket_backend}\n"
        f"agent_communication:\n  backend: {communication}\n"
    )
    merged, added, _ = merge_config(current, read("config/context_compass_config.yaml"))
    assert current.rstrip() in merged
    assert "work_tracking" not in added and "agent_communication" not in added


def test_legacy_upgrade_adds_mailbox_default_without_changing_ticket_choice():
    current = "work_tracking:\n  backend: github_codex_plugin\n"
    merged, added, _ = merge_config(current, read("config/context_compass_config.yaml"))
    assert "agent_communication" in added
    assert "  backend: mailbox" in merged
    assert current.rstrip() in merged
