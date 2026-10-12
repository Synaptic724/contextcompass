# Request Tracking

## Purpose

Make request order and compaction boundaries visible through `prompt_id`.
The marker counts user requests, not assistant responses. Its state belongs in
Context Compass so recovery does not depend on temporary chat memory.

## Marker contract

```text
prompt_id: compact_0_turn_0
```

- `compact` is the number of confirmed compaction events in this session.
- `turn` is the user-request index in the current compaction segment, starting
  at zero. Neither number has a single-digit limit.
- Start a genuinely new session at `compact_0_turn_0` for its first user request.
- Increment `turn` exactly once for each subsequent user request. A submitted
  clarification, correction, approval, or steering message is a new request,
  even if it arrives while work is running. Multiple questions in one submitted
  request still count once.
- Assistant progress messages, final responses, tool calls/results, retries,
  and internal continuations do NOT advance `turn`. They belong to the request
  that caused them. Runtime notifications and compaction notices are not user
  requests.
- Append the current `prompt_id` to user-facing assistant messages. Multiple
  messages for the same request intentionally repeat the same marker. It is not
  a globally unique message identifier or a count of model/API invocations.
- Keep the marker outside any required attestation block; it does not add a
  field to the canonical onboarding attestation.

## Compaction and handoff

- On each confirmed compaction, increment `compact` once and reset `turn` to
  zero. Complete REONBOARD before returning to ordinary work.
- A compaction can occur inside one request. Its resumed work uses the new
  segment's `turn_0`; the next user request uses `turn_1`. Do not fabricate a new
  user request to explain the reset.
- If a new user request is the first work after compaction, it occupies
  `turn_0`. Apply the compaction transition before counting that request so it
  is not accidentally assigned `turn_1`.
- Re-reading instructions or repeating a certification request is not another
  compaction. Repeated processing of the same event must not increment twice.
- A handoff without compaction does not increment `compact`. A continuation of
  the same session restores its own row. A separate agent/session starts its
  own count and does not inherit another agent's counter.

Example, with two responses to one request:

```text
First user request, progress:  prompt_id: compact_0_turn_0
First user request, final:     prompt_id: compact_0_turn_0
Second user request:           prompt_id: compact_0_turn_1
Compaction, resumed work:      prompt_id: compact_1_turn_0
Next user request:             prompt_id: compact_1_turn_1
```

## Durable state

Use `mailbox_board.md` / `## Request Tracking`, inside its USER-DEFINED region.
This store is independent of `agent_communication.backend`. In `codex_mcp`
mode maintain the same row through narrow state-section reads per
`agent_session_state.md`; never open message sections for counter work.
Maintain one row per session, alongside the existing agent check-in roster:

| Field | Meaning |
| --- | --- |
| `session_key` | Stable key for this conversation/session, independent of the assigned agent name. |
| `agent_name` | Current certified name; update it if the user renames the agent during re-onboarding. |
| `prompt_id` | Current `compact_<count>_turn_<count>` marker. |
| `request_ref` | Current user-message ID, or a receipt timestamp assigned once when the request arrives. |
| `request_status` | `open` while handling that request; `complete` when its final response is ready. |
| `compaction_ref` | Last processed compaction event ID or its fixed receipt timestamp; `none` initially. |

- Prefer an exposed native conversation/session ID for `session_key`. If none
  is available, establish a key from the runtime owner and the first check-in
  UTC timestamp. Keep it for this session, even when the certified name changes.
- Prefer native user-message and compaction-event IDs for the two references.
  A runtime turn ID is not necessarily a user-message ID: steering can add a
  user request inside an existing runtime turn. Never merge those requests.
- When IDs are unavailable, capture each receipt timestamp once and preserve
  it. A new tool read or a new response must not mint another request/event.
- These keys are local correlation metadata, not extra random response IDs.
  Keep summaries, message contents, credentials, and personal file paths out
  of the table. In permitted pointer-only recovery summaries, a pointer to this
  section and the session row is sufficient.
- After effective onboarding authorization, as defined by `AGENTS.MD` /
  Project Instructions Bootstrap, update your
  row for each new user request before doing ordinary work; mark it complete
  before its final response. A resumed `open` request retains its index unless
  a confirmed compaction starts a new segment. Counter writes still require a
  known name and must never guess one; there is no pre-authorization write
  exception with or without a waiver.
- After effective onboarding authorization for re-entry, persist the compaction transition with your check-in
  before resuming. Match `compaction_ref` so one event is not applied twice.
- Before effective onboarding authorization, reading the row is allowed
  but writing it is not. Derive the pending marker from the row and visible
  requests/events, then persist it with the first authorized check-in. Do not
  introduce a pre-authorization write exception for counters.
- Re-read before editing shared state. Change only your session row, preserving
  the other rows and all existing mailbox messages and check-ins.
- Counter maintenance is separate from message polling. A single active agent
  updates its counter without polling the message section.

## Recovery when state is missing

Read the saved row before assigning a marker after compaction or handoff. Do not
choose another agent's row, the largest number on the board, or zero merely
because your chat context is shorter. An empty tracking section in an upgraded
install does not prove an existing conversation is new.

If the session cannot be matched or prior counts/events cannot be established,
use `prompt_id: UNKNOWN` and state what is missing. Recover from available
evidence or ask the user to identify the session or approve a new counting
baseline. Do not silently reset or invent a historical count. An interrupted
pre-certification flow can lose pending counts; report that uncertainty too.

The counter makes continuity easier to inspect. It does not replace required
reads, evidence, ticket notes, or re-onboarding, and it does not prove adherence.

## References

- `AGENTS.MD`
- `agent_onboarding/default/general/skills/compaction_requirements.md`
- `agent_onboarding/default/general/skills/mailbox_protocol.md`
- `mailbox_board.md`
