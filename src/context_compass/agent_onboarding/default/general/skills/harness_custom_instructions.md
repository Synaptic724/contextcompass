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
   approval requirements still apply. The form, the instruction clauses and
   the apply-and-verify steps are in `harness_custom_instructions_setup.md`;
   read it in full before offering the form. If the user declines or chooses
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
  `CLAUDE.md` or `AGENTS.md` is a different scope and does not prove personal
  setup is present.
- Claude Code (v2.1.277 or later) reads a repository's `AGENTS.md` as project
  instructions. By default it does so only when no `CLAUDE.md` or
  `CLAUDE.local.md` exists in the working directory or above; its Project
  instructions setting can load both or `CLAUDE.md` only. The personal
  `~/.claude/CLAUDE.md` loads alongside either.
- A root `AGENTS.md` that points to `context_compass/AGENTS.MD` therefore
  already reaches Claude Code. Do not add a project `CLAUDE.md` just to repeat
  that pointer: under the default setting, it stops `AGENTS.md` from loading.
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
