"""Contracts for the claude_internal_communication message transport.

These check the shipped routing and guidance, not live Claude Code sessions.
"""

from __future__ import annotations

import pytest

from conftest import PKG_ROOT
from reading_routes import (CHAT_TRANSPORTS, COMMUNICATIONS, RouteError, configured_backends,
                            registry, requirements)

pytestmark = pytest.mark.unit

GENERAL = "agent_onboarding/default/general/"
SKILL = GENERAL + "skills/claude_internal_communication.md"
OTHER_TRANSPORTS = {GENERAL + "skills/mailbox_protocol.md", GENERAL + "skills/codex_mcp.md"}


def read(path):
    return (PKG_ROOT / path).read_text(encoding="utf-8")


def flat(path):
    return " ".join(read(path).replace("`", "").split())


def eager(role, ticket, communication, event="onboard"):
    result = requirements(PKG_ROOT, registry(PKG_ROOT), role, ticket, communication, event, [])
    return result["role_chain"], {item["path"] for item in result["required"]}


def test_selector_lists_the_transport_as_a_chat_transport():
    assert COMMUNICATIONS == ("mailbox", "codex_mcp", "claude_internal_communication")
    assert CHAT_TRANSPORTS == ("codex_mcp", "claude_internal_communication")


@pytest.mark.parametrize("ticket", ["local", "github_codex_plugin", "github_issues"])
@pytest.mark.parametrize("event", ["onboard", "reonboard"])
def test_every_working_role_reads_only_the_claude_transport(ticket, event):
    for role in registry(PKG_ROOT):
        chain, paths = eager(role, ticket, "claude_internal_communication", event)
        if "general" not in chain:
            continue
        assert SKILL in paths, (role, ticket)
        assert not paths & OTHER_TRANSPORTS, (role, ticket, sorted(paths & OTHER_TRANSPORTS))


@pytest.mark.parametrize("communication", ["mailbox", "codex_mcp"])
def test_other_transports_never_read_the_claude_skill(communication):
    _, paths = eager("engineer", "local", communication)
    assert SKILL not in paths


def test_switching_to_the_claude_transport_swaps_only_the_message_skill():
    _, mcp = eager("engineer", "local", "codex_mcp")
    _, claude = eager("engineer", "local", "claude_internal_communication")
    assert claude - mcp == {SKILL}
    assert mcp - claude == {GENERAL + "skills/codex_mcp.md"}


def test_config_offers_the_transport_and_keeps_the_mailbox_default(tmp_path):
    config = read("config/context_compass_config.yaml")
    line = next(l for l in config.splitlines() if l.strip().startswith("backend: mailbox"))
    assert "claude_internal_communication" in line and "Claude agents only" in line
    (tmp_path / "config").mkdir()
    selector = tmp_path / "config/context_compass_config.yaml"
    selector.write_text("agent_communication:\n  backend: claude_internal_communication\n", encoding="utf-8")
    assert configured_backends(tmp_path) == ("local", "claude_internal_communication")
    selector.write_text("agent_communication:\n  backend: claude\n", encoding="utf-8")
    with pytest.raises(RouteError, match="claude_internal_communication"):
        configured_backends(tmp_path)


def test_skill_is_for_claude_agents_only_and_names_the_builtin_messaging():
    text = flat(SKILL)
    for phrase in ("teams of Claude agents only", "must be a Claude Code session",
                   "uses mailbox, or codex_mcp for Codex", "ListAgents", "SendMessage",
                   "nothing to poll", "Remote Control", "2.1.224", "2.1.234"):
        assert phrase in text, phrase


def test_skill_keeps_the_transport_governance():
    text = flat(SKILL)
    for phrase in ("replaces message transport only", "Checked-In Agents", "## Messages",
                   "message alerts", "Never write mailbox messages or alerts",
                   "Send only to recipients your owner has authorized",
                   "Record the agent-to-session mapping in the canonical ticket",
                   "not your owner's instruction", "cannot approve an action, lift a pause, or grant a permission",
                   "delivery, not completion", "Do not fall back to mailbox messages or harness tracking",
                   "No silent transport fallback"):
        assert phrase in text, phrase


def test_policy_and_selector_describe_the_transport():
    policy = flat("AGENTS.MD")
    assert "claude_internal_communication selects Claude Code's built-in agent messaging" in policy
    assert "for teams of Claude agents only" in policy
    selector = flat(GENERAL + "skills/agent_communication_backend.md")
    assert "| claude_internal_communication |" in selector
    assert "teams of Claude agents only" in selector
    state = flat(GENERAL + "skills/agent_session_state.md")
    assert "In codex_mcp or claude_internal_communication mode, read only ## Checked-In Agents" in state
