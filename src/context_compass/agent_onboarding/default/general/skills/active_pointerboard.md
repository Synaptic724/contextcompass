

# active_pointerboard

Purpose
- Keep a single, compact routing view of active work.
- Make post-compaction re-entry fast without replacing ticket detail.
- Prevent "what am I working on?" ambiguity.

Canonical board path
- `context_compass/attention_board.md`

Scope
- Pointer data only.
- No deep analysis, no full history replay, no speculative claims.
- Detailed context remains in the selected backend's ticket.
- Artifact pointers belong in ticket `Artifact Links` and `artifact_board.md`,
  not in `attention_board.md`.

Required columns
- `work_item`: short active event label.
- `status`: `ready` | `in_progress` | `blocked` | `review`.
- `mode`: `discovery` | `implementation` | `validation` | `handoff`.
- `owner`: current executor (for now usually `reading`).
- `agent_name`: one or more assigned agent names, comma-separated.
- `blocker`: concrete blocker or `none`.
- `next`: one concrete next action.
- `outcome`: intended near-term result for this active item.
- `exit_signal`: explicit condition that indicates the row should route/switch.
- `ticket`: local mode uses a context-compass-relative ticket path (no
  `context_compass/` prefix); `github_codex_plugin` uses the canonical Issue URL.
- `updated_at`: ISO-8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`).
- `reread`: `REQUIRED` | `HELPFUL`.

Update triggers (mandatory)
1) When a work item changes status.
2) When mode/outcome/exit_signal changes.
3) When blocker state changes.
4) Before compaction/handoff.
5) Immediately after re-onboarding if board is stale.
6) When switch conditions become true and routing must change.

Operating rules
- Pointer board never overrides ticket truth.
- `owner` is executor/runtime identity; `agent_name` is assignment identity.
- Every row must map to exactly one canonical ticket reference for its backend.
- In plugin mode, the primary claim in `issue_board.md` must name the same agent
  as the active row, and fetched Issue-body Status must agree with the row's status.
- Check references against the selected backend before work. A local path in
  plugin mode or Issue URL in local mode is an unresolved backend transition;
  stop and reconcile it instead of maintaining two copies of the same ticket.
- Keep row text short and operational.
- Put rows in `active_items`, routing detail entries in `active_attention_details`,
  and closed anchors in `closed_anchors`; use the board's USER-DEFINED regions.
- Every active row has one matching `WORK_ITEM` detail entry. Its
  `SWITCH_TRIGGER` agrees with `exit_signal`; its `RESUME_HIERARCHY` is the
  parent-first active ticket chain ending at the row's `ticket`. In plugin mode,
  use Issue URLs. For a standalone task, the hierarchy contains only that one
  ticket reference. Use the board's entry format.
- If a claim is uncertain, mark it in the ticket `Unknowns`, not on this board.
- Execution is blocked when active work has no matching board row; repair board routing before continuing implementation or validation.

Re-entry protocol
Resolve `work_tracking.backend` from YAML before opening the ticket references.
1) Open `context_compass/attention_board.md`.
2) Read rows with `reread=REQUIRED`.
3) Read `SWITCH_TRIGGER` and `RESUME_HIERARCHY` in active attention details.
4) Read linked local tickets or fetch exact Issues through the selected plugin,
   verify canonical Status/Notes, then resume from `next`.

Ticket closure sync protocol (mandatory)
The file-move steps below apply only to `local`. Plugin closure follows
`agent_onboarding/default/general/skills/github/workflow.md` using the same
row/detail removal and closed-anchor rules.
1) When a ticket is moved to a completed folder, update board rows in the same change pass.
2) Remove/replace any `## Active Items` row referencing the closed ticket.
3) Prune `## Active Attention Details` entries tied only to the closed ticket.
4) Add one compact row to `## Recently Closed Anchors` for traceability.
5) Keep anchors capped to 12 rows (drop oldest first).
6) Keep active rows free of completed ticket paths or closed Issue URLs.

Older-board adoption
- A board with no USER-DEFINED regions needs the existing board-migration flow
  before whole-file conformance; inspect the migration preview first.
- Before upgrading an already-regioned board, check for legacy attention
  details outside protected regions. Preserve those entries in their ticket
  Notes or an existing protected region and verify the copy before upgrading;
  unprotected text is package structure and is replaced during conformance.
- After the new region exists, explicitly move current routing entries into
  `active_attention_details`, preserving all unrelated standing Notes. The
  updater carries region bodies by name; it does not relocate Notes content
  automatically. Do not discard a preserved legacy entry until its routing
  information has been verified in the new location.

Anti-patterns
- Using board as a second ticket system.
- Copying long narrative into rows.
- Leaving stale `in_progress` rows after handoff.
- Tracking artifact file paths in attention-board rows/details.

References
- the selected backend's general workflow skill
- `context_compass/SKILLS.MD`
- `context_compass/agent_onboarding/default/general/skills/memory_management.md`
- `context_compass/agent_onboarding/default/general/skills/reactive_documentation.md`
- `context_compass/agent_onboarding/default/general/skills/active_documentation.md`
- Local closure: `agent_onboarding/default/general/skills/ticket_closure_attention_sync.md`
- Plugin closure: `agent_onboarding/default/general/skills/github/workflow.md`





