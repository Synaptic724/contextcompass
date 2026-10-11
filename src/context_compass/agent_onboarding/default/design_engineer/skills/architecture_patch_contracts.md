# architecture_patch_contracts

Purpose
- Define the authoring contract for
  `system_docs/patches/active/<patch_id>/architecture_patch.md`.
- Ensure architecture-level deltas are explicit before implementation is routed.

When required
- Any patch that changes architecture boundaries, cross-component interactions,
  policy gates, lifecycle sequencing, or canonical `src_architecture` behavior.

Required sections (minimum)
1) Patch scope and non-goals
2) Changed-components matrix
3) Interface and boundary deltas
4) Cross-component invariants
5) Migration/rollout order
6) Rollback strategy
7) Validation expectations and evidence plan
8) Ticket coverage map (epic/story/task linkage)
9) Unknowns and decision requests

Authoring rules
- Keep this document domain-agnostic and reusable.
- Write constraints as enforceable statements, not preferences.
- Use explicit ordering for migrations and rollback.
- If a claim cannot be evidenced, mark `UNKNOWN` and route investigation.

Quality gate
- Patch id is explicit and stable.
- Every changed boundary has an explicit delta statement.
- Every new or changed invariant is testable.
- Migration and rollback are internally consistent.
- Ticket linkage is complete and current.

Handoff requirements
- Link architecture patch in the active ticket artifact section.
- Do not route implementation ready-state until this contract is complete.

References
- `agent_onboarding/default/design_engineer/skills/patch_framework_design.md`
- `agent_onboarding/default/design_engineer/skills/src_architecture_instructions.md`
- the selected backend's general workflow skill
