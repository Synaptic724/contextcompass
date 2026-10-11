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
