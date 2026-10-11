

# reactive_documentation

Purpose
- Keep compaction-proof breadcrumbs while work is in flight.
- Capture broad findings quickly without losing source truth.
- Preserve momentum by recording only what must be re-read later.

When to use
- Any investigation, debugging pass, architecture revalidation, or broad repo trace.
- Immediately after discovering a core claim that could be lost after compaction.

Core stance
- Do not dump raw transcript sludge as durable memory.
- Do not over-structure notes into heavy ceremony.
- Use targeted, broad claims plus exact evidence pointers.
- Start from UNKNOWN and promote to FACT only with evidence.

Canonical storage
- Tickets are first-class memory:
  - `Notes` for in-flight findings captured during execution.
  - `Decision Log` for accepted facts and decisions.
  - `Unknowns` for unresolved or blocked claims.
  - `Context / Handoff Summary` for current state and next actions.
- `attention_board.md` is routing-only state, not detailed finding storage.
- Avoid creating side memory stores unless explicitly requested.

Reactive capture protocol (mandatory)
1) Classify claim type:
   - `FACT`: verified directly in source.
   - `UNKNOWN`: not yet verified or ambiguous.
   - `HYPOTHESIS`: explicit idea/opinion awaiting evidence.
   - `DECISION`: explicit direction and rationale.
   - `DECISION_REQUEST`: explicit Architect decision required before proceeding.
   - `PLAN`: concrete next implementation slice.
   - `STRATEGY_DISCUSSION`: structured options analysis needed before implementation.
   - `ASSUMPTION_CHALLENGE`: explicit challenge to an assumption with evidence.
   - `CONFLICT`: evidence-backed contradiction between direction and mission outcomes.
   - `TRADEOFF`: multiple viable options with meaningful pros/cons.
   - `BLOCKER`: hard stop requiring external unblock action.
   - `ALIGNMENT_CHECK`: explicit scope/intent confirmation checkpoint.
   - `MEASURE`: validation/profiling result.
   - `RISK`: risk that needs mitigation follow-up.
   - `RAISE`: immediate generic escalation when a serious issue is detected and precise type is not yet clear.
2) Record one broad claim line:
   - 1-2 sentences, general and scannable.
3) Attach evidence pointers:
   - `path/to/file.py:start_line-end_line` (preferred), plus symbol when useful.
4) Mark re-read priority:
   - `REQUIRED`: must reopen on next session.
   - `HELPFUL`: context only.
5) Add compaction usefulness score:
   - `SCORE_0_TO_10` (must meet
     `workflow.ticket_microcycle.minimum_note_score`).
6) Record one concrete next action:
   - single step that moves verification or implementation forward.

Entry template
- `DATETIME`: `YYYY-MM-DDTHH:MM:SSZ`
- `TYPE`:
  FACT | UNKNOWN | HYPOTHESIS | DECISION | DECISION_REQUEST | PLAN |
  STRATEGY_DISCUSSION | ASSUMPTION_CHALLENGE | CONFLICT | TRADEOFF |
  BLOCKER | ALIGNMENT_CHECK | MEASURE | RISK | RAISE
- `CLAIM`: <broad finding>
- `EVIDENCE`:
  - <path:start_line-end_line>
  - <path:start_line-end_line>
- `REREAD`: REQUIRED | HELPFUL
- `SCORE_0_TO_10`: <0-10>
- `NEXT`: <single concrete step>
- Detailed collaboration semantics for each `TYPE` are defined in:
  `context_compass/agent_onboarding/default/general/skills/execution_contract.md`.
- `RAISE` notes must be recategorized to a concrete type within one microcycle.

Quality bar
- Prefer targeted claims over narrative replay.
- Every durable claim needs `file:start_line-end_line` evidence.
- No evidence means mark it `UNKNOWN`.
- Keep entries append-only when possible.

Anti-patterns
- Long logs with no evidence.
- Broad assertions with no file pointers.
- Rewriting history instead of adding incremental updates.
- Treating speculative reasoning as fact.
- Implementing directly from UNKNOWN/HYPOTHESIS without evidence-backed promotion.

Re-entry checklist
- Open active ticket handoff summary first.
- Re-open entries marked `REREAD: REQUIRED`.
- Resume from the most recent `NEXT` action.

References
- `agent_onboarding/default/general/skills/memory_management.md`
- `agent_onboarding/default/general/skills/active_documentation.md`
- `agent_onboarding/default/general/skills/compaction_requirements.md`
- the selected backend's general workflow skill
- `context_compass/SKILLS.MD`






