# role_local_workflows

Purpose
- Define how workflows are stored and governed in Context Compass.

Rules
- Workflows are first-class role artifacts.
- Actual workflow definitions live inside roles, not in a top-level registry.
- Canonical role-local paths are:
  - `<role_root>/WORKFLOWS.MD`
  - `<role_root>/workflows/`
- Templates may live at the top level under `templates/`.
- Workflows are user-generated and user-approved only.
- Agents may suggest or scaffold workflows when explicitly asked.
- Agents must not silently create, modify, or adopt a new workflow at their
  own discretion.
- Workflow inheritance is parent-first by role chain, mirroring the skill
  model conceptually.
- Role-local workflow manifests should stay lightweight:
  - purpose
  - inheritance
  - activation rule
  - active workflow paths or `none`
  - optional on-demand workflow paths or `none`
- Active workflows for the selected backend are baseline-readable for that role.
- On-demand workflows are discoverable but should not be read until:
  - the user explicitly asks to use them, or
  - the current task explicitly triggers them.
- A role may mix:
  - active starter workflows
  - on-demand scaffolding workflows
  in the same manifest, as long as the distinction is explicit.

Non-goals
- This does not create a top-level workflow registry.
- This does not require every role to define active workflows immediately.

References
- `PROFILE_CLASS_CREATION_GUIDE.md`
- `templates/workflow_simple_template.md`
- `templates/workflow_advanced_template.md`
