"""Source-policy and structural regressions, not live agent or hosting behavior."""

from __future__ import annotations

import copy
import json
import re
import shutil

import pytest

from conftest import PKG_ROOT
from ticket_design import (
    ContractError, bundle, digest, initial_metadata, native_projection, render_new, transition,
    validate_attribution, validate_ticket,
)

pytestmark = pytest.mark.unit
GENERAL = PKG_ROOT / "agent_onboarding/default/general"


def normalized(path):
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def event_note(event, evidence="src/example.py:1-5"):
    return f"""- DATETIME: 2026-10-14T12:00:00Z
  EVENT_ID: {event}
  AUTHOR: builder_1
  AUTHOR_ROLE: engineer
  TYPE: FACT
  CLAIM: The current scoped transition and supporting evidence are recorded.
  EVIDENCE:
    - {evidence}
  IMPACT: Current state is explicit without copying detailed reports.
  NEXT: Continue the next authorized step.
  REREAD: HELPFUL
  SCORE_0_TO_10: 8
"""


@pytest.mark.parametrize("relative", [
    "AGENTS.MD", "behavioral_guidelines/work_intake_and_execution.md",
    "policies/policy_skills.md",
])
def test_owning_policies_do_not_reinstate_per_edit_approval(relative):
    text = normalized(GENERAL / relative)
    assert "within authorized scope" in text
    assert "no per-step approval" in text
    assert "reserved" in text and "security" in text
    for obsolete in (
        "treat all edits as requiring explicit confirmation",
        "wait for explicit approval before edits",
        "only after explicit confirmation",
        "share it and wait for approval",
    ):
        assert obsolete not in text


def test_discovery_has_both_eligible_and_unauthorized_boundaries():
    text = normalized(GENERAL / "skills/ticketing.md")
    for phrase in (
        "outside the currently managed workstream", "authorized repository",
        "self-accept", "exact help request", "does not grant new access",
        "complete authorized outcome", "required tests", "required reviews",
    ):
        assert phrase in text


def test_inherited_lifecycle_does_not_reintroduce_routine_confirmation():
    text = normalized(GENERAL / "skills/agent_lifecycle.md")
    assert "only after confirmation" not in text
    assert "ticketing.md" in text
    assert "required tests/reviews" in text
    assert "reserved" in text


def test_engineer_policy_inherits_authorized_work_without_per_edit_confirmation():
    text = normalized(PKG_ROOT / "agent_onboarding/default/engineer/AGENTS.MD")
    assert "all** edits as requiring explicit confirmation" not in text
    assert "explicit confirmation, every time" not in text
    assert "within authorized scope" in text
    assert "no per-step approval" in text
    assert "reserved" in text and "security" in text


@pytest.mark.parametrize("relative", [
    "AGENTS.MD", "skills/ticketing.md", "skills/ticket_microcycle.md",
    "skills/workflow.md", "skills/active_documentation.md",
    "skills/github/workflow.md", "skills/github/codex_plugin.md",
    "skills/context_window_budget.md",
    "../engineer/behavioral_guidelines/task_execution_and_validation.md",
])
def test_distinct_findings_can_use_multiple_comments_without_body_copy(relative):
    text = normalized(GENERAL / relative)
    assert "multiple meaningful comments" in text
    assert "no forced" in text and "body" in text
    assert "history" in text or "historical" in text
    assert "attribut" in text or "author" in text


@pytest.mark.parametrize("relative", [
    "skills/github/workflow.md", "skills/github/codex_plugin.md",
    "skills/ticket_design.md", "skills/codex_mcp.md",
])
def test_busy_body_writer_does_not_own_independent_append_only_comments(relative):
    text = normalized(GENERAL / relative)
    assert "append-only comment" in text
    assert "body-writer permission" in text
    assert "full-body" in text and "overlapping" in text
    assert "readback" in text


def test_unavailable_and_denied_comment_operations_are_distinct():
    text = normalized(GENERAL / "skills/github/codex_plugin.md")
    for phrase in (
        "capability gap", "not a permission denial", "pr_number",
        "do not assume", "denied action", "do not switch", "readback",
    ):
        assert phrase in text


@pytest.mark.parametrize("kind", ["task", "story", "epic"])
def test_current_resume_view_is_not_an_append_only_history_replay(kind):
    text = normalized(PKG_ROOT / f"templates/{kind}_template.md")
    for phrase in (
        "one current resume view", "scope/outcome", "decisions/holds",
        "source/evidence revision", "completed/remaining", "failed/unrun",
        "owners", "next 1-3 actions", "historical",
    ):
        assert phrase in text


def test_reread_relevance_and_actual_recovery_are_not_blanket_checkpoint_rules():
    text = normalized(GENERAL / "skills/context_compaction.md")
    for phrase in (
        "one current resume view", "ordinary comment", "required", "helpful",
        "relevance", "mandatory", "re-onboard", "history",
    ):
        assert phrase in text
    ticketing = normalized(GENERAL / "skills/ticketing.md")
    assert "not a default maximum" in ticketing
    assert "failed or unrun required tests" in ticketing


