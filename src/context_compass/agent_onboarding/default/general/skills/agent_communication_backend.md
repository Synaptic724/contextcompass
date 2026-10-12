# Agent communication backend

Read `agent_communication.backend` from `config/context_compass_config.yaml` after
project instructions and before reading messaging baseline skills. The selected
transport applies to every role inheriting `general`, including recovery
after compaction or handoff. Resolve exactly one transport before agent-to-agent
communication work.

| YAML value | message transport | required general readset |
| --- | --- | --- |
| `mailbox` | addressed entries in `mailbox_board.md` plus `attention_board.md` alerts | shared + mailbox message baseline |
| `codex_mcp` | available message-only MCP thread tools | shared + MCP message baseline |

An absent `agent_communication` block or absent `backend` key means `mailbox`.
A blank value, unknown value, or contradictory configuration blocks
communication work. Do not choose a transport from installed tools, available
plugins, or folder contents.

## Independence from ticket backend

`agent_communication.backend` and `work_tracking.backend` are independent
selectors. All four combinations are supported. Ticket selection never implies
a transport, and transport selection never implies a ticket backend. Resolve
both before work. Missing communication selection defaults to `mailbox`;
missing ticket selection defaults to `local` per `work_tracking_backend.md`.

## Shared state in both modes

Both transports use the same shared agent-session state store defined in
`agent_session_state.md`. Registration and setup outcomes remain in existing
`mailbox_board.md` sections. No migration or deletion
occurs when switching transports. In `codex_mcp` mode read those state
sections narrowly and never read mailbox message instructions, `## Messages`,
or `attention_board.md` message alerts for communication.

## No fallback

If the selected transport, required tools, or contact authority fails, stop
and report the failed operation. Do not switch transports silently, do not
use harness-native tracking as a substitute, and do not use CLI authentication
as a substitute for the selected path. Selecting `codex_mcp` does not grant
contact authority or permission to create agents.

## Older configuration

There is no legacy alias for this selector. Older installs without this block
continue on `mailbox` with unchanged semantics.
