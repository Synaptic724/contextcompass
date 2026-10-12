

# compaction_requirements

Purpose
- Define the mandatory post-compaction recovery contract.
- Prevent policy drift by forcing deterministic, auditable re-onboarding.

Non-negotiable triggers
Resolve `AGENTS.MD` / Project Instructions Bootstrap before applying the
onboarding and recovery defaults in this document. Requirements not explicitly
overridden remain mandatory; do not treat a later MUST as cancelling an override.

- **REONBOARD** is mandatory after any context compaction or handoff.
- **ONBOARD** is mandatory at the start of a fresh session.
- Do not substitute ONBOARD for REONBOARD or vice-versa.
- Treat a confirmed compaction as a recovery event; a handoff alone does not
  change recovery requirements.

Non-negotiable rules
- After a trigger event: **STOP. REONBOARD/ONBOARD. THEN ACT.**
- Do not trust memory from before compaction as authoritative context.
- Performative compliance is forbidden:
  - marker-only "REREAD" logs are not compliance
  - claiming completion without comprehension proof is non-compliance
- Re-onboarding exists for decision quality and trust.
  - If you cannot explain what a document changes in your behavior,
    you have not read it sufficiently.
- Manual source-document reading is canonical; onboarding dump files are non-canonical.
- Loop-based/batch document-reading commands are forbidden
  (for/foreach/while loops, xargs-style runners, or piped file-list iterators).
- Files over 500 LOC MUST be read in explicit sequential chunks (<= 500 lines each).
- That chunking rule governs documents you have decided to read whole. It is NOT
  an instruction to read an indexed document whole. `src_components.md`,
  `src_graph.md` and `llm_full.md` are entered through their indexes and sliced.
  Chunking a 25,000-line graph into fifty sequential reads is not compliance -
  it is the exact failure the index exists to prevent.

No policy negotiation
- Do NOT propose changing policy gates, redefining certification, or reducing the readset as a workaround.
- If policy design needs to change, you may flag it, but you MUST still comply with the current policy unless the user explicitly authorizes changes.


External-memory-first rule
- Repository files and, when configured, GitHub Issues/Project are the durable
  work record. Harness session memory is not.
- Compaction summaries MUST be empty when the runtime allows empty summaries.
- If empty summaries are not allowed, emit the smallest possible pointer summary:
  - high-level outcomes only
  - critical policy anchor paths that MUST be re-read
  - active ticket path(s) or Issue URL(s)
  - changed file path(s)
  - immediate next action (one line)
- Do NOT write narrative replay in compaction summaries.

Required post-compaction sequence (REONBOARD)
Run this sequence exactly once per trigger event.

1) Read `context_compass/AGENTS.MD`.
2) Complete the Project Instructions Bootstrap: re-read and resolve
   `context_compass/special_instructions/` before applying anything below.
3) Read `agent_onboarding/default/general/skills/execution_contract.md` in full,
   applying resolved project replacements/waivers within their stated scope.
4) Read `config/context_compass_config.yaml` and resolve `work_tracking.backend`
   using `work_tracking_backend.md` plus `agent_communication.backend` using
   `agent_communication_backend.md`, then resolve the selected role via the
   registry table in `context_compass/SKILLS.MD`. Read only the selected
   message skill and preserve pauses and pending approvals.
   - If the active role cannot be determined: **STOP and ask the user**.
5) Read the resolved role `SKILLS.MD` chain in parent-first order.
6) Read every path in every section each resolved `SKILLS.MD` marks as
   **baseline**. Roles name these differently - **Active skills**, **Required
   baseline skills**, **Baseline system orientation** - and a role may add
   another. Match on the baseline label, not a fixed list of headings.
   - In `general`, re-read the shared baseline and only the backend baseline
     selected by `work_tracking.backend` in config. A missing key means local.
   - This includes the role's system-orientation set where it declares one. For
     `engineer` that is `system_docs/src_architecture.md` plus
     `src_architecture_index.md` and `src_components_index.md`, when they exist.
     Compaction is exactly when the shape of the system is lost, so re-entry is
     the wrong place to skip it. See
     `agent_onboarding/default/general/skills/context_compaction.md`.
   - On-demand skills are NOT required unless triggered by the active task.
     If triggered, they become mandatory and MUST be read before proceeding.
   - Self-directed skills are NOT required at re-entry either, but they have no
     trigger to wait for. Read them during the work, on your own initiative. Do
     not report "no trigger fired" for a Self-directed section - none exists.
7) Re-open `attention_board.md` and all active ticket(s) in the selected backend
   and verify they match. In plugin mode, also check `issue_board.md`, fetched
   Issue-body Status/Notes, and relevant Issue comments. Do not read local
   ticket archives in place of the active Issues.
   Recover shared presence and setup outcomes before resuming.
   Do not write the transition until effective onboarding authorization permits it.
   Existing custom instructions suppress the setup form; a recorded decline
   must not become another setup prompt merely because compaction occurred.
