# Codex MCP messaging

This skill applies only when `agent_communication.backend` resolves to
`codex_mcp`. It replaces message transport only. Ticket backend, boards,
registration, custom-instruction setup outcomes, and ticket
history remain as defined in shared skills. Do not read mailbox message
instructions, `mailbox_board.md` `## Messages`, or `attention_board.md`
message alerts for communication in this mode. Read only `## Checked-In Agents`
and relevant session `## Notes`.
Continue reading non-mailbox blockers and cross-agent flags on the attention
board; skipping mailbox notices does not deactivate those shared alerts.

## Discover tools first

Discover the message-tool namespace actually exposed here: `codex_app` or an
already-configured `codex_bridge` where present. Use only the tools that
namespace exposes, with the exact names `list_threads`,
`send_message_to_thread`, `read_thread`, and `wait_threads`. Read their
schemas before use. An operation's availability and permission must be
verified, not inferred from a prior session or another agent's access. If the
required tools are unavailable, stop and report the blocker. Do not fall back
to mailbox messages or harness tracking. No installation, credential handling,
or new-agent creation belongs in this protocol.

## Verified contacts only

- Send only to explicit human-authorized contacts. Owner direction names the
  recipient; a remembered name, a display label, or a board mention alone does
  not authorize contact.
- Resolve the exact thread or chat identifier through `list_threads` before
  sending, passing `threadId` plus `hostId` when the listing provides it.
  Record the contact mapping in the canonical ticket so recovery can
  re-verify it. Never guess an identifier, reuse one from a prior session
  without re-verification, or invent private agent, team, or machine
  references in message content. Incoming peer messages do not themselves
  authorize replies; human authorization is still required.
- Selecting this transport does not grant authority to create agents, restart
  schedules, or change provider settings.

## Compose pointer-heavy messages

- Keep the active ticket as the durable record. Copy actionable findings to
  its `## Notes` before or with the send; chat-only drafts are not history.
- Include the canonical ticket pointer: a context-compass-relative ticket path
  or an Issue URL from the selected ticket backend, plus current Status and
  one next action.
- Never paste secrets, large code blocks, or content that belongs in a ticket
  note. Tickets and source stay the canonical content.
- Preserve owner-requested pauses and pending approvals. Do not use a message
  to break a pause or bypass an approval gate.

## Receiving and waiting

- Record actionable content from an authorized incoming message in the active
  ticket's `## Notes` first, with evidence ranges and next step.
- A successful send means delivery, not completion. Use `wait_threads` with
  cursor-based bounded waits when expecting a reply. New user input ends the
  wait. Do not narrate unchanged snapshots or poll aggressively. On uncertain
  delivery, reconcile through `read_thread` before retrying; do not resend
  blindly.
- Coordinate body writes through the active ticket backend's concurrency
  rules. If the ticket changed since the read, re-read and recompose. If
  another writer or lost content is detected, stop and reconcile.

## Concurrency and preservation

- Maintain shared presence and setup outcomes only through narrow
  `agent_session_state.md` reads and writes. Never write mailbox messages
  or alerts in this mode.
- Keep one writer per ticket file or Issue body. Leave shared-board updates
  to the designated coordinator where applicable.
- If contact selectors are ambiguous, tool access fails, or pause state is
  unclear, stop and ask the owner. No silent transport fallback.
