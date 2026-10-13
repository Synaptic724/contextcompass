"""New-format contract delivery through the standalone script, without hosting writes."""

from __future__ import annotations

import copy
import json
import re

import pytest

from conftest import PKG_ROOT, TOOLS, run_tool, write
from ticket_design import ContractError, digest, initial_metadata, render_new, validate_ticket

pytestmark = pytest.mark.integration
SCRIPT = TOOLS / "ticket_design.py"


def event_note():
    return """- DATETIME: 2026-10-12T12:00:00Z
  EVENT_ID: CREATE-EXAMPLE
  AUTHOR: planner_1
  AUTHOR_ROLE: engineer
  TYPE: FACT
  CLAIM: A new generic ticket was created from the selected design.
  EVIDENCE:
    - src/example.py:1-8
  IMPACT: Ownership, scope and one next step are explicit.
  NEXT: Review scope before actual implementation.
  REREAD: REQUIRED
  SCORE_0_TO_10: 9
"""


@pytest.mark.parametrize("kind", ["epic", "story", "task"])
def test_script_validates_complete_new_ticket_without_editing_it(kind, tmp_path):
    ticket_id = f"{kind.upper()}-2026-10-12-generic"
    data = initial_metadata(PKG_ROOT, ticket_id, "CREATE-EXAMPLE")
    text = render_new(PKG_ROOT, kind, ticket_id, "A generic outcome", "project_owner",
                      "worker_1", "engineer", event_note(), data)
    path = write(tmp_path / f"{kind}.md", text)
    before = path.read_bytes()
    result = run_tool(SCRIPT, "--root", PKG_ROOT, "validate", "--kind", kind, "--ticket", path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "truth/authorization remain separate" in result.stdout
    assert path.read_bytes() == before


@pytest.mark.parametrize("backend", ["local", "github_codex_plugin"])
def test_source_bundle_has_one_selected_template_and_refuses_existing_output(backend, tmp_path):
    output = tmp_path / "contract.md"
    first = run_tool(SCRIPT, "--root", PKG_ROOT, "bundle", "--kind", "story", "--backend", backend, "--out", output)
    assert first.returncode == 0, first.stderr
    original = output.read_bytes()
    bundle_text = output.read_text(encoding="utf-8")
    assert "ordinary chat messages need no name/role prefix" in bundle_text
    assert "Authored responses, posts" not in bundle_text
    sources = re.findall(r"<!-- SOURCE: (.*?); sha256: ([0-9a-f]{64}) -->", bundle_text)
    assert len({path for path, _ in sources}) == len(sources)
    for path, sha in sources:
        assert digest((PKG_ROOT / path).read_text(encoding="utf-8")) == sha
    assert ("templates/story_template.md", digest((PKG_ROOT / "templates/story_template.md").read_text())) in sources
    second = run_tool(SCRIPT, "--root", PKG_ROOT, "bundle", "--kind", "story", "--backend", backend, "--out", output)
    assert second.returncode == 2
    assert output.read_bytes() == original


def test_rejected_ticket_is_unchanged_and_not_promoted_to_acceptance(tmp_path):
    ticket_id = "TASK-2026-10-12-generic"
    data = initial_metadata(PKG_ROOT, ticket_id, "CREATE-EXAMPLE")
    text = render_new(PKG_ROOT, "task", ticket_id, "A generic outcome", "project_owner",
                      "worker_1", "engineer", event_note(), data)
    invalid = copy.deepcopy(data)
    invalid.update(phase="acceptance", execution="idle", resolution="accepted")
    changed = text.replace(json.dumps(data, indent=2), json.dumps(invalid, indent=2))
    path = write(tmp_path / "task.md", changed)
    before = path.read_bytes()
    result = run_tool(SCRIPT, "--root", PKG_ROOT, "validate", "--kind", "task", "--ticket", path)
    assert result.returncode == 2
    assert path.read_bytes() == before


def test_generic_custom_template_survives_new_ticket_rendering(tmp_path):
    config = (PKG_ROOT / "config/context_compass_config.yaml").read_text()
    write(tmp_path / "config/context_compass_config.yaml", config.replace("task: templates/task_template.md", "task: user_defined/custom_task.md"))
    for relative in ("templates/ticket_contract.json", "templates/task_template.md",
                     "agent_onboarding/default/general/skills/execution_contract.md"):
        write(tmp_path / relative, (PKG_ROOT / relative).read_text())
    custom_text = (PKG_ROOT / "templates/task_template.md").read_text().replace(
        "<!-- END USER-DEFINED: project_fields -->", "- CUSTOM_CONVENTION: keep exactly\n<!-- END USER-DEFINED: project_fields -->")
    custom = write(tmp_path / "user_defined/custom_task.md", custom_text)
    before = custom.read_bytes()
    ticket_id = "TASK-2026-10-12-custom"
    data = initial_metadata(tmp_path, ticket_id, "CREATE-EXAMPLE")
    rendered = render_new(tmp_path, "task", ticket_id, "Custom scoped outcome", "project_owner",
                          "worker_1", "engineer", event_note(), data)
    assert "- CUSTOM_CONVENTION: keep exactly\n" in rendered
    assert custom.read_bytes() == before
    assert validate_ticket(tmp_path, rendered, "task") == data


def test_identity_rules_name_ticket_contributions_without_account_inference():
    identity = (PKG_ROOT / "agent_onboarding/default/general/skills/agent_identity.md").read_text()
    assert "Ticket bodies, Notes and ticket comments must identify" in identity
    assert "Sign each authored ticket post, comment, and structured Note" in identity
    assert "not the model name, runtime UUID, publishing account, or ticket Owner" in " ".join(identity.split())
    assert "neither a per-post approval gate nor a posting cadence" in identity
    for kind in ("epic", "story", "task"):
        template = (PKG_ROOT / f"templates/{kind}_template.md").read_text()
        assert "AUTHOR:" in template and "AUTHOR_ROLE:" in template
        assert "## Contribution Attribution" in template
        assert "Ticket/Work Author(s)" in template and "Published By" in template and "Independent Review" in template


@pytest.mark.parametrize("relative", [
    "agent_onboarding/default/general/skills/agent_identity.md",
    "agent_onboarding/default/general/AGENTS.MD",
    "agent_onboarding/default/general/skills/agent_stance.md",
    "templates/ticket_contract.json",
    "../../README.md",
])
def test_mandatory_name_role_attribution_is_ticket_scoped_not_chat_scoped(relative):
    text = " ".join((PKG_ROOT / relative).read_text(encoding="utf-8").split()).lower()
    assert "ticket bodies, notes and ticket comments" in text
    assert any(exemption in text for exemption in (
        "ordinary chat messages do not require a name/role prefix",
        "ordinary chat messages do not need a name/role prefix",
        "ordinary chat messages need no name/role prefix",
    ))
    assert "prefix user-facing responses" not in text
    assert "represent yourself in responses" not in text
    assert "authored responses, posts" not in text


@pytest.mark.parametrize("kind", ["task", "story", "epic"])
@pytest.mark.parametrize("backend", ["local", "github_codex_plugin"])
def test_generated_contract_carries_routine_closure_and_linked_evidence(kind, backend, tmp_path):
    output = tmp_path / f"{kind}-{backend}.md"
    result = run_tool(SCRIPT, "--root", PKG_ROOT, "bundle", "--kind", kind,
                      "--backend", backend, "--out", output)
    assert result.returncode == 0, result.stdout + result.stderr
    text = " ".join(output.read_text(encoding="utf-8").split()).lower()
    for phrase in ("authorized agents close routine completed work",
                   "reserved owner decisions still wait", "self-checks are not independent review",
                   "unchanged checks/acks", "material limits", "retrievable",
                   "child completion does not accept the parent",
                   "delegated acceptance or reserved-owner disposition"):
        assert phrase in text, (kind, backend, phrase)
    template = (PKG_ROOT / f"templates/{kind}_template.md").read_text(encoding="utf-8")
    assert template in output.read_text(encoding="utf-8")
