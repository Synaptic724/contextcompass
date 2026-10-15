"""Guard the delegated lifecycle correction without adding a runtime engine."""

from pathlib import Path

import pytest

from conftest import PKG_ROOT


GENERAL = PKG_ROOT / "agent_onboarding/default/general"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


@pytest.mark.parametrize("relative", [
    "AGENTS.MD", "skills/ticketing.md", "skills/workflow.md",
    "skills/github/workflow.md", "skills/github/codex_plugin.md",
    "behavioral_guidelines/work_intake_and_execution.md",
    "../engineer/behavioral_guidelines/task_execution_and_validation.md",
])
def test_routine_closure_is_delegated_but_reserved_decisions_wait(relative):
    text = normalized(GENERAL / relative)
    assert "authorized agents close routine completed work" in text
    assert "required tests" in text and "required reviews" in text
    assert "reserved owner decisions still wait" in text
    assert "without another owner ping" in text
    assert "ask the user to confirm acceptance" not in text
    assert "only after explicit confirmation" not in text


@pytest.mark.parametrize("relative", [
    "AGENTS.MD", "skills/ticketing.md", "skills/workflow.md",
    "skills/github/workflow.md", "skills/github/codex_plugin.md",
    "behavioral_guidelines/work_intake_and_execution.md",
    "../engineer/behavioral_guidelines/task_execution_and_validation.md",
])
def test_scoped_review_and_author_independence_remain_explicit(relative):
    text = normalized(GENERAL / relative)
    assert "review is proportionate" in text
    assert "uncertainty" in text and "contract" in text
    assert "self-checks are not independent" in text


@pytest.mark.parametrize("relative", [
    "skills/ticketing.md", "skills/workflow.md", "skills/ticket_microcycle.md",
    "skills/github/workflow.md", "skills/github/codex_plugin.md",
])
def test_concise_linked_evidence_does_not_replace_state_or_history(relative):
    text = normalized(GENERAL / relative)
    for phrase in ("claim", "impact", "material limits", "next action", "retrievable",
                   "full linked reports", "unchanged checks/acks", "in-body state"):
        assert phrase in text, (relative, phrase)
    assert "history" in text or "prior notes" in text


def test_parent_synthesis_does_not_accept_parent_from_child_completion():
    for relative in ("skills/ticketing.md", "skills/workflow.md",
                     "skills/ticket_microcycle.md", "skills/github/workflow.md"):
        text = normalized(GENERAL / relative)
        assert "child completion does not accept the parent" in text
        assert "remaining work" in text


@pytest.mark.parametrize("kind", ["task", "story", "epic"])
def test_templates_keep_attribution_with_delegated_or_reserved_acceptance(kind):
    text = normalized(PKG_ROOT / f"templates/{kind}_template.md")
    assert "delegated acceptance or reserved-owner disposition" in text
    assert "author:" in text and "author_role:" in text
    assert "ticket/work author(s)" in text and "published by" in text
    assert "independent review" in text
    assert "acceptance criteria confirmed by user" not in text


def test_microcycle_and_plugin_safety_gates_are_not_waived():
    microcycle = normalized(GENERAL / "skills/ticket_microcycle.md")
    for term in ("strict", "relaxed", "onboarding/reentry", "evidence timing",
                 "denied/uncertain-write", "note-quality"):
        assert term in microcycle
    plugin = normalized(GENERAL / "skills/github/codex_plugin.md")
    for term in ("read the latest complete body", "historical note", "fetch again",
                 "re-read and recompose", "do not infer authority from tool access",
                 "ambiguous create", "stop and reconcile"):
        assert term in plugin
