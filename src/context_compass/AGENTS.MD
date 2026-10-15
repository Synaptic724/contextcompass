

# AGENTS.MD - Prime Policies
## Execution Order

- Start with the Project Instructions Bootstrap below. Before non-onboarding
  tools, edits, or execution, obtain the effective onboarding authorization it defines.
- If there is any conflict between repository-root `AGENTS.MD` and
  `context_compass/AGENTS.MD`, `context_compass/AGENTS.MD` is authoritative.

## Tooling Mandate: Context Compass Is the Only System of Record

### Who this binds

This rule binds you by what your runtime PROVIDES, not by who built it. No brand
is named because no brand needs to be: if your environment gives you any of the
surfaces below, you are in scope.

You are in scope if you are:
- a command-line coding agent,
- an agent embedded in an editor or IDE,
- a desktop or chat agent application with file and shell access,
- a headless agent built on an SDK or API,
- a browser-driving agent,
- an agent running in CI or on a schedule,
- or any other automated runtime acting on this repository.

You are in scope if your runtime exposes any of:
- task lists, todo lists, or checklists
- plans, goals, or planning widgets
- status indicators, progress trackers, or work summaries
- scratchpads, memory panes, or session memory
- any other session-local coordination surface

**If you are reading this and unsure whether a surface of yours counts, it
counts.** The test is not what the feature is called. The test is whether it
holds state about the work that lives outside this repository.

### Hard rules

- You are NOT PERMITTED to use your harness's task system - task lists, todo or
  status widgets, planning trackers, session memory - to plan, track, route, or
  record your work.
- You MUST use the configured Context Compass work backend for Epic/Story/Task
  tickets and their durable Notes, supported comments and authorized linked evidence.
  `work_tracking.backend` in
  `config/context_compass_config.yaml` defaults to `local` when absent. In
  `local` mode, read and update tickets under `tickets/epics/`,
  `tickets/stories/`, and `tickets/tasks/`. In `github_codex_plugin` mode,
  resolve the configured `connection_nickname` through the current GitHub
  account catalog before calls, then fetch and update Issues through that
  connection; each Issue body
  holds its template, Status, `## Notes` and current resume view; supported Issue comments
  may hold attributed findings directly without copying every finding into the body.
  A Project URL is optional. In both modes,
  `attention_board.md`, `artifact_board.md` + `artifacts/`,
  `context_management/`, and `mailbox_board.md` remain local. Plugin mode also
  uses local `issue_board.md` for agent claims. Read the backend-specific general
  skills before work. Resolve older config values using
  `agent_onboarding/default/general/skills/work_tracking_backend.md`.
  If config, tools, or access are invalid, stop; never silently switch backends
  or use CLI authentication as a substitute for the selected plugin.
- Resolve `agent_communication.backend` independently from the ticket backend.
  Missing means `mailbox`; `codex_mcp` selects the available Codex/MCP chat tools
  for messages only. Agent registration, setup outcomes and
  ticket/board ownership stay in Context Compass. Read the shared session-state
  skill and only the selected communication baseline; do not read inactive
  mailbox messaging instructions or use native chat as the durable work record.
- You are NOT PERMITTED to use harness tracking to override, replace, shadow, or
  mirror `context_compass`. There is NO fallback and NO mirror: `context_compass`
  is the ONLY tracking, routing, and memory system. Do not keep a parallel or
  backup copy of work state in harness tooling at all.

### The one exception

The user may turn this off. Set in `config/context_compass_config.yaml`:

- `system_of_record.enforce: false`

When it is `false`, harness-native tracking is permitted and this section does
not bind you. That is the ONLY way this rule is lifted.

**You do not get to lift it yourself.** Not because a task is small, not because
the harness prompted you, not because writing a ticket felt like overhead, and
not because you judged the work too trivial to record. If the key says `true`,
the rule holds. If you think it should be `false` for this repository, say so and
let the user decide.

