# Context Compass™

Context Compass™ is a policy-driven context orchestrator for AI-assisted execution.
Apache-2.0 licensed; "Context Compass" is a trademark of Mark Thomas Geleta. See
`LICENSE` and `NOTICE` in this directory.
It gives agents a deterministic way to onboard, route work, preserve context,
and recover cleanly after compaction or session reset.

This repository is built as a public library. You can use it directly, fork it,
or adapt it to your own role stack and process requirements.

## What This Project Is

Context Compass is not a prompt snippet and not a one-shot template.
It is a file-backed coordination system that defines:

- how an agent should read policy,
- how a role is selected and resolved,
- how work must be routed through tickets,
- how evidence is captured while work is in motion,
- and how continuity is preserved across interruptions.

The goal is practical reliability: less agent drift, better state continuity,
and auditable execution quality.

## What It Solves

Most failures in long AI sessions are process failures:

- policy gets partially remembered,
- onboarding claims drift from what was actually read,
- execution starts without durable state,
- and compaction wipes critical context.

Context Compass addresses that by making execution contract-driven:

- onboarding is explicit,
- role resolution is explicit,
- certification is explicit,
- ticket routing is explicit,
- compaction re-entry is explicit.

## Agent Support

This distribution is wired to a single runtime entrypoint: `AGENTS.MD`.

`AGENTS.MD` is a widely adopted convention for repository-level agent
instructions, so most coding-agent runtimes pick it up without configuration. If
yours looks for a different filename, point that file at `AGENTS.MD` rather than
duplicating the policy - two copies of a contract drift, and the drift is silent.

Context Compass is runtime-neutral by design. Nothing in the routing or policy
core depends on which vendor's agent is reading it; the requirements are file
access, shell or tool access, and the ability to follow written instructions.

## Core Design Principles

1. Evidence before assertion.
2. Deterministic gates before execution.
3. Durable state in files, not chat memory.
4. Parent-first role inheritance.
5. Re-onboarding after compaction/handoff.
6. Explicit uncertainty (`UNKNOWN`) over silent guessing.

## Repository Structure

```text
context_compass/
  AGENTS.MD                     runtime entrypoint
  SKILLS.MD                     the role registry
  MANIFEST.md                   generated: path, owner, hash for every file
  CONTEXT_COMPACTION.md
  PROFILE_CLASS_CREATION_GUIDE.md
  README.md

  config/
    context_compass_config.yaml behaviour settings only

  agent_onboarding/
    default/                    ships with the package, replaced on upgrade
      new/  general/  engineer/  design_engineer/  platform_engineer/
      qa_engineer/  security_engineer/  story_designer/  story_novel_artist/
      researcher/  draft_writer/  developmental_editor/  line_copy_editor/
      continuity_fact_checker/  proofreader/
    user_defined/               YOURS - never replaced, never removed
      <your overlays>

  tools/                        manifest, cleanup, upgrade, document indexing
  templates/                    ticket templates
  examples/                     the shape and quality bar for every document type

  system_docs/                  SHIPS EMPTY - your architecture and component
                                maps go here; nothing is seeded
  tickets/                      yours
  artifacts/                    yours
  context_management/           yours - context board and artifacts
  special_instructions/         yours - project-specific rules

  attention_board.md            live routing; package owns only the MANAGED block
  issue_board.md                local agent claims for github_codex_plugin
  artifact_board.md
  mailbox_board.md
```

Five directories are yours and are never written to by an upgrade: `system_docs/`,
`tickets/`, `artifacts/`, `context_management/`, `special_instructions/`, plus
`agent_onboarding/user_defined/`. Everything else belongs to the package and is
replaced when you upgrade. `MANIFEST.md` records which is which, per file.

`system_docs/` ships empty on purpose. A seeded placeholder in a live lane gets
read as repository truth no matter what banner sits on it, so the shape
reference lives in `examples/` instead and this directory stays yours.

## Optional GitHub Work Tracking

Local Epic/Story/Task files remain the default. An opt-in setting in
`config/context_compass_config.yaml` chooses `local` or `github_codex_plugin`.
Plugin mode requires a Codex `connection_nickname` and target `issues_repository`.
The agent resolves that exact nickname before calling the plugin, rather than
choosing a GitHub account implicitly. Plugin mode uses Issues for tickets, with Status
and Notes in their bodies. The Project URL is optional. Local boards and other
Context Compass documents stay in the repository; plugin connection permissions
are managed outside this YAML.

The two YAML examples, plugin setup, and migration instructions are in
`agent_onboarding/default/general/skills/github/README.md`. Do not switch an
existing project with local tickets until you have reviewed their full content
and the exact Issue destination.

## Optional MCP Messaging

`agent_communication.backend` selects `mailbox` or `codex_mcp` independently of
ticket storage. Missing means `mailbox`, preserving existing installations.
With `codex_mcp`, agents read the MCP skill instead of mailbox message features.
Existing registration, request counters and setup outcomes stay in the mailbox
board's state sections; other boards and their ownership rules do not change.
Stored messages and alerts are left untouched. Available tools and human
authorization are still required; this setting installs nothing.

## How It Works

### 1) Policy Bootstrap

The agent starts from the runtime entrypoint:

