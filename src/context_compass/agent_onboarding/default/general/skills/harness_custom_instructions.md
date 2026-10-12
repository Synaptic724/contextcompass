# Harness Custom Instructions

## Purpose

Help users put Context Compass onboarding and recovery instructions in the
personal instructions their agent harness loads. Use the user's choices for
native tracking, coordination, and subagents. Check what is already configured
before offering setup.

This skill applies to every role, including direct onboarding as `engineer`.
It configures user-editable instructions, not the provider's system prompt.

## Check before asking

Apply `AGENTS.MD` / Project Instructions Bootstrap before this procedure. An
explicit project override can change its onboarding inspection or setup steps;
do not inspect personal files or show a form that the applicable override skips.
Record such a skipped check honestly, not as evidence of PRESENT or ABSENT status.

1. Identify the current harness from the supplied runtime context. Do not assume
   that the model name identifies the application. Ask which application is in
   use only when it cannot be determined.
2. Inspect the effective personal/global instruction source for that harness,
   including documented overrides and imports. Instructions supplied to this
   session are useful evidence; read the backing file when accessible.
3. Look for an operative Context Compass instruction or a loaded import/pointer
   to one. Recognize `Context Compass`, `ContextCompass`, and `context_compass`
   case-insensitively, then read the surrounding text. A passing mention in an
   example, a disabled block, or this repository's own package files is not proof
   that the user's custom instructions are configured.
4. Classify the result:
   - **PRESENT:** Context Compass is already included in the effective custom
     instructions. Follow that setup. Do not show the form, append another
     block, or replace the user's choices with this skill's defaults.
   - **ABSENT:** The effective source is readable and lacks the integration, or
     its documented location is confirmed missing. Offer the form below.
   - **UNKNOWN:** The location, access, active override, or loaded contents cannot
     be established. Explain that and ask for the location or a manual check.
     Do not classify an access failure as ABSENT or launch the setup form.
5. Offer setup once per session when ABSENT, unless an applicable explicit
   project replacement resolved in the Project Instructions Bootstrap replaces
   this offer within its stated scope; effective onboarding authorization then
   proceeds without this form, and the remaining reads, attestation, and
   approval requirements still apply. If the user declines or chooses
   manual setup, respect that choice through re-onboarding in the same session.
   After effective onboarding authorization, keep that outcome under mailbox `## Notes`, associated
   with the session identity from `agent_session_state.md`.
   This setup-outcome store is independent of `agent_communication.backend`. Do not store the contents of
   their personal instructions there. Retry only when requested or when the
   harness or instruction source changes.

Reading these sources, when required, is an onboarding read. File writes still
require effective onboarding authorization and the user's separate, explicit
approval of the custom-instruction edit. Waiving a certification token is not
permission to modify personal/global instructions.
Declining this optional setup does not block onboarding or relax repository
policy. Do not repeat the form on every request or compaction.

## Common harnesses

`~` means the current user's home directory. Resolve it on the active host;
never embed a contributor's username, private repository, or machine path in a
shipped instruction block.

| Harness | Default personal instruction source |
| --- | --- |
| Codex app / CLI / IDE | `~/.codex/AGENTS.md` |
| Claude Code | `~/.claude/CLAUDE.md` |
| Gemini CLI | `~/.gemini/GEMINI.md` |

### Codex

- Resolve `CODEX_HOME` first; its default is `~/.codex`.
- At that level, a non-empty `AGENTS.override.md` takes precedence over
  `AGENTS.md`. Inspect the effective file, not just the default filename.
- Codex's Custom Instructions setting edits the personal `AGENTS.md`. If an
  override is active, explain which file actually supplies the instructions.
- Propose an append to the effective user-owned source. Do not replace
  `config.toml`, change system/developer instructions, or edit managed policy.
- A file edit alone does not prove a running session has reloaded it. Confirm
  the instruction chain in a new run/session as documented by Codex.

### Claude Code

- Resolve `CLAUDE_CONFIG_DIR` when set; otherwise use `~/.claude`.
- Inspect its `CLAUDE.md` and relevant user-level rules/imports. A project
  `CLAUDE.md` is a different scope and does not prove personal setup is present.
- Claude Code loads `CLAUDE.md`; do not assume it automatically loads a file
  merely because another harness calls that file `AGENTS.md`.
- Use `/memory` or the current version's `/context` display to inspect loaded
  instructions. Append only to a user-owned source with approval, then verify
  loading in a fresh session. Do not modify organization-managed instructions.

### Gemini CLI

- `GEMINI_CLI_HOME`, when set, replaces the home root; `.gemini` remains a child
  of that root. Otherwise use the current user's home directory.
- Inspect the effective `context.fileName` setting. It may name one or several
  instruction files instead of the default `GEMINI.md`.
- `/memory show` displays the combined loaded context. Distinguish personal
  instructions from workspace files when deciding whether setup is present.
- After an approved edit, `/memory reload` reloads the context files;
  `/memory show` lets the user verify the result.
- Do not replace the system prompt through `GEMINI_SYSTEM_MD` for this feature.

### Other applications and hosted sessions

Use that application's documented custom-instruction interface. Do not guess
paths or assume account settings are exposed as local files. When direct access
is unavailable, explain where the user can place the proposed text themselves.
Check the active host: a local personal file need not exist in a remote or hosted
session. Inspect only relevant instruction/configuration fields, not credentials
or unrelated application data.

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

## Sources

- [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex personalization](https://learn.chatgpt.com/docs/reference/settings#personalization)
- [Claude Code instruction files](https://code.claude.com/docs/en/memory)
- [Claude Code configuration directory](https://code.claude.com/docs/en/claude-directory)
- [Gemini CLI context files](https://geminicli.com/docs/cli/gemini-md/)
- [Gemini CLI configuration](https://geminicli.com/docs/reference/configuration/)

## References

- `AGENTS.MD`
- `agent_onboarding/default/general/skills/mailbox_protocol.md`
- `config/context_compass_config.yaml`
