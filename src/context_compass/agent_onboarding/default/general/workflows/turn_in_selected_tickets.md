# Workflow: turn_in_selected_tickets

## Metadata
- Workflow ID: WF-turn-in-selected-tickets
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
  - user explicitly asks to turn in one or more tickets
- Created: 2026-04-26T12:32:40Z
- Updated: 2026-04-26T12:32:40Z

## Purpose
Provide a lighter closure path than full cleanup:
- list candidate tickets
- ask which tickets should be turned in
- close only the selected set
- sync board and artifact state

## Required Reads
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `attention_board.md`
- `artifact_board.md`
- `agent_onboarding/default/general/skills/ticketing.md`

## Required Skills
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `agent_onboarding/default/general/skills/ticketing.md`

## Backend Routing
Resolve YAML and fetch/read the candidate tickets before asking for selection.
`all` means the displayed candidate set, never every Issue in the repository.
Local closure uses the inherited local closure skill. Plugin closure preserves
the Issue body and Notes, records completion, verifies the body, closes through
the plugin, and releases the local claim. Use the selected backend's workflow
and keep its acceptance gate and board/artifact sync rules.

## Phase Sequence
1. Intake
- objective:
  - define the candidate closure set
- required actions:
  - list the current candidate tickets
- stop conditions:
  - no candidate tickets exist

2. Investigation
- objective:
  - identify the selectable set
- required actions:
  - review board and artifact state for the candidates
- required note or artifact updates:
  - record the candidate set in the owning task notes

3. Strategy
- objective:
  - obtain explicit closure selection
- required actions:
  - ask which tickets should be turned in
  - accept explicit selection or `all`
- decision points:
  - selected subset vs full set

4. Implementation
- objective:
  - close the selected tickets only
- scope controls:
  - in `local`, move selected tickets to completed folders
  - in `github_codex_plugin`, verify completion metadata and close selected Issues
  - release only the selected Issues' claims after confirmed closure
  - sync board and artifact state for each one

5. Validation
- objective:
  - prove the selected set is closed
- required checks:
  - selected tickets are no longer active on the board
  - canonical local completed paths or fetched Issue body/state prove closure
  - artifact rows reflect the closure outcome

6. Handoff / Closure
- objective:
  - summarize what was turned in and what remains
- required board or ticket sync:
  - leave unselected tickets routed if they remain active

## Attention Board Behavior
- Required row fields:
  - current active rows are the candidate set
- Mode transitions:
  - `handoff` after the selected set is turned in
- Exit signal rules:
  - selected tickets are closed and board/artifact state is synchronized

## Context / Handoff Summary
This workflow is the lighter sibling of `cleanup_context_compass`: chosen
ticket closure without the broader asset-scope prompt.
