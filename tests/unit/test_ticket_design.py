"""Declared future contract checks, not proof of authorization or live agent behavior."""

from __future__ import annotations

import copy
import json
import re

import pytest

from conftest import PKG_ROOT, write
from ticket_design import (
    ContractError, bundle, definition, design_instructions, digest, future_status, initial_metadata,
    native_projection, render_new, settings, template_path, transition,
    validate_attribution, validate_note, validate_ticket,
)

pytestmark = pytest.mark.unit


def note(event="EV-CREATE", author="builder_1", role="engineer", score=9, kind="FACT"):
    return f"""- DATETIME: 2026-10-12T12:00:00Z
  EVENT_ID: {event}
  AUTHOR: {author}
  AUTHOR_ROLE: {role}
  TYPE: {kind}
  CLAIM: Scoped work and its actual evidence are recorded.
  EVIDENCE:
    - src/example.py:1-5
  IMPACT: The named scope and next action are explicit.
  NEXT: Execute the next authorized single step.
  REREAD: REQUIRED
  SCORE_0_TO_10: {score}
"""


def make(kind="task", agile=True, attribution=None):
    ticket_id = f"{kind.upper()}-2026-10-12-example"
    metadata = initial_metadata(PKG_ROOT, ticket_id, "EV-CREATE") if agile else None
    text = render_new(PKG_ROOT, kind, ticket_id, "Generic scoped outcome", "coordinator_1",
                      "builder_1", "engineer", note(), metadata, attribution)
    return text, metadata


def replace_metadata(text, data):
    return re.sub(r"(?ms)(<!-- BEGIN AGILE_METADATA -->\n```json\n).*?(\n```\n<!-- END AGILE_METADATA -->)",
                  lambda match: match[1] + json.dumps(data, indent=2) + match[2], text)


@pytest.mark.parametrize("kind", ["epic", "story", "task"])
@pytest.mark.parametrize("agile", [False, True])
def test_optional_design_keeps_complete_named_composition(kind, agile):
    text, metadata = make(kind, agile)
    canonical = (PKG_ROOT / f"templates/{kind}_template.md").read_text(encoding="utf-8")
    assert re.findall(r"(?m)^## .+$", canonical) == re.findall(r"(?m)^## .+$", text)
    assert "- Owner: coordinator_1" in text
    assert "- Agent Name: builder_1" in text
    assert "- Agent Role: engineer" in text
    assert "AUTHOR: builder_1" in text and "AUTHOR_ROLE: engineer" in text
    assert validate_ticket(PKG_ROOT, text, kind) == metadata
    assert ("BEGIN AGILE_METADATA" in text) is agile


@pytest.mark.parametrize("field,value", [
    ("phase", "invented"), ("execution", "running"), ("resolution", "closed"),
    ("revision", True), ("revision", 0), ("schema_version", True),
    ("profile", "agile"), ("profile", {"id": "agile", "version": True}),
    ("contract_ref", "unverified"), ("ticket_id", "TASK-2026-10-12-other"),
])
def test_invalid_metadata_is_rejected_without_a_write(field, value):
    text, metadata = make()
    metadata[field] = value
    with pytest.raises(ContractError):
        validate_ticket(PKG_ROOT, replace_metadata(text, metadata), "task")


@pytest.mark.parametrize("phase", definition(PKG_ROOT)[0]["phases"])
@pytest.mark.parametrize("execution", definition(PKG_ROOT)[0]["execution"])
def test_phase_and_execution_are_orthogonal(phase, execution):
    text, metadata = make()
    metadata.update(phase=phase, execution=execution)
    metadata["evidence_refs"].update({key: "EV-CREATE" for key in ("readiness", "start", "blocker", "pause")})
    text = replace_metadata(text, metadata)
    text = re.sub(r"(?m)^- Status:.*$", lambda _: "- Status: " + future_status(metadata), text)
    assert validate_ticket(PKG_ROOT, text, "task") == metadata


@pytest.mark.parametrize("resolution", ["accepted", "canceled", "duplicate"])
@pytest.mark.parametrize("execution", ["draft", "ready", "active", "blocked", "paused"])
def test_terminal_resolution_cannot_claim_active_work(resolution, execution):
    text, metadata = make()
    metadata.update(resolution=resolution, execution=execution)
    with pytest.raises(ContractError, match="Terminal"):
        validate_ticket(PKG_ROOT, replace_metadata(text, metadata), "task")


