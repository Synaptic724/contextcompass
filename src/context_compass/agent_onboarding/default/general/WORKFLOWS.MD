# WORKFLOWS.MD - general

Purpose
- Define role-local workflow availability for the `general` role.

Inheritance
- `INHERITS_WORKFLOWS_FROM: none`

Activation rule
- Workflows are optional macro behaviors.
- Workflows are user-generated and user-approved only.
- When a workflow is selected for work, treat the parent-first role chain as
  the workflow lookup order.
- The active workflows below apply in both backends. Resolve
  `work_tracking.backend` before their actions and use the corresponding
  ticket reads, writes, closure, and responsibility rules. Each macro preserves
  its existing scope and selection gates.
- The on-demand role/workflow creation paths remain available in both modes.

Active workflows (both backends)
- `agent_onboarding/default/general/workflows/cleanup_context_compass.md`
- `agent_onboarding/default/general/workflows/start_context_compass_work.md`
- `agent_onboarding/default/general/workflows/turn_in_selected_tickets.md`
- `agent_onboarding/default/general/workflows/sync_attention_board.md`

On-demand workflows
- `agent_onboarding/default/general/workflows/role_creation.md`
- `agent_onboarding/default/general/workflows/workflow_creation.md`
