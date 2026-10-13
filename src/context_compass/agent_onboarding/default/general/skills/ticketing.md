

# ticketing

Purpose
- Define the ticketing system used to plan, execute, and close work in this repo.

Ticket types
- Epic: big project or cross-cutting initiative with multiple stories.
- Story: medium scope, user- or system-facing slice that can stand alone or live under an epic.
- Task: small, single deliverable that can stand alone.

Templates
- `templates/epic_template.md`
- `templates/story_template.md`
- `templates/task_template.md`
- `configuration_standards.md`
- `artifact_board.md`
- `context_management/context_board.md`

New-ticket design
- Resolve `ticket_design` guidance and template paths using `ticket_design.md`.
- Optional Agile metadata and named attribution follow that source-owned contract.
  Do not migrate old tickets, replace the full composition, or infer agent identity
  from the hosting account. When metadata is present, its derived Status replaces
  the ordinary Status enum for that ticket only; all actual acceptance gates remain.

Deep descriptive model (required)
Each ticket must be specific, evidence-based, and durable. Avoid vague goals.

Required elements
- Agent Name metadata (one or more assigned names; comma-separated when multiple)
- Problem / Opportunity
- Context (why now, relationship to architecture)
- MRP alignment
- Ticket Contract (`ENTRY_GATE`, `EXECUTION_BOUNDARY`, `DEPENDENCIES`,
  `EXIT_GATE`, `FAILURE_ESCALATION`)
- Goals / Non-goals
- Scope boundaries
- Requirements (functional + non-functional)
- Acceptance criteria (observable outcomes)
- Risks / Mitigations
- Validation plan (tests or verification)
- Decision log
- State Transition Event (`from_state`, `to_state`, `transition_reason`)
- Applicable Anti-Patterns (lane-specific checklist only)
- Noting Behavior (task/story/epic focus)
- Artifact Links (Optional, required when artifacts exist)
- Context Management (Optional, only when reusable reread packs are needed)
- Notes (active findings with evidence pointers)
- Context / Handoff summary

Workflow rules
1) Choose the smallest ticket type that fits the scope:
   - Big project: epic -> stories -> tasks.
   - Medium scope: story -> tasks.
   - Small scope: task only.
2) Keep links consistent (epic <-> story <-> task IDs) when using multiple levels.
3) Track progress with checkboxes and status fields.
4) Use the Ticket Microcycle while active:
   - `Investigate -> Document -> Strategy/Plan -> Document -> Implement -> Document -> Validate -> Document`.
5) Record each meaningful changed finding once in `## Notes` before dependent work,
   at the appropriate ticket depth; unchanged checks/ACKs are not substantive findings.
6) Treat new claims as `UNKNOWN` by default; promote to `FACT` only with evidence.
7) If investigation expands beyond the current subsystem or exceeds
   `workflow.ticket_microcycle.expansion_gate_max_files`, add a `DECISION`
   note and request user confirmation.
8) Update Context / Handoff Summary as work changes.
9) Before closing a ticket:
   - The assigned agent owns current status, evidence, requested scoped review and final closure.
   - Review is proportionate to actual consequence, uncertainty and the contract, not an automatic
     full-code-review parking state. High-consequence or uncertain changes request scoped review
     of the actual revision and question; self-checks are not independent review.
   - Authorized agents close routine completed work after criteria, required tests and required
     reviews are satisfied, without another owner ping. Reserved owner decisions still wait.
     Missing authority or a required gate is a specific blocker; do not infer acceptance.
10) After acceptance under delegated authority or explicit reserved-owner disposition:
   - Add a completion summary + UTC datetime.
   - In local mode, move the ticket to its matching completed folder.
   - In plugin mode, record accepted metadata and its derived Status for an Agile
     design, or `Status: done` for a non-Agile design. Record the transition reason,
     verify the body, close the Issue, and verify state through the plugin.
11) Immediately run deterministic closure sync for `attention_board.md`:
   - Remove/replace active row(s) that point to the closed ticket.
   - Prune stale attention details tied only to the closed ticket.
   - Add one compact row under `Recently Closed Anchors`.
   - Keep anchor rows capped (oldest removed first).
12) If ticket artifacts exist, run artifact closure sync:
   - Apply artifact disposition (`delete_on_close`, `retain_as_reference`, or
     `promote_to_documentation`).
   - Update `artifact_board.md` active/cleared entries.

Mandatory execution gates
- Active ticket gate:
  - Do not implement or validate without an active ticket in the selected backend.
- Routing gate:
  - Do not implement or validate unless `attention_board.md` has an active row
    that points to the same active ticket.
- Notes gate:
  - Do not start another investigation/edit/validation tranche until the current
    meaningful finding is appended to ticket `## Notes` with evidence pointers.
- Repair gate:
  - If any gate is broken or stale, stop and repair ticket/board/notes state
    before continuing.
- Artifact gate:
  - When artifacts are present, ticket `Artifact Links (Optional)` and
    `artifact_board.md` must stay synchronized.