8) Publish the required REONBOARD attestation (below), reporting actual reads and any applicable waivers honestly.
9) Obtain effective onboarding authorization. By default, request certification
   and wait for a message that includes:
   - `AGENT_NAME: <name>`
   - the exact token: `CERTIFY: APPROVED`.
   If an explicit project override removes that requirement, complete the
   remaining requirements and any specified replacement without asking for a waived token.

README policy
- Role README reads are allowed only for `new` first-time onboarding.
- Non-`new` profile re-entry MUST use `SKILLS.MD` + skill/policy docs (not role READMEs).
  Project instruction files under `special_instructions/` are governed by the
  Project Instructions Bootstrap, not by this role README rule.

## Attestation format (CANONICAL - this is the only definition)

One shape for both events. Swap the first token: `ONBOARD: COMPLETE` for a fresh
session, `REONBOARD: COMPLETE` after compaction or handoff. Every other document
in this package points here rather than restating the field list.

```text
ONBOARD: COMPLETE                     # or REONBOARD: COMPLETE
AGENT_NAME: <name|REQUIRED_FROM_USER>
ROLES:
- general: <one rule from this role that changes what I do>
- <role>:  <one rule from this role that changes what I do>
RESUMING: <active ticket + next action, or "no active work">   # REONBOARD only
NO_ACTION_TAKEN_YET: true
```

**Six or seven lines. One line per ROLE in the chain - never per document, and
never a list of files.**

A file list is the cheapest thing to fabricate and the least useful thing to read.
It proves nothing (any agent can name a path it did not open) and costs tokens
proportional to the readset, which on a user-defined role runs past ninety
documents. What a reader actually needs is: which roles are in force, and what each
one changes about your behaviour. That is the whole point of resolving a chain.

So: no `FILES_REREAD`, no per-document proof, no readset manifest. If a specific
document changed your plan in a way the role line would bury, add one line and say
so - but more lines are not more proof.

ROLES (requirements)
- One line per role in the resolved chain, parent-first, `general` always first.
- Each line names **a specific, checkable rule from that role** and what it changes
  about what you will do. Not a summary of the role's purpose.
- Generic restatements ("be direct", "follow policy", "use tickets") are invalid -
  they could be written without reading anything, which is exactly what this is
  meant to detect.
- Do NOT reuse a rule across roles. If two roles produce the same callout, you have
  not read the child.
- `special_instructions/` gets its own line when the directory is non-empty, because
  it is project policy and outranks role defaults.
  Identify applicable overrides there instead of claiming waived reads were performed.
- **Boards are not roles and get no proof line.** `attention_board.md`,
  `artifact_board.md` and `context_management/context_board.md` are live state, not
  policy. A routing table has no rule to call out, and demanding one produces
  invented rules - the exact confabulation this is meant to catch. They are covered
  by `RESUMING`, below.
- **Do not ask permission to keep it short.** This form IS the requirement, not a
  concession, so there is nothing to request and no round-trip to spend.

RESUMING (REONBOARD only)
- One line: the active ticket you routed to and the next concrete action, taken from
  `attention_board.md`. Or `no active work` if the board carries none.
- Omit it entirely on a fresh `ONBOARD` - nothing has been resumed.
- This replaces the old `FILES_REREAD` list. What matters after compaction is where
  the work continues, not which paths were opened to find that out.

Attestation contract (default unless explicitly overridden)
- Emit the still-required attestation after the effective re-onboarding reads
  and before authorization. Read-only onboarding tools remain permitted.
- Do not perform non-onboarding actions before effective onboarding authorization.
- By default, after posting attestation, request certification and continue only after the user replies
  with a message that includes:
  - `AGENT_NAME: <name>`
  - `CERTIFY: APPROVED`
- An applicable explicit waiver/replacement follows Project Instructions Bootstrap;
  it does not cause a second request for the waived approval or false read claims.
- If attestation cannot be completed: **STOP and ask the user for instructions**.
- "Parallel/bulk reads" are allowed only if the documents were actually read.
  Marker-only loops remain forbidden.

Execution gate
- If any still-applicable required item above is incomplete, do not proceed.
- If scope, status, or expectations are unclear after re-onboarding: stop and ask.
- During resumed execution: UNKNOWN is the default for unevidenced claims.

Outcome contract
- Re-onboarding remains required after compaction/handoff unless explicitly
  overridden within the scope delegated by Project Instructions Bootstrap.
- The objective is to re-establish the operating rules each time so drift cannot accumulate.

References
- `AGENTS.MD`
- `agent_onboarding/default/general/skills/context_compaction.md`
- `agent_onboarding/default/general/skills/self_certification.md`
- `agent_onboarding/default/general/skills/user_approved_certification.md`
- `agent_onboarding/default/general/skills/harness_custom_instructions.md`
