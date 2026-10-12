# Work tracking backend

Read `work_tracking.backend` from `config/context_compass_config.yaml` after
project instructions and before reading backend-specific general skills. The
selected backend applies to every role inheriting `general`, including recovery
after compaction or handoff. Resolve exactly one backend before ticket work.

| YAML value | canonical ticket record | required general readset |
| --- | --- | --- |
| `local` | Markdown files in `tickets/epics/`, `tickets/stories/`, `tickets/tasks/` | shared + Local backend baseline |
| `github_codex_plugin` | Issue bodies in the configured GitHub repository | shared + GitHub Codex plugin baseline |

An absent `work_tracking` block or absent `backend` key means `local`. A blank
value, unknown value, or contradictory configuration blocks ticket work. Do not
choose a backend from a token, installed CLI, available plugin, or folder.

## Local

Read and update the existing ticket files, including the relevant backlog and
completed lanes when the task calls for them. Route from `attention_board.md`
using context-compass-relative paths. No GitHub access or settings are required.
Local mode ignores the GitHub connection nickname and other plugin settings.

Local ticket-writing helpers, including `graph_semantics_tickets.py --create`,
belong to this backend. In plugin mode, use their dry-run findings to compose
Issues through the plugin; do not generate an editable local ticket stack.
The generator reads the installed config beside its target ticket lane and
enforces this boundary. Its dependency-free selector requires the published
literal YAML block format; aliases, merges, flow selectors, and duplicate keys
stop the helper rather than defaulting to local writes.

## GitHub Codex plugin

Require `work_tracking.github_codex_plugin.connection_nickname` as a non-empty
string naming the Codex connection, and `issues_repository` in `owner/repo`
form. Resolve that exact nickname through the current GitHub tool account
catalog before using the connected plugin's repository or Issue tools. Read
`github/codex_plugin.md` and `github/workflow.md` before operating this backend.
Fetch the selected Issues instead of reading local ticket folders for current
ticket state. Issue bodies retain the existing Epic/Story/Task template sections,
Status, `## Notes`, and handoff summary. The canonical reference is an Issue URL.

`work_tracking.github_codex_plugin.project_url` is optional. It can identify an
associated Project, but Project fields are not the ticket-status authority in
this mode. Project management requires a tool that actually exposes that
operation; its absence does not prevent Issue ticket work.

If plugin access, required Issue tools, or repository permission fails, stop and
report the failed operation. Do not switch to local tickets, `gh`, or direct
HTTP as an implicit fallback. CLI helpers under `github/` are optional standalone
tools and are not part of this backend's onboarding or authentication.

## Independent communication selector

Resolve `agent_communication.backend` separately using
`agent_communication_backend.md`. Ticket and communication selectors combine
independently; all four combinations are supported. Default mailbox transport
remains compatible with both ticket backends.

## Shared state and changing backends

`system_of_record.enforce` is independent of backend selection. Both backends
use local attention, artifact, context-management, and mailbox boards. System
docs, special instructions, artifacts, context packs, and agent identities stay
local. Plugin mode additionally uses `issue_board.md` for local agent claims.
Boards hold references and responsibility; they do not duplicate ticket Notes.

Changing YAML does not migrate tickets. An agent must stop if the existing active
route uses the other backend; follow `github/migration.md` when the owner requests
local-to-Issue migration. A reverse move also requires an explicit source/destination
mapping and full content verification. Keep one editable record for each ticket.

## Older configuration

`files` is a legacy alias for `local`, so older local installs keep working.
The earlier `github` value selected a CLI/Project workflow and is not an alias
for `github_codex_plugin`. Stop and ask the owner to select the new explicit
value before acting; do not change an existing transport automatically.

Upgrade tools preserve existing `work_tracking` blocks. To opt into the plugin
from an older config, explicitly set `backend: github_codex_plugin` and create
the matching `github_codex_plugin` settings block. Copy the chosen repository
and optional Project URL from the old `github` block after reviewing them;
legacy Project Status mappings are not required by this backend.
Set `connection_nickname` explicitly from the current Codex connection nickname.
Upgrades preserve existing config blocks; they do not choose an account or
infer a nickname from an earlier CLI login. An older plugin config without this
field must be completed before plugin operations resume.
If those earlier Issues contain ticket Notes in comments, complete the history
and Status reconciliation in `github/migration.md` before resuming their work.
