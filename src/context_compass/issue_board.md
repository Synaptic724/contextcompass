# Issue Board

<!-- BEGIN MANAGED: BoardContract -->
## How this board works

This board is active only when `work_tracking.backend: github_codex_plugin`. It assigns
Context Compass agents to GitHub Issues; it does not duplicate Issue bodies,
Notes, blockers, or ticket Status. `attention_board.md` remains the narrow
current-focus route, while this board holds the wider responsibility map.

MANAGED regions are package-owned and replaced on upgrade. USER-DEFINED region
bodies are project-owned and preserved. Write claims only inside the regions
below. All Issue URLs must belong to the configured `issues_repository`.

- `active_claims`: one primary writer claim per Issue, with optional reviewer
  or support rows. Names must resolve through `mailbox_board.md`.
- `released_claims`: short trace of released claims, capped at 12 rows.
- `notes`: standing local responsibility conventions, not Issue content.

The `claim` value is `primary`, `review`, or `support`; `responsibility` says
what the agent is doing. `owner` is the accountable human or team, and
`agent_name` is the Context Compass execution identity. A GitHub assignee is
not an agent identity. Only the primary claim may edit the Issue body; other
agents send findings through the configured communication backend for the primary writer to append to
Issue-body Notes. Release or transfer claims explicitly at handoff or closure.
Mailbox and MCP modes use the same local roster/state and Issue claim ownership.

The board ships with empty user regions. In `local` mode leave them inactive;
the local ticket files and attention board remain the complete work route.
<!-- END MANAGED: BoardContract -->

## Active Claims
| issue | claim | owner | agent_name | responsibility | branch_or_pr | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
<!-- BEGIN USER-DEFINED: active_claims -->
<!-- END USER-DEFINED: active_claims -->

## Released Claims
| issue | agent_name | responsibility | reason | released_at |
| --- | --- | --- | --- | --- |
<!-- BEGIN USER-DEFINED: released_claims -->
<!-- END USER-DEFINED: released_claims -->

## Notes
<!-- BEGIN USER-DEFINED: notes -->
<!-- END USER-DEFINED: notes -->
