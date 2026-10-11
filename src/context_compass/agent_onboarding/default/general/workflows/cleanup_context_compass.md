# Workflow: cleanup_context_compass

## Metadata
- Workflow ID: WF-cleanup-context-compass
- Status: active
- Owner: user
- Allowed Roles:
  - general
  - engineer
  - design_engineer
  - platform_engineer
  - qa_engineer
  - security_engineer
  - user_defined/*
- Default Roles:
  - general
- Trigger:
  - user explicitly asks to clean up Context Compass work state
- Created: 2026-04-26T11:45:35Z
- Updated: 2026-04-26T11:45:35Z

## Not the same thing as the cleanup tool
This workflow cleans up **work state**: it closes tickets and syncs the boards.

`tools/cleanup_context_compass.py` cleans up **the package**: it returns files to
the state the manifest describes. Same words, different operation, and running
the wrong one is not a small mistake - this workflow closes tickets, that tool
deletes files.

If you want to turn in tickets, you are in the right document. If you want to
strip one project's content out of an install, see
`agent_onboarding/default/engineer/skills/package_maintenance.md`.

## Purpose
Provide one explicit cleanup workflow for Context Compass work state:
- ask whether to clean up "my assets" or "everything"
- list the candidate tickets
- ask the user which tickets to turn in
- if the user says `all`, close all candidate tickets
- sync `attention_board.md` and `artifact_board.md` through the normal closure
  rules

## Use When
- The user explicitly asks to clean up current Context Compass work.
- The user wants to turn in tickets and synchronize board/artifact state.

## Do Not Use When
- The user has not asked for cleanup.
- The user only wants to inspect state without closing tickets.
- The current lane is still ambiguous about which tickets should remain open.

## Inputs
- Required:
  - cleanup scope decision:
    - `my assets`
    - `everything`
  - ticket selection decision:
    - one or more listed tickets
    - `all`
- Optional:
  - target `AGENT_NAME` if `my assets` is selected and the active identity is
    not already explicit

## Outputs
- Expected artifacts:
  - selected local tickets moved to completed folders, or selected Issues closed
  - artifact rows updated according to existing artifact disposition rules
- Expected ticket state:
  - selected tickets closed
  - unselected tickets remain active
- Expected board state:
  - active rows for closed tickets removed or replaced
  - recently closed anchors updated

## Required Reads
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `attention_board.md`
- `artifact_board.md`
- `agent_onboarding/default/general/skills/ticketing.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/general/skills/agent_identity.md`

## Required Skills
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `agent_onboarding/default/general/skills/ticketing.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/general/skills/agent_identity.md`

## Backend Routing
Resolve YAML before collecting candidates. Preserve the same `my assets` versus
`everything` choice and explicit ticket selection in both modes. `everything`
means all current active board candidates; `all` means that reviewed set, not
every Issue in the remote repository. In plugin mode, fetch candidate bodies,
verify `issue_board.md` claims, and preserve Notes while closing selected Issues
through the plugin. GitHub assignees do not replace the `agent_name` scope filter.
Local mode uses the inherited local closure skill. Both modes retain acceptance,
artifact disposition, and attention detail/anchor synchronization gates.

## Preconditions / Gates
- A cleanup task ticket exists and is routed from `attention_board.md`.
- Candidate tickets are identified from the current active board state.
- The workflow asks the user:
  - "Do you want me to cleanup my assets or everything?"
- If `my assets` is chosen:
  - resolve the target `agent_name`
  - if no agent name can be determined, stop and ask
- Before any closure:
  - list the candidate tickets
  - ask which tickets should be turned in
  - if the user says `all`, treat all candidate tickets as selected

## Phase Sequence
1. Intake
- objective:
  - determine cleanup scope
- required actions:
  - ask: `Do you want me to cleanup my assets or everything?`
  - if `my assets`, identify the target `agent_name`
- stop conditions:
  - user does not choose a scope
  - `my assets` is chosen but the target agent identity is ambiguous

2. Investigation
- objective:
  - identify candidate tickets and artifacts
- required actions:
  - read `attention_board.md`
  - collect candidate tickets:
    - `my assets`: rows whose `agent_name` contains the target name
    - `everything`: all active rows
  - review ticket/artifact links for those candidates
- required note or artifact updates:
  - record the candidate set in the cleanup task `## Notes`

3. Strategy
- objective:
  - obtain explicit closure approval from the user
- required actions:
  - list the candidate tickets for the chosen scope
  - ask which tickets should be turned in
  - accept explicit ticket list or `all`
- decision points:
  - if the user picks a subset, close only that subset
  - if the user picks `all`, close all candidates

4. Implementation
- objective:
  - turn in the selected tickets
- scope controls:
  - close only explicitly selected tickets through the selected backend
  - move local tickets to completed folders, or verify completion and close Issues
  - release only the selected Issues' local claims after confirmed closure
  - run deterministic board sync for each closed ticket
  - apply existing artifact disposition rules for each closed ticket
  - do not close tickets the user did not select

5. Validation
- objective:
  - prove cleanup state is consistent
- required checks:
  - closed tickets are no longer routed in `## Active Items`
  - closed tickets appear in `## Recently Closed Anchors`
  - active attention details no longer route only to closed tickets
  - `artifact_board.md` reflects the closure/disposition results
  - canonical completed paths or fetched Issue body/state verify actual closure

6. Handoff / Closure
- objective:
  - summarize what was turned in and what remains
- required board or ticket sync:
  - update the cleanup task notes and handoff summary
  - leave any unclosed tickets still routed on the board

## Ticket Behavior
- Required ticket types:
  - one task to own the cleanup pass
- Required metadata:
  - `Agent Name`
- Required note cadence:
  - record the chosen scope
  - record the candidate ticket set
  - record the selected closure set
- Required artifact links:
  - none unless the cleanup lane itself creates support artifacts

## Attention Board Behavior
- Required row fields:
  - `agent_name` matters for `my assets` filtering
- Mode transitions:
  - `discovery` while identifying candidates
  - `implementation` while turning in selected tickets
  - `handoff` while summarizing what remains
- Exit signal rules:
  - all selected tickets are closed and board/artifact state is synchronized

## Escalation Rules
- Stop and ask if the user does not specify `my assets` or `everything`.
- Stop and ask if `my assets` is selected but agent identity is unclear.
- Stop and ask if a ticket selection is ambiguous.
- Raise `BLOCKER` if ticket/board state is too stale to identify candidates
  safely.

## Success Criteria
- The workflow always asks scope first.
- The workflow always lists candidate tickets before closure.
- Selected tickets are completed through the selected backend and verified.
- Board and artifact state are synchronized through the existing closure rules.

## Anti-Patterns
- Closing tickets without explicit user selection.
- Treating `artifact_board.md` as optional during cleanup.
- Wiping unrelated board rows when the user selected only `my assets`.
- Treating `owner` as the assigned agent identity instead of `agent_name`.

## Context / Handoff Summary
This workflow is the first concrete role-local workflow in Context Compass. It
is intentionally conservative: explicit user scope, explicit ticket selection,
then deterministic closure sync.
