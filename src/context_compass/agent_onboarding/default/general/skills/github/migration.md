# Migrating local tickets to GitHub Issues

Keep `work_tracking.backend: local` while preparing a migration. The owner must
request the move and review the destination and full proposed Issue content;
changing YAML alone neither creates Issues nor archives local work.

1. Inventory the chosen active, backlog, and completed Epic/Story/Task files.
   Record immutable IDs, parent/dependency IDs, Status, full Notes history,
   handoff context, source paths, artifact links, and context-pack associations.
   Preserve all authored content rather than replacing it with a summary.
2. Prepare `work_tracking.github_codex_plugin.connection_nickname` and
   `issues_repository`. Resolve the current named connection and verify its
   authenticated profile as specified in `codex_plugin.md`, then verify it can
   read that exact repository and its Issues. A Project URL is optional context.
   Inspect the exposed create/update tools and report missing write permission
   when a requested operation fails. Keep that explicit connection for all
   migration operations; changing the ticket backend is still the final step.
3. Produce a preview containing each full proposed title/body and its source ID.
   Notes stay under `## Notes` in the body in original order. Show parent/child
   links, blockers, Status, desired open/closed state, and the board/reference
   changes. Flag private content, unresolved IDs, and duplicates before publication.
4. After the owner approves the preview, create parent Issues before children
   through the plugin. Search for each immutable ID before creation and keep
   the returned URL. On an ambiguous create outcome, reconcile by fetch/search
   before retrying; never blindly create another Issue.
5. Map IDs to verified Issue URLs and update both sides of hierarchy/dependency
   links while preserving the complete bodies and Notes. Use native relationship
   tools only if exposed. Completed tickets receive their completion metadata
   and a verified closed state; pending or blocked tickets stay open.
6. Reconcile `issue_board.md`, `attention_board.md`, `artifact_board.md`, and
   context links to Issue URLs. Verify body content, Notes history, Status,
   open/closed state, dependencies, and each active route against the inventory.
   The body is canonical; local boards carry claims and pointers only.
7. After full reconciliation, set `backend: github_codex_plugin`. Retain the
   original local tickets as read-only history. Subsequent ticket updates go
   through the plugin only, and recovery fetches the Issues instead of the archives.

A partial run retains the source files and verified ID-to-URL mapping. Resume
by reconciling existing Issues before any new write. No automatic rollback
by deleting Issues, no silent CLI/local fallback, and no duplicate editable
work record is part of migration.

Moving back to local tickets also requires an explicit inventory and complete
Issue-body/Notes export into the matching local template paths before selecting
`local`. Preserve the verified Issue links and review every route at cutover;
changing the backend value by itself is not a reverse migration.

## Moving local tickets into github_issues

The same rules hold: the owner requests the move and reviews the destination and
the proposed Issues, `work_tracking.backend` changes last, and nothing is created
twice. Use the GitHub tools you have; `github_issues` needs no plugin connection.
Keep the repository private; a public one is the owner's explicit decision,
recorded in the header issue's owner notes.

1. Inventory the open tickets: every Epic, Story and Task outside `completed/`
   and `archive/`. Completed tickets stay as files unless the owner asks for them.
2. Preview each Issue: its title is the ticket's heading, its body is the ticket
   file unchanged, and its label is `cc-epic`, `cc-story` or `cc-task`. List the
   parent links, bodies over 65,536 characters, IDs that already appear in the
   repository, and private content.
3. After the owner approves, create parents before children. Search for each ID
   first and reuse an Issue that carries it. A body over 65,536 characters is
   created short, with its ID, and filled by one edit (`issues_backend.md`, Size).
   Record each ID-to-URL pair as it is created, so an interrupted run resumes
   without duplicates.
4. Where one migrated ticket names another by ID or file path, add the other's
   Issue number after the name, for example `STORY-2026-01-02-example (#12)`.
   Leave evidence pointers such as `path:12-34` unchanged.
5. Verify every Issue against its file: every line present in order, the label,
   the title and the open state.
6. Move the boards as `issues_setup.md` describes ("Moving from local boards").
7. Once the owner approves the switch, set the backend, then move each migrated
   file into its lane's `archive/` folder with a first line linking its Issue. The
   file stays as read-only history; the Issue is the live record.

## Moving from github_codex_plugin to github_issues

The tickets are already Issues. Set `work_tracking.github_issues.repository` to
the plugin's `issues_repository`, add `cc-epic`, `cc-story` or `cc-task` to each
open ticket Issue and to the recently closed ones the attention board names, then
move the boards as `issues_setup.md` describes. Ticket bodies stay as they are.

## Earlier GitHub CLI configuration

If the earlier `backend: github` workflow already created Issues, keep those
Issue IDs and URLs when choosing `github_codex_plugin`; do not create replacement
Issues. Read each complete body, all historical ticket-note comments, and any
existing Project Status mapping before the switch.

Reconcile the reviewed workflow Status into the template's body metadata. Carry
historical ticket-note comments into `## Notes` in original order, preserving
timestamps, authors, claims, evidence, and next actions. Retain the original
comments as history and verify that no note was lost or duplicated. Verify open/
closed state and local claim/route links against that same Issue URL before
resuming plugin work. An unreadable history or unresolved status mapping blocks
this transition; an optional Project link does not erase its prior evidence.
