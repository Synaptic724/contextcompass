# SKILLS.MD - line_copy_editor

Purpose
- Define required baseline skills for the line_copy_editor role.
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
- `agent_onboarding/default/line_copy_editor/AGENTS.MD`
- `agent_onboarding/default/line_copy_editor/WORKFLOWS.MD`
- `agent_onboarding/default/line_copy_editor/skills/line_copy_editor.md`
- `agent_onboarding/default/line_copy_editor/skills/line_copy_editor_execution.md`
- `agent_onboarding/default/line_copy_editor/skills/line_copy_editor_deliverables.md`
- `agent_onboarding/default/line_copy_editor/policies/line_copy_editor_quality_policy.md`
- `agent_onboarding/default/line_copy_editor/policies/line_copy_editor_handoff_policy.md`
- `agent_onboarding/default/line_copy_editor/behavioral_guidelines/line_copy_editor_workflow.md`
- `agent_onboarding/default/line_copy_editor/examples/line_copy_editor_task_flow.md`

On-demand role-context skills (lazy readset index)

- `agent_onboarding/default/line_copy_editor/skills/line_copy_editor_advanced_context.md`
  - Covers: the extra requirements for advanced line copy editor work.
  - Trigger: any one of these.
    - Task requires multi-voice register harmonization.
    - Task requires style conversion for a different target market.
    - Task requires compressed copy edit under strict turnaround.
  - Do not proceed in that specialized scope until this file is read.
