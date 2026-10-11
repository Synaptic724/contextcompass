# Maintenance Work State

Instructions live in `contributor/`; work state does not. Work state is the
record of what is being done, decided, and verified. Keep the two separate.

## Where work state lives

- Active maintenance work is tracked in the repository's local operational
  Context Compass instance: its tickets, boards, notes, and linked artifacts.
- `contributor/` files describe how to do the work. Do not store assignments,
  findings, session memory, or status in them.
- Do not track maintenance work in harness task lists, plans, scratchpads, or
  session memory. Do not create a parallel durable record outside Context Compass.
  If the local instance cannot be read or written, stop
  and report the barrier instead of substituting another tracker.

## What never holds work state

- `src/context_compass/` lanes (boards, tickets, mailbox, system documents):
  that is the clean shipping seed, and working state there would publish to
  every install.
- `contributor/` guides, `tests/`, and packaging files: instructions and
  product only.
- Chat transcripts, harness memory, and personal instruction files.

## Identifiers and secrets

- Public guides and shipping seeds must not contain live agent rosters, session
  keys, mailbox rows, personal machine paths, or private repository references.
  Keep examples generic; preserve legitimate author credits and license notices.
- Authorized private operational records may contain the correlation metadata
  the normal protocol requires (agent names, session keys, check-in rows,
  counters) and evidence needed for the authorized task. The operational instance
  is identified in [the maintainer entrypoint](../AGENTS.md#operational-instance).
- Never put secrets, credentials, or API keys in work state,
  documents, commands, arguments, or logs.

## Evidence expectations

- Findings cite concrete paths with line ranges; claims without evidence stay
  marked unknown until investigated.
- Use repository-relative evidence paths where possible. Keep any necessary
  private context in the authorized local instance, not the contributor guides
  or shipping copy; do not copy whole personal instruction/configuration files.
