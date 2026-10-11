

# ticket_closure_attention_sync

Purpose
- Enforce deterministic synchronization between ticket closure and `attention_board.md`.
- Prevent stale routing rows and historical note buildup on the pointer board.

When to use
- Any time a ticket is moved to `tickets/epics/completed/`, `tickets/stories/completed/`, or `tickets/tasks/completed/`.
- For review/blocked or other status changes without closure, use
  `active_pointerboard.md` update rules instead. Keep the active route and its
  details synchronized; do not create a closed anchor for an open ticket.

Deterministic closure sync protocol (mandatory)
1) Identify the previous active path (`old_ticket`), the moved completed path
   (`completed_ticket`), and completion datetime (`YYYY-MM-DDTHH:MM:SSZ`).
2) Open `context_compass/attention_board.md`.
3) In `## Active Items`:
   - If a row points to `old_ticket` and no immediate successor ticket exists, remove the row.
   - If a successor ticket exists, replace the row `ticket`, `status`, `mode`, `next`, `outcome`, `exit_signal`, and `updated_at` values.
4) In `## Active Attention Details`:
   - Edit only the `active_attention_details` USER-DEFINED region.
   - Match entries to active rows by `WORK_ITEM`. Remove an entry when its row
     is removed; update it when the row routes to a successor.
   - Prune legacy entries whose `NEXT` or `EVIDENCE` only concern `old_ticket`
     and no longer route active work.
   - Each remaining row needs a matching `SWITCH_TRIGGER` and
     `RESUME_HIERARCHY`, using the board's entry format and current ticket paths.
5) In `## Recently Closed Anchors`:
   - Add one compact anchor for `completed_ticket` with status `done`, a short
     completion `note`, and the completion timestamp in `closed_at`.
   - Keep at most 12 anchor rows; remove oldest rows first when adding a new one.
6) Verify board invariants before saving.
7) If the closed ticket has artifacts:
   - apply artifact disposition (`delete_on_close`, `retain_as_reference`, or
     `promote_to_documentation`),
   - update `context_compass/artifact_board.md` active/cleared rows.

Board invariants (must hold)
- `## Active Items` rows must only reference non-completed tickets.
- Every active row must map to one canonical ticket path.
- `next` text must be one concrete action.
- `outcome` and `exit_signal` must be concrete and non-empty for active rows.
- `## Active Attention Details` must only contain active-routing details.
- Active routing details must include `SWITCH_TRIGGER` and `RESUME_HIERARCHY`.
- Board must remain compact; durable narrative belongs in ticket `## Notes`.

Verification
- Inspect the `## Active Items` section only, ending at the next `##` heading.
  Locate the `ticket` column by its header name; inspect that field in each data
  row, skipping the header, separator, and region markers.
- Each ticket path must resolve to an existing non-completed ticket. A value
  under `tickets/epics/completed/`, `tickets/stories/completed/`, or
  `tickets/tasks/completed/` is a stale active route. Ticket paths do not carry
  a `context_compass/` prefix.
- Do not use a whole-board or whole-section text search as this check. Completed
  paths are valid in `## Recently Closed Anchors` and can occur as references in
  another cell; those are not the active row's ticket field.
- Check that detail entries match the remaining active rows and their current
  switch/resume paths. Keep this inspection inside the declared details region.
- Locate the structural headings when needed:
- `rg -n "## Active Items|## Active Attention Details|## Recently Closed Anchors" context_compass/attention_board.md`

Anti-patterns
- Leaving closed ticket rows in `## Active Items`.
- Keeping deep historical narratives in board detail section.
- Using board detail section as a duplicate of ticket notes.

References
- `context_compass/agent_onboarding/default/general/skills/workflow.md`
- `context_compass/agent_onboarding/default/general/skills/ticketing.md`
- `context_compass/agent_onboarding/default/general/skills/active_pointerboard.md`