def test_acceptance_needs_idle_phase_and_each_gate_reference():
    text, metadata = make()
    metadata.update(phase="acceptance", execution="idle", resolution="accepted")
    text = replace_metadata(text, metadata)
    with pytest.raises(ContractError, match="evidence"):
        validate_ticket(PKG_ROOT, text, "task")
    metadata["evidence_refs"].update({key: "EV-CREATE" for key in ("acceptance", "validation", "children", "routing")})
    text = replace_metadata(text, metadata)
    text = re.sub(r"(?m)^- Status:.*$", lambda _: "- Status: " + future_status(metadata), text)
    with pytest.raises(ContractError, match="explicit gate"):
        validate_ticket(PKG_ROOT, text, "task")
    text = text.replace("  TYPE: FACT", "  ACCEPTANCE: authorized\n  VALIDATION: recorded\n  CHILDREN: dispositioned\n  ROUTING: reconciled\n  TYPE: FACT")
    assert validate_ticket(PKG_ROOT, text, "task")["resolution"] == "accepted"
    assert native_projection(PKG_ROOT, text, "task", "open")["result"] == "projection_pending"


def test_closed_host_is_never_inferred_as_acceptance():
    text, metadata = make()
    assert native_projection(PKG_ROOT, text, "task", "closed") == {"state": "open", "result": "discrepancy"}
    for resolution in ("canceled", "duplicate"):
        data = copy.deepcopy(metadata)
        data.update(resolution=resolution, execution="idle")
        data["evidence_refs"].update(disposition="EV-CREATE", successor="EV-CREATE")
        changed = replace_metadata(text, data)
        changed = re.sub(r"(?m)^- Status:.*$", lambda _: "- Status: " + future_status(data), changed)
        assert native_projection(PKG_ROOT, changed, "task", "open")["state_reason"] == "not_planned"


def test_unknown_evidence_does_not_drive_the_new_state():
    text, metadata = make()
    text = text.replace("TYPE: FACT", "TYPE: UNKNOWN")
    with pytest.raises(ContractError, match="Unresolved evidence"):
        validate_ticket(PKG_ROOT, text, "task")


def test_transition_preserves_full_history_custom_content_and_is_idempotent():
    text, metadata = make()
    text = text.replace("<!-- END USER-DEFINED: project_fields -->", "- CUSTOM: preserve exact bytes\n<!-- END USER-DEFINED: project_fields -->")
    next_data = copy.deepcopy(metadata)
    next_data.update(revision=2, phase="implementation", execution="active", last_event_id="EV-START")
    next_data["evidence_refs"].update(transition="EV-START", start="EV-START")
    changed = transition(PKG_ROOT, text, "task", next_data, note("EV-START"), 1, digest(text))
    assert note().strip() in changed and note("EV-START").strip() in changed
    assert "- CUSTOM: preserve exact bytes\n" in changed
    assert validate_ticket(PKG_ROOT, changed, "task") == next_data
    assert transition(PKG_ROOT, changed, "task", next_data, note("EV-START"), 2, digest(changed)) == changed
    with pytest.raises(ContractError, match="Conflicting duplicate"):
        transition(PKG_ROOT, changed, "task", next_data, note("EV-START", author="other_1"), 2, digest(changed))
    with pytest.raises(ContractError, match="Stale"):
        transition(PKG_ROOT, text + "human edit\n", "task", next_data, note("EV-START"), 1, digest(text))


def test_pause_retains_phase_and_rejects_conflicting_derived_status():
    text, metadata = make()
    metadata.update(revision=2, phase="test", execution="paused", last_event_id="EV-PAUSE")
    metadata["evidence_refs"].update(transition="EV-PAUSE", pause="EV-PAUSE")
    with pytest.raises(ContractError, match="retains"):
        transition(PKG_ROOT, text, "task", metadata, note("EV-PAUSE"), 1, digest(text))
    with pytest.raises(ContractError, match="derived"):
        validate_ticket(PKG_ROOT, text.replace("planning / draft / unresolved", "done"), "task")


def attribution():
    return {
        "authors": [{"actor": "builder_1", "role": "engineer", "kind": "implementation",
                     "scope": "src/example.py", "revision": "sha256:example", "evidence_ref": "EV-CODE"}],
        "published_by": {"service": "github", "account": "shared_publisher", "receipt_ref": "UNKNOWN"},
        "reviews": [],
    }


def test_shared_publisher_is_not_an_author_or_executor():
    data = attribution()
    data["authors"].append({**data["authors"][0], "actor": "tester_1", "role": "qa_engineer", "kind": "test"})
    validate_attribution(PKG_ROOT, data)
    text, _ = make(attribution=data)
    assert "builder_1" in text and "tester_1" in text and "shared_publisher" in text
    assert "- Owner: coordinator_1" in text and "- Agent Name: builder_1" in text
    with pytest.raises(ContractError, match="readable view"):
        validate_ticket(PKG_ROOT, text.replace("- Published By: {", "- Published By: edited {"), "task")


