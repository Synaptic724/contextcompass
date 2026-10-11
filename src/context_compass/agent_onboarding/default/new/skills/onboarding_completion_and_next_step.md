
# onboarding_completion_and_next_step

Purpose
- Define how to finish `new` onboarding cleanly and transition to steady-state.

Completion sequence
Apply `AGENTS.MD` / Project Instructions Bootstrap before the default setup
and role prompts below. Do not repeat a waived step or declare skipped reads completed.

1) Confirm user understands:
   - system purpose,
   - profile class model,
   - configuration authority.
   - how personal custom instructions can direct recovery after compaction.
   Follow `agent_onboarding/default/general/skills/harness_custom_instructions.md`
   for the presence check and optional setup form. Do not repeat a completed or
   declined form, and do not treat existing integration as missing.
2) Present role options by reading the registry table in
   `context_compass/SKILLS.MD` and offering every role whose
   `selectable after onboarding` column is `yes`. The descriptions below are
   a convenience gloss for the shipped default roles, not the list itself:
   - `general` (shared baseline)
   - `engineer` (recommended default)
   - `design_engineer` (design/architecture/handoff)
   - `platform_engineer` (CI/CD/deploy/observability/ops)
   - `qa_engineer` (test strategy/quality gates/release signoff)
   - `security_engineer` (security review/threat modeling/hardening)
   - `story_designer` (fiction narrative architecture)
   - `story_novel_artist` (fiction visual language and art direction)
   - `researcher` (evidence-backed plausibility and constraints)
   - `draft_writer` (manuscript drafting and rewrites)
   - `developmental_editor` (structural editing and rewrite planning)
   - `line_copy_editor` (line-level prose polish)
   - `continuity_fact_checker` (canon/timeline/fact validation)
   - `proofreader` (final lock for surface quality and formatting)
3) Recommend `engineer` explicitly for general code-development work.
4) If the user requests a specialized posture, recommend the matching role instead.
5) Confirm selected class and align config guidance.
6) State next action:
   - continue onboarding via selected class path map.

Recommended wording
- "Onboarding is complete. Role options are `general`, `engineer`,
  `design_engineer`, `platform_engineer`, `qa_engineer`, `security_engineer`,
  `story_designer`, `story_novel_artist`, `researcher`, `draft_writer`,
  `developmental_editor`, `line_copy_editor`, `continuity_fact_checker`,
  or `proofreader`.
  For general code development, `engineer` is recommended. Which do you want to
  use for this session?"

Exit criteria
- Selected role is explicit.
- User is informed a role is selected at each onboarding, not stored in config.
- Next read path is clear and deterministic.
- Resolved Project Instructions Bootstrap replacements/waivers carry forward;
  later role defaults do not reinstate them.

References
- `agent_onboarding/default/new/skills/configuration_map_guide.md`
- `config/context_compass_config.yaml`
- `SKILLS.MD`
