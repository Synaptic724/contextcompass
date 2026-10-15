

# Story: <short, outcome-focused title>

## Metadata
- Story ID: STORY-YYYY-MM-DD-<slug>
- Epic: EPIC-YYYY-MM-DD-<slug>
- Status: draft | ready | in_progress | blocked | done
- Owner: <accountable person/coordinator/team; not inferred technical author>
- Agent Name: <actual assigned executor names, comma-separated; not publishing account>
- Agent Role: <actual executor role/function; UNKNOWN if not established>
- Priority: p0 | p1 | p2 | p3
- Created: YYYY-MM-DDTHH:MM:SSZ
- Updated: YYYY-MM-DDTHH:MM:SSZ

## User Narrative
As a <user/persona>, I want <capability>, so that <outcome>.

## Value / MRP Alignment
<Explain how this story strengthens the holistic core.>

## Ticket Contract
- ENTRY_GATE: <active board row and linked task/story prerequisites satisfied>
- EXECUTION_BOUNDARY: <story-level surfaces allowed; no unrelated expansion>
- DEPENDENCIES: <task set and prerequisite tickets/stories/epic milestones>
- EXIT_GATE: <acceptance + child-task state + board-sync requirements>
- FAILURE_ESCALATION: <when to raise DECISION_REQUEST/CONFLICT/BLOCKER>

## Requirements (Functional)
- 

## Requirements (Non-Functional)
- 

## Scope Boundaries
- In scope:
- Out of scope:

## State Transition Event
- from_state: draft | ready | in_progress | blocked | review
- to_state: ready | in_progress | blocked | review | done
- transition_reason: <why this transition is valid now>

## Dependencies / Related Work
- 

## Tasks (Implementation Checklist)
- [ ] Task: <TASK-ID> - <short description>
- [ ] Task: <TASK-ID> - <short description>
- [ ] Enforce Ticket Microcycle across all linked tasks.
- [ ] Record meaningful attributed findings in supported Notes/comments or authorized linked evidence.

## Acceptance Criteria
- 

## Validation / Test Plan
- 

## UX / API / Data Notes
- 

## Risks / Mitigations
- 

## Applicable Anti-Patterns
- [ ] No story-state transition without linked task-state evidence.
- [ ] No closure while required tasks remain active or un-routed.
- [ ] No cross-task synthesis claims without ticket-note evidence pointers.

## Open Questions
- 

## Decision Log
- 

## Artifact Links (Optional)
Qualified independent reviewer acceptance and direct closure follow shared `ticketing.md`;
this does not make independent review mandatory for every ticket.

- ARTIFACTS_REQUIRED: true | false
- ARTIFACT_PATHS:
  - <artifacts/YYYY-MM-DD_<slug>.<ext>>
- DISPOSITION: delete_on_close | retain_as_reference | promote_to_documentation
- CLEANUP_TRIGGER: <when artifact cleanup/retention decision is applied>

## Context Management
- CONTEXT_MANAGEMENT_REQUIRED: true | false
- CONTEXT_IDS:
  - CTX-YYYY-MM-DD-<slug> | UNKNOWN
- CONTEXT_TOPICS:
  - <topic or question> | UNKNOWN
- IF_UNKNOWN: UNKNOWN | ask user before implementation | none

## Contribution Attribution
- Ticket/Work Author(s): <actor; contribution kind; scope; artifact revision; evidence>
- Published By: <observed hosting service/account and receipt; UNKNOWN before publication>
- Independent Review: <reviewer; exact target revision/scope; verdict/evidence; independence>

## Notes
- DATETIME: YYYY-MM-DDTHH:MM:SSZ
  AUTHOR: <full assigned agent name or verified human author>
  AUTHOR_ROLE: <actual role/function>
  TYPE:
    FACT | UNKNOWN | HYPOTHESIS | DECISION | DECISION_REQUEST | PLAN |
    STRATEGY_DISCUSSION | ASSUMPTION_CHALLENGE | CONFLICT | TRADEOFF |
    BLOCKER | ALIGNMENT_CHECK | MEASURE | RISK | RAISE
  CLAIM: <short finding>
  EVIDENCE:
  - <path:start_line-end_line>
  - <path:start_line-end_line>
  IMPACT: <why this matters>
  NEXT: <one concrete next action>
  REREAD: REQUIRED | HELPFUL
  SCORE_0_TO_10: <0-10 compaction usefulness>

## Closure Confirmation
- [ ] Work walkthrough shared with user
- [ ] Criteria, required tests/reviews and delegated acceptance or reserved-owner disposition recorded
- [ ] Applicable anti-pattern checks are clear or escalated with evidence.

## Noting Behavior
- Note focus: cross-task synthesis, dependency flow, and state-transition logic.
- Add notes when task routing changes, gate decisions are made, or risks shift.
- Reference child-task notes for evidence instead of duplicating tactical detail.
- Keep notes append-only and preserve UNKNOWN-first promotion discipline.
- Multiple meaningful comments may hold evidence directly; no forced body copy before ordinary
  continuation. Current scope/state/decisions/handoff stay coherent at material transitions.

## Context / Handoff Summary
<One current resume view: scope/outcome; controlling decisions/holds; source/evidence revision;
completed/remaining criteria; failed/unrun limits; owners; next 1-3 actions and necessary links.>
Update this view in place. Preserve historical Notes/comments and link unchanged context/full evidence.

## Project-Specific Additions
<!-- BEGIN USER-DEFINED: project_fields -->
<!-- END USER-DEFINED: project_fields -->

<!--
Anything this project needs on every ticket of this kind goes in the region
above: extra fields, a compliance checklist, a link to a local convention.

The region is yours. An upgrade replaces every other line of this template with
the new version's text and carries this region across untouched, so a local
addition here is not a divergence you re-resolve on every upgrade - which is
what editing the rest of the template would cost you.
-->
