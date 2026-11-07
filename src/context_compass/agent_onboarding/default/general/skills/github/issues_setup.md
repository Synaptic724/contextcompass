# GitHub Issues setup

This skill sets up a repository for `work_tracking.backend: github_issues`,
refreshes the header issue after an upgrade, creates an agent issue and moves a
project off local boards. `github/issues_backend.md` defines the records and
write rules used here; follow it throughout.

## Labels

Create each missing label, one at a time: `cc-header`, `cc-agent`, `cc-epic`,
`cc-story`, `cc-task` and `cc-active`. If GitHub refuses, raise it to your owner.

## Header issue

1. Look for an open issue labelled `cc-header`. If there is none, create one
   titled `Context Compass: how this repository works` from
   `templates/github_issues_header.md`. Replace `<VERSION>` with this install's
   Context Compass version and `<REPOSITORY>` with the configured repository, then
   add the `cc-header` label. Pin it if your access allows; pinning is optional.
2. If agents create headers at the same time, the lowest-numbered open
   `cc-header` issue is the header. Close each other one after posting
   `duplicate` with a link to the header.
3. After an upgrade, refresh it: claim the header issue, replace everything
   outside the owner-notes region with the new template, keep the owner-notes
   region exactly as it was, update the version line, run the body check and
   release.

## Agent issue

At your first check-in, create `Agent: <AGENT_NAME>` with the `cc-agent` label if
no issue carries your name. Reopen a closed one rather than creating another. If
two open agent issues carry your name, use the lowest-numbered one and close the
other after posting `duplicate`.

```text
<!-- cc-agent: <AGENT_NAME> -->
# Agent: <AGENT_NAME>
- owner: <owner>
- session_key: <session key>
- checked_in_at: <ISO-8601 UTC>
- last_checked: <ISO-8601 UTC>
- presence: active

## Setup notes
<custom-instruction setup outcomes and standing handoff notes>

<!-- cc-promoted-through: none -->
```

## Moving from local boards

Only when the owner asks, and only after the tickets are Issues
(`github/migration.md` covers local ticket files and plugin-mode Issues):

1. Choose a quiet point. Every agent consumes its messages, finishes or hands
   off its claimed work, and checks out of the local boards.
2. Create the labels and the header issue. Every ticket Issue carries `cc-epic`,
   `cc-story` or `cc-task`. Copy the board Notes regions that hold notes into the
   header's owner-notes region; skip empty regions and bare headings.
3. For each active row on `attention_board.md`, write the ticket's `## Route`
   section and add `cc-active`. Its `resume_hierarchy` lists Issue URLs, not
   file paths.
4. Copy each open artifact and context entry into its ticket's Artifact Links and
   Context Management sections, unless the section already lists it.
5. Show the owner the result. Set `work_tracking.backend: github_issues` only after
   the owner approves it, and then agents check in on GitHub and claim their
   tickets afresh. Each agent carries its own setup notes from
   `mailbox_board.md` into its agent issue.
6. Leave the local board files in place, and add one line to each board's Notes:
   the date, that it moved to GitHub Issues, and the header issue's link. In this
   mode nothing reads them.
