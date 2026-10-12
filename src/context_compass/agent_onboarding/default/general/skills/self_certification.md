

# self_certification

Purpose
- Ensure onboarding is complete before any tool usage or edits.

Required flow
- Complete `context_compass/AGENTS.MD` / Project Instructions Bootstrap first.
  The steps below apply to the effective readset and authorization rule; do not
  reinstate a requirement explicitly waived there.
- Read routing authority from:
  - `context_compass/config/context_compass_config.yaml`
  - `context_compass/SKILLS.MD`
  - `context_compass/agent_onboarding/default/general/SKILLS.MD`
  - selected role `SKILLS.MD` path from `context_compass/SKILLS.MD`
- Complete role-driven onboarding reads from:
  - `context_compass/config/context_compass_config.yaml`
  - `context_compass/SKILLS.MD`
  - the resolved role `SKILLS.MD` chain.
- For a given trigger event, complete the readset once; do not duplicate-read
  the same onboarding set before certification unless a new
  compaction/handoff/session-reset event occurs.
- Manual source-document reading from the readset is required; onboarding dump
  files are non-compliant.
- Performative onboarding is forbidden: marker-only reread logs do not satisfy
  the read requirement.
- If the user challenges onboarding truthfulness (e.g., "you didn't read that", "you're lying",
  "performative compliance"):
  - Treat the challenged authorization claim as unverified and STOP.
  - Recheck the applicable instructions and actual reads. Re-request
    `CERTIFY: APPROVED` only if certification remains required; a challenge does
    not itself invent a new requirement or cancel a valid project override.
  - Do not debate, rationalize, or offer bypass options.
- Before requesting certification, provide concise **read-integrity proof**:
  - concrete rule callouts from reread docs, AND
  - a one-line "what this changes in my behavior" per callout.
  - Tool logs/dumps are not proof.
- Before requesting certification, include `AGENT_NAME` in the attestation:
  - use the provided name if the user already gave one in the current trigger event
  - otherwise use `AGENT_NAME: REQUIRED_FROM_USER`
- For ONBOARD/REONBOARD attestations, keep declarations concise with
  `ROLES`, `AGENT_NAME`, and `NO_ACTION_TAKEN_YET: true`.
- Summarize the effective onboarding outcome honestly, distinguishing reads
  performed from requirements waived. Request approval only when still required.
- By default, require the approval message to include:
  - `AGENT_NAME: <name>`
  - the exact token `CERTIFY: APPROVED`.
- Do not use tools or edit files until effective onboarding authorization
  (normally the user providing that token), **except
  tools needed to READ onboarding documents, boards and tickets.** Reads are
  permitted before authorization; writes are not, which is why check-in happens
  immediately after it. Root `AGENTS.MD` "Certification gating" is authoritative.
- With an applicable explicit project replacement/waiver (Project Instructions
  Bootstrap), effective onboarding authorization governs instead of the literal
  token: satisfy the replacement plus all remaining requirements before any
  non-onboarding writes. A waived token never authorizes guessing identities,
  counters, or unperformed reads; identity, mailbox, and counter rules apply
  with a known owner-provided or project-instructed name.
- If the override is a waiver with no replacement, omit the named requirement
  and complete the remaining requirements; do not invent another approval prompt.

Certification record
- Track certification in the session narrative and update `attention_board.md`
  routing when certification state affects execution.
- Shared check-in and session state require effective onboarding authorization
  in both communication modes per `agent_session_state.md`.


