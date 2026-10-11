# Engineer Example: Artifact Workflow

This is a local-backend example. In plugin mode, use the same content and
artifact rules, but place the ticket in an Issue and route via its URL.

Context
- An engineer needs to make control-file casing uniform so every role registry
  and entrypoint resolves on a case-sensitive filesystem.
- The agent wants to capture scratch thoughts before committing to a ticket.

Scratch capture (`user_defined/`, the lane no tool writes to)
- Path: `user_defined/ideas/context_compass_control_file_casing.md`
- Example content:

```md
# idea: context_compass_control_file_casing
## Why now
- mixed-case control files resolve on Windows and fail on Linux.
- a readset path that fails to resolve blocks certification, not just a read.

## Early hypothesis
- every control file uses one casing convention: `SKILLS.MD`, `AGENTS.MD`,
  `WORKFLOWS.MD`.
- renaming the files is the small half; the reference sweep is the real work.

## Risk notes
- a `*.md` glob silently skips `*.MD` files, so the sweep looks complete while
  uppercase-named files keep the stale references.
- case-only renames need `git mv --force` when `core.ignorecase` is true.

## Promote when
- the registry, every `INHERITS_SKILLS_FROM` header, and every readset entry
  agree on one casing.
```

- Path: `user_defined/todo/context_compass_control_file_casing.md`
- Example content:

```md
# todo: context_compass_control_file_casing
- [ ] inventory every control-file reference, both extensions
- [ ] rename the files, then sweep the references
- [ ] prove every readset path still resolves
```

Promote to ticket (curated)
- Path: `tickets/stories/YYYY-MM-DD_context_compass_control_file_casing_story.md`
- Example content:

```md
# story: context_compass_control_file_casing
## Goal
- one casing convention for control files, with every reference agreeing

## Scope
- role registry, role `SKILLS.MD` files, and every document that cites them

## Out of scope
- role-policy redesign or behavior changes

## Files to touch
- context_compass/SKILLS.MD
- context_compass/agent_onboarding/*/*/SKILLS.MD
- context_compass/README.md
- context_compass/system_docs/src_architecture.md

## Risks
- extension-filtered search hides references in uppercase-named files
- blanket find/replace rewrites prose that names a retired file on purpose

## Tests
- every registry `skills path` resolves to a file on disk
- every `extends` value matches the target's `INHERITS_SKILLS_FROM` header
- zero occurrences of the retired casing outside generated bundles

## Done criteria
- registry parses, all roles resolve, all readset paths resolve
- no remaining reference to the retired casing
```

Strategy alignment
- Path: `attention_board.md` (route active work item to the canonical ticket)
- Path: active ticket `## Notes` (store rationale, evidence, and next actions)

Tactics / runbook
- Path: `tickets/tasks/YYYY-MM-DD_context_compass_control_file_casing_task.md`
- Example content:

```md
# task: context_compass_control_file_casing
## Preconditions
- current references are inventoried across both extensions
- scope constrained to docs and policy wiring

## Steps
1) rename the control files
2) sweep every reference, matching on lowercased suffix so uppercase-named
   files are included
3) re-resolve every readset path and every inheritance header
4) document counts and outcomes in ticket notes
```

Work queue conversion
- In local mode, convert the approved todo into a story/task ticket in
  `tickets/stories/` or `tickets/tasks/`; plugin mode uses an Issue body.
- Example work items (summarized):
  - Task: rename control files to the single casing convention
  - Task: sweep references and prove readset resolution after the rename
