
# Context Compaction Policy

## Purpose
Ensure continuity and minimize lost context when a session is compacted or
handed off.

## External Memory Priority
- Repository artifacts are the source of truth for durable context.
- `attention_board.md` is the canonical active-attention state and is mandatory
  during active work.
- Compaction summaries MUST be empty when the runtime/platform allows empty summaries.
- If empty summaries are not allowed, write only minimal pointer summaries:
  - high-level outcomes (no narrative replay)
  - critical policy anchor paths that MUST be re-read
  - active ticket path(s) or Issue URL(s)
  - changed file path(s)
  - next immediate action
- Avoid narrative replay; keep durable state externalized to files.

## Required Review Set
Before initiating compaction/handoff:
- You MUST ensure the durable state is up to date:
  - `attention_board.md` reflects the current routing, status, blockers, and next actions.
  - Active tickets linked from `attention_board.md` have current checklists and `## Notes`.

Core review set - apply the Project Instructions Bootstrap in `AGENTS.MD`
first, then complete every requirement not explicitly overridden. Count an
already completed read once for this trigger rather than restarting the sequence:
- `AGENTS.MD`
- `special_instructions/` project rules and resolved overrides
- `CONTEXT_COMPACTION.md`
- `agent_onboarding/default/general/skills/execution_contract.md`
- `config/context_compass_config.yaml`
- `SKILLS.MD`
- resolved role `SKILLS.MD` chain (parent-first; the SKILLS files themselves)
- `agent_onboarding/default/general/skills/compaction_requirements.md`
- the workflow skill for the selected work backend
- `attention_board.md`
- Active Epic/Story/Task tickets in the selected backend; in plugin mode also
  read `issue_board.md`, fetch Issue-body Status/Notes, and read relevant comments.

Conditional review set (ONLY when triggered):
- `artifact_board.md` (when active tickets include artifacts or artifact disposition changes)
- `artifacts/README.md` (when artifact lifecycle protocol is active)

System-context documents are governed by ONE document, and it is not this one:

- **`agent_onboarding/default/general/skills/context_compaction.md` is canonical**
  for which `system_docs/*` are re-read at compaction, which are sliced during the
  work, and which are on-demand. Follow it.
- This file previously restated that policy and drifted from it - it gated the
  orientation set behind a trigger list and named `src_components.md` as a whole-
  document read, both of which are now wrong. The restatement is removed rather
  than repaired, because a policy maintained in two places is a policy that will
  disagree again.

The short version, so this file is not misleading on its own: the role's baseline
orientation set is re-read at re-entry, and the large indexed documents are sliced
through their indexes during the work whenever a question needs them - no trigger
and no permission required. The canonical text is in the skill above.

Read discipline (non-negotiable)
- Review-set document reads must be manual per file path.
- Loop-based/batch document-reading commands are forbidden (for/foreach/while
  loops, xargs-style runners, or piped file-list iterators).
- For files over 500 LOC, read in explicit 500-line chunks in sequential order.
- **That chunking rule governs documents you have decided to read whole. It is
  NOT an instruction to read an indexed document whole.** `src_components.md`,
  `src_graph.md` and `llm_full.md` are entered through their indexes and sliced.

## Required Updates
- Update `attention_board.md` during work so active items, status, blockers, and
  next actions stay current.
- Update `artifact_board.md` when active tickets have artifacts or artifact
  disposition changes.
- Before compaction/handoff, verify `attention_board.md` is current and matches
  active ticket status.
- Update the `## Notes` section of all active tickets with latest findings and
  `path:start_line-end_line` evidence pointers (use `start=end` for single-line
  evidence).
- Ensure each meaningful finding was written as a note before the next
  investigation tranche (no end-of-pass batching).
- Ensure UNKNOWN-first discipline was followed (unverified claims remain
  `UNKNOWN`).
- Ensure note entries carry re-entry metadata:
  - `REREAD` (`REQUIRED` or `HELPFUL`)
  - `SCORE_0_TO_10` compaction usefulness score
- Update the "Context / Handoff Summary" section of all active tickets.
- Capture open questions, decisions, and next steps in the relevant ticket.
- Ensure status fields and checkboxes are accurate.
- Ensure tickets carry enough state so compaction summaries can stay empty or
  minimal.
- Ensure ticket `Artifact Links` sections and `artifact_board.md` stay
  synchronized when artifacts exist.

## Handoff Summary Checklist
- Current state and progress (what is done vs remaining).
- Key decisions and rationale.
- Known risks and active blockers.
- Immediate next steps (1-3 concrete actions).
- References to any critical files or paths.

## Post-Compaction Verification
After compaction/handoff, before any action:
- `agent_onboarding/default/general/skills/compaction_requirements.md` has been
  re-applied before any action.
- A `REONBOARD: COMPLETE` attestation (with read-integrity proof) was posted before any action.
- `attention_board.md` was re-opened and still matches active ticket state.
- `artifact_board.md` was re-opened when artifact-linked tickets are active.
- The active tickets still represent the correct plan.
- The next steps are unambiguous.
- Re-onboarding document reads were performed manually per file path (no
  loop-based/batch document reads).
