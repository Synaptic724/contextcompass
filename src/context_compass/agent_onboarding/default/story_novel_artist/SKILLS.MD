# SKILLS.MD - story_novel_artist

Purpose
- Define required baseline skills for the story_novel_artist role.
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
- `agent_onboarding/default/story_novel_artist/AGENTS.MD`
- `agent_onboarding/default/story_novel_artist/WORKFLOWS.MD`
- `agent_onboarding/default/story_novel_artist/skills/story_novel_artist.md`
- `agent_onboarding/default/story_novel_artist/skills/story_novel_artist_execution.md`
- `agent_onboarding/default/story_novel_artist/skills/story_novel_artist_deliverables.md`
- `agent_onboarding/default/story_novel_artist/policies/story_novel_artist_quality_policy.md`
- `agent_onboarding/default/story_novel_artist/policies/story_novel_artist_handoff_policy.md`
- `agent_onboarding/default/story_novel_artist/behavioral_guidelines/story_novel_artist_workflow.md`
- `agent_onboarding/default/story_novel_artist/examples/story_novel_artist_task_flow.md`

On-demand role-context skills
Trigger conditions (any one makes these mandatory):
- Task requires style transfer across books in a series.
- Task requires publishing-channel-specific art packaging variants.
- Task requires model/provider migration without losing visual canon.

If triggered:
- `agent_onboarding/default/story_novel_artist/skills/story_novel_artist_advanced_context.md`
- Do not proceed in this specialized scope until the on-demand read is satisfied.
