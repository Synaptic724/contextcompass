

# SKILLS.MD - general

Purpose
- Define the eager and lazy readsets for the `general` role.

Inheritance
- `INHERITS_SKILLS_FROM: none`

Activation rule
- Read every shared baseline path, exactly one ticket backend baseline below,
  the Local boards baseline unless the backend is `github_issues`, and the
  selected communication baseline below.
- Resolve `work_tracking.backend` from `config/context_compass_config.yaml`
  before these reads. Missing means `local`; `github_codex_plugin` requires an
  Issue repository and connected GitHub plugin; `github_issues` requires an
  Issue repository and keeps every board in GitHub Issues. Resolve legacy values
  using `work_tracking_backend.md`; an invalid selection blocks work.
- Resolve `agent_communication.backend` from the same config before messaging
  reads. Missing means `mailbox`. Resolve using
  `agent_communication_backend.md`; an invalid selection blocks communication
  work. Ticket and communication selectors are independent.

Readsets
- Eager: the baseline sections below - shared, plus the selected ticket and
  communication baselines. Read them in full at onboarding and at recovery.
- Lazy: the On-demand index at the end of this file. Each entry says what the
  file covers and which trigger loads it. You hold the index from onboarding;
  when a trigger fires, read that whole file before acting in its scope. An
  index line is a pointer, not the procedure.

Shared baseline skills
- `agent_onboarding/default/general/AGENTS.MD`
- `agent_onboarding/default/general/skills/general.md`
- `agent_onboarding/default/general/skills/execution_contract.md`
- `agent_onboarding/default/general/skills/compaction_requirements.md`
- `agent_onboarding/default/general/skills/harness_custom_instructions.md`
- `agent_onboarding/default/general/policies/policy_skills.md`
- `agent_onboarding/default/general/skills/agent_stance.md`
- `agent_onboarding/default/general/skills/agent_lifecycle.md`
- `agent_onboarding/default/general/skills/agent_identity.md`
- `agent_onboarding/default/general/skills/career_selection.md`
- `agent_onboarding/default/general/skills/mrp_policy.md`
- `agent_onboarding/default/general/skills/configuration_standards.md`
- `agent_onboarding/default/general/skills/context_gold.md`
- `agent_onboarding/default/general/skills/security_and_secrets.md`
- `agent_onboarding/default/general/skills/repo_topology.md`
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `agent_onboarding/default/general/skills/ticketing.md`
- `agent_onboarding/default/general/skills/memory_management.md`
- `agent_onboarding/default/general/skills/reactive_documentation.md`
- `agent_onboarding/default/general/skills/active_documentation.md`
- `agent_onboarding/default/general/skills/context_window_budget.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/general/skills/agent_communication_backend.md`
- `agent_onboarding/default/general/skills/agent_session_state.md`
- `agent_onboarding/default/general/skills/unknowns_gate_reference.md`
- `agent_onboarding/default/general/skills/self_certification.md`
- `agent_onboarding/default/general/skills/user_approved_certification.md`
- `agent_onboarding/default/general/skills/ticket_microcycle.md`
- `agent_onboarding/default/general/skills/role_local_workflows.md`
- `agent_onboarding/default/general/WORKFLOWS.MD`
- `agent_onboarding/default/general/skills/context_compaction.md`

- `agent_onboarding/default/general/behavioral_guidelines/agent_lifecycle_and_heartbeat.md`
- `agent_onboarding/default/general/behavioral_guidelines/onboarding_summary.md`

Local backend baseline
Read these paths when `work_tracking.backend` resolves to `local`.
- `agent_onboarding/default/general/skills/ticketing_skill_contract.md`
- `agent_onboarding/default/general/skills/workflow.md`
- `agent_onboarding/default/general/behavioral_guidelines/work_intake_and_execution.md`

GitHub Codex plugin baseline
Read these paths only when `work_tracking.backend` is `github_codex_plugin`.
- `agent_onboarding/default/general/skills/github/codex_plugin.md`
- `agent_onboarding/default/general/skills/github/workflow.md`
- `issue_board.md`

GitHub Issues backend baseline
Read this path only when `work_tracking.backend` is `github_issues`. Tickets and
every board live in GitHub Issues; it replaces the local board reads.
- `agent_onboarding/default/general/skills/github/issues_backend.md`

Local boards baseline
Read this path when the ticket backend keeps its boards in local files: `local`
or `github_codex_plugin`.
- `attention_board.md`

Mailbox communication baseline
Read this path only when `agent_communication.backend` resolves to `mailbox`
(the default when absent) and the boards are local files. In `github_issues`
mode, mailbox messages are events on agent issues, described in
`github/issues_backend.md`.
- `agent_onboarding/default/general/skills/mailbox_protocol.md`

