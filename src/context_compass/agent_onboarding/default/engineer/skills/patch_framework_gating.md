
# patch_framework_gating

Purpose
- Define mandatory engineer gates for using patch-framework artifacts during
  system-impacting changes.
- Ensure implementation work is blocked until required patch contracts exist.
- Enforce required artifact consumption behavior via
  `patch_artifact_consumption.md`.

When this gate applies
- The task changes architecture/component boundaries, lifecycle behavior,
  policy/gating behavior, or cross-component interaction contracts.
- The task changes code that requires updates to `system_docs/src_architecture.md`
  or `system_docs/src_components.md`.
- The task changes source wiring/ownership enough that
  `system_docs/src_graph.md` must be refreshed.
- The user explicitly requests patch-based planning/governance.

Non-negotiable entry gate
- Do not implement system-impacting code changes until all required artifacts
  exist for the active patch id and are linked from the active ticket.
- If artifacts are missing, mark `BLOCKED` and create/update patch artifacts
  first.
- Do not implement until the required artifact read order is completed and
  consumption mapping is documented in ticket notes.

Required patch artifacts
1) `system_docs/patches/active/<patch_id>/architecture_patch.md` (required)
2) `system_docs/patches/active/<patch_id>/component_patch_<component>.md`
   for each changed component (required)
3) `system_docs/patches/active/<patch_id>/code_description_patch_<component>.md`
   (conditional)

`code_description_patch` required triggers
- Complex control flow or state-machine changes.
- New/changed policy gate pipelines.
- Non-trivial error semantics or rollback behavior.
- Concurrency or idempotency-sensitive changes.

Engineer execution gate checklist
- [ ] Active ticket routes this work from `attention_board.md`.
- [ ] Patch id is explicit and stable.
- [ ] Required patch docs exist and are ticket-linked.
- [ ] Required read order from `patch_artifact_consumption.md` is complete.
- [ ] Ticket notes contain patch-section to implementation/validation mapping.
- [ ] Unknowns in patch docs are either resolved or explicitly accepted.
- [ ] Implementation scope matches patch doc boundaries.

Engineer closure gate checklist
- [ ] Implementation evidence captured in ticket notes.
- [ ] Durable deltas merged into canonical docs.
- [ ] Temporary patch docs removed from `system_docs/patches/active/<patch_id>/`
      unless an explicit retention exception is approved.
- [ ] Attention board and artifact board synchronized.

Manual validation expectation
- Confirm required artifacts exist under
  `system_docs/patches/active/<patch_id>/`.
- Confirm artifact links are present in the active ticket.
- Confirm required read-order and mapping notes are documented before
  implementation.

Failure behavior
- If any entry/closure gate fails, stop and raise `BLOCKER` or
  `DECISION_REQUEST` in ticket notes before continuing.

References
- `agent_onboarding/default/general/skills/ticketing.md`
- the selected backend's general workflow and closure skills
- `agent_onboarding/default/engineer/skills/patch_artifact_consumption.md`
