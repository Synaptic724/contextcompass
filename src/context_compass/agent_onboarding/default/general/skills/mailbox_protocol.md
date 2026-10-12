# Mailbox Protocol

This skill applies only when `agent_communication.backend` resolves to
`mailbox` (the default when absent). In `codex_mcp` mode skip the checking,
sending, and receiving sections below and use `codex_mcp.md` for transport.
Maintain shared presence, counters, and setup outcomes in both modes through
`agent_session_state.md`; existing board columns and schemas are unchanged.

Canonical board: `context_compass/mailbox_board.md`.
Alert surface: `## Message Alerts` section at the top of
`context_compass/attention_board.md`.

## Why this exists

Targeted agent-to-agent communication previously routed through
`attention_board.md` attention details (board bloat, no addressee
semantics) or through the user manually ferrying data between agents.
The mailbox gives addressed, consume-on-read delivery while keeping
`attention_board.md` routing/broadcast-only and keeping tickets as the
single durable history.

## Check-in (mandatory, first action after effective onboarding authorization)

- **Read** `mailbox_board.md` during onboarding and re-onboarding - the roster and
  any messages addressed to you. **Write** your check-in row as your FIRST action
  once effective onboarding authorization is reached, per `AGENTS.MD` /
  Project Instructions Bootstrap, and the agent name is known. By default,
  authorization requires `CERTIFY: APPROVED`. With an explicit waiver, complete
  the remaining requirements and any specified replacement; no substitute token
  is required for a waived step.
  - Why not during the gate: a check-in is a write, and `AGENTS.MD`'s
    pre-authorization carve-out permits reads only. The row also needs an
    `AGENT_NAME`: normally that value arrives in the certification message,
    or with a certification replacement, from owner/project instructions - so
    before authorization there is nothing valid to write into it.
- Then add or update your row in `## Checked-In Agents`:
  `| <agent_name> | <owner> | <checked_in_at> | <last_checked> | active |`
- `checked_in_at` is set when you first check in for the session;
  `last_checked` updates EVERY time you read the message section.
- In that same first authorized check-in, initialize or recover YOUR session
  row under `## Request Tracking`, using `request_tracking.md` and the shared
  duties in `agent_session_state.md`. Keep the stable
  session key when the user changes your name during re-onboarding. The existing
  roster's columns and message schema are unchanged.
- Timestamps are ISO-8601 UTC, same as all boards.
- When your session ends deliberately (final closure of your last lane),
  set `status` to `departed`. Stale `active` rows older than a day may be
  marked `stale` by any agent during their own check-in.

## When checking is required (keep it cheap)

- If you are the ONLY agent in `## Checked-In Agents` with status
  `active`, do not poll messages. Maintain your request counter once per user
  request as defined in `request_tracking.md`; that is not message polling.
- If MULTIPLE agents are active, read your messages:
  - at onboarding / re-onboarding (after check-in),
  - at every lane open, lane switch, and lane closure,
  - periodically between substantial work units (a board glance when you
    already touch `attention_board.md` is sufficient cadence),
  - whenever `attention_board.md` `## Message Alerts` names you.

## Sending a message

1. Append a structured entry to `## Messages` in `mailbox_board.md`:
   - `TO:` recipient agent_name (one recipient per message; send two
     messages for two recipients)
   - `FROM:` your agent_name
   - `DATETIME:` ISO-8601 UTC
   - `TYPE:` `HANDOFF` (work/finding transfer), `NOTICE` (FYI a lane
     needs), `QUESTION` (needs a reply), `ACK` (reply/receipt)
   - `CLAIM:` one to five lines, specific and actionable
   - `EVIDENCE:` `path:start-end` or ticket path (required for
     HANDOFF/NOTICE; tickets/source stay the canonical content)
   - `ACK_REQUESTED:` true|false
2. Add one alert line to `attention_board.md` under `## Message Alerts`:
   `- NEW MESSAGE for <agent_name> (from <agent_name>, <DATETIME>)`
3. Keep messages pointer-heavy. Never paste secrets, large code blocks,
   or content that belongs in a ticket note.

## Receiving a message

1. For each message addressed to you, copy anything actionable into your
   active (or a new) ticket's `## Notes` first - durable history lives in
   tickets, never in the mailbox.
2. DELETE the message from `## Messages`. Consumption is deletion; a
   read message must not linger.
3. Clear your alert line(s) from `attention_board.md` `## Message Alerts`
   in the same working pass.
4. If `ACK_REQUESTED: true`, send a `TYPE: ACK` message back (with its
   own alert line).
5. Update your `last_checked` timestamp.

## Concurrency discipline

- Both boards are shared files: on a write-conflict, re-read the current
  content and retry your edit against it. Never resolve a race by
  overwriting another agent's concurrent change.
- Legal writes are: appending messages, maintaining YOUR check-in row,
  maintaining YOUR request-tracking row and setup outcome in `## Notes`,
  and deleting messages addressed TO YOU. Never delete or edit another
  agent's messages or check-in row (stale-marking excepted).

## Boundary with attention_board.md

- Broadcast facts every lane must see (API/key-map changes, repo-wide
  regressions) remain `attention_board.md` attention details.
- Point-to-point content (handoffs, questions, acks, FYIs for one agent)
  belongs here. If you are about to write an attention detail naming a
  single agent, it is a mailbox message.
