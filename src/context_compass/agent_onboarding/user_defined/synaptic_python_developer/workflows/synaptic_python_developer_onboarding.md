# Workflow: synaptic_python_developer_onboarding

## Metadata
- Workflow ID: WF-synaptic-python-developer-onboarding
- Status: active
- Owner: user
- Allowed Roles:
  - synaptic_python_developer
- Default Roles:
  - synaptic_python_developer
- Trigger:
  - user explicitly asks to run
    `synaptic_python_developer_onboarding`
  - user explicitly asks to run
    `synaptic_python_developer_onboarding workflow`
  - user explicitly asks to enter Context Compass onboarding as
    `synaptic_python_developer`
- Created: 2026-05-31T11:29:07Z
- Updated: 2026-05-31T21:46:27Z

## Purpose
Provide one explicit synaptic-role onboarding macro that:
- starts with `context_compass/AGENTS.MD`
- resolves the `synaptic_python_developer` role chain
- uses `Get-Content` for document reads
- avoids agents
- allows up to 30 parallel read threads/tool reads when safe
- reads `src_architecture.md` whole, then descends the hierarchy: the component
  index, sliced components, the graph index, sliced graph

## Use When
- The user explicitly names `synaptic_python_developer_onboarding`.
- The user explicitly asks to onboard as `synaptic_python_developer`.

## Do Not Use When
- The user selected a different role.
- The user only wants ordinary task execution and did not ask for onboarding or
  re-onboarding.

## Inputs
- Required:
  - `AGENT_NAME` if not already supplied for the current onboarding cycle
  - explicit workflow selection or explicit synaptic onboarding request
- Optional:
  - certification message if the user includes it during the same turn
  - explicit request to also read `src_graph_index.md`

## Outputs
- Expected artifacts:
  - one onboarding or re-onboarding attestation for the synaptic role
- Expected ticket state:
  - one active task routing the onboarding pass when ticket gating is required
- Expected board state:
  - one active board row for the onboarding lane while the pass is in progress
  - no agent-created child-agent lanes

## Required Reads
- `context_compass/AGENTS.MD`
- all Markdown documents in `context_compass/special_instructions/`, resolving
  project replacements/waivers (Project Instructions Bootstrap) before the
  contract, registry, and role reads below
- `agent_onboarding/default/general/skills/execution_contract.md`
- `config/context_compass_config.yaml`
- `context_compass/SKILLS.MD`
- `agent_onboarding/default/general/SKILLS.MD`
- `agent_onboarding/default/engineer/SKILLS.MD`
- `agent_onboarding/user_defined/synaptic_python_developer/SKILLS.MD`
- `context_compass/system_docs/src_architecture.md` (whole)
- `context_compass/system_docs/src_architecture_index.md`
- `context_compass/system_docs/src_components_index.md`

Project replacements/waivers resolved in the Project Instructions Bootstrap
(`context_compass/AGENTS.MD`) prevail within their stated scope; later role
reads in this workflow do not reinstate them.

`src_components.md` and `src_graph.md` are NOT onboarding reads. They are sliced
through their indexes during the work, whenever the work needs them - which is
often, and needs no permission. Onboarding gives you the narrative and the maps;
it does not preload the territory. On a real repository the three documents
together run past 36,000 lines, and an agent that reads them all has spent its
context before the first ticket.

## Required Skills
- `agent_onboarding/default/general/skills/self_certification.md`
- `agent_onboarding/default/general/skills/user_approved_certification.md`
- `agent_onboarding/default/engineer/skills/context_protocol.md`
- `agent_onboarding/default/engineer/skills/src_graph_usage.md`
- `agent_onboarding/default/general/skills/agent_identity.md`

## Preconditions / Gates
- Start with `context_compass/AGENTS.MD`.
- Use `Get-Content` for content reads.
- Do not use agents.
- Up to 30 parallel read threads/tool reads are allowed only when the reads are
  real reads and the file chunking rules are still respected.
- Respect `reading.read_loc_max` and `reading.viewer_tool_read_limit`.
- By default, if certification is not already present, request:
  - `AGENT_NAME: <name>`
  - `CERTIFY: APPROVED`
  before any non-onboarding action. With an applicable explicit project
  replacement, effective onboarding authorization follows the replacement
  instead; never wait for a waived token.
- Consume the graph through `src_graph_index.md` and slice `src_graph.md`. The
  index is the entry point, not a substitute of last resort. `src_graph.md` is
  never read whole - on a real repository it runs past 25,000 lines.
- This workflow does not override
  `agent_onboarding/default/engineer/skills/context_protocol.md` or
  `agent_onboarding/default/engineer/SKILLS.MD`. Where a lane preference and the
  reading hierarchy disagree, the hierarchy wins.

