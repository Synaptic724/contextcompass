

# policy_skills

Purpose
- Enforce the policy chain so edits stay deterministic and reviewable.

When to use
- At the start of every session and before editing in a new directory.

Canonical Contract (from AGENTS.MD)
This repository is a public library. Code quality and documentation are
first-class deliverables.

Placement
- Keep `AGENTS.MD` at the repository root.
- Per-directory variants are allowed when explicitly needed.

Certification gate (default unless explicitly overridden)
- Apply `AGENTS.MD` / Project Instructions Bootstrap before this procedure.
- Complete the effective onboarding readset and any required attestation.
- By default, request approval and require the approval message to include the exact token
  `CERTIFY: APPROVED`.
- Do not use non-onboarding tools or edit files until effective onboarding authorization,
  **except tools needed to READ onboarding documents, boards and tickets.** Without
  that carve-out this rule would forbid the onboarding reads it depends on. Reads
  are permitted; writes - including your mailbox check-in - wait for effective
  authorization. Normally this requires the token and assigned name; an explicit
  waiver removes only its named requirement, without inventing a replacement prompt.
  Root `AGENTS.MD` / Project Instructions Bootstrap and its certification gate govern.

Required flow
- Read `AGENTS.MD` and directory-local `AGENTS.MD` (if present).
- Complete the Project Instructions Bootstrap and resolve project instructions
  before applying the remaining onboarding or recovery defaults below.
- Read
  `context_compass/agent_onboarding/default/general/skills/execution_contract.md`
  in full after the Project Instructions Bootstrap, applying project
  replacements/waivers resolved there within their stated scope.
- Follow role `SKILLS.MD` routing from:
  - `context_compass/SKILLS.MD` - the single role registry; the registry table
    is the only place roles are declared
  - selected role `SKILLS.MD` and inherited parent `SKILLS.MD` files
- Do NOT look for a roles map in `context_compass/config/context_compass_config.yaml`.
  That file holds behaviour settings only and does not enumerate roles.
- For first-time `new` profile setup, follow
  `agent_onboarding/default/new/skills/first_time_profile_setup.md`.
- Apply README policy from the `reads README` column of the registry table:
  - `new` reads role README files.
  - No other role requires README reads.
- For onboarding/re-onboarding, complete role-driven onboarding reads from:
  - `context_compass/config/context_compass_config.yaml`
  - `context_compass/SKILLS.MD`
  - resolved role `SKILLS.MD` chain in parent-first order, walked via each
    file's `INHERITS_SKILLS_FROM` header starting from the registry row for
    the selected role.
- Use manual source-document reads for onboarding; do not use onboarding dump
  artifacts as policy input.
- Treat every section a role `SKILLS.MD` marks as **baseline** as mandatory reads.
  The headings vary by role - **Active skills**, **Required baseline skills**,
  **Baseline system orientation** - so match on the baseline label rather than on
  a fixed list of names.
  - On-demand skills are required only when the task triggers them.
  - Self-directed skills carry no trigger: read them at your own initiative when
    the work needs them. They are outside certification but not gated.
- After any compaction/handoff re-entry, complete the same full readset before
  any non-onboarding action.
- Read
  `context_compass/agent_onboarding/default/general/skills/execution_contract.md`
  and apply its active-partner + performance-engineering rules.
- Route active work from `context_compass/attention_board.md` and keep detailed
  state in ticket `## Notes`.
- Use the Ticket Microcycle with meaningful-finding note gates during
  execution.
- Use Epic/Story/Task tickets in the selected work backend for all planned
  work. Local `tickets/` lanes apply only when `work_tracking.backend` resolves to `local`.
- Resolve `agent_communication.backend` independently and read only the
  selected message skill. Default `mailbox` remains compatible with both
  ticket backends.
- For code-engineering tasks, hand off to engineer profile docs after general
  onboarding:
  - `agent_onboarding/default/engineer/skills/context_protocol.md`
  - `agent_onboarding/default/engineer/skills/staleness_protocol.md`
  - `agent_onboarding/default/engineer/skills/technical_expertise.md`

Truthfulness rule
- Never claim tests or checks ran unless they actually ran.

