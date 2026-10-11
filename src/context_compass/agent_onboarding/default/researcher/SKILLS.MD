# SKILLS.MD - researcher

Purpose
- Define required baseline skills for the researcher role.
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
- `agent_onboarding/default/researcher/AGENTS.MD`
- `agent_onboarding/default/researcher/WORKFLOWS.MD`
- `agent_onboarding/default/researcher/skills/researcher.md`
- `agent_onboarding/default/researcher/skills/researcher_execution.md`
- `agent_onboarding/default/researcher/skills/researcher_deliverables.md`
- `agent_onboarding/default/researcher/policies/researcher_quality_policy.md`
- `agent_onboarding/default/researcher/policies/researcher_handoff_policy.md`
- `agent_onboarding/default/researcher/behavioral_guidelines/researcher_workflow.md`
- `agent_onboarding/default/researcher/examples/researcher_task_flow.md`

On-demand role-context skills
Trigger conditions (any one makes these mandatory):
- Task requires domain-specific expert emulation with source ranking.
- Task requires period-authenticity or jurisdiction-sensitive details.
- Task requires fast-turnaround research under strict evidence budget.

If triggered:
- `agent_onboarding/default/researcher/skills/researcher_advanced_context.md`
- Do not proceed in this specialized scope until the on-demand read is satisfied.
