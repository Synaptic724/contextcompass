# SKILLS.MD - developmental_editor

Purpose
- Define required baseline skills for the developmental_editor role.
- This role is optimized for fiction-book workflow specialization.

Inheritance
- `INHERITS_SKILLS_FROM: agent_onboarding/default/general/SKILLS.MD`

Skill classes (non-negotiable)
- This role ADDS two classes of its own:
  A) Required baseline skills (always required for onboarding/certification)
  B) On-demand role-context skills (required only when the active task triggers them)
- It also INHERITS the parent chain's classes. `general` contributes shared
  baseline skills and only the backend baseline selected by YAML. This section
  describes what this file adds; it is not the complete list of required reads.

Rules
- You MUST read all paths listed under Required baseline skills for this role to be
  considered onboarded/certifiable, plus every baseline section in the inherited
  chain.
- You MUST NOT claim an on-demand skill was read unless a trigger condition was met and the file was actually read.
- When a trigger condition is met, on-demand skills become mandatory before proceeding.

Required baseline skills
- `agent_onboarding/default/developmental_editor/AGENTS.MD`
- `agent_onboarding/default/developmental_editor/WORKFLOWS.MD`
- `agent_onboarding/default/developmental_editor/skills/developmental_editor.md`
- `agent_onboarding/default/developmental_editor/skills/developmental_editor_execution.md`
- `agent_onboarding/default/developmental_editor/skills/developmental_editor_deliverables.md`
- `agent_onboarding/default/developmental_editor/policies/developmental_editor_quality_policy.md`
- `agent_onboarding/default/developmental_editor/policies/developmental_editor_handoff_policy.md`
- `agent_onboarding/default/developmental_editor/behavioral_guidelines/developmental_editor_workflow.md`
- `agent_onboarding/default/developmental_editor/examples/developmental_editor_task_flow.md`

On-demand role-context skills
Trigger conditions (any one makes these mandatory):
- Task requires triage for heavily fragmented or incomplete manuscripts.
- Task requires genre-specific structural redesign.
- Task requires accelerated pre-release structural recovery.

If triggered:
- `agent_onboarding/default/developmental_editor/skills/developmental_editor_advanced_context.md`
- Do not proceed in this specialized scope until the on-demand read is satisfied.
