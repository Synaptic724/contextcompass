
# patch_framework_design

Purpose
- Define how `design_engineer` builds and maintains patch-framework contracts.
- Make patch design artifacts mandatory and consistent before engineer
  implementation starts.
- Orchestrate the three contract skills:
  - `architecture_patch_contracts.md`,
  - `component_patch_contracts.md`,
  - `code_description_patch_contracts.md`.

Design ownership
- Own system-level patch intent in `architecture_patch.md`.
- Own component-level delta contracts in `component_patch_<component>.md`.
- Decide when `code_description_patch_<component>.md` is required.
- Own patch-to-ticket mapping and merge/cleanup design criteria.
- Keep contract language domain-agnostic and reusable.

When this gate applies
- Any design that changes architecture/component contracts, lifecycle, or
  cross-component behavior.
- Any design expected to update canonical `system_docs/src_architecture.md` or
  `system_docs/src_components.md`.
- Any design expected to refresh `system_docs/src_graph.md` because
  documented source wiring or ownership moved.

Required design outputs (before implementation)
1) `system_docs/patches/active/<patch_id>/architecture_patch.md`
2) `system_docs/patches/active/<patch_id>/component_patch_<component>.md` for
   each changed component
3) `system_docs/patches/active/<patch_id>/code_description_patch_<component>.md`
   when complexity triggers apply

Mandatory authoring protocol
- Build `architecture_patch.md` using
  `architecture_patch_contracts.md`.
- Build each `component_patch_<component>.md` using
  `component_patch_contracts.md`.
- Build required `code_description_patch_<component>.md` files using
  `code_description_patch_contracts.md`.

`code_description_patch` complexity triggers
- State-machine or policy-gate flow changes.
- Multi-branch error/rollback semantics.
- Concurrency/idempotency-sensitive logic.
- Non-trivial orchestration or mediator behavior.

Design quality gate checklist
- [ ] Patch id is explicit and stable.
- [ ] Architecture patch includes invariants, interfaces, migration order, and rollback.
- [ ] Component patches include before/after behavior and validation expectations.
- [ ] Conditional code-description patches exist for triggered components.
- [ ] Patch docs are linked from active ticket(s) and coverage matrix is complete.

Design-to-engineer handoff rule
- Do not route implementation as ready until design quality gate is satisfied.
- If gate fails, keep design lane active and raise `BLOCKER` or
  `DECISION_REQUEST` in ticket notes.
- Engineer lane must be blocked if required patch docs are missing, unlinked, or
  fail contract quality checks.

Closure design obligations
- Ensure implementation evidence is sufficient for canonical merge.
- Ensure temporary patch artifacts are removed or explicitly retained by policy.

Manual validation expectation
- Confirm architecture/component/code-description patch artifacts exist as
  required for the active patch id.
- Confirm each required artifact is linked from active ticket(s).
- Confirm design quality checklist is satisfied before handoff.

References
- `agent_onboarding/default/engineer/skills/patch_framework_gating.md`
- `agent_onboarding/default/general/skills/ticketing.md`
- the selected backend's general workflow skill
- `agent_onboarding/default/design_engineer/skills/architecture_patch_contracts.md`
- `agent_onboarding/default/design_engineer/skills/component_patch_contracts.md`
- `agent_onboarding/default/design_engineer/skills/code_description_patch_contracts.md`
