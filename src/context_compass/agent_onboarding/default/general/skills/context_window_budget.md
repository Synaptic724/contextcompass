

# context_window_budget

Purpose
- Keep discovery FOCUSED so there is budget left to read the thing that matters
  properly. This is about aim, not about reading less.
- Prevent repeated context compaction caused by broad, unfocused repository scans.
- Force incremental discovery with durable notes in active tickets.

What this skill is about, and what it is NOT about
- It governs **how wide you range**, not **how carefully you read what is in front of
  you**. Those are different budgets and confusing them is the failure this section
  exists to prevent.
- **Reading the code you are about to change is never "expansion".** The
  implementation, the things it calls that your claim depends on, and its tests are
  IN scope by definition. Read them fully. That is the work, not a detour from it.
- If you find yourself using `grep` to avoid opening files because opening files feels
  expensive, you have applied this skill wrongly. A search hit is not a read and never
  substitutes for one - see
  `agent_onboarding/default/general/skills/unknowns_gate_reference.md`.

Core rule
- Do not attempt to read "the whole repo" during one investigation pass.
- Discovery must happen in bounded slices, with evidence logged before scope expands.
- UNKNOWN is the default claim state until evidence promotes the claim to FACT.
- Strict/relaxed microcycle enforcement is controlled by
  `config/context_compass_config.yaml`.

Scope budgeting protocol (mandatory)
1) Start from `attention_board.md` and the active ticket.
2) Investigate until one meaningful finding is identified.
3) Record the finding in supported Notes, attributed comments or authorized linked evidence.
4) Before dependent investigation, ensure that record has:
   - evidence (`path:start_line-end_line`),
   - impact,
   - concrete next step.
5) Repeat the loop for each additional meaningful finding.

Multiple meaningful comments may carry findings directly; no forced body copy is required
before ordinary continuation. Preserve historical Notes/comments and actual author attribution.

**Reading one unit through is ONE pass, not one per finding.** Do not stop in the
middle of a file to write a note. Finish the class, the method, the call path you
are following - then write up what you found, however many findings that is. A
single note may carry several.

This matters because the loop above, read strictly, rewards discovery in small
discrete hits - which is the shape `grep` produces and the opposite of the shape
reading produces. Fragmenting a read to satisfy a note cadence gets you notes about
lines instead of understanding of behaviour, and that is the trade going the wrong
way. The cadence exists so findings do not evaporate at compaction, not to
interrupt you mid-file.

Expansion gate
- If work requires jumping OUTSIDE the current subsystem, record why in ticket notes first.
- If planned discovery outside the current scope exceeds
  `workflow.ticket_microcycle.expansion_gate_max_files`, ask the user to
  confirm expansion.
- **The gate counts SCOPE, not files read.** It fires when you leave the subsystem the
  ticket is about - not when you open the fifth file inside it. The implementation you
  are changing, what it calls, and its tests are one scope however many files that is,
  and no permission is needed to read them.
  - Read literally as a five-file cap it produces the opposite of its intent: an agent
    that greps rather than opens, to stay under a number. Counting files was never the
    point; not wandering into unrelated subsystems was.

Structured Note/state-event payload
- The fields below apply to structured Notes. Supported ordinary comments follow shared
  `ticketing.md`: actual author/role, result, evidence, limits and next action, without
  copying every report or requiring every structured Note field.
- `DATETIME` (`YYYY-MM-DDTHH:MM:SSZ`)
- `TYPE`:
  `FACT` | `UNKNOWN` | `HYPOTHESIS` | `DECISION` | `DECISION_REQUEST` |
  `PLAN` | `STRATEGY_DISCUSSION` | `ASSUMPTION_CHALLENGE` | `CONFLICT` |
  `TRADEOFF` | `BLOCKER` | `ALIGNMENT_CHECK` | `MEASURE` | `RISK` |
  `RAISE`
- `CLAIM`
- `EVIDENCE` (`path:start_line-end_line`)
  - The range must cover **the logic the claim describes** - normally a whole
    function or method. `start=end` is valid only for a genuinely single-line fact:
    a config value, a constant, a declaration, an import.
  - A one-line range under a claim about BEHAVIOUR is the signature of a search hit
    pasted in place of a read. See "A SEARCH HIT IS NOT A READ" in
    `agent_onboarding/default/general/skills/unknowns_gate_reference.md`.
- `IMPACT`
- `NEXT`
- `REREAD` (`REQUIRED` | `HELPFUL`)
- `SCORE_0_TO_10` (must meet
  `workflow.ticket_microcycle.minimum_note_score`)

Anti-patterns
- Ranging across architecture, components and unrelated subsystems with no ticket
  notes in between. The defect is the absent notes and the unfocused range - NOT the
  reading. Reading the code in the scope you are working is required, not a smell.
- Using `grep`, `rg` or AST output in place of opening the file, to keep an
  investigation looking small. That is not budget discipline; it is a claim with no
  evidence behind it.
- Deferring all findings to an end-of-pass summary.
- Keeping critical findings only in temporary chat context.
- Implementing directly from `UNKNOWN` or `HYPOTHESIS` without evidence-backed promotion.

Success criteria
- Active tickets remain sufficient to resume work after compaction without replaying large context.
- Each meaningful finding leaves explicit evidence and a concrete next action.

References
- `agent_onboarding/default/general/skills/active_documentation.md`
- `agent_onboarding/default/general/skills/reactive_documentation.md`
- `agent_onboarding/default/general/skills/compaction_requirements.md`
- the YAML-selected backend's general workflow skill



