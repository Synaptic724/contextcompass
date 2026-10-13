

# Context Compass Workflow (Epic / Story / Task)

## Purpose
Provide a consistent planning and tracking workflow that uses structured tickets and survives context compaction.

## Ticket Size Guidance
- Epic: big project or cross-cutting initiative with multiple stories.
- Story: medium scope that delivers a user- or system-facing slice and needs multiple tasks.
- Task: small, single deliverable that can stand alone.

## Folder Structure
- `tickets/epics/` - epic tickets
- `tickets/epics/backlog/` - parked epic tickets not yet active
- `tickets/epics/completed/` - completed epic tickets with summary + datetime
- `tickets/stories/` - story tickets
- `tickets/stories/backlog/` - parked story tickets not yet active
- `tickets/stories/completed/` - completed story tickets with summary + datetime
- `tickets/tasks/` - task tickets
- `tickets/tasks/backlog/` - parked task tickets not yet active
- `tickets/tasks/completed/` - completed task tickets with summary + datetime
- `templates/` - templates for all ticket types
- `system_docs/` - canonical system docs:
  `src_architecture.md`, `src_components.md`, `tests_architecture.md`,
  `tests_components.md`,
  `src_graph.md`, and instruction docs
- `artifact_board.md` - artifact association index (ticket-linked artifacts only)
- `artifacts/` - supporting artifact storage root
- `context_management/context_board.md` - optional context-pack association
  index
- `context_management/artifacts/` - optional derived context reread packs

## Workflow Steps
1. Choose the smallest ticket type that fits the scope:
    - Big project: epic -> stories -> tasks.
    - Medium scope: story -> tasks.
    - Small scope: task only.
2. Create the required ticket(s) using the templates.
   - If a ticket is intentionally parked, place it in the matching
     `*/backlog/` folder.
3. Track progress using checkboxes (`- [ ]`) and keep status fields updated.
4. Keep links consistent (epic <-> story <-> task IDs) when using multiple levels.
5. Use the Ticket Microcycle continuously:
    - `Investigate -> Document -> Strategy/Plan -> Document -> Implement -> Document -> Validate -> Document`.
6. Record each meaningful changed finding once at appropriate ticket depth before dependent work.
   Keep concise claim, impact, material limits and next action inline with exact retrievable
   supporting comment/doc links. Do not copy full linked reports or create substantive Notes for
   unchanged checks/ACKs; preserve required in-body state/evidence and all existing history.
   - Use evidence ranges (`path:start_line-end_line`) rather than single-line anchors.
   - If the ticket sets `CONTEXT_MANAGEMENT_REQUIRED: true`, also update the
     linked context artifact when that finding changes required rereads or
     active topics.
7. Update "Context / Handoff Summary" sections as work progresses.
8. If artifacts are produced:
    - add/update the ticket `Artifact Links (Optional)` section,
    - add/update `artifact_board.md` row(s) for each active artifact.
9. If the ticket enables context management:
    - add/update the ticket `Context Management` section,
    - add/update `context_management/context_board.md` row(s) for each active
      context artifact.
10. Before closing a ticket:
    - The assigned agent owns current status, evidence, requested scoped review and final closure.
    - Review is proportionate to actual consequence, uncertainty and the contract, not an automatic
      full-code review. Self-checks are not independent review; high-consequence or uncertain changes
      request scoped review of the actual revision and consequential question.
    - Authorized agents close routine completed work after criteria, required tests and required
      reviews are satisfied, without another owner ping. Reserved owner decisions still wait.
      Missing authority or a required gate is a specific blocker.
11. After acceptance under delegated authority or explicit reserved-owner disposition:
    - Add a short completion summary with a UTC datetime.
    - Move the file to its matching completed folder (`tickets/epics/completed/`,
      `tickets/stories/completed/`, or `tickets/tasks/completed/`).
12. Immediately run deterministic board sync for closure:
    - Remove/replace active rows that point to the closed ticket.
    - Prune stale attention details tied only to the closed ticket.
    - Add one compact closed anchor row.
    - Keep closed anchors capped by dropping the oldest rows first.
13. If ticket artifacts exist, run artifact closure sync:
    - apply artifact disposition (`delete_on_close`, `retain_as_reference`, or
      `promote_to_documentation`),
    - update `artifact_board.md` active/cleared rows accordingly.
14. If ticket context management is active, run context-board sync:
    - remove or update active context rows tied only to the closed ticket,
    - clear or relink rows according to successor ticket state,
    - keep the board focused on active context-managed lanes only.

## DO NOT ASSUME / Unknowns Gate
Rule: No Unverified Claims.
Any statement that is not directly supported by evidence must be treated as UNKNOWN.

