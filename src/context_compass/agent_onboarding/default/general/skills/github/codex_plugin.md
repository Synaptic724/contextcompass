# GitHub Codex plugin operations

This skill applies to `work_tracking.backend: github_codex_plugin`. Use the
connected GitHub plugin's Issue tools. Discover the tools exposed in the current
agent session and read their schemas; an operation's availability and permission
must be verified, not inferred from a repository URL or a previous agent's access.
These connection-selection rules also apply to an owner-approved migration
using plugin tools while the current ticket backend remains `local`.

## Resolve the connection nickname

Before any plugin read or write, resolve the configured account using the
current tool schemas. Existing onboarding/certification gates still apply;
nickname selection does not grant permission to run tools before those gates.

1. Read `work_tracking.github_codex_plugin.connection_nickname`. Require a
   non-empty string; a missing, blank, or non-string value stops plugin work.
2. Find an exact match to the Codex connection nickname exposed as `link_name`
   in the GitHub tools' available-account catalog. Match the configured spelling
   and spacing, not a substring, case-folded guess, or remembered account.
   `profile_nickname`, `profile_name`, email, and GitHub login are different
   metadata; never substitute them for the configured connection nickname.
3. Require exactly one distinct current connection. Missing nickname metadata,
   no match, multiple matches, or malformed connection data blocks the operation;
   ask the owner to correct the connection/config rather than choosing another.
   This applies even with a single connected account. Repeated identical catalog
   entries for the same `link_id` are one connection; conflicting entries stop.
4. Resolve the matched account's current `link_id` and pass it explicitly to
   every GitHub call that requires an account selector. Never put credentials
   or a connection ID in YAML, and do not reuse an ID from a prior session.
   If the current tools cannot expose or select the named connection, stop.
5. Use an available read-only authenticated profile/whoami tool through that
   same connection before ticket operations. Compare the returned stable ID
   with its advertised `profile_id` when present. A mismatch, unverifiable
   identity, or authentication failure stops work; do not fall back to another
   connection. The owner need not store a real GitHub username in YAML.
6. Verify access to the configured `issues_repository` through the selected
   connection. Nickname selects the account, not the repository owner, and does
   not grant repository permissions. Keep the binding for this work tranche;
   repeat resolution after recovery, config changes, reconnection, or changed
   tool/account metadata rather than silently changing accounts.

## Read and route

1. Resolve the nickname above, then read `issues_repository` from YAML. Verify
   that the plugin resolves that repository and exposes required Issue tools.
   Check Issues support from available metadata or Issue reads; a normalized
   repository response may omit that field, which does not mean it is disabled.
2. Read local `issue_board.md` and `attention_board.md` for agent claims and
   focus. Fetch the exact active Issue by repository and Issue number from its
   URL, then fetch its comments when relevant to current decisions or recovery.
3. For intake, search only the configured repository with an Issue-only query
   such as `repo:<owner>/<repo> is:issue`. Narrow by the immutable ticket ID or
   current assignment. Follow result limits/pagination; a truncated search is
   not evidence that another ticket does not exist. If the tool has no cursor,
   narrow the query or report the result set as incomplete; never invent a page.
4. Read the Issue body, Status, parent/dependency links, and next action. The
   selected backend's Issue body is the durable ticket; local archived ticket
   files and plugin search snippets do not substitute for this fetch.

## Create and update

- Compose the complete matching Epic/Story/Task template before creation.
  Use `github_create_issue` or the equivalent exposed Issue-create tool with
  the explicit repository, title, and body. Keep a stable template ID; route by
  the returned Issue URL and fetch it to verify the content.
- For supported append-only comments, verify the exact Issue, relevant current context, account,
  audience and action/content authority. Reuse valid bindings in intact context and verify the
  saved comment/permalink by readback. No body-writer permission, whole-body read solely for
  custody, or full-policy reread is required for an independent contribution.
- Multiple meaningful comments may hold distinct attributed results, explanation, failed/unrun
  limits and next action. Keep coherent findings together and link long logs/code. There is
  no forced body copy before ordinary continuation and no comment-count quota.
- For Notes, Status, decisions, or handoff changes, read the latest complete
  body, preserve every unrelated section and historical note, and send the
  resulting full body through `github_update_issue`. Fetch again afterward and
  verify both the intended change and retained content. Never send a note alone
  as the replacement body.
- Hold the primary local claim while editing. Coordinate body writes through
  the selected communication transport per `agent_communication_backend.md`
  (mailbox messages or MCP thread tools); the current update tool does not
  expose an atomic compare-and-swap lease. If the body changed since the read, re-read and recompose; if another
  writer or lost content is detected, stop and reconcile before continuing.
  These safeguards cover full-body replacements and overlapping mutable fields, not an
  append-only comment. A comment author does not take custody from a busy body writer.
- Omit labels, assignees, milestone, title, and state when the change does not
  target them. The update tool's label and assignee arguments replace their
  full sets; use additive tools for approved additions where exposed.
- Close through `github_update_issue(state: closed, state_reason: completed)`
  after a verified completion body update and satisfied criteria, required tests and required reviews.
  Authorized agents close routine completed work without another owner ping; reserved owner decisions
  still wait for explicit disposition. Do not infer authority from tool access or bypass unmet gates.
  A reopened Issue requires the owner-approved reason and body Status update.

## Capability boundaries
The assigned agent maintains current status, evidence, requested scoped review and final closure;
review is proportionate to consequence, uncertainty and contract. Self-checks are not independent review.
A qualified independent reviewer may accept and close under shared `ticketing.md`; coordinate
actual overlapping writes, not a ceremonial author return. Verify canonical acceptance before
the native close and its readback. A denied close stays pending; do not switch identity to bypass it.
Keep concise claim, impact, material limits and next action with exact retrievable evidence.
Current in-body state/decisions/handoff remain coherent at material transitions; detailed findings
may remain in supported comments/documents. Do not copy full linked reports or add substantive
Notes for unchanged checks/ACKs; preserve required in-body state/evidence and all history/custom regions.

The plugin currently exposes Issue search, fetch, create, update, and comment
reads. A tool called `add_comment_to_issue` is documented for PR Conversation
comments and uses `pr_number`; do not assume that means ordinary Issue-comment
creation is supported. Check current schemas rather than the tool's name. An unavailable ordinary
Issue-comment operation is a capability gap, not a permission denial. Retain the contribution in
an existing authorized evidence location through a supported operation, or report the exact
unavailable write and hold only dependent work. Do not claim the comment was saved.
Preserve the exact denied action on a real denial; do not switch account, backend or route to
bypass it. Reconcile uncertain effects before a permitted retry. Existing Notes stay in the body;
their preservation does not force every new comment into that section.

Parent/child and blocker relationships always retain explicit Issue links and
IDs in template metadata/checklists. Use native sub-issue or dependency tools
only when the current plugin exposes them and verify the result. Missing native
relationship tools do not justify losing the readable relationships.

Project tools are not currently exposed by this plugin. Treat an optional
Project URL as context; never claim membership or Project Status was updated
without an available tool and verified result. Do not require CLI installation,
CLI login, API tokens in YAML, or manual shell authentication to use this mode.

Ticket and communication selectors are independent. Both ticket backends work
with either transport; default mailbox transport remains compatible.

Authentication belongs to the owner's plugin connection. On missing access or
403/404 errors, name the operation and destination and request the relevant
connection/permission fix. Do not create a local replacement ticket, retry an
ambiguous create blindly, or switch transports. Tool and owner approvals still
apply to writes.
