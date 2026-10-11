"""Lint the shipped onboarding contract, not the behavior of a language model.

These checks keep the bootstrap and its dependent routes connected. Scenario
review is still needed to assess the meaning of an override in actual use.
"""

from __future__ import annotations

import re

import pytest

from conftest import PKG_ROOT, REPO_ROOT

pytestmark = pytest.mark.unit

BOOTSTRAP = "Project Instructions Bootstrap"
AUTHORIZATION = "effective onboarding authorization"
GENERAL = "agent_onboarding/default/general/"
NEW = "agent_onboarding/default/new/"
SYNAPTIC_FLOW = (
    "agent_onboarding/user_defined/synaptic_python_developer/workflows/"
    "synaptic_python_developer_onboarding.md"
)


def read(relative: str) -> str:
    return (PKG_ROOT / relative).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(text.replace("`", "").lower().split())


def section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text)
    assert match is not None, f"Missing canonical section: {heading}"
    return match.group(1)


def test_bootstrap_is_defined_before_onboarding_and_recovery_defaults():
    root = read("AGENTS.MD")
    assert root.count(f"## {BOOTSTRAP}") == 1, "Keep one canonical delegation contract"
    bootstrap = root.index(f"## {BOOTSTRAP}")
    assert bootstrap < root.index("## Onboarding Directive")
    assert bootstrap < root.index("## Compaction Directive")
    assert bootstrap < root.index("## Onboarding Gate")


def test_bootstrap_declares_scoped_precedence_and_its_boundaries():
    text = normalized(section(read("AGENTS.MD"), BOOTSTRAP))
    for concept in (
        "special_instructions/", "onboarding", "explicit",
        "override", "scope", "default", "later", "system", "developer",
        "permission", "owner", "conflict",
    ):
        assert concept in text, f"Bootstrap omits the {concept!r} contract"
    assert any(word in text for word in ("re-onboarding", "reonboard", "recovery"))
    assert re.search(r"precedence|outrank|prevail", text)
    assert re.search(r"waiv|replac", text), "Overrides must affect requirements, not just style"
    assert "filename" in text or "file name" in text
    assert "unreadable" in text or "cannot be read" in text
    assert "empty" in text or "absent" in text


def test_execution_contract_keeps_explicit_user_direction_above_repo_policy():
    text = normalized(read(GENERAL + "skills/execution_contract.md"))
    authority = text.split("execution authority order is:", 1)[1].split("hard rule", 1)[0]
    assert authority.index("explicit user instructions") < authority.index("agents.md")


@pytest.mark.parametrize("relative", [
    "SKILLS.MD",
    "CONTEXT_COMPACTION.md",
    "special_instructions/README.md",
    GENERAL + "AGENTS.MD",
    GENERAL + "policies/policy_skills.md",
    GENERAL + "skills/execution_contract.md",
    GENERAL + "skills/compaction_requirements.md",
    NEW + "AGENTS.MD",
    NEW + "behavioral_guidelines/user_onboarding_flow.md",
    NEW + "skills/first_time_profile_setup.md",
    NEW + "skills/onboarding_completion_and_next_step.md",
    SYNAPTIC_FLOW,
])
def test_entry_routes_reference_the_canonical_bootstrap(relative):
    assert BOOTSTRAP.lower() in normalized(read(relative)), relative


@pytest.mark.parametrize("relative", [
    "AGENTS.MD",
    GENERAL + "policies/policy_skills.md",
])
def test_old_contract_immediately_after_entrypoint_order_is_not_reintroduced(relative):
    text = normalized(read(relative))
    for path in ("agents.md", "context_compass/agents.md"):
        assert f"in full immediately after {path}" not in text, relative


@pytest.mark.parametrize("relative", [
    GENERAL + "skills/self_certification.md",
    GENERAL + "skills/user_approved_certification.md",
    GENERAL + "skills/agent_identity.md",
    GENERAL + "skills/agent_lifecycle.md",
    GENERAL + "skills/mailbox_protocol.md",
    GENERAL + "skills/request_tracking.md",
    GENERAL + "skills/harness_custom_instructions.md",
])
def test_gate_dependents_use_effective_onboarding_authorization(relative):
    assert AUTHORIZATION in normalized(read(relative)), relative


def test_default_token_and_name_are_preserved_and_missing_names_are_not_invented():
    root = normalized(read("AGENTS.MD"))
    bootstrap = normalized(section(read("AGENTS.MD"), BOOTSTRAP))
    assert AUTHORIZATION in bootstrap
    assert "certify: approved" in root
    assert "agent_name" in root
    assert "name" in bootstrap and ("missing" in bootstrap or "unknown" in bootstrap)
    for relative in (
        GENERAL + "skills/self_certification.md",
        GENERAL + "skills/user_approved_certification.md",
        GENERAL + "skills/agent_identity.md",
        GENERAL + "skills/mailbox_protocol.md",
    ):
        text = normalized(read(relative))
        assert "certify: approved" in text, relative
        assert "default" in text, f"Normal certification must remain explicit in {relative}"


def test_folder_readme_does_not_ship_an_active_override():
    text = normalized(read("special_instructions/README.md"))
    assert "markdown" in text
    assert BOOTSTRAP.lower() in text
    assert re.search(r"(does not|no) (activate|grant|provide|set|active).*?(override|waiver)", text), (
        "The folder README must explicitly state it does not activate an override"
    )


def test_project_markdown_is_not_excluded_by_the_role_readme_policy():
    bootstrap = normalized(section(read("AGENTS.MD"), BOOTSTRAP))
    assert "readme" in bootstrap and "markdown" in bootstrap
    for relative in ("AGENTS.MD", GENERAL + "skills/compaction_requirements.md"):
        text = read(relative)
        assert not re.search(r"(?m)^- README reads are allowed", text), relative
        assert "role readme" in normalized(text), relative


def test_maintainer_guidance_distinguishes_project_overrides_from_session_waivers():
    for relative in ("contributor/AGENTS.md", "contributor/agents/recovery.md"):
        text = normalized((REPO_ROOT / relative).read_text(encoding="utf-8"))
        assert "project" in text and "override" in text, relative
        assert "session" in text, relative
        assert "never as a standing rule" not in text, relative
