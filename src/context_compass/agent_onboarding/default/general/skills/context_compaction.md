

# Context Compaction Policy

## Purpose
Ensure continuity and minimize lost context when a session is compacted or handed off.

## External Memory Priority
- Repository artifacts are the source of truth for durable context.
- `attention_board.md` is the canonical active-attention state and is mandatory
  during active work.
- Compaction summaries MUST be empty when the runtime/platform allows empty summaries.
- If empty summaries are not allowed, write only minimal pointer summaries:
  - high-level outcomes (no narrative replay)
  - policy anchor paths that MUST be re-read
  - active ticket path(s) or Issue URL(s)
  - changed file path(s)
  - next immediate action

## Required Review Set

Core review set (ALWAYS required) - review these files in order:
- `AGENTS.MD`
- `agent_onboarding/default/general/skills/execution_contract.md`
- `config/context_compass_config.yaml`
- `context_compass/SKILLS.MD`
- resolved role `SKILLS.MD` chain (parent-first; the SKILLS files themselves)
- `agent_onboarding/default/general/skills/compaction_requirements.md`
- the workflow skill for the selected work backend
- `attention_board.md`
- Active Epic/Story/Task tickets in the selected backend; in plugin mode also
  read `issue_board.md`, fetch Issue-body Status/Notes, and read relevant comments.
- **The role's baseline system-orientation set, when the role declares one and the
  files exist.** For `engineer` and everything inheriting it that is:
  - `system_docs/src_architecture.md`
  - `system_docs/src_architecture_index.md`
  - `system_docs/src_components_index.md`

  The narrative plus two maps - cheap, and compaction is exactly when you lose the
  shape of the system, so this is the wrong place to be frugal. This sits in the
  ALWAYS set deliberately: it is baseline in `engineer/SKILLS.MD` and named as
  baseline in `compaction_requirements.md`, and filing it under a conditional
  heading is what produced an agent concluding no trigger had fired and re-reading
  none of it.

Conditional review set (ONLY when triggered):
- `artifact_board.md` (when active tickets include artifacts or artifact disposition changes)
- `artifacts/README.md` (when artifact lifecycle protocol is active)

- **Do NOT bulk re-read `src_components.md` or `src_graph.md` here.** They are
  sliced through the indexes above, during the work, whenever a question needs
  them - which needs no trigger and no permission. Bulk-reading them at
  re-entry costs ~33,000 lines to reload context you will immediately compact
  again. Holding the indexes means you can look anything up in one slice; that
  is the point of holding them.

- Authoring instructions are on-demand and become mandatory when the session is
  actually writing a system document:
  - `agent_onboarding/default/design_engineer/skills/src_architecture_instructions.md`
  - `agent_onboarding/default/design_engineer/skills/tests_architecture_instructions.md`
  - `agent_onboarding/default/design_engineer/skills/src_components_instructions.md`
  - `agent_onboarding/default/design_engineer/skills/tests_components_instructions.md`
  - `agent_onboarding/default/engineer/skills/src_graph_usage.md`
  - `system_docs/tests_architecture.md`, `system_docs/tests_components.md`
    (when the work concerns the suite)

Read discipline (non-negotiable)
- Review-set document reads must be manual per file path.
- Loop-based/batch document-reading commands are forbidden (for/foreach/while
  loops, xargs-style runners, or piped file-list iterators).
- For files over 500 LOC, read in explicit 500-line chunks in sequential order.
- **This chunking rule is for documents you have decided to read whole. It is not
  a licence to read an indexed document whole.** `src_components.md` and
  `src_graph.md` are entered through their indexes and sliced to the section you
  need. Chunking a 25,000-line graph into fifty sequential reads is not
  discipline - it is the failure the index was built to prevent.

## Required Updates
- Update `attention_board.md` during work so active items, status, blockers, and
  next actions stay current.
- Before compaction/handoff, verify `attention_board.md` is current and matches
  active ticket status.
- Update the `## Notes` section of all active tickets with latest findings and
  `path:start_line-end_line` evidence pointers (use `start=end` for single-line evidence).
- Ensure each meaningful finding was written as a note before the next investigation tranche.
- Ensure UNKNOWN-first discipline was followed (unverified claims remain `UNKNOWN`).
- Ensure note entries carry re-entry metadata when required by the ticket contract.
- Capture open questions, decisions, and next steps in the relevant ticket.
- Ensure status fields and checkboxes are accurate.
- Ensure tickets carry enough state so compaction summaries can stay empty or minimal.
- If artifacts exist: keep ticket `Artifact Links` sections and `artifact_board.md` synchronized.

## Handoff Summary Checklist
- Current state and progress (what is done vs remaining).
- Key decisions and rationale.
- Known risks and active blockers.
- Immediate next steps (1-3 concrete actions).
- References to any critical files or paths.

## Post-Compaction Verification
After compaction, re-open the core review set and confirm:
- `agent_onboarding/default/general/skills/compaction_requirements.md` has been re-applied before any action.
- A `REONBOARD: COMPLETE` attestation (with read-integrity proof) was posted before any action.
- `attention_board.md` was re-opened and still matches active ticket state.
- If artifacts are active: `artifact_board.md` was re-opened and is consistent with tickets.
- The active tickets still represent the correct plan.
- The next steps are unambiguous.
- Re-onboarding document reads were performed manually per file path (no loop-based/batch reads).