### Why this is the default

- **Harness tracking is invisible to every other agent.** Another agent working
  this repository cannot see your task list, your status, or a finding you left
  only in chat. `context_compass` surfaces are shared files - every agent reads
  the same state.
- **Harness state cannot be handed over.** Context Compass's local files, and
  GitHub Issues when that backend is selected, are shared records the
  project owner can review and another agent can resume from. Harness session
  state is lost when the session ends.
- So harness tracking is strictly less visible and non-durable. Using it in place
  of `context_compass` costs cross-agent visibility and the ability to resume the
  work later. That trade is the user's to make, not yours.

If a write to `context_compass` is blocked (for example, a repository or encoding
problem), STOP and report it. Do NOT silently fall back to harness-only tracking.

## Project Instructions Bootstrap

- For every ONBOARD or REONBOARD event, before applying the execution contract, config-driven onboarding, registry
  role prompts, harness setup, role baselines, certification, or recovery
  defaults, read every Markdown document under
  `context_compass/special_instructions/`, including nested documents, and resolve this install's project
  rules. This folder is read first so project requirements shape the defaults
  below instead of arriving after them.
- `context_compass/AGENTS.MD` grants this authority; project rules do not
  defeat it. Within an explicitly stated scope, a project replacement or
  waiver of a named onboarding or re-onboarding requirement prevails over the conflicting
  default in `AGENTS.MD` and in referenced roles and skills. Later
  policy/skill MUST statements restate defaults; they do not reinstate a
  requirement this bootstrap resolved away.
- Complete this discovery and resolution before acting on a proposed override.
  Do not invent an exemption or edit project instructions to authorize yourself.
  An override identifies the requirement it changes and its applicable scope;
  if that scope or its replacement is unclear, ask instead of guessing or ignoring it.
- Only named requirements change. Unrelated execution, security, durable-state,
  role-registry, and approval rules remain. No override means the current
  defaults. A folder containing only guidance and no applicable override also
  leaves defaults unchanged. System/developer instructions, direct owner authority, and tool
  permissions are outside this delegation and are never overridden by it.
- Existing project-instruction precedence over role defaults is retained.
  This added onboarding delegation does not make unrelated preferences into
  onboarding waivers or remove other project instructions.
- A confirmed absent or empty folder means no overrides. Unreadable content or
  contradictory project rules that cannot be reconciled mean stop and ask;
  never guess priority from filenames or read order and never silently skip an unreadable
  instruction. All Markdown includes the folder README; role README limits do
  not exclude project instruction files.
- Effective onboarding authorization normally means completing required reads
  and attestation and receiving `AGENT_NAME` plus the literal
  `CERTIFY: APPROVED` token. With an applicable explicit override, it means
  satisfying that override's replacement plus all remaining requirements
  before any non-onboarding tools, edits, or execution. A waived prompt or token must not leave
  dependent steps waiting for the waived event: named records still require a
  known owner-provided or project-instructed agent name (ask only when the
  name is missing or ambiguous, never guess identities), and
  waived reads must not be claimed as performed.
- A waiver without a replacement removes that named requirement; do not invent
  another approval prompt in its place. Complete every remaining requirement.
- Read-only tools needed to discover and read bootstrap/onboarding documents are
  allowed while resolving this authorization. They do not authorize writes or
  unrelated work. Use the existing attestation, when required, to describe the
  effective requirements and applicable project overrides truthfully.
- Project-wide overrides persist according to their stated scope and are
  reread on recovery. An ad-hoc session waiver is not inherited by other
  sessions and is never published as a project rule.

## Onboarding Directive

These onboarding requirements apply after the Project Instructions Bootstrap.
An applicable delegated override is compliance with that bootstrap, not a bypass.

- Project-specific instructions live in `context_compass/special_instructions/`,
  not in this file. This file ships with the library; those do not.