Secrets policy (non-negotiable)
- Never place secrets in the repo or in tickets/docs.
- If a user requests storing secrets in-repo, refuse and request a safe
  alternative.

Documentation and Convention Precedence
- Before making edits, read and follow existing repository conventions:
  `README`, `CONTRIBUTING`, `docs/`, and any architecture/design notes.
- Do not invent new conventions if the repo already has a pattern.
- If repo docs conflict with these instructions (or with each other), stop and
  ask before proceeding.

Unknowns Gate
- Apply the canonical policy in
  `agent_onboarding/default/general/skills/unknowns_gate_reference.md`.
- UNKNOWN remains the default for unevidenced claims in this policy.
- Routing decisions (scope, onboarding completeness, stale-doc status) must be
  evidence-backed; if verification is incomplete, route as UNKNOWN and block
  downstream synthesis until verified.
- Policy conflicts must include explicit evidence and impact statements before
  requesting user resolution.

Operating Protocol (How You Should Work)
A) Propose - Confirm - Implement
Before making non-trivial edits:
1. Restate the goal in 3-5 bullets.
2. List the constraints you will obey (scope, policy, and workflow gates).
3. List the exact files / symbols you will modify.
   If any of the above is uncertain, stop and ask before editing.

B) Scope Control
- Stay within the declared files/symbols.
- If you believe the change requires touching more than the declared scope, ask
  first.

C) Documentation Ritual
As a ritual, after implementing a change:
- Re-read touched policy docs, ticket notes, and board rows.
- Ensure state, evidence, and next actions are accurate and current.

Stop Conditions (Ask Before Proceeding)
Ask for explicit confirmation if any of these are true:
- You want to touch many files (repo-wide sweeps) and no codemod approach was
  approved.
- You want to rename/move files or symbols.
- You want to change public API shape or semantics.
- You want to introduce new dependencies or tooling.
- You want to change formatting across files.

Summary
- This is a public library.
- Documentation is part of the API.
- Do precise, scoped edits.
- Keep onboarding, certification, and ticket routing deterministic.

Order of authority (highest to lowest)

This ranking answers **"how should I behave?"** - it is a policy ordering, not a
statement about where truth lives.

This is a project-document ordering, subject to system/developer instructions
and explicit user direction:

1. The package `AGENTS.MD` bootstrap and delegation contract.
2. Applicable project onboarding overrides within that delegated scope.
3. Remaining `AGENTS.MD` requirements and inherited role-policy defaults.
4. `SKILLS.MD` routing and remaining skill requirements.
5. Example documentation.
6. Repo documentation (`README`, `docs/`).
7. Code (last resort *for policy*).

Existing project-instruction precedence over role defaults remains in force.
The delegation changes only explicitly overridden requirements, not unrelated policy.

**A different question has the opposite answer.** For **"what does this system
actually do?"** the ordering inverts: the code is authoritative and every document
is a description of it, accurate as of whenever somebody last wrote it down.

- Deciding whether you may edit a file, skip a gate, or claim a test ran -> policy
  order above. Code does not get a vote.
- Deciding what a function returns, who owns a lifecycle, whether a field can be
  `None` -> **read the code.** A document that disagrees with the source is stale,
  not authoritative. Record the contradiction and fix or file it.

"Code (last resort)" has never meant "avoid reading the source". It means the
source does not set policy. An agent that cites this line as a reason to describe
behaviour it never opened has inverted the rule - and the Unknowns Gate in
`agent_onboarding/default/general/AGENTS.MD` already forbids exactly that.

Operational guidance (enriched)
- Do not improvise conventions; mirror the skills and examples.
- Treat skills as the executable version of policy.
- Use examples as canonical style references, not suggestions.
- Keep scope minimal and reviewable; do not widen without approval.
- If a change implies touching many files or renames, ask first.

Workflow
1) Check for AGENTS.override.md in the target directory.
2) Read AGENTS.MD to confirm non-negotiables.
3) Read the specific skills for the change type.
4) Review relevant examples and mirror the pattern.
5) If work is code-engineering, continue with engineer profile docs before
   implementation.




