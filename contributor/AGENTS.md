# Maintainer-Agent Entrypoint

Audience: an agent asked to change, test, or release Context Compass itself
(payload, tools, tests, packaging, contributor guides). For using Context
Compass inside another project, follow [the Quickstart](../README.md#quickstart)
instead, then the installed project's `context_compass/AGENTS.MD`.

## Read path

This folder orients maintenance work. It does not replace the normal
onboarding, re-onboarding, and certification flow of the operational instance
the work runs in: complete its required reads and gates before normal work.
Perform the applicable flow once per trigger, not again for every guide link. Distinguish
explicit persistent project rules (delegated `special_instructions/` replacements and
overrides that persist per their stated scope and are reread on recovery) from ad-hoc
session waivers, which are never inherited by other sessions and never published as
project rules.

1. Locate the [operational instance](#operational-instance) and follow its
   entrypoint for the applicable ONBOARD or REONBOARD flow.
2. Read [Maintaining the repository](maintaining.md): where changes belong,
   ownership rules, shipping cleanliness, and generated files.
3. Read [Maintenance work state](agents/work-state.md): where assignments,
   findings, and evidence belong.
4. Read [Recovery after interruption](agents/recovery.md): how to resume work
   without replacing the instance's required recovery flow.
5. Follow [Testing changes](testing.md) and [Preparing a release](releasing.md)
   when the task requires them. These remain the shared procedures for humans
   and agents; do not create another copy under `agents/`.

[The contributor overview](README.md) and [the user Quickstart](../README.md#quickstart)
are background references, not replacements for the instance's baseline reads.

Links in these guides resolve relative to the containing document. Shell
commands and file operations resolve from the repository root unless a guide
says otherwise.

## Operational instance

Maintenance work runs inside an owner-designated operational Context Compass
instance, and that instance's own policy governs execution there. This checkout
uses the repository-relative entrypoint `.local/context_compass/AGENTS.MD`.
Read that file, not the shipping seed's entrypoint, to operate this local instance.
Respect an owner-designated alternative. The local copy is excluded from this
checkout's version control and may be absent in a fresh clone. If its entrypoint
is missing, no instance is designated, or the location is ambiguous, stop and ask
the owner for the working instance or authorization to initialize one.
Never fall back to the shipped seed lanes under `src/context_compass/` or to
harness tracking, and do not invent exemptions from the instance's
pre-certification read-only rule. When the instance policy states relative
paths, resolve them from that instance's base, not from this document folder.

## Scope and change discipline

- Change only what the assignment names. No unrelated cleanup and no scope
  expansion without owner approval.
- The Markdown payload is product behavior: follow references through the
  entrypoint, skills, templates, and examples before calling a policy edit
  done, as [the maintenance guide](maintaining.md) describes.
- Keep the role registry and runtime policy under `src/context_compass/`
  unchanged unless the assignment explicitly names them.
- Never commit, push, tag, dispatch workflows, or publish without explicit
  approval; a local version change is not release approval.

## Delegation boundaries

- An owner-authorized supervisor may assign bounded packets to approved agents.
  Implement only the assigned packet and write allowlist; other paths stay read-only.
- The reviewer checks the actual changes and evidence before accepting them;
  an implementation report alone is not verification.
- Do not create subagents or hand work to other agents unless the assignment
  explicitly authorizes that delegation.
- Report blockers with exact commands and errors instead of working around
  permissions, globals, or harness settings.
- Record assignments, findings, decisions, and results in the durable
  [maintenance state](agents/work-state.md), never only in chat.

## Verification and completion

- Verify per [Testing changes](testing.md): run the relevant suites and record results and
  skips honestly. A local run on one interpreter is not the release matrix.
- Review the full diff for user-data loss, stale instructions, and private
  content before handing back, as [Maintaining the repository](maintaining.md) describes.
- Refresh generated files only as [the maintenance guide](maintaining.md) describes; never hand-edit
  hashes, ranges, or the review dump.
- The completion report states what changed, what was read, what was
  verified, and what remains open. Stop at the checkpoint; do not invent
  follow-up work.