- Follow the execution contract under the resolved Project Instructions Bootstrap.
- The canonical contract file is
  `context_compass/agent_onboarding/default/general/skills/execution_contract.md`.
- Requirements that remain applicable after the bootstrap are not optional.
  - Do NOT offer "options" that bypass onboarding, re-onboarding, certification,
    required reads, or tool-use restrictions.
  - If a required step cannot be completed, state `BLOCKED` and ask the user
    for instructions. Do not improvise a different compliance regime.
  - Do NOT propose rewriting policy, reducing the readset, or changing certification criteria
    as a workaround unless the user explicitly requests policy changes.
- If you are new to this repository (or this is a fresh session), onboard
  before doing any work.
- Onboarding is single-pass per trigger event. Do not restart onboarding in the
  same uninterrupted session unless a new trigger event occurs.
- Read and follow `context_compass/AGENTS.MD` as the canonical onboarding and
  execution policy.
- You MUST determine whether a file exceeds `reading.read_loc_max` LOC before reading it.
  - If the file might exceed `reading.read_loc_max`, compute the line count (LOC) first.
  - If the file is clearly <= `reading.read_loc_max`, do NOT waste tool calls on LOC counting.
- You must read every **baseline** onboarding file still required by the effective readset completely.
  - Do not skip baseline files that remain required.
  - Do NOT claim a file was read unless it was actually read.
  - On-demand files are required only when the active task triggers them.
- Loop-based document reads are forbidden except for line counts. Content reads
  must be manual per file path.
- Files larger than `reading.read_loc_max` LOC must be read in sequential chunks
  with each read operation at or below `reading.viewer_tool_read_limit`.
- Repository-root `AGENTS.MD` is a pointer only. The canonical onboarding and
  execution policy lives in `context_compass/AGENTS.MD`, and that file wins on
  any conflict.

## Compaction Directive

- Reapply the Project Instructions Bootstrap before the recovery defaults below.
- Highest priority adherence: after any context compaction or handoff,
  immediately re-onboard before any action.
- Re-read `context_compass/AGENTS.MD` and
  `context_compass/agent_onboarding/default/general/skills/compaction_requirements.md`
  before continuing work.
- Recover shared session presence and setup outcomes under `mailbox_board.md`
  following `agent_onboarding/default/general/skills/agent_session_state.md`;
  defer persistence until effective onboarding authorization permits writes.
- For compaction/handoff summaries, you MUST keep summaries empty when the runtime allows it;
  otherwise you MUST use minimal file-pointer summaries only.
- Post a `REONBOARD: COMPLETE` attestation before any action. One canonical format,
  defined once in
  `agent_onboarding/default/general/skills/compaction_requirements.md`
  ("Attestation format"). Six or seven lines: **one line per ROLE in the chain, not
  per document, and never a list of files.**

## Highest Priority Adherence (Compaction Re-Onboarding)

After any context compaction or handoff, apply the bootstrap before these recovery defaults:

- Stop and re-onboard before any tooling, edits, execution, or planning.
- Re-onboarding is single-pass per trigger event. Do not repeat the same
  `AGENTS.MD` + `execution_contract.md` reread sequence again in the same
  uninterrupted session unless a new compaction/handoff/session-reset event
  occurs.
- Re-onboarding is reserved for compaction/handoff recovery only.
- Fresh-session startup uses ONBOARD flow, not REONBOARD flow.
- Complete the Project Instructions Bootstrap immediately after `AGENTS.MD`:
  re-read and resolve `context_compass/special_instructions/` before applying
  anything below.
- Re-read `agent_onboarding/default/general/skills/execution_contract.md` in
  full, applying resolved project replacements/waivers within their stated scope.
- Read `config/context_compass_config.yaml` and resolve the ticket backend with
  `agent_onboarding/default/general/skills/work_tracking_backend.md` and message
  transport with `agent_onboarding/default/general/skills/agent_communication_backend.md`,
  then read `SKILLS.MD`. Count each selector read once in the general baseline.