## Phase Sequence
1. Intake
- objective:
  - confirm the synaptic onboarding lane
- required actions:
  - resolve the workflow name or the explicit synaptic onboarding request to
    the `synaptic_python_developer` role
  - confirm no-agent execution
  - resolve or request `AGENT_NAME`
- stop conditions:
  - the role is not synaptic
  - the user redirects away from onboarding

2. Investigation
- objective:
  - load the canonical onboarding chain and prepare the source-doc read
- required actions:
  - read the role-chain onboarding docs in parent-first order
  - determine which requested docs exceed chunk limits
  - plan chunked `Get-Content` reads for large source docs
- required note or artifact updates:
  - record the intended source-doc bundle in the owning task notes only after
    effective onboarding authorization permits writes

3. Strategy
- objective:
  - make onboarding state explicit
- required actions:
  - publish ONBOARD or REONBOARD attestation with read-integrity proof
  - request certification if it remains required and is not already supplied
- decision points:
  - if effective onboarding authorization is satisfied, continue
  - if an applicable requirement is unmet, stop and satisfy that requirement;
    do not request a token explicitly waived by Project Instructions Bootstrap

4. Implementation
- objective:
  - complete the orientation bundle: the narrative plus the two maps
- scope controls:
  - the bundle is implicit in this workflow and does not require the user to
    restate it
  - read `src_architecture.md` whole, plus `src_architecture_index.md` and
    `src_components_index.md`
  - do NOT bulk-read `src_components.md` or `src_graph.md` here. They are sliced
    during the work, keyed on names the architecture and the indexes give you
  - use `Get-Content`
  - chunk large files sequentially
  - parallelize only when safe and within the no-agent constraint

5. Validation
- objective:
  - prove the orientation bundle is complete
- required checks:
  - `AGENTS.MD` was read first
  - the resolved role chain was read
  - `src_architecture.md` was read whole, and both indexes were read
  - `src_components.md` and `src_graph.md` were NOT bulk-read. Having read them
    end to end is a failed check, not a thorough one
  - no agent workflow was used

6. Handoff / Closure
- objective:
  - summarize the ready state after onboarding
- required board or ticket sync:
  - leave the lane in `handoff` or close it if the user accepts the onboarding
    completion

## Ticket Behavior
- Required ticket types:
  - one task when this onboarding pass is treated as active repo work
- Required metadata:
  - `Agent Name`
- Required note cadence:
  - record the source-doc bundle
  - record certification state
  - record completion of the requested reads
- Required artifact links:
  - none

## Attention Board Behavior
- Required row fields:
  - the active row must route to the onboarding task when one exists
- Mode transitions:
  - `discovery` while role chain and chunk plan are being assembled
  - `implementation` while the requested source docs are being read
  - `handoff` after the onboarding bundle is complete
- Exit signal rules:
  - the synaptic onboarding chain is complete and the requested source-doc
    bundle is read without using agents

## Escalation Rules
- Stop and ask if the user changes the role.
- Stop and ask if `AGENT_NAME` is required and still ambiguous.
- Raise `BLOCKER` if the requested source-doc bundle cannot be read within the
  current policy gates.

## Success Criteria
- Running the workflow name alone is sufficient to trigger the orientation bundle.
- The workflow starts with `context_compass/AGENTS.MD`.
- The workflow uses `Get-Content` and no agents.
- The synaptic role chain is onboarded.
- `src_architecture.md` is read whole; both indexes are read.
- The agent finishes onboarding able to LOOK UP any component or node on demand,
  rather than having memorised the documents that contain them.

## Anti-Patterns
- Skipping `AGENTS.MD` and jumping directly to source docs.
- **Bulk-reading `src_components.md` or `src_graph.md` during onboarding.** This
  workflow previously required exactly that, and named the raw graph as the
  primary consumption surface while treating its index as an opt-in extra. That
  is backwards, it contradicts
  `agent_onboarding/default/engineer/skills/context_protocol.md`, and on a real
  repository it costs ~36,000 lines of context before the first ticket is opened.
- **Asking the user for permission to read a system document during the work.**
  Reading is agent-driven. Ask for guidance on WHERE to look; never for
  authorisation to look.
- Treating an index as a degraded substitute for its document. The index is how
  the document is meant to be entered.
- Using agents even though the workflow explicitly forbids them.

## Context / Handoff Summary
Start at `AGENTS.MD`, onboard as `synaptic_python_developer`, use `Get-Content`,
do not use agents, and finish with the architecture narrative plus both indexes.
The large documents are not preloaded: they are sliced during the work, on the
agent's own initiative, keyed on names the narrative and indexes supply.

