# Agent session state

Shared registration, request-counter, and setup-outcome duties that hold in
both communication modes. The store remains existing `mailbox_board.md`
sections. No columns are renamed and no state is migrated or deleted by
selecting a transport. This document extracts the shared duties; it does not
replace the board schema.

## Store

Use `mailbox_board.md` inside its USER-DEFINED region:

- `## Checked-In Agents` roster rows for session presence.
- `## Request Tracking` rows for `prompt_id` markers per `request_tracking.md`.
- `## Notes` associated with the session key for harness setup outcomes per
  `harness_custom_instructions.md`.

Column order and message schema elsewhere on the board are unchanged. Boards
hold references and responsibility; detailed history lives in tickets.

## Roster row form

- Add or update your row in `## Checked-In Agents` exactly as:
  `| <agent_name> | <owner> | <checked_in_at> | <last_checked> | active |`
- `checked_in_at` is set when you first check in for the session.
- `last_checked` updates every time you read the message section in mailbox
  mode; that refresh behavior is retained. In `codex_mcp` mode update it on
  each narrow state check-in pass.
- When your session ends deliberately, set presence to `departed`. Stale
  marking applies only to `active` rows older than one day and may be set by
  any agent during its own check-in.

## Authorization

Reading state rows is allowed during onboarding and re-onboarding. Writing
rows waits for effective onboarding authorization as defined by `AGENTS.MD`
and the Project Instructions Bootstrap, with a known owner-provided or
project-instructed agent name. Counters and names must never be guessed.
There is no pre-authorization write exception with or without a waiver.

First authorized actions, in order, include writing the check-in row and
persisting the request-counter row for the current request, then consuming
only the sections allowed by the selected transport.

## Narrow reads in codex_mcp mode

In `codex_mcp` mode, read only `## Checked-In Agents`,
`## Request Tracking`, and relevant session `## Notes` above. Never read
mailbox message instructions, `## Messages`, or `attention_board.md`
message alerts for communication. Existing user-region names and table columns
stay unchanged. Counter maintenance is separate from message
polling. A single active agent updates its counter without polling any message
surface.

## Concurrency

Re-read before editing shared state. Maintain only your own check-in row,
your own request-tracking row, and your own setup outcome. Never delete or
edit another agent's rows, except stale-marking an old `active` presence row
during your own check-in. On a write conflict, re-read and retry against
current content without overwriting another agent's concurrent change.

Timestamps are ISO-8601 UTC. When a session ends deliberately, set presence
to `departed`. Keep the stable session key when the certified name changes
during re-onboarding.

## References

Communication protocol references are conditional, not extra shared reads.
Read only the protocol selected by `agent_communication.backend`.

- `AGENTS.MD`
- `agent_onboarding/default/general/skills/agent_communication_backend.md`
- `agent_onboarding/default/general/skills/request_tracking.md`
- `agent_onboarding/default/general/skills/harness_custom_instructions.md`
- `agent_onboarding/default/general/skills/mailbox_protocol.md`
- `agent_onboarding/default/general/skills/codex_mcp.md`
- `mailbox_board.md`