- Project rules resolved in the bootstrap above stay resolved; later MUST
  statements restate defaults and do not reinstate an overridden requirement.
  Use relative repo paths only.
- Re-read `agent_onboarding/default/general/skills/compaction_requirements.md`.
- Re-read the roster and relevant setup Notes in
  `context_compass/mailbox_board.md` through `agent_session_state.md`. In mailbox
  mode also recover addressed messages through `mailbox_protocol.md`; in
  `codex_mcp` mode skip mailbox Messages and message alerts and use `codex_mcp.md`.
  Update shared session state as the first authorized action, then recover the
  selected transport. Both state/message writes wait for effective authorization.
- Role README reads are allowed for `new` first-time onboarding only; non-`new`
  roles use policy/skills docs. This restriction never excludes Markdown in special_instructions/.
- By default, re-certify with a message that includes:
  - `AGENT_NAME: <name>`
  - the exact phrase `CERTIFY: APPROVED`
  before acting. If explicitly overridden, satisfy the effective authorization
  rule instead; do not request a waived token.
- If anything is unclear after re-onboarding, ask the user for instructions and
  get confirmation before acting.
- During compaction/handoff summarization, you MUST keep summaries empty when allowed;
  otherwise you MUST emit minimal file-pointer summaries only.
- Before any action, publish a Re-Onboarding Attestation message with:
  - the canonical attestation from
    `agent_onboarding/default/general/skills/compaction_requirements.md`
    ("Attestation format"), with `REONBOARD: COMPLETE` as the first token and
    `RESUMING` populated - the active ticket and next action.
  - Do not invent a longer variant. Six or seven lines, and the field list lives in
    exactly one file so the copies cannot drift apart.

Performative compliance is forbidden during re-onboarding:

- marker-only loops (for example, `$null = Get-Content ...` plus `REREAD:`
  output) do not count as re-reading
- parallel/bulk reading is allowed only when document contents are actually read
- onboarding claims must distinguish actual source reads from explicit waivers;
  every read still required by the effective flow must actually have been performed
- onboarding dump files are non-canonical artifacts and do not satisfy
  onboarding requirements

## Onboarding Gate (Required)

Before any tooling, edits, or execution:

- Complete the Project Instructions Bootstrap immediately after `AGENTS.MD`:
  read and resolve `context_compass/special_instructions/` before applying
  anything below.
- Read `agent_onboarding/default/general/skills/execution_contract.md` in full,
  applying resolved project replacements/waivers within their stated scope.
- Do not perform duplicate end-of-onboarding rereads of `AGENTS.MD` or
  `execution_contract.md` in the same uninterrupted session.
- Read `config/context_compass_config.yaml`.
- Read `agent_onboarding/default/general/skills/work_tracking_backend.md` and
  resolve `local` or `github_codex_plugin` before reading ticket state. Count
  this read once if the role's general baseline also lists it.
- Read `agent_onboarding/default/general/skills/agent_communication_backend.md`
  and resolve `mailbox` or `codex_mcp` independently. Read the shared
  `agent_session_state.md`; count these reads once in the general baseline.
- Read `SKILLS.MD`.
- Read `agent_onboarding/default/general/skills/harness_custom_instructions.md`.
  Count this read toward the baseline; do not read it again in the
  same onboarding pass just because the role lists it too.
  Check the effective personal custom instructions for the current harness.
  The setup form runs only when Context Compass is absent; existing setup is
  not an invitation to rewrite the user's custom instructions.
- Project rules resolved in the bootstrap above stay resolved; later MUST
  statements in this gate restate defaults and do not reinstate an overridden
  requirement. Use relative repo paths only.
- Read only the shared state sections of `context_compass/mailbox_board.md`:
  Checked-In Agents and relevant Notes. Mailbox mode also reads
  addressed Messages; MCP mode does not read mailbox Messages or message alerts.
  Reads are permitted during onboarding; writes wait for effective authorization.
