# Workflow: sync_attention_board

## Metadata
- Workflow ID: WF-sync-attention-board
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
  - user explicitly asks to rebuild or repair `attention_board.md`
- Created: 2026-04-26T12:32:40Z
- Updated: 2026-04-26T12:32:40Z

## Purpose
Rebuild or repair `attention_board.md` from current active ticket truth when
the board drifts or becomes stale.

## Required Reads
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `attention_board.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/general/skills/ticketing.md`

## Required Skills
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/general/skills/ticketing.md`

## Backend Routing
Resolve YAML before rebuilding. Local mode derives ticket truth from the local
lanes. Plugin mode fetches Issue bodies/state for current routes and claims in
`issue_board.md`; search the configured repository only when references are
missing. An unrelated open Issue is not automatically active Context Compass
work. Confirm scope/identity for unmatched candidates, and never infer an agent
claim from a GitHub assignee. Preserve protected regions and unrelated alerts.

## Phase Sequence
1. Intake
- objective:
  - confirm the board is the target
- required actions:
  - ask what drift or stale state the user wants corrected when not already explicit
- stop conditions:
  - target board problem is unclear

2. Investigation
- objective:
  - derive the true active set from tickets
- required actions:
  - inspect the current active tickets
  - read local files or fetch exact Issues through the selected backend
  - compare them to the current board rows
- required note or artifact updates:
  - record the mismatch set in the owning task notes

3. Strategy
- objective:
  - choose repair or full rebuild
- decision points:
  - small drift -> patch rows/details
  - large drift -> rebuild the active set from ticket truth

4. Implementation
- objective:
  - synchronize the board to ticket truth
- scope controls:
  - keep the board compact
  - keep artifact pointers out
  - preserve `owner` vs `agent_name`

5. Validation
- objective:
  - prove the board matches ticket truth
- required checks:
  - every active row maps to a live ticket
  - no completed-ticket paths remain in active rows
  - plugin routes have open Issues with matching body Status and primary claims

6. Handoff / Closure
- objective:
  - summarize what drift was fixed
- required board or ticket sync:
  - leave the board as the refreshed routing source of truth

## Attention Board Behavior
- Required row fields:
  - preserve the full active row schema
- Mode transitions:
  - usually `handoff` when sync is complete
- Exit signal rules:
  - the board matches current active ticket truth

## Context / Handoff Summary
This workflow repairs board drift without turning the board into a second ticket
system.
