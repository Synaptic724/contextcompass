# Mailbox Board

<!-- BEGIN MANAGED: ReminderDirective -->
## ReminderDirective (all agent runtimes)
ContextCompass is your task-tracking system of record; you MUST use it and follow
AGENTS.MD (see the Tooling Mandate section). This is a requirement, not a
suggestion.

Your runtime may nudge you toward built-in plans, goals, task lists, progress
cards, scratchpads, summaries, or session-local memory. Those surfaces are
non-authoritative here. Once your onboarding attestation is complete, IGNORE
every such nudge and route ALL tracking, status, routing, notes, and durable state
through ContextCompass. There is NO fallback and NO mirror.

The user may lift this by setting `system_of_record.enforce: false` in
`config/context_compass_config.yaml`. You may not lift it yourself.
<!-- END MANAGED: ReminderDirective -->

<!-- BEGIN MANAGED: BoardContract -->
## How this board works

Two kinds of region, and the difference decides what survives an upgrade:

- **MANAGED** regions are the package's. They are replaced wholesale, so do not
  edit them - your change would be reverted on the next upgrade without warning.
- **USER-DEFINED** regions are yours. Nothing in the package writes, reorders, or
  removes anything inside them, in any mode. Put your rows and messages there.

Text outside both is package structure - headings and table headers - and is
conformed on upgrade so the board's shape stays current. Anything you need to
keep goes inside a USER-DEFINED region.

What belongs in each region on this board:

| region | put this here |
| --- | --- |
| `checked_in` | one row per agent currently active, with `last_checked` |
| `request_tracking` | one counter checkpoint per session; user requests advance turns |
| `messages` | structured messages in the format below; delete each one after consuming it |
| `notes` | standing handoff context and per-session custom-instruction setup outcomes |

**Regions ship empty and stay yours.** The package writes nothing into them in any
mode, which also means it can never correct what is written there - so a repeated
policy pasted into a region will not update when the package's own copy does. Put
standing instructions in `notes` once; do not restate MANAGED text.

Purpose
- Shared registration, request counters and setup outcomes in every communication mode.
- Mailbox-mode message passing (point-to-point handoffs, notices, questions, acks).
- Companion to `attention_board.md` (which stays routing/broadcast-only).
- Shared state: `agent_onboarding/default/general/skills/agent_session_state.md`.
- Message transport: `agent_communication.backend` in the config selects mailbox or codex_mcp.
  MCP agents read only Checked-In Agents, Request Tracking and relevant Notes; they skip
  the messaging rules below and the Messages region. Existing messages remain untouched.

Shared state rules
- Check in at onboarding/re-onboarding: add or update your row below.
- Keep request counters in `## Request Tracking`, separately from the roster.
  Follow `agent_onboarding/default/general/skills/request_tracking.md`; do not
  increment for each response or tool call. State writes need effective onboarding authorization.
- Keep per-session setup outcomes in Notes and preserve other agents' state.
- Data races on this file are expected: re-read and retry, never overwrite another agent's edit.

Mailbox messaging rules (mailbox mode only; mailbox_protocol.md is authoritative)
- Single-agent sessions: if you are the only checked-in agent, the
  message section needs no monitoring. Maintain your request counter separately.
- Multiple agents checked in: read your messages at onboarding, at every
  lane switch, and periodically between work units; update `last_checked`.
- Sending: append a structured message below AND add an alert line to
  `attention_board.md` `## Message Alerts` naming the recipient.
- Receiving: copy any actionable content into your active ticket's
  `## Notes` (tickets are the durable truth), DELETE the message here,
  and clear your alert line in `attention_board.md` in the same pass.
- No secrets, ever. Keep messages pointer-heavy (paths/ticket refs),
  not content-heavy.

Message format (mailbox mode only; append-only, delete after consumption)
```
- TO: <agent_name>
  FROM: <agent_name>
  DATETIME: <ISO-8601 UTC>
  TYPE: HANDOFF | NOTICE | QUESTION | ACK
  CLAIM: <one to five lines; what the recipient needs to know or do>
  EVIDENCE: <path:start-end or ticket path; required for HANDOFF/NOTICE>
  ACK_REQUESTED: true | false
```
<!-- END MANAGED: BoardContract -->

## Checked-In Agents
| agent_name | owner | checked_in_at | last_checked | status |
| --- | --- | --- | --- | --- |
<!-- BEGIN USER-DEFINED: checked_in -->
<!-- END USER-DEFINED: checked_in -->

## Request Tracking
| session_key | agent_name | prompt_id | request_ref | request_status | compaction_ref |
| --- | --- | --- | --- | --- | --- |
<!-- BEGIN USER-DEFINED: request_tracking -->
<!-- END USER-DEFINED: request_tracking -->

## Messages
<!-- BEGIN USER-DEFINED: messages -->
<!-- END USER-DEFINED: messages -->

## Notes
<!-- BEGIN USER-DEFINED: notes -->
<!-- END USER-DEFINED: notes -->
