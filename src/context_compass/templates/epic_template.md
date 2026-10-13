

# Epic: <short, outcome-focused title>

## Metadata
- Epic ID: EPIC-YYYY-MM-DD-<slug>
- Status: draft | ready | in_progress | blocked | done
- Owner: <accountable person/coordinator/team; not inferred technical author>
- Agent Name: <actual assigned executor names, comma-separated; not publishing account>
- Agent Role: <actual executor role/function; UNKNOWN if not established>
- Priority: p0 | p1 | p2 | p3
- Created: YYYY-MM-DDTHH:MM:SSZ
- Updated: YYYY-MM-DDTHH:MM:SSZ
- Target Window: <e.g., 2026-Q1>
- Related Program/Initiative:

## Problem / Opportunity
<Describe the problem or opportunity with concrete evidence and context.>

## MRP Alignment (Most Reasonable Product)
<Explain the holistic core being built and why this is the right long-term foundation.>

## Ticket Contract
- ENTRY_GATE: <program lane is routed and prerequisite story set is defined>
- EXECUTION_BOUNDARY: <epic-level scope and explicit exclusions>
- DEPENDENCIES: <required stories, policies, and architecture anchors>
- EXIT_GATE: <all required stories accepted + board/closure sync complete>
- FAILURE_ESCALATION: <when to raise DECISION_REQUEST/CONFLICT/BLOCKER>

## Goals (Outcomes)
- 

## Non-Goals (Explicit Exclusions)
- 

## Scope Boundaries
- In scope:
- Out of scope:

## State Transition Event
- from_state: draft | ready | in_progress | blocked | review
- to_state: ready | in_progress | blocked | review | done
- transition_reason: <why this transition is valid now>

## Success Metrics
- 

## Requirements (Functional + Non-Functional)
- 

## Constraints / Assumptions
- 

## Dependencies / External References
- 

## Milestones (Track Progress)
- [ ] Milestone 1: <name> - <clear success criteria>
- [ ] Milestone 2: <name> - <clear success criteria>

## Stories (Required to Complete)
- [ ] Story: <STORY-ID> - <short description>
- [ ] Story: <STORY-ID> - <short description>

## Tasks (Cross-Cutting or Epic-Level)
- [ ] Task: Complete story <STORY-ID>
- [ ] Task: Complete story <STORY-ID>
- [ ] Task: <cross-cutting task>
- [ ] Task: Verify Ticket Microcycle enforcement across active tickets/stories/tasks.

## Acceptance Criteria (Epic Done)
- 

## Risks / Mitigations
- 

## Applicable Anti-Patterns
- [ ] No epic-state transition without story-level evidence.
- [ ] No closure while required stories are incomplete or unaccepted.
- [ ] No program claims without source evidence from story/task notes.

## Validation / Test Approach
- 

## Rollout / Adoption Plan
- 

## Open Questions
- 

## Decision Log
- 

## Artifact Links (Optional)
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
- Note focus: program-level direction, cross-story tradeoffs, and tranche order.
- Add notes when priorities, sequencing, or scope boundaries change.
- Reference story/task evidence instead of duplicating tactical execution logs.
- Keep notes append-only and preserve UNKNOWN-first promotion discipline.

## Context / Handoff Summary
<Succinct summary of current state, key decisions, and next steps for future context.>

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
