# component_patch_contracts

Purpose
- Define the authoring contract for
  `system_docs/patches/active/<patch_id>/component_patch_<component>.md`.
- Ensure each changed component has a concrete delta contract before code work.

When required
- One component patch is required for every changed component in the patch
  scope.

Required section contract (per component)
1) Component purpose and boundary in current architecture
2) Before/after behavior summary
3) Interface deltas (inputs, outputs, error semantics)
4) State and lifecycle deltas
5) Failure mode deltas
6) Dependency and ordering constraints
7) Validation expectations
8) Unknowns and open decisions

Authoring rules
- Keep one component per file; do not merge multiple components.
- Keep behavior deltas concrete and externally observable.
- Include ownership and cleanup implications when lifecycle changes.
- Use explicit language for constraints (`MUST`, `MUST NOT`, `REQUIRED`).

Quality gate
- Component name matches architecture patch matrix.
- Interface/state/failure deltas are all present.
- Dependency order is explicit for implementation sequencing.
- Validation expectations map to test/verification actions.

Handoff requirements
- Link every component patch from the active ticket.
- Do not route implementation until all changed components have patch files.

References
- `agent_onboarding/default/design_engineer/skills/patch_framework_design.md`
- `agent_onboarding/default/design_engineer/skills/src_components_instructions.md`
- the selected backend's general workflow skill
