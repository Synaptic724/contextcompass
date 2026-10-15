# GitHub Issue ticket workflow

This skill applies only when `work_tracking.backend: github_codex_plugin`.
Use the configured GitHub plugin for ticket operations. Each Issue is one
Epic, Story, or Task using the existing template. Resolve `connection_nickname`
through `codex_plugin.md` before all plugin operations, including recovery.
Its body owns current Status, decisions, requirements and handoff context. Notes,
supported comments and authorized documents retain attributed evidence. Local ticket files are inactive
for the same work; a Project URL is optional context.

## Intake and hierarchy

- Choose the smallest Epic/Story/Task shape under shared `ticketing.md`. Preserve
  every required section from the matching template, including the immutable ID,
  Agent Name, Ticket Contract, acceptance criteria, transition reason, Artifact
  Links, Context Management, `## Notes`, and Context / Handoff Summary.
- Check the exact configured repository and full title/body before creating an
  Issue, then fetch the returned Issue URL and verify it. Migration of existing
  tickets remains a separate operation; the mode setting does not publish them.
- Use Issue URLs in parent metadata, child checklists, and dependency fields.
  Epics, stories, and tasks remain meaningful sizes of work even though GitHub
  stores all three as Issues. Follow parent-first routing and keep reciprocal
  references consistent. Native hierarchy tools are optional enhancements when
  exposed; explicit links remain required. Do not invent or discard a dependency.
- A blocked Issue stays open and carries the chosen design's blocked state,
  its blocker Issue links or concrete external condition, and one unblock action.

## Microcycle, Notes, and Status

For a new design with `AGILE_METADATA`, follow `ticket_design.md` and the
canonical definition instead of the ordinary Status enum below. Metadata owns
workflow; the body retains canonical Notes and a derived Status view. Native
closure remains a projection, not acceptance. Authored posts/comments/Notes
identify their actual agent name and role/function under `agent_identity.md`.

- The configured microcycle and structured Note fields remain. Multiple meaningful comments
  or authorized linked documents may carry attributed findings directly. No forced body copy
  of every finding is required before ordinary continuation. Preserve historical Notes/comments.
- Append-only comments need no body-writer permission. Reuse valid account/audience/context
  binding, use a supported operation and verify readback; no full-policy reread per comment.
  Latest complete body/revision and writer coordination apply to actual full-body replacements
  or overlapping mutable fields, not every contribution. Follow `codex_plugin.md`.
- Keep template Status and Updated metadata current. Record each state change
  and reason in State Transition Event and Notes. `draft`, `ready`,
  `in_progress`, `blocked`, and `review` are open Issue states; a completed
  ticket has `Status: done` and GitHub state `closed`.
- For a non-Agile design the Issue body Status is authoritative for routing.
  For an Agile design use its canonical metadata and checked derived Status. Open/closed is
  GitHub's coarse lifecycle check. Stop and reconcile a mismatch with the body
  or attention route; an optional Project's Status cannot override the ticket.
- Update Context / Handoff Summary in the same canonical body when continuation
  changes. A full-body update must retain unrelated sections and prior history.

## Local responsibility and routing
Record each meaningful changed finding once at the appropriate ticket depth. Keep concise claim,
impact, material limits and next action inline with exact retrievable comment/doc links; do not copy
full linked reports or create substantive Notes for unchanged checks/ACKs. Preserve required in-body
state/evidence at material transitions, prior history and custom regions; details may remain in comments.
The assigned agent owns current status, evidence, requested scoped review and final closure.
Alternatively, a qualified independent reviewer may accept and close under shared `ticketing.md`,
without another author handback solely for closure. Keep actual body-write custody and verify
the accepted canonical state before native closure; a denied close remains pending projection.
Review is proportionate to actual consequence, uncertainty and contract, not automatic full-code
review. High-consequence or uncertain changes request scoped review; self-checks are not independent.
Parent owners synthesize child outcomes and remaining work; child completion does not accept the parent.

- `issue_board.md` holds local agent claims; `mailbox_board.md` is the roster.
  Keep one primary writer for conflicting body/field edits and coordinate reviewer/support work.
  Independent append-only comments do not acquire that body claim or require its permission.
  Coordination transport follows `agent_communication.backend`; in `codex_mcp`
  mode skip mailbox messages and alerts while preserving shared state per
  `agent_session_state.md`.
  GitHub usernames and assignees are separate from Context Compass agent names.
- `attention_board.md` holds current focus. The `ticket` cell is the Issue URL;
  `RESUME_HIERARCHY` lists parent-first Issue URLs ending at that same Issue.
  The active row's agent agrees with the primary claim, and its status agrees
  with the fetched Issue body Status. Claim plus route must exist before work.
- Artifact, context-pack, system-doc, and special-instruction files remain
  local. Associate their board rows with the Issue URL and preserve the existing
  artifact/context gates. Never mirror Issue Notes into a local ticket or board.

## Closure and recovery

- Authorized agents close routine completed work after criteria, required tests and required reviews
  are satisfied, without another owner ping. Reserved owner decisions still wait; record missing
  authority or an unmet gate as the specific blocker. Record delegated acceptance or reserved-owner
  disposition, completion summary,
  accepted metadata/derived Status for Agile or `Status: done` for non-Agile,
  Updated timestamp, and transition reason in the Issue body;
  verify that update, close the Issue through the plugin, and verify state.
- Remove or replace active attention rows/details, add one compact closed anchor,
  release the local claim, and synchronize artifact/context dispositions. An
  open Issue with accepted metadata or `Status: done` after a failed close has a
  pending projection to repair; do not report the ticket closed.
- After compaction/handoff, reread YAML, both ticket and communication selectors
  plus their baselines, `issue_board.md`,
  attention route, and the exact active Issue bodies and relevant comments.
  Recover from canonical Notes and next action. Read parent Issues in the
  declared hierarchy rather than substituting local epic/story/task folders.
- If the plugin is unavailable or required writes fail, stop with the concrete
  blocker. Resume through the same backend after access is repaired.

Use `migration.md` only when the owner requests an existing ticket migration.
