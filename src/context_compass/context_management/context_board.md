# Context Board

Purpose
- Canonical index of active context-management associations.
- Track reusable reread packs linked to tickets.
- Keep `attention_board.md` ticket-only and free of context-artifact paths.
- Unused in `github_issues` mode: each ticket's Context Management section holds
  its context packs.

Scope rules
- `attention_board.md` routes tickets only; do not add context artifact paths
  there.
- Tickets remain canonical execution memory; this board is an association
  index for derived context packs.
- Add rows only when a ticket sets `CONTEXT_MANAGEMENT_REQUIRED: true`.
- Every context row must include:
  - `context_id`
  - `ticket`
  - `context_artifact_path`
  - `agent_name`

## Active Context Links
| context_id | ticket | context_artifact_path | context_type | owner | agent_name | status | next | updated_at | reread |
|---|---|---|---|---|---|---|---|---|---|


## Recently Cleared Context Links
| context_id | ticket | context_artifact_path | reason | cleared_at |
|---|---|---|---|---|
