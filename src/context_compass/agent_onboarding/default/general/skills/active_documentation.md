

# active_documentation

Purpose
- Keep durable, compaction-safe working memory directly inside active tickets.
- Ensure findings are captured with concrete evidence pointers while work is in
  flight.
- Prevent context loss with durable evidence and one current resume view.

Core rule
- Every active ticket (epic/story/task) must include a `## Notes` section.
- During execution, save meaningful attributed findings when required by dependent work.
  Multiple meaningful comments or authorized documents may hold evidence directly; no forced
  body copy is required before ordinary continuation. Preserve historical Notes/comments.
- Evidence pointers must include file paths with explicit start/end line ranges
  (`path:start_line-end_line`).
- UNKNOWN is the default claim state until evidence promotes a claim to FACT.
- Do not continue investigation to the next finding until the current finding
  is documented.
- Before dependent code edits or validation, retain the relevant finding with evidence and
  next action in a supported durable contribution, not necessarily another body Note.

Canonical storage
- Primary: the selected ticket's Notes, supported comments and authorized linked evidence.
- Current state/scope/decisions/handoff stay coherent at material transitions and closure.
- Secondary: `attention_board.md` for routing state only.
- Do not move detailed findings into `attention_board.md`; keep detail in
  ticket notes.

Required note entry shape
For note entries:
- `DATETIME`: `YYYY-MM-DDTHH:MM:SSZ` (UTC)
- `TYPE`:
  `FACT` | `UNKNOWN` | `HYPOTHESIS` | `DECISION` | `DECISION_REQUEST` |
  `PLAN` | `STRATEGY_DISCUSSION` | `ASSUMPTION_CHALLENGE` | `CONFLICT` |
  `TRADEOFF` | `BLOCKER` | `ALIGNMENT_CHECK` | `MEASURE` | `RISK` |
  `RAISE`
- `CLAIM`: short technical finding.
- `EVIDENCE`: one or more `path:start_line-end_line` pointers.
- `IMPACT`: why this matters for current work.
- `NEXT`: one concrete next action.
- `REREAD`: `REQUIRED` | `HELPFUL`.
- `SCORE_0_TO_10`: must meet
  `workflow.ticket_microcycle.minimum_note_score`.
- `TYPE` semantics and conflict/strategy expectations are governed by:
  `context_compass/agent_onboarding/default/general/skills/execution_contract.md`.

Example
- `DATETIME`: 2026-02-14T00:00:00Z
- `TYPE`: FACT
- `CLAIM`: Role routing currently depends on explicit top-level map + config alignment.
- `EVIDENCE`:
  - `SKILLS.MD:27-42`
  - `config/context_compass_config.yaml:68-83`
  - `attention_board.md:1-20`
- `IMPACT`: Incorrect map/config alignment can route the agent to the wrong role chain.
- `NEXT`: Validate selected role path resolution before execution begins.

Update triggers (mandatory)
1) New verified finding.
2) New unknown/blocker.
3) Decision that changes scope or approach.
4) Measurement result (test/profile/benchmark).
5) Any meaningful finding that would be risky to lose on compaction.
6) Before handoff or compaction.

Quality bar
- Keep historical Notes/comments append-only unless correcting a factual error. Update only the
  one current resume view in place; link unchanged context and full evidence.
- Prefer high-signal claims with precise evidence over long narrative.
- If a finding is single-line evidence, still write a range with same start/end.
- Mark unverified items as `UNKNOWN`; never promote to fact without evidence.
- Never store secrets in notes.
- No implementation from `UNKNOWN` or `HYPOTHESIS` notes without evidence-backed promotion to `FACT` or `DECISION`.

References
- `agent_onboarding/default/general/skills/reactive_documentation.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/general/skills/ticketing.md`
- the selected backend's general workflow skill








