# Workflow: start_context_compass_work

## Metadata
- Workflow ID: WF-start-context-compass-work
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
  - user explicitly asks to start a new Context Compass lane
- Created: 2026-04-26T12:32:40Z
- Updated: 2026-04-26T12:32:40Z

## Purpose
Start a new Context Compass lane in a structured way:
- ask what lane we are starting
- choose the right epic/story/task shape
- add the board row
- link patch artifacts when the lane is system-impacting

## Required Reads
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `attention_board.md`
- `agent_onboarding/default/general/skills/ticketing.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/engineer/skills/patch_framework_gating.md`

## Required Skills
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `agent_onboarding/default/general/skills/ticketing.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/engineer/skills/patch_framework_gating.md`

## Backend Routing
Resolve YAML before ticket work. In `local`, create the existing template files
and use relative paths. In `github_codex_plugin`, create template bodies through
the plugin in the configured repository, link parents/children by Issue URL,
and add the primary claims to `issue_board.md`. The shared patch/artifact gates
and lane-shape decisions apply in both modes. Use the selected backend's already
read general workflow; do not create a parallel local ticket for an Issue.

## Phase Sequence
1. Intake
- objective:
  - determine what lane is being opened
- required actions:
  - ask what lane we are starting
  - ask for the smallest meaningful outcome if the scope is too broad
- stop conditions:
  - lane objective is still ambiguous

2. Investigation
- objective:
  - classify the lane
- required actions:
  - decide whether this needs:
    - task only
    - story plus task
    - epic plus story plus task
  - decide whether patch artifacts are required
- required note or artifact updates:
  - record the lane classification in the owning task notes

3. Strategy
- objective:
  - define the startup structure
- decision points:
  - if system-impacting, create or require patch artifacts
  - if not system-impacting, stay ticket-only

4. Implementation
- objective:
  - stage the lane
- scope controls:
  - create the needed ticket stack
  - add the active board row
  - link patch artifacts if required

5. Validation
- objective:
  - prove the lane is routable
- required checks:
  - local ticket paths exist, or the plugin fetches the exact created Issues
  - plugin primary claims agree with the active row's assigned agents
  - the board row routes to the active ticket
  - patch links exist when required

6. Handoff / Closure
- objective:
  - summarize what lane was opened
- required board or ticket sync:
  - leave the new lane as active routed work

## Attention Board Behavior
- Required row fields:
  - create one new active row for the lane
- Mode transitions:
  - `discovery` while classifying
  - `implementation` once staged
- Exit signal rules:
  - the lane is fully routable with ticket and board state aligned

## Context / Handoff Summary
This workflow opens new work cleanly instead of letting implementation start
without proper ticket and board state.
