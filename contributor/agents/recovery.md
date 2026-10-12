# Recovery After Interruption

Compaction, handoffs, and fresh sessions are normal. Resume from files, not
from memory. Resolve project instructions on each recovery event, then follow
the effective flow below. A persistent project override differs from an ad-hoc
waiver that applied only to another session.

## Re-entry sequence

1. Read [the root entrypoint](../../AGENTS.md), then
   [the maintainer entrypoint](../AGENTS.md).
2. Complete the operational instance's ONBOARD flow (fresh session) or
   REONBOARD flow (after compaction or handoff): required reads, attestation,
   and certification gates before any normal work, including re-resolution of
   project overrides. Persistent delegated rules re-apply per their stated
   scope; ad-hoc session waivers are not inherited across sessions.
3. Recover local state: the instance's attention routing, the active ticket,
   its notes and handoff summary, shared session state, messages through the
   configured communication backend, and any artifact named in the assignment.
   MCP mode skips mailbox Messages and message alerts, not registration or counters.
4. Re-read only the guide sections the next action needs.
5. Continue from the ticket's recorded next action. If the ticket, board, and
   notes disagree, stop and reconcile before acting.

## Handoff notes

- Leave the ticket's handoff summary current before stopping: state,
  decisions, next action, open questions.
- Keep handoff pointers minimal (ticket and board paths); do not paste long
  transcripts into durable state.