Evidence means at least one of:
- A specific source file reference (preferred: file + symbol/method/class name).
- A citation to an explicit, already-verified artifact (e.g., a prior approved doc section).

If not evidenced => UNKNOWN.

UNKNOWN items must be explicitly labeled UNKNOWN (or added to an Unknowns section).
UNKNOWN items must be investigated by reading the relevant source(s).
If investigation cannot be completed (missing source access, ambiguity, or time),
the item must remain UNKNOWN and must not be promoted to fact.

No reasonable assumptions.
Do not infer behavior from naming, patterns, conventions, or typical frameworks.
Only the code/docs count.

When unsure:
- Mark it UNKNOWN.
- Identify the most likely evidence target (file + symbol).
- Investigate, then update the doc (or leave it UNKNOWN).

## Status Discipline
- Update "Status" and "Updated" fields whenever work changes state
  (UTC DateTime format: `YYYY-MM-DDTHH:MM:SSZ`).
- Prefer: draft -> ready -> in_progress -> blocked/done.
- If blocked, explain why and list the unblock action.

## Ticket Contract (Required)
- Every active ticket must include a `Ticket Contract` section:
  - `ENTRY_GATE`
  - `EXECUTION_BOUNDARY`
  - `DEPENDENCIES`
  - `EXIT_GATE`
  - `FAILURE_ESCALATION`
- Every status transition should include a `State Transition Event`:
  - `from_state`
  - `to_state`
  - `transition_reason`
- Contract requirements are YAML-authoritative in
  `workflow.ticket_contract` (`config/context_compass_config.yaml`).

## Ticket Microcycle (Required)
- Route from `attention_board.md` to one active ticket at a time.
- Investigate until one meaningful finding is identified.
- Immediately document that finding in the ticket `## Notes` section before
  reading more.
- When `CONTEXT_MANAGEMENT_REQUIRED: true`, also update the linked context
  artifact before continuing if the finding changes the reusable reread pack or
  topic focus.
- Use UNKNOWN as the default claim state; promote to FACT only with evidence.
- Do not implement from `UNKNOWN` or `HYPOTHESIS` without an evidence-backed
  decision.
- If investigation expands beyond the current subsystem or exceeds
  `workflow.ticket_microcycle.expansion_gate_max_files`, add a `DECISION` note
  and request user confirmation before continuing.
- Score each note for compaction usefulness (`SCORE_0_TO_10`); improve notes
  below `workflow.ticket_microcycle.minimum_note_score`.

## Microcycle Configuration
- Policy toggle source: `config/context_compass_config.yaml`.
- Default mode is `enabled: true` with strict gate enforcement.
- Threshold source is `workflow.ticket_microcycle`:
  - `expansion_gate_max_files` (authoritative value is YAML-driven).
  - `minimum_note_score` (authoritative value is YAML-driven).
  - Do not hardcode numeric threshold copies in policy docs.
- If disabled (`enabled: false`), use relaxed mode:
  - Keep investigate->document notes for meaningful findings.
  - Require note updates before implementation and validation transitions.
  - Keep UNKNOWN->FACT promotion evidence requirements unchanged.
- Read-window settings:
  - `reading.viewer_tool_read_limit` = max lines per view/read operation.
  - `reading.read_loc_max` = max LOC per manual chunked read.
  - Default for both is `500`.

## Per-Ticket Noting Behavior
- Parent owners reconcile child outcomes and remaining work with synthesis, not duplicate tactical
  logs. Child completion does not accept the parent; assess its own criteria and authority.
- Task notes: tactical findings, immediate impact, and one-step continuation.
- Story notes: cross-task synthesis, dependency movement, and gate transitions.
- Epic notes: program-level direction, cross-story tradeoffs, and tranche order.
- Note behavior requirements are YAML-authoritative in
  `workflow.note_behavior` (`config/context_compass_config.yaml`).

## Artifact Protocol (Required)
- Artifacts are optional and only required when a ticket produces support files.
- `attention_board.md` remains ticket-routing-only and must not store artifact
  pointers.
- Artifact pointers belong in ticket `Artifact Links (Optional)` sections.
- Artifact associations are indexed in `artifact_board.md`.
- Artifact protocol is YAML-authoritative in
  `artifacts` (`config/context_compass_config.yaml`):
  - `store_root`
  - `board_path`
  - `attention_board_tracks_artifacts`
  - `require_ticket_association`
  - `cleanup_on_ticket_close`
  - `allowed_dispositions`

## Context Management Protocol (Optional)
- Context management is optional and only active when a ticket sets
  `CONTEXT_MANAGEMENT_REQUIRED: true`.
- `attention_board.md` remains ticket-routing-only and must not store context
  artifact pointers.