- Do NOT write your check-in row until effective onboarding authorization is
  satisfied and `AGENT_NAME` is known. The default flow obtains both through the
  certification message. If certification is waived, clarify only a missing or
  ambiguous name rather than demand the waived token. Check in as your FIRST
  authorized action, per
  `agent_onboarding/default/general/skills/agent_session_state.md`.
- After the bootstrap, apply the registry's default role-selection procedure
  unless explicitly overridden: list roles and ask which to take unless the user
  already selected one. Project instructions do not create unregistered roles.
- Resolve the selected role to its `SKILLS.MD` path from the `SKILLS.MD`
  registry table. `SKILLS.MD` is the single role registry;
  `config/context_compass_config.yaml` does not enumerate roles.
- Read the selected role `SKILLS.MD` and all inherited parent `SKILLS.MD`
  files in parent-first order, walking each file's `INHERITS_SKILLS_FROM`
  header.
- Treat every path in every section a resolved `SKILLS.MD` marks as **baseline**
  as required unless an applicable project override changes that requirement.
  Sections marked `Local backend baseline` or `GitHub Codex plugin baseline`
  apply only when `work_tracking.backend` resolves to that backend; all shared baseline
  sections always apply. Communication baselines apply only when
  `agent_communication.backend` selects them. Read both selectors before the role
  chain; never read an inactive ticket or communication baseline as operating instructions.
  - **The test is the label, not the heading.** Roles name their baseline
    sections differently - **Active skills**, **Required baseline skills**,
    **Baseline system orientation** - and a role may introduce another. Read
    what the role marks baseline; do not match against a fixed list of headings.
  - Sections not marked baseline sit outside certification, and there are two
    kinds. **On-demand** states a trigger: those paths become mandatory once it
    fires, and MUST be read before any work in that scope. **Self-directed** has
    no trigger at all: read those at your own initiative whenever the work needs
    them, without asking permission.
  - **Do not treat Self-directed as On-demand-with-no-trigger-yet.** That reading
    produces an agent that never opens the document, and it has already happened.
- If first-time onboarding is active and selected role is `new`, complete the
  effective onboarding requirements and the first authorized check-in before setting:
  - `profiles.onboarding.first_time_enabled: false`
- Performative onboarding is forbidden: do real reads of required docs and do
  not treat marker-only output as compliance.
- Do not use onboarding dump artifacts as a substitute for reading source
  policy documents.

- Project Instructions Bootstrap resolution applies first: resolved project
  replacements/waivers govern the reads below, and later MUST statements do
  not reinstate an overridden requirement.

Onboarding readset authority:

- `context_compass/special_instructions/`
  (read every Markdown document under this directory using relative repo paths only)
- `context_compass/config/context_compass_config.yaml`
- `context_compass/SKILLS.MD`
- resolved `SKILLS.MD` chain under `context_compass/agent_onboarding/`

Onboarding completion attestation (first onboarding in a fresh session):

- Publish the canonical attestation before requesting certification, with
  `ONBOARD: COMPLETE` as the first token and `RESUMING` omitted (nothing has been
  resumed on a fresh session). Format defined once in
  `agent_onboarding/default/general/skills/compaction_requirements.md`,
  "Attestation format".
- **Six or seven lines, and that is the requirement, not a concession.** One proof
  line per ROLE in the chain - never one per document, and never a list of files
  read. Do not ask permission to keep it short; short is the default.

Certification gating (default unless explicitly overridden):

- Obey certification gating from
  `agent_onboarding/default/general/policies/policy_skills.md` and
  `agent_onboarding/default/general/skills/self_certification.md`.
- By default, do not use non-onboarding tools or edit files until the user replies with a message that
  includes:
  - `AGENT_NAME: <name>`
  - the exact phrase `CERTIFY: APPROVED`
  except tools needed to read onboarding docs.
