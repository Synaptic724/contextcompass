

# Task: <short, action-focused title>

## Metadata
- Task ID: TASK-YYYY-MM-DD-<slug>
- Story: STORY-YYYY-MM-DD-<slug>
- Status: draft | ready | in_progress | blocked | done
- Owner: <accountable person/coordinator/team; not inferred technical author>
- Agent Name: <actual assigned executor names, comma-separated; not publishing account>
- Agent Role: <actual executor role/function; UNKNOWN if not established>
- Priority: p0 | p1 | p2 | p3
- Created: YYYY-MM-DDTHH:MM:SSZ
- Updated: YYYY-MM-DDTHH:MM:SSZ

## Objective
<Define the smallest meaningful outcome this task delivers.>

## Ticket Contract
- ENTRY_GATE: <active board row and latest note requirements before work starts>
- EXECUTION_BOUNDARY: <files/symbols/surfaces allowed in this task>
- DEPENDENCIES: <upstream/downstream tickets or docs this task depends on>
- EXIT_GATE: <conditions required before status can move to review/done>
- FAILURE_ESCALATION: <when to record DECISION_REQUEST/CONFLICT/BLOCKER>

## Scope Boundaries
- In scope:
- Out of scope:

## State Transition Event
- from_state: draft | ready | in_progress | blocked | review
- to_state: ready | in_progress | blocked | review | done
- transition_reason: <why this transition is valid now>

## Steps / Checklist
- [ ] 
- [ ] 
- [ ] Run Ticket Microcycle during execution:
      `Investigate -> Document -> Strategy/Plan -> Document -> Implement ->
      Document -> Validate -> Document`.
- [ ] Record meaningful attributed findings in supported Notes/comments or authorized linked evidence
      before dependent work; no forced body copy.

## Deliverables
- 

## Files / Paths Impacted
- 

## Validation
- Not run.
- Recommended commands:
  - 

## Risks / Rollback Notes
- 

## Applicable Anti-Patterns
- [ ] No status transition without evidence-backed transition reason.
- [ ] No implementation/validation from `UNKNOWN` or `HYPOTHESIS`.
- [ ] No closure without delegated acceptance or reserved-owner disposition and board-sync completion.

## Done Checklist
- [ ] Steps complete and checked off
- [ ] Deliverables produced and linked
- [ ] Documentation updated (if needed)
- [ ] Validation status recorded
- [ ] Unknown-first discipline followed (`UNKNOWN` promoted to `FACT` only with evidence)
- [ ] Notes quality maintained (`SCORE_0_TO_10` >=
      `workflow.ticket_microcycle.minimum_note_score`)
- [ ] Applicable anti-pattern checks are clear or escalated with evidence.
- [ ] Criteria, required tests/reviews and delegated acceptance or reserved-owner disposition recorded
- [ ] Board sync completed for successor routing or closure anchor update.

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

## Noting Behavior
- Note focus: tactical findings, concrete impacts, and single-step continuation.
- Multiple meaningful comments or authorized documents may hold findings directly; no forced
  body copy of every finding is required before ordinary continuation.
- Keep notes append-only; correct history only for factual errors.
- Promote `UNKNOWN` to `FACT` only with direct evidence pointers.

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
