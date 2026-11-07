# GitHub Issues backend

This skill applies only when `work_tracking.backend: github_issues`. Tickets and
every board live in GitHub Issues in the repository named by
`work_tracking.github_issues.repository`. This file describes the mechanics. Use
the GitHub tools your harness provides; it names no tool.

## Access

You need read and write access to that repository's issues, comments and
labels. If you lack it, or GitHub denies an operation, stop and raise the gap to
your owner. Never switch to local boards, another account, another repository or
another backend to work around it. Keep the repository private: everything
posted to a public repository is public.

## Records

| Record | What it holds | Who writes it |
| --- | --- | --- |
| Header issue | one per repository, label `cc-header`, pinned when possible: how these boards work, plus the owner's notes | its holder at setup or upgrade; the owner edits the notes |
| Ticket issue | one Epic, Story or Task, label `cc-epic`, `cc-story` or `cc-task`: the ticket template plus a `## Route` section | the ticket's holder |
| Agent issue | one per agent, titled `Agent: <AGENT_NAME>`, label `cc-agent`: that agent's presence and setup notes | that agent |
| Agent card | one comment per agent per issue | that agent |
| Event | one comment per claim, release, message or other event | anyone; never edited |

Accounts may be shared, so GitHub's author field does not identify an agent.
The name in a record's marker does. Edit only the card and agent issue that
carry your name, and only the bodies you hold.

```text
<!-- cc-card: <AGENT_NAME> -->
**Card: <AGENT_NAME>** | role: primary, review or support | updated <ISO-8601 UTC>
STEP: <what you are doing now>
FINDINGS: <results not yet promoted, with evidence links>
NEXT: <one concrete action>

<!-- cc-event: <type> <AGENT_NAME> -->
**<type>** by <AGENT_NAME> | <ISO-8601 UTC>
<the fields the type needs>
```

Event types: `claim` (ROLE), `release` and `break` (CLAIM: the claim's comment
URL, REASON), `message` and `ack` (the message fields under Presence),
`artifact` (PATH, TYPE, DISPOSITION), `stale`, `collision` and `duplicate`
(REASON and the affected link).

## Writing without collisions

GitHub has no write lock. A body, title or open/closed state is replaced whole on
every save: the last save wins, with no merge and no error. Comments are separate
records, so posting one never collides with anyone. So every record has one
writer or is append-only.

- **Events** are appended and never edited. Correct one with a new event.
- **Your card** holds your current state on that issue. Edit it in place and
  find it again by its marker. Before it reaches GitHub's 65,536-character limit,
  start a new card that links the old one.
- **A body** is saved only by its holder. Read the body and its last-edited time.
  Just before saving, check that time again. After saving, read the edit history
  and confirm no other edit landed between your read and your save. If one did,
  restore the lost text from history, save again and post `collision`. The
  issue's updated time also moves when comments arrive, so it cannot detect body
  edits.
- **Title and open/closed state** are changed only by the holder.
- **Labels and assignees** change one at a time, never by setting the whole
  list. Read them back: GitHub drops label changes from accounts without push
  access without an error.
- **Volume.** GitHub limits content writes to about 80 a minute and 500 an hour
  per account, shared by every agent using it. Post events and card updates for
  state changes, not for every step.

## Claims

A claim is the write lock for a ticket.

1. To take a ticket, post `claim` with `ROLE: primary`, then re-read the issue's
   comments.
2. You hold the ticket only if yours is the earliest `primary` claim that no later
   `release` or `break` names. If you are not first, post `release` for your
   claim and do not act as holder. Claim again after the holder releases.
3. `review` and `support` claims say what you are doing. Any number may be open,
   and none grants the body.
4. Release before a handoff. Closing the issue releases every claim on it.
5. Post `break` against a claim, with the reason, only when its holder's agent
   issue is closed or stale, or the owner tells you to. Then claim normally.

The holder is the ticket's only body writer. An assignee or label showing the
holder is a display hint, never the source of truth.

## Promotion

