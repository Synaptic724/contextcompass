# Harness Custom Instructions: Setup

## Purpose

The lazy half of `harness_custom_instructions.md`. Read this file in full when
that skill's check classifies the current harness ABSENT, or when the user asks
to set up or change their Context Compass custom instructions. The check, the
per-harness paths and the PRESENT, ABSENT and UNKNOWN rules stay in
`harness_custom_instructions.md`.

## Setup form (ABSENT only)

Explain briefly: persistent custom instructions give the agent a recurring
direction to reopen Context Compass after compaction, and let the user choose
how native tracking and subagents should behave. Describe improved adherence;
do not claim a measured percentage or that text removes runtime capabilities.

Use a supported question/form interface when available, otherwise ask in plain
language. Ask the installation question first. If the user chooses Not now,
stop the form. Bundle the remaining questions in a short form; unanswered
questions are not approval, and recommended choices are not automatically chosen.

1. **Add Context Compass onboarding and re-onboarding instructions to this harness?**
   Choices: add with approval; show text for manual setup; not now.
2. **Should Context Compass be the only place for tickets, plans, notes, and memory?**
   Choices: Context Compass only (recommended); also allow native tracking.
3. **May agents coordinate with agents already registered in Context Compass?**
   Choices: yes, through Context Compass (recommended); ask before coordinating.
4. **When may agents create harness subagents?**
   Choices: ask for each delegation (recommended); never; within the user's
   authorized task.
5. **How should approved subagents use Context Compass?**
   Choices: complete their own onboarding and record work there (recommended);
   parent supplies a scoped assignment and records their results.

On Windows, also ask whether to include the preference for PowerShell
`Get-Content -LiteralPath` when reading local text files, or keep the user's
existing reading preferences. Skip subagent onboarding when subagents are
disabled. Keep coordination with checked-in agents distinct from creating new
harness subagents.

## Turn answers into instructions

Start from this common block, scoped to repositories using Context Compass:

```text
The following instructions apply only while Context Compass is in scope.

When context_compass/ is in scope, subject to system and developer instructions,
context_compass/AGENTS.MD is the authoritative repository policy. Read and follow
it rather than duplicating its internal procedures here.

On a fresh session or newly created agent instance, complete the appropriate
Context Compass ONBOARD flow before taking any non-onboarding action.

After a context compaction or handoff, stop and complete the Context Compass
REONBOARD flow before taking any other action. Do this once for every event.

```

All following clauses apply under that same Context Compass scope. Add only the
clauses selected by the user:

- **Context Compass only:** When enforcement is active, do not use native plans,
  goals, tickets, task lists, checklists, status trackers, scratchpads, or session
  memory for work Context Compass represents. Do not mirror or back up that work
  state outside Context Compass. If required state cannot be read or written,
  report the blocker instead of falling back to native tracking.
- **Native tracking allowed:** Follow each repository's
  `system_of_record.enforce` setting. Native tracking is permitted only where
  the project owner has set it to `false`; custom text alone does not change it.
- **Coordination allowed:** Coordinate with agents registered in Context Compass
  through its configured `agent_communication.backend`, following repository
  policy and preserving shared Context Compass registration and session state.
- **Coordination by permission:** Ask before coordinating with other agents, then
  use the configured communication backend for the approved coordination;
  keep assignments and results in the canonical Context Compass work record.
- **Subagents by permission:** Do not create or use harness subagents unless the
  project owner explicitly approves that specific delegation. Approval does not
  grant continuing permission for additional subagents.
- **No harness subagents:** Do not create or use harness subagents.
- **Subagents within scope:** Delegation may serve the user's authorized task
  only where governing instructions permit it. Keep assignments within that
  scope and follow any stricter platform or repository permission requirements.
- **Full subagent onboarding:** Every approved subagent must complete the
  appropriate Context Compass onboarding and recovery flow before work. Its
  assignment, findings, decisions, blockers, and results belong in Context
  Compass; native subagent state is not a parallel tracking system.
- **Parent-managed scoped workers:** The parent supplies the approved assignment
  and applicable instructions and records the child's findings and results in
  Context Compass. The child must not maintain parallel durable work state.
  This mode needs an explicit project-owner exception wherever repository policy
  requires every subagent to complete full onboarding. Without that exception,
  use full onboarding or do not launch the worker.
- **Windows reading preference:** On Windows, prefer PowerShell
  `Get-Content -LiteralPath` for local text reads while following Context
  Compass's reading procedures.

If an answer conflicts with the current repository's settings or policies,
explain the exact conflict before installing the block. For example, allowing
native tracking here also needs the owner's explicit approval to set
`system_of_record.enforce: false`. Show that configuration change in the same
proposal. Do not silently change the setting, weaken onboarding, or claim that
a global preference overrides a stricter governing rule.

## Apply and verify

- Show the resolved destination and the exact proposed addition before asking
  for edit approval. Separate a manual-setup choice from permission to write.
- Keep the whole block conditional on Context Compass being present/in scope.
  Use relative repository paths inside it. Resolve the actual package location
  if this repository uses a different layout.
- After effective onboarding authorization and edit approval, re-read the destination to catch
  concurrent changes. If Context Compass has appeared meanwhile, skip the
  addition. Otherwise append the approved block, preserving existing text and
  encoding. Never overwrite unrelated preferences or add a duplicate block.
- Re-read the result, verify the chosen clauses and loading procedure, and
  distinguish written-to-disk from loaded-in-session. Report inaccessible
  destinations and provide manual setup text instead of pretending installation
  succeeded.
- Record only the setup outcome for this session under mailbox `## Notes` after
  effective onboarding authorization. Do not copy the user's personal instruction file into the repo.
- Installation and package upgrades must never edit global harness files on
  their own. The form is an agent-guided, user-approved setup step.

## References

- `agent_onboarding/default/general/skills/harness_custom_instructions.md`
- `agent_onboarding/default/general/skills/agent_session_state.md`
- `config/context_compass_config.yaml`