def test_changing_role_does_not_make_author_review_independent():
    data = attribution()
    review = {"actor": "builder_1", "role": "reviewer", "scope": "src/example.py",
              "target_revision": "sha256:example", "verdict": "pass", "evidence_ref": "EV-REVIEW", "independent": True}
    data["reviews"].append(review)
    with pytest.raises(ContractError, match="independently"):
        validate_attribution(PKG_ROOT, data)
    review["actor"] = "reviewer_1"
    validate_attribution(PKG_ROOT, data)
    review["target_revision"] = "UNKNOWN"
    with pytest.raises(ContractError):
        validate_attribution(PKG_ROOT, data)


def test_note_has_real_identity_and_local_configured_quality(tmp_path):
    for path in ("config/context_compass_config.yaml", "templates/ticket_contract.json",
                 "agent_onboarding/default/general/skills/execution_contract.md"):
        write(tmp_path / path, (PKG_ROOT / path).read_text(encoding="utf-8"))
    config = tmp_path / "config/context_compass_config.yaml"
    config.write_text(config.read_text().replace("minimum_note_score: 7", "minimum_note_score: 10"), encoding="utf-8")
    with pytest.raises(ContractError, match="quality"):
        validate_note(tmp_path, note(score=9))
    assert validate_note(tmp_path, note(score=10))["AUTHOR"] == "builder_1"
    with pytest.raises(ContractError, match="author"):
        validate_note(PKG_ROOT, note(author="UNKNOWN"))


def test_custom_template_selection_stays_inside_project_root(tmp_path):
    config = (PKG_ROOT / "config/context_compass_config.yaml").read_text(encoding="utf-8")
    write(tmp_path / "config/context_compass_config.yaml", config.replace("task: templates/task_template.md", "task: user_defined/my_task.md"))
    custom = write(tmp_path / "user_defined/my_task.md", "# Project-specific complete template\n")
    assert template_path(tmp_path, "task") == custom.resolve()
    cfg = tmp_path / "config/context_compass_config.yaml"
    cfg.write_text(cfg.read_text().replace("user_defined/my_task.md", "../outside.md"), encoding="utf-8")
    with pytest.raises(ContractError, match="leaves"):
        template_path(tmp_path, "task")


@pytest.mark.parametrize("backend", ["local", "github_codex_plugin"])
def test_bundle_delivers_actual_source_and_explicit_host_binding(backend):
    text = bundle(PKG_ROOT, "task", backend)
    assert '"binding_version": 1' in text
    assert f'"backend": "{backend}"' in text
    assert '"minimum_note_score": 7' in text
    spec_text = (PKG_ROOT / "templates/ticket_contract.json").read_text(encoding="utf-8")
    assert spec_text in text
    assert "sha256: " + digest(spec_text) in text
    assert text.count("<!-- SOURCE: templates/task_template.md;") == 1
    assert "templates/story_template.md" not in re.findall(r"<!-- SOURCE: (.*?);", text)
    assert design_instructions(PKG_ROOT) in json.loads(re.search(r"(?s)## Host Binding\n\n```json\n(.*?)\n```", text)[1])["design_instructions"]


def test_unknown_contributor_is_not_guessed_or_independently_cleared():
    data = attribution()
    data["authors"][0].update(actor="UNKNOWN", role="UNKNOWN")
    validate_attribution(PKG_ROOT, data)
    data["reviews"].append({"actor": "reviewer_1", "role": "reviewer", "scope": "src/example.py",
                            "target_revision": "sha256:example", "verdict": "pass", "evidence_ref": "EV-REVIEW", "independent": True})
    with pytest.raises(ContractError, match="independently"):
        validate_attribution(PKG_ROOT, data)


def test_runtime_uuid_is_not_used_as_a_note_author_name():
    with pytest.raises(ContractError, match="author"):
        validate_note(PKG_ROOT, note(author="12345678-1234-1234-1234-123456789abc"))


@pytest.mark.parametrize("mutation", [
    lambda text: text.replace("<!-- END AGILE_METADATA -->", "<!-- END AGILE_METADATA -->\n<!-- END AGILE_METADATA -->"),
    lambda text: text.replace('"schema_version": 1,', '"schema_version": 1, "schema_version": 1,'),
    lambda text: text.replace("- Agent Role: engineer\n", ""),
    lambda text: text.replace("AUTHOR: builder_1", "AUTHOR: UNKNOWN"),
])
def test_malformed_or_ambiguous_authority_is_refused(mutation):
    text, _ = make()
    with pytest.raises(ContractError):
        validate_ticket(PKG_ROOT, mutation(text), "task")


def test_explicit_empty_metadata_is_not_silently_treated_as_non_agile():
    with pytest.raises(ContractError):
        render_new(PKG_ROOT, "task", "TASK-2026-10-12-empty", "Example", "owner_1",
                   "builder_1", "engineer", note(), metadata={})