The holder copies what matters from cards and events into the body: findings
into `## Notes`, decisions and dispositions into their sections. Promotion adds;
it never rewrites another agent's text. After promoting, the holder ends the body
with `<!-- cc-promoted-through: <comment URL> -->`. Readers take the body plus
every comment after that stamp.

## The boards in this mode

Wherever Context Compass names a local board, use its GitHub form:

| Local board | In `github_issues` mode |
| --- | --- |
| `attention_board.md` active row and its details | the ticket's `## Route` section, with label `cc-active` while the route is active |
| Attention board view | open issues labelled `cc-active` |
| Recently closed anchors | recently closed ticket issues |
| Message alerts | none: unacknowledged `message` events on the recipient's agent issue are the alert |
| `issue_board.md` claims | `claim`, `release` and `break` events on each ticket |
| `mailbox_board.md` Checked-In Agents | open agent issues and their bodies |
| `mailbox_board.md` Messages | `message` events on the recipient's agent issue |
| `mailbox_board.md` Notes | the agent issue body |
| `artifact_board.md` | the ticket's Artifact Links section; dispositions apply at closure |
| `context_management/context_board.md` | the ticket's Context Management section and its `Context ID` values |
| Board Notes regions | the header issue's owner-notes region |

```text
## Route
- status: ready, in_progress, blocked or review
- mode: <mode>
- next: <one concrete action>
- outcome: <what done looks like>
- exit_signal: <what ends or switches this route>
- blocker: none or <the blocker>
- resume_hierarchy: <parent-first Issue URLs ending at this ticket>
- updated_at: <ISO-8601 UTC>
```

Artifact files, context packs, system documents and special instructions stay in
the repository, and tickets link them. Gates keep their meaning: "an active
attention row routing to the ticket" is an active `## Route` with `cc-active` on
a ticket you hold.

## Presence

Session identity, authorization, presence values and timestamps follow
`agent_session_state.md`. Only the store differs: your agent issue.

- **Check in** as your first authorized action. Use your open
  `Agent: <AGENT_NAME>` issue, reopen your closed one, or create it as
  `github/issues_setup.md` describes. Set agent name, owner, session key,
  `checked_in_at`, `last_checked` and presence `active` in its body.
- **Stay current.** Update `last_checked` whenever you read your messages, and at
  each state check under a chat transport (`codex_mcp` or
  `claude_internal_communication`).
- **Messages** (`mailbox` transport). A `message` event on the recipient's agent
  issue carries TO, FROM, DATETIME, TYPE (HANDOFF, NOTICE, QUESTION or ACK),
  CLAIM, EVIDENCE and ACK_REQUESTED. To consume one, copy actionable content into
  your active ticket, post `ack` naming the message, and move your agent issue's
  promotion stamp past it. Under a chat transport, messages travel through that
  transport and only presence lives here.
- **Check out** when your session ends: release your claims, set each of your
  cards' STEP to `checked out`, set presence `departed` and close your agent
  issue.
- **Stale agents.** An open agent issue whose `last_checked` is more than a day
  old is stale. During your own check-in you may post `stale` on it, close it and
  `break` its claims with that reason.

## Tickets

The shared ticket rules apply: templates, Status, Notes, the microcycle and
closure. The ticket body is canonical and its Status drives routing; GitHub's
open/closed state follows it. Close only after `Status: done`, the completion
summary and the artifact dispositions are saved and verified; then remove
`cc-active` and close. Keep parent and child links explicit in each body; native
sub-issues and dependencies may mirror them.

Rules written for plugin mode about Issue tickets apply here unchanged: the body
holds the template, Status and Notes, a full-body update keeps every earlier
note, and closure is verified before and after. Use your GitHub tools where they
say the plugin, and claim events where they say `issue_board.md`.

## Recovery

After compaction or handoff, re-read the header issue, your agent issue and its
unacknowledged messages, every ticket you hold (its body plus the comments after
its stamp) and the `cc-active` view. Resume from your held ticket's `## Route`.

## Setup

If the repository has no `cc-header` issue, a label above is missing, or the
header issue's version is older than this install's, follow
`github/issues_setup.md` before other work.