def test_microcycle_switch_stays_enabled_but_does_not_force_body_copy():
    text = normalized(PKG_ROOT / "config/context_compass_config.yaml")
    assert "require_note_before_continue: true" in text
    assert "minimum_note_score: 7" in text
    assert "comment" in text and "no forced body copy" in text


@pytest.mark.parametrize("backend", ["local", "github_codex_plugin"])
def test_source_bundle_delivers_the_comment_boundary_without_a_second_rulebook(backend):
    text = " ".join(bundle(PKG_ROOT, "task", backend).split()).lower()
    for phrase in (
        "multiple meaningful comments", "no forced", "append-only comments",
        "full-body", "required tests", "reserved", "history",
    ):
        assert phrase in text


def test_three_external_findings_need_links_not_copied_reports_and_stale_body_fails():
    """The real body helper preserves linked evidence; no comment API is simulated."""
    ticket_id = "TASK-2026-10-14-example"
    metadata = initial_metadata(PKG_ROOT, ticket_id, "CREATE")
    original = render_new(PKG_ROOT, "task", ticket_id, "Generic authorized outcome",
                          "project_owner", "builder_1", "engineer", event_note("CREATE"),
                          metadata)
    original = original.replace("<!-- END USER-DEFINED: project_fields -->",
                                "- CUSTOM: retain exactly\n<!-- END USER-DEFINED: project_fields -->")
    comments = [f"https://github.com/example/project/issues/1#issuecomment-{n}" for n in (1, 2, 3)]
    linked = event_note("START", "\n    - ".join(comments))
    next_data = copy.deepcopy(metadata)
    next_data.update(revision=2, phase="implementation", execution="active", last_event_id="START")
    next_data["evidence_refs"].update(transition="START", start="START")
    changed = transition(PKG_ROOT, original, "task", next_data, linked, 1, digest(original))
    assert all(url in changed for url in comments)
    assert event_note("CREATE").strip() in changed
    assert "- CUSTOM: retain exactly\n" in changed
    assert len(re.findall(r"(?m)^- DATETIME:", changed)) == 2
    assert validate_ticket(PKG_ROOT, changed, "task") == next_data
    with pytest.raises(ContractError, match="Stale"):
        transition(PKG_ROOT, original + "another body writer's edit\n", "task",
                   next_data, linked, 1, digest(original))


def test_real_onboarding_security_and_review_gates_remain_in_the_source():
    root = normalized(PKG_ROOT / "AGENTS.MD")
    assert "certify: approved" in root
    assert "re-onboarding" in root and "baseline" in root
    text = normalized(GENERAL / "skills/ticketing.md")
    assert "reserved owner decisions still wait" in text
    assert "self-checks are not independent" in text
    assert "denied" in text and "uncertain" in text


@pytest.mark.parametrize("relative", [
    "skills/ticketing.md", "skills/workflow.md", "skills/github/workflow.md",
    "skills/github/codex_plugin.md", "skills/ticket_design.md",
])
def test_qualified_reviewer_direct_closure_is_full_current_acceptance_not_a_new_gate(relative):
    text = normalized(GENERAL / relative)
    assert "qualified independent reviewer" in text
    if relative != "skills/ticketing.md":
        assert "ticketing.md" in text


def test_canonical_reviewer_rule_retains_whole_ticket_and_authority_limits():
    text = normalized(GENERAL / "skills/ticketing.md")
    for phrase in (
        "qualified independent reviewer", "all ticket criteria", "current-revision evidence",
        "scoped pass", "reserved", "no extra coordinator approval", "not required for every",
    ):
        assert phrase in text, phrase


@pytest.mark.parametrize("kind", ["task", "story", "epic"])
def test_selected_templates_preserve_qualified_reviewer_completion_path(kind):
    text = normalized(PKG_ROOT / f"templates/{kind}_template.md")
    assert "qualified independent reviewer" in text
    assert "ticketing.md" in text


