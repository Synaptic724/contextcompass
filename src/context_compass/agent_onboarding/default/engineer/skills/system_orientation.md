

# system_orientation

Purpose
- Provide a consistent way to explain this repo's workflow and docs.
- Translate agent stories and repo docs into clear, actionable guidance.

When to use
- The user asks how the system works or how to interact with it.
- The user wants a concise walkthrough before work begins.

Required behavior
- Start with the authority chain from `AGENTS.MD`.
- Read the required docs before explaining how the system works:
  - `AGENTS.MD`
  - `config/context_compass_config.yaml`
  - `SKILLS.MD`
  - `agent_onboarding/default/general/SKILLS.MD`
  - `agent_onboarding/default/engineer/SKILLS.MD`
  - the selected backend's general workflow skill
- Do not restate or override policy; cite the relevant skill or doc.

Core references
- Fresh-install posture for `system_docs/`: `system_docs/system_docs_read_first.md`
  (read this before asserting that a context map is missing or wrong)
- Agent stories: `agent_onboarding/default/general/behavioral_guidelines/README.md`
- Ticketing: the selected backend's general workflow skill and `templates/`
- System context, in the order it is meant to be used - each step names the key the
  next one is looked up by. Do not treat these as a flat menu:
  1. `system_docs/src_architecture.md` - which part of the system (read whole)
     plus `system_docs/src_architecture_index.md` to slice back into it later
  2. `system_docs/src_components_index.md` - look up that part
  3. `system_docs/src_components.md` - **slice**: what it owns, its Key Files
  4. `system_docs/src_graph_index.md` - look up those nodes
  5. `system_docs/src_graph.md` - **slice**: wiring, ownership, callers
  6. the code itself - the only authoritative account of current behaviour

  Steps 1 and 2 are **baseline** - the narrative and the two indexes, read at
  onboarding when they exist. Everything below them is **Self-directed**: you slice
  it yourself, unprompted, whenever the work needs it. No trigger list, no
  permission step - which is why it is not called On-demand, a state that does have
  a trigger and does mean wait. Authority for both halves is
  `agent_onboarding/default/engineer/SKILLS.MD`.
- Graph workflow context: `agent_onboarding/default/engineer/skills/src_graph_usage.md`
- Test architecture context: `system_docs/tests_architecture.md`
- Test components context: `system_docs/tests_components.md`
  (the tests pair describes the suite; it is not step 7 of the chain above, and it
  is Self-directed - read it when the work concerns the suite, not because you were
  already reading the src pair, and not because something gave you permission)
- Active patch docs (when patch lane is active):
  `system_docs/patches/active/<patch_id>/`
- Repo examples: `examples/` (within context_compass)

Artifact taxonomy (curated vs scratch)
- Curated, user-owned (source of truth):
  - `attention_board.md` (canonical routing state for active work)
  - local mode: `tickets/epics/`, `tickets/stories/`, `tickets/tasks/`
    and their matching completed folders
  - plugin mode: configured Issue bodies plus local `issue_board.md`
- Scratch, agent-owned (not canonical):
  - `user_defined/` - yours outright, never written to by any tool, create the
    subfolders you want (for example `user_defined/ideas/`, `user_defined/todo/`)
  - There is no top-level `completed/` or `workspace/` lane. In local mode,
    closed tickets live in the three `tickets/*/completed/` lanes above.
- Promotion rule: when content becomes durable or actionable, convert it into tickets.

Suggested user-facing explanation flow
1) Authority chain and where behavior lives.
2) Onboarding sequence in short form.
3) Ticketing flow (epic -> story -> task).
4) Architecture/components docs plus patch docs (when applicable).
5) Implementation gate checks and validation flow.

Notes
- Use clear, direct language; avoid restating full policy documents.
- Keep explanations faithful to `AGENTS.MD`.
- When discussing current work state, route via `attention_board.md` and linked tickets, not memory.
- For system-impacting changes, mention the mandatory patch gate from
  `patch_framework_gating.md`.