Codex MCP communication baseline
Read this path only when `agent_communication.backend` resolves to
`codex_mcp`.
- `agent_onboarding/default/general/skills/codex_mcp.md`

Every shared-state instruction stays baseline in both transports.

Note on the board paths. With local boards, `attention_board.md` and, in plugin
mode, `issue_board.md` are eager reads, but they are **live mutable state, not
policy**. You open them to learn what is happening right now, not to learn a
rule. They get no attestation proof line - the one-line `RESUMING` field covers
them. See `agent_onboarding/default/general/skills/compaction_requirements.md`.
Do not invent a rule to quote from a routing table. `artifact_board.md` and
`context_management/context_board.md` are in the lazy index below; open them
when an artifact or a context pack is in play. In `github_issues` mode every
board is a GitHub record instead, as `github/issues_backend.md` maps them.

On-demand skills (lazy readset index)
These files are not in the eager readset. Claiming one was read without its
trigger firing is a false attestation; once its trigger fires, it is mandatory,
and you read the whole file before proceeding in that scope. On-demand is the
trigger-gated state. It is not the Self-directed state `engineer` uses for its
system documents, which has no trigger; the states are defined in
`context_compass/SKILLS.MD`.

- `agent_onboarding/default/general/skills/ticket_closure_attention_sync.md`
  - Covers: the full attention-board sync when a local ticket closes.
  - Trigger: local backend, before you move a ticket to a `completed/` folder.
- `agent_onboarding/default/general/workflows/start_context_compass_work.md`
  - Covers: starting a new lane - objective, ticket shape, backend and board route.
  - Trigger: the user explicitly asks to start a new Context Compass lane.
- `agent_onboarding/default/general/workflows/turn_in_selected_tickets.md`
  - Covers: closing a user-selected set of tickets.
  - Trigger: the user explicitly asks to turn in one or more tickets.
- `agent_onboarding/default/general/workflows/cleanup_context_compass.md`
  - Covers: cleaning up work state (closing tickets, syncing boards). Not a
    package reset.
  - Trigger: the user explicitly asks to clean up Context Compass work state.
- `agent_onboarding/default/general/workflows/sync_attention_board.md`
  - Covers: rebuilding or repairing `attention_board.md` from current ticket truth.
  - Trigger: the user explicitly asks to rebuild or repair `attention_board.md`.
- `artifact_board.md`
  - Covers: the registry of artifacts linked to tickets and their dispositions.
  - Trigger: with local boards, the active ticket lists artifacts, or you create,
    link, retain or clean up an artifact.
- `agent_onboarding/default/general/skills/context_management.md`
  - Covers: reusable context packs and how tickets reference them.
  - Trigger: a ticket sets `CONTEXT_MANAGEMENT_REQUIRED: true`, or the user asks
    for a reusable context pack.
- `context_management/context_board.md`
  - Covers: the index of context packs and their `Context ID` values.
  - Trigger: the same as `context_management.md`, with local boards.
- `agent_onboarding/default/general/skills/harness_custom_instructions_setup.md`
  - Covers: the custom-instruction setup form, instruction clauses, and the
    apply-and-verify steps.
  - Trigger: the custom-instruction check classifies this harness ABSENT, or the
    user asks to set up or change these instructions.
- `agent_onboarding/default/general/skills/package_upgrade.md`
  - Covers: upgrading or repairing a `context_compass/` install without losing
    project work.
  - Trigger: the user asks to upgrade, repair or check this install, or you are
    reviewing an upgrade plan.
- `agent_onboarding/default/general/skills/ticket_design.md`
  - Covers: ticket templates, optional Agile metadata and named attribution.
  - Trigger: creating a new ticket, using a custom ticket template, or reading or
    writing a ticket that contains `AGILE_METADATA` or `TICKET_ATTRIBUTION`.
  - Read the selected full template and canonical `templates/ticket_contract.json`.
    Do not apply this design to historical records or change an agent's role.
- `agent_onboarding/default/general/skills/github/issues_setup.md`
  - Covers: labels, the header issue, creating an agent issue, and moving a
    project from local boards to `github_issues`.
  - Trigger: in `github_issues` mode, the repository has no `cc-header` issue, a
    `cc-` label is missing, the header's version is older than this install's,
    you have no agent issue at check-in, or the owner asks to move off local
    boards.
- `agent_onboarding/default/general/skills/github/migration.md`
  - Covers: moving existing file tickets to GitHub Issues.
  - Trigger: the user asks to migrate existing file tickets to GitHub Issues.
  - Keep local mode active until a reviewed dry run, complete remote verification,
    and explicit owner approval of the destination and content.
- `agent_onboarding/default/general/skills/llm_full_usage.md`
  - Covers: reading or regenerating the `llm_full.md` whole-package review dump
    through its index.
  - Trigger: `llm_full.md` exists at the repository root and you are about to read
    from it, or you have been asked to regenerate it.