def test_source_bound_metadata_has_no_silent_historical_rebind(tmp_path):
    ticket_id = "TASK-2026-10-14-source-bound-example"
    original_data = initial_metadata(PKG_ROOT, ticket_id, "CREATE")
    original = render_new(PKG_ROOT, "task", ticket_id, "Generic source-bound work",
                          "project_owner", "builder_1", "engineer", event_note("CREATE"),
                          original_data)
    changed_root = tmp_path / "package"
    shutil.copytree(PKG_ROOT, changed_root)
    path = changed_root / "templates/ticket_contract.json"
    spec = json.loads(path.read_text(encoding="utf-8"))
    spec["policy"].append("Different policy text for the source-binding control.")
    path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    changed_data = initial_metadata(changed_root, ticket_id, "CREATE")
    assert changed_data["contract_ref"] != original_data["contract_ref"]
    original_hash = digest(original)
    with pytest.raises(ContractError, match="profile/schema/source"):
        validate_ticket(changed_root, original, "task")
    next_data = copy.deepcopy(changed_data)
    next_data.update(revision=2, execution="active", phase="implementation", last_event_id="START")
    next_data["evidence_refs"].update(transition="START", start="START")
    with pytest.raises(ContractError, match="profile/schema/source"):
        transition(changed_root, original, "task", next_data, event_note("START"),
                   1, original_hash)
    assert digest(original) == original_hash
    fresh = render_new(changed_root, "task", ticket_id, "Generic source-bound work",
                       "project_owner", "builder_1", "engineer", event_note("CREATE"),
                       changed_data)
    assert validate_ticket(changed_root, fresh, "task") == changed_data
    guidance = normalized(GENERAL / "skills/ticket_design.md")
    assert "policy-only" in guidance and "no rebind command" in guidance


def acceptance_fixture(actor="reviewer_1"):
    ticket_id = "TASK-2026-10-14-acceptance-example"
    original_data = initial_metadata(PKG_ROOT, ticket_id, "CREATE")
    original = render_new(PKG_ROOT, "task", ticket_id, "Generic accepted outcome",
                          "project_owner", "builder_1", "engineer", event_note("CREATE"),
                          original_data)
    data = copy.deepcopy(original_data)
    data.update(revision=2, phase="acceptance", execution="idle", resolution="accepted",
                last_event_id="ACCEPT")
    data["evidence_refs"] = {key: "ACCEPT" for key in
                             ("transition", "acceptance", "validation", "children", "routing")}
    note = event_note("ACCEPT").replace("AUTHOR: builder_1", f"AUTHOR: {actor}")
    note += ("  ACCEPTANCE: authorized\n  VALIDATION: recorded\n"
             "  CHILDREN: dispositioned\n  ROUTING: reconciled\n")
    return original, data, note


@pytest.mark.parametrize("actor", ["builder_1", "reviewer_1"])
def test_authorized_owner_or_reviewer_completion_is_separate_from_native_close(actor):
    original, data, note = acceptance_fixture(actor)
    accepted = transition(PKG_ROOT, original, "task", data, note, 1, digest(original))
    assert validate_ticket(PKG_ROOT, accepted, "task")["resolution"] == "accepted"
    pending = native_projection(PKG_ROOT, accepted, "task", "open")
    assert pending["state"] == "closed" and pending["result"] == "projection_pending"
    assert native_projection(PKG_ROOT, accepted, "task", "closed")["result"] == "consistent"


@pytest.mark.parametrize("field,value", [
    ("ACCEPTANCE", "authorized"), ("VALIDATION", "recorded"),
    ("CHILDREN", "dispositioned"), ("ROUTING", "reconciled"),
])
def test_scoped_or_incomplete_evidence_cannot_establish_full_acceptance(field, value):
    original, data, note = acceptance_fixture()
    incomplete = note.replace(f"  {field}: {value}\n", "")
    with pytest.raises(ContractError, match="Acceptance requires explicit gate conclusions"):
        transition(PKG_ROOT, original, "task", data, incomplete, 1, digest(original))


def test_self_authored_review_cannot_be_relabelled_independent():
    attribution = {
        "authors": [{"actor": "builder_1", "role": "engineer", "kind": "implementation",
                     "scope": "source", "revision": "R1", "evidence_ref": "source.py:1-5"}],
        "published_by": {"service": "fixture", "account": "fixture", "receipt_ref": "receipt"},
        "reviews": [{"actor": "builder_1", "role": "reviewer", "scope": "source",
                     "target_revision": "R1", "verdict": "pass", "evidence_ref": "review:1-5",
                     "independent": True}],
    }
    with pytest.raises(ContractError, match="author/material editor"):
        validate_attribution(PKG_ROOT, attribution)


def test_scoped_review_pass_does_not_implicitly_accept_or_close():
    ticket_id = "TASK-2026-10-14-scoped-review-example"
    data = initial_metadata(PKG_ROOT, ticket_id, "CREATE")
    attribution = {
        "authors": [{"actor": "builder_1", "role": "engineer", "kind": "implementation",
                     "scope": "source", "revision": "R1", "evidence_ref": "source.py:1-5"}],
        "published_by": {"service": "fixture", "account": "fixture", "receipt_ref": "receipt"},
        "reviews": [{"actor": "reviewer_1", "role": "reviewer", "scope": "one clause",
                     "target_revision": "R1", "verdict": "pass", "evidence_ref": "review:1-5",
                     "independent": True}],
    }
    draft = render_new(PKG_ROOT, "task", ticket_id, "Generic partial review",
                       "project_owner", "builder_1", "engineer", event_note("CREATE"),
                       data, attribution)
    assert validate_ticket(PKG_ROOT, draft, "task")["resolution"] == "unresolved"
    assert native_projection(PKG_ROOT, draft, "task", "open")["state"] == "open"