- Context-management gate:
  - Context management is optional.
  - When `CONTEXT_MANAGEMENT_REQUIRED: true`, ticket `Context Management` and
    `context_management/context_board.md` must stay synchronized.
  - Tickets should reference reusable context packs by `Context ID`.
  - When `CONTEXT_MANAGEMENT_REQUIRED: true`, do not implement or validate
    until linked context artifacts were actually read.
  - When `CONTEXT_MANAGEMENT_REQUIRED: true`, keep the linked context artifact
    updated during the Ticket Microcycle whenever meaningful findings change
    the reread bundle or active topics.
- Attention-board boundary gate:
  - `attention_board.md` must remain ticket-routing-only (no artifact pointers).

Notes format requirement
- New note entries should include:
  - `DATETIME` (ISO-8601 UTC: `YYYY-MM-DDTHH:MM:SSZ`)
  - `AUTHOR` (full assigned agent name or verified human author)
  - `AUTHOR_ROLE` (actual role/function, not inferred from the publishing account)
  - `TYPE`:
    `FACT` | `UNKNOWN` | `HYPOTHESIS` | `DECISION` | `DECISION_REQUEST` |
    `PLAN` | `STRATEGY_DISCUSSION` | `ASSUMPTION_CHALLENGE` | `CONFLICT` |
    `TRADEOFF` | `BLOCKER` | `ALIGNMENT_CHECK` | `MEASURE` | `RISK` |
    `RAISE`
  - `CLAIM`
  - `EVIDENCE`:
    - inline form for one short path (`path:start_line-end_line`)
    - one path per line when path count >= 2 or line would exceed hard cap
  - `IMPACT`
  - `NEXT`
  - `REREAD` (`REQUIRED` | `HELPFUL`)
  - `SCORE_0_TO_10` (compaction usefulness score; improve entries below
    `workflow.ticket_microcycle.minimum_note_score`)
- Keep notes append-only except when correcting factual errors.
- Preserve all existing history and custom regions; concise Notes do not authorize historical compaction.
- Keep concise claim, impact, material limits and next action inline, with exact retrievable
  comment/doc links for supporting detail; do not copy full linked reports. A link alone does not
  replace required in-body state, decisions, evidence or unresolved limits.
- Unchanged checks/ACKs do not require a substantive finding Note; required state/routing/evidence
  updates still apply. This does not relax configured timing or note-quality gates.
- In plugin mode, `## Notes` remains in the Issue body. A full-body update must
  preserve every previous note and unrelated section; follow `github/codex_plugin.md`.
- Deep semantic meaning and collaboration behavior for each `TYPE` are defined in:
  `context_compass/agent_onboarding/default/general/skills/execution_contract.md`.

Per-ticket noting behavior
- Task notes: tactical findings, immediate impacts, and one-step continuation.
- Story notes: cross-task synthesis, dependency movement, and gate transitions.
- Epic notes: program direction, cross-story tradeoffs, and tranche order.
- Parent owners reconcile child outcomes and remaining work in synthesis Notes, not duplicate
  tactical logs. Child completion does not accept the parent; its own criteria/authority still apply.

Status discipline
- Update Status and Updated fields on each state change (UTC DateTime: `YYYY-MM-DDTHH:MM:SSZ`).
- Keep `Agent Name` current when ticket assignment changes.
- Prefer: draft -> ready -> in_progress -> blocked/done.
- If blocked, document the blocker and the unblock action.

Ticket contract discipline
- Every active ticket should contain `Ticket Contract`.
- Every status transition should be documented via `State Transition Event`.
- Keep anti-pattern checks local to the lane (`Applicable Anti-Patterns`);
  do not duplicate a global anti-pattern catalog in each ticket.

Config authority
- Source thresholds from `config/context_compass_config.yaml` under
  `workflow.ticket_microcycle`.
- Values are authoritative in YAML.
- Do not duplicate numeric defaults in policy docs.
- Ticket contract gates are authoritative under `workflow.ticket_contract`.
- Note behavior defaults are authoritative under `workflow.note_behavior`.
- Artifact protocol is authoritative under `artifacts`.

Formatting discipline
- Follow `configuration_standards.md`.
- Default prose target is 90-110 characters per line.
- Hard cap is 120 characters per line.
- `EVIDENCE` should use one path per line when multiple paths are present or
  inline length would exceed hard cap.

Validation reporting
- Never claim tests ran unless they actually ran.
- If not run, say "Not run" and explain why.

Optional context-management section
- Tickets may include:
  - `CONTEXT_MANAGEMENT_REQUIRED: true | false`
  - `CONTEXT_IDS:` (0 or more `Context ID` values from
    `context_management/context_board.md`)
  - `CONTEXT_TOPICS:` (0 or more topic bullets)
  - `IF_UNKNOWN:` (`UNKNOWN` | `ask user before implementation` | `none`)
- Default posture:
  - `CONTEXT_MANAGEMENT_REQUIRED: false`
- If a required context-management field is not known, write `UNKNOWN`
  explicitly.

