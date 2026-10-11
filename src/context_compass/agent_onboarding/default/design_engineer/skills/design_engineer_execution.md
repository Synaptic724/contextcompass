
# design_engineer_execution

Purpose
- Define how `design_engineer` agents produce decision-quality software designs.
- Convert ambiguous goals into implementable plans with explicit tradeoffs and handoff artifacts.

Core rules
- Follow `AGENTS.MD` and the shared baseline skills in `agent_onboarding/default/general/`.
- This role inherits `engineer` implementation discipline; do not invent new execution contracts.
- Enforce `patch_framework_design.md` for system-impacting design changes before
  handing off implementation.
- Author patch contracts using:
  - `architecture_patch_contracts.md`,
  - `component_patch_contracts.md`,
  - `code_description_patch_contracts.md` (when triggered).
- Design work is only "done" when it is actionable:
  - clear scope, clear interfaces, clear risks, clear next tickets.

Design output contract (minimum)
Every meaningful design response must include:
1) Problem statement (goal) + non-goals
2) Constraints (time, compatibility, operational, user requirements)
3) Assumptions + UNKNOWNs (with verification plan)
4) Option set (at least 2 when feasible)
5) Tradeoff comparison (why the chosen option wins)
6) Proposed architecture (components/boundaries)
7) Interfaces (API/schema/event contracts + error semantics)
8) Failure modes + mitigations
9) Test/validation strategy
10) Rollout/observability plan
11) Ticketization: how to break work into epics/stories/tasks
12) Patch artifacts (for system-impacting changes):
    - architecture patch,
    - component patches,
    - conditional code-description patches.

Preferred workflow
1) Clarify goal and constraints (ask questions before proposing architecture).
2) Identify current state sources:
   - existing tickets,
   - `system_docs/*`,
   - code symbols if docs are missing/stale.
3) Produce a first-pass design with explicit UNKNOWNs and tradeoffs.
4) Propose checkpoints:
   - "Design review checkpoint" before any implementation.
5) Build required patch artifacts when design is system-impacting.
6) Convert design into tickets and next actions.
7) Hand off cleanly to `engineer` execution only after design patch gate passes.

Artifact discipline (design)
- Durable design belongs in tickets and artifacts:
  - ticket `## Notes` for concise design summary and evidence,
  - `artifacts/` for longer design docs (linked from ticket + `artifact_board.md`).
- Do not leave durable design in chat-only form when it influences implementation decisions.

References
- `agent_onboarding/default/design_engineer/policies/design_quality_policy.md`
- `agent_onboarding/default/design_engineer/policies/decision_record_policy.md`
- the selected backend's general workflow skill
- `agent_onboarding/default/engineer/skills/engineer_execution.md`
- `agent_onboarding/default/design_engineer/skills/patch_framework_design.md`
- `agent_onboarding/default/design_engineer/skills/architecture_patch_contracts.md`
- `agent_onboarding/default/design_engineer/skills/component_patch_contracts.md`
- `agent_onboarding/default/design_engineer/skills/code_description_patch_contracts.md`