- Context artifact pointers belong in ticket `Context Management` sections.
- Tickets should point at context packs by `Context ID`.
- Context associations are indexed in `context_management/context_board.md`.
- Context artifacts live under `context_management/artifacts/`.
- When active:
  - linked `Context ID` values must resolve through the context board
  - linked context artifacts must be read before implementation or validation
  - ticket section and context board must stay synchronized
  - linked context artifacts must be updated during the Ticket Microcycle when
    meaningful findings change required rereads or active topics
  - if the required context cannot be defined concretely, write `UNKNOWN` and
    ask the user before implementation

## Anti-Pattern Catalog (Canonical)
- Anti-patterns are managed centrally in policy/docs; do not paste the full
  catalog into every ticket.
- Each ticket should keep an `Applicable Anti-Patterns` checklist with only the
  relevant lane checks.
- Any unresolved anti-pattern must be escalated with a note entry (`DECISION`,
  `DECISION_REQUEST`, `CONFLICT`, or `BLOCKER`) and evidence pointers.

## Documentation Formatting Standards
- Canonical standards doc: `configuration_standards.md`.
- Config source: `config/context_compass_config.yaml` under
  `documentation_format`.
- Default prose formatting:
  - target 90-110 characters per line
  - hard cap 120 characters per line
- `EVIDENCE` formatting:
  - inline form is allowed only for one short path under hard cap
  - use one path per line when there are multiple paths or line length would
    exceed hard cap

## Completion Summary Format
At the top of the completed ticket, add:

- Completed: YYYY-MM-DDTHH:MM:SSZ
- Summary: <1-3 lines describing what was delivered>

## Context Compaction Rule
Before context compaction or major handoff:
- Follow `agent_onboarding/default/general/skills/context_compaction.md`.
- Ensure the active tickets contain accurate handoff summaries.


## Agent Operating Notes (Optional but Recommended)
This section exists to reduce "process drift" when the workflow is executed by multiple humans and/or AI agents.

### Definition of Done (DoD) for a ticket
Before moving a ticket to a completed folder:
- [ ] `attention_board.md` is synchronized using deterministic closure-sync rules.
- [ ] `artifact_board.md` is synchronized when ticket artifacts exist.
- [ ] `context_management/context_board.md` is synchronized when context
      management is active for the ticket.
- [ ] Acceptance criteria are explicitly met (not "mostly done").
- [ ] Required tests/reviews and delegated acceptance or reserved-owner disposition are recorded.
- [ ] Any new/changed behavior has been documented in the relevant C4/C3 docs.
- [ ] Unknowns introduced during work are either resolved (with evidence) or
      recorded as **UNKNOWN** with investigation pointers.
- [ ] Completion summary includes the *user-visible* outcomes and any
      important caveats.
- [ ] Artifact disposition is recorded (cleanup or retained with reason) when
      artifacts were produced.

### When a task changes architecture or components
If a ticket modifies system behavior, make a small doc update as part of the same change:
- Update `system_docs/src_architecture.md` when system boundaries/boot/ownership/invariants change.
- Update `system_docs/src_components.md` when ownership, wiring, registries, or call flows change.
- Those two are AUTHORED: edit them directly, and regenerate each one's
  `*_index.md` in the same pass.
- `system_docs/src_graph.md` is GENERATED. **Do not edit it.** When source wiring
  or ownership coverage changes, edit the per-file descriptors and reassemble -
  a hand-edit is lost on the next run and breaks the index hash in the meantime,
  which makes every slice refuse. See
  `agent_onboarding/default/engineer/skills/src_graph_generation.md`.
- Keep diagrams in sync with the change.

### Evidence discipline still applies
Even inside tickets:
- Prefer `path/to/file:Symbol` evidence when describing a behavior change.
- If you can't confirm, mark it **UNKNOWN** and create a follow-up task for investigation.

### Active Notes Discipline
- Every active ticket must include a `## Notes` section.
- Every active ticket must include a `Noting Behavior` section aligned to
  ticket type (task/story/epic).
- New notes entries should be append-only and include:
  - `DATETIME`
  - `TYPE`:
    `FACT` | `UNKNOWN` | `HYPOTHESIS` | `DECISION` | `DECISION_REQUEST` |
    `PLAN` | `STRATEGY_DISCUSSION` | `ASSUMPTION_CHALLENGE` | `CONFLICT` |
    `TRADEOFF` | `BLOCKER` | `ALIGNMENT_CHECK` | `MEASURE` | `RISK` |
    `RAISE`
  - `CLAIM`
  - `EVIDENCE`:
    - inline (`path:start_line-end_line`) for one short path
    - one path per line when path count >= 2 or line would exceed hard cap
  - `IMPACT`
  - `NEXT`
  - `REREAD` (`REQUIRED` | `HELPFUL`)
  - `SCORE_0_TO_10` (must meet `workflow.ticket_microcycle.minimum_note_score`)