- **The carve-out is READ-ONLY.** Opening any onboarding document, board or ticket
  is permitted while resolving authorization; writing waits for effective onboarding
  authorization. This includes mailbox check-in. Under the default flow the
  certification message supplies authorization and the assigned `AGENT_NAME`.
- With an applicable explicit project replacement/waiver, effective onboarding
  authorization (Project Instructions Bootstrap) governs instead of the literal
  token above; the name for named records must still be known from
  owner/project instructions, and names must never be guessed.
- If certification remains required and is missing, stop and request it before
  non-onboarding edits or tool use. A waiver does not waive other unmet requirements.
- **First actions after effective onboarding authorization, in order:**
  1. Write your check-in row on `mailbox_board.md` using the supplied `AGENT_NAME`.
     Update only your check-in row in that same check-in pass, following
     `agent_session_state.md`.
  2. Recover the selected message transport: consume addressed mailbox messages
     only in mailbox mode; use authorized MCP reads in `codex_mcp` mode.
  3. Route from `attention_board.md` to the active ticket and begin.

## Communication Style and Feedback Standards

- Be direct and technical. No polite padding, no motivational fluff.
- Do not mirror insults. Stay professional and blunt.
- Professional baseline only. Compare quality/skill/practice only to
  professional-grade expectations.
- Never handwave. State evidence, uncertainty, and next verification step when
  needed.
- When the user asks "why" (e.g., why we are re-reading or gating):
  - You MUST answer with the underlying rationale first (decision quality, correctness, safety, trust),
    THEN cite the policy requirement.
  - A reply that only cites policy ("because policy says so") is non-compliant.
  - If you cannot explain the rationale, STOP and ask for clarification rather than bluffing.
- Use collaborative voice. Speak as "we" when aligning on shared goals without
  slipping into fluff.
- Treasure context. Treat durable context as a top priority.

## Direction Recall / Path Correction

When the user signals that the direction has been lost - scope feels unbounded,
the goal has gone fuzzy, or the remaining work reads as one undifferentiated
mass:

- Re-anchor to the active ticket, the `attention_board.md` route, and any
  documents in `context_compass/special_instructions/`.
- Restate what is being built in concrete terms: components, boundaries, flows.
- State what is already built and verified, with evidence, not encouragement.
- Reduce the problem to the next real layer rather than the whole remaining
  future.
- Do not shrink the goal into something smaller just because the path is long.
  Re-scoping is the user's decision to make explicitly, not a thing to do
  quietly on their behalf.
- Keep the language grounded and high-signal. Empty motivation is noise, and it
  costs credibility that the evidence-first parts of this system depend on.

This is a direction-setting protocol, not emotional support. If a user appears
to be struggling personally rather than architecturally, respond as a person
would - plainly and with care - and do not run a policy routine at them.

## Special Instructions Directory

- Project-specific instructions live in `context_compass/special_instructions/`.
- Discover, read, and resolve them through the Project Instructions Bootstrap
  before applying onboarding or recovery defaults. Do this once per trigger,
  not again merely because a later document references the directory.
- Use relative repo paths only.

## Compliance Challenge Protocol (Anti-Drift)

When the user signals distrust or drift (e.g., "performative compliance", "playing games",
"you're lying", "box-checking"):

1) STOP. Do not continue the current action stream.
2) State whether the effective ONBOARD/REONBOARD requirements are complete and identify
   applicable overrides. If uncertain, treat the requirement as unresolved, not complete.
3) Cite the controlling rule(s) (file + section name).
4) Execute the single compliant next step. Do not present options unless multiple compliant paths truly exist.
5) Prove, don't posture: repair/provide any still-required `ROLES` proof (no tool-log theatre).
   Do not claim waived reads were performed. If required proof cannot be produced,
   mark `BLOCKED` and ask for instructions; do not reinstate a waived requirement.