- The agent reads `AGENTS.MD`, loads `special_instructions/`, and resolves any
  explicit project onboarding overrides before applying the shared policy chain.

Project instructions can replace or waive a named onboarding requirement within
their stated scope. Everything else remains in force, and later role documents
do not undo an applicable override. The same bootstrap runs after compaction or
handoff. The shipped folder activates no overrides; normal onboarding remains
the default until the project owner adds instructions.

The canonical rule is `AGENTS.MD` / `Project Instructions Bootstrap`. It does not
change platform instructions or tool permissions.

### 2) Role Routing

`SKILLS.MD` is the single role registry. Its table declares every role and the
`SKILLS.MD` path each one resolves to. The selected role resolves to a
`SKILLS.MD` chain with parent-first inheritance, walked via the
`INHERITS_SKILLS_FROM` header in each file.

Each role declares its skills in sections, and the section is what classifies the
paths under it:

- **baseline sections** (must read for certification). A role may have more than
  one and names them for what they hold — `engineer` carries both
  `Required baseline skills` and a `Baseline system orientation` set.
- **`On-demand`** (read when the trigger applies).
- **`Self-directed`** (read when useful to the work, without waiting for a trigger).

The default is to read every section marked baseline, not to match a fixed list
of heading names. Project onboarding overrides are resolved before applying
those requirements; unaffected baseline requirements still apply.

### 3) Certification Gate

Under the default onboarding rules, before implementation:

- onboarding must be complete,
- read-integrity must be attested,
- and user approval must include `CERTIFY: APPROVED`.

An explicit project override changes only the requirement it names. Named work
records still need a known agent name, and writes wait for effective onboarding
authorization as defined by the bootstrap.

### 4) Ticket-First Execution

Work is routed through:

- `attention_board.md` for active pointer routing,
- `tickets/` for durable execution memory,
- `artifact_board.md` for linked outputs.

The active ticket `## Notes` is the canonical memory stream for findings,
decisions, blockers, and evidence.

### 5) Compaction / Re-Entry

After compaction or handoff:

- reload project instructions and re-onboard using the same routing authority,
- rebuild context from board + ticket state,
- and satisfy the effective authorization requirements before resuming action.

Fresh sessions use ONBOARD rather than REONBOARD. Without an explicit override,
the normal certification requirement remains in force in both flows.

This prevents "performative compliance" and keeps behavior auditable.

## Role Model

Context Compass currently includes both software and fiction workflows.

The authoritative list is the registry table in `SKILLS.MD`. The lanes below are
a reader's overview and may lag the registry; when they disagree, the registry
wins.

### Software Lane

- `general`
- `engineer`
- `design_engineer`
- `platform_engineer`
- `qa_engineer`
- `security_engineer`

### Fiction Authoring Lane

- `story_designer`
- `story_novel_artist`
- `researcher`
- `draft_writer`
- `developmental_editor`
- `line_copy_editor`
- `continuity_fact_checker`
- `proofreader`

### User-Defined Lane

- `user_defined/<name>` overlays for team or personal specialization

## Configuration Authority

Two files with two distinct jobs.

**`SKILLS.MD` - the single role registry.**
One table declares every role: its `SKILLS.MD` path, its parent role, whether
it is user-defined, whether it is selectable after onboarding, and whether it
reads READMEs. A role exists if and only if it has a row there. Adding a role
is a one-row edit.

**`config/context_compass_config.yaml` - behaviour settings only.**
It does not enumerate roles and is never consulted to resolve one.

- `profiles.onboarding` for first-time onboarding state and transitions,
- `system_of_record.enforce` for whether agents may use their own harness's task
  tracking instead of this package (default `true`, meaning they may not),
- `workflow` for ticket microcycle behavior,
- `artifacts` for artifact retention rules,
- `documentation_format` for line length and evidence formatting,
- `reading` for read-window and chunking limits.

There is no stored active role. Role selection is per agent, per session, so
several agents can hold different roles in the same repository at once.

## Quick Start

1. Place `context_compass/` in your repository.
2. Point your agent at `context_compass/AGENTS.MD`.
3. Ask it to onboard as a role from `SKILLS.MD`, such as `engineer`.
4. The bootstrap reads project instructions before applying the role's onboarding requirements.
5. Under the default flow, provide `AGENT_NAME: <name>` and `CERTIFY: APPROVED`.
6. Execute through ticket routing (`attention_board.md` + active ticket notes).

## Why Teams Use This

- Reproducible agent behavior across sessions.
- Explicit role specialization without policy fragmentation.
- Better handoffs and lower context-loss cost.
- Clear evidence trails for decisions and changes.
- Portable model across agent runtimes.

## Recommended Operating Discipline

- Keep role docs as delta layers (do not duplicate parent skills).
- Keep ticket notes high-signal and evidence-backed.
- Keep board rows routing-focused and concise.
- Treat compaction as a reliability event, not a convenience event.
- Prefer explicit blocker states over hidden assumptions.

## Public Library Intent

Context Compass is intended to be reusable by:

- solo builders,
- engineering teams,
- hybrid technical + creative workflows,
- and multi-agent pipelines that require deterministic process control.

If you extend this library, keep your routing manifest, role maps, and
certification gates explicit so downstream users inherit a stable system.

## License

MIT



