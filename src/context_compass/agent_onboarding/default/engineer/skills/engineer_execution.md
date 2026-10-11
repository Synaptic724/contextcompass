

# engineer_execution

Purpose
- Define how engineer agents plan and implement code changes in this
  repository.

Core rules
- Follow `AGENTS.MD` and the shared baseline skills in
  `agent_onboarding/default/general/`.
- Propose a plan before editing; keep scope tight and reviewable.
- Enforce `patch_framework_gating.md` for system-impacting changes before any
  implementation edits.
- Consume required patch artifacts using
  `patch_artifact_consumption.md` before editing system-impacting code.
- Follow repository SQL rules in `AGENTS.MD` when touching SQL tools.
- Update docstrings for every touched function/class and add tests for
  behavioral changes.
- Keep scratch ideas and todos under `user_defined/`. That directory exists, is
  yours outright, and no tool writes to it in any mode - create whatever subfolders
  you need. Earlier revisions of this skill named `workspace/agent/`, which the
  package has never shipped and which no lane policy protects, so scratch written
  there was swept on the next cleanup.
- Promote durable plans and execution artifacts into the selected ticket
  backend; the `tickets/` folders are local-mode storage only.

Preferred workflow
1) Clarify the goal, constraints, and affected files.
2) Route from `attention_board.md` to the active ticket and follow the Ticket
   Microcycle.
3) If scope is system-impacting, verify patch-framework entry gate artifacts
   exist and are linked before editing code.
4) Build and record patch-section to implementation/validation mapping in ticket
   notes.
5) Review existing docstrings and contracts in the target modules.
6) Implement changes with small, cohesive functions and explicit error handling.
7) Run tests (or report "Not run" with reasoning).
8) Summarize changes and list follow-ups.

Artifact discipline (engineer)
- Ideas/opinions/todo: `user_defined/` only.
- Plans and scope control: use `templates/` and create Epic/Story/Task tickets
  in the selected backend.
- For system-impacting changes under patch framework:
  - maintain active patch docs under `system_docs/patches/active/<patch_id>/`,
  - link patch docs from active tickets,
  - complete merge+cleanup closure gates before marking work done.
- Status updates: keep `attention_board.md` current and append detailed
  findings to ticket `## Notes`.
- Closures: use the selected backend's closure procedure with summary + date.
- Convert approved todos into tickets instead of leaving them in scratch.

Examples
- `agent_onboarding/default/engineer/examples/artifact_workflow.md`

References
- `AGENTS.MD`
- the selected backend's general workflow skill
- `agent_onboarding/default/engineer/skills/patch_framework_gating.md`
- `agent_onboarding/default/engineer/skills/patch_artifact_consumption.md`
