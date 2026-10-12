

# user_approved_certification

Purpose
- Define the explicit approval step that unlocks tool usage and edits.

Approval script
- Resolve `context_compass/AGENTS.MD` / Project Instructions Bootstrap before
  using this script. Its defaults apply only where not explicitly overridden.
- By default, ask the user to reply with a message that includes:
  - `AGENT_NAME: <name>`
  - the exact token `CERTIFY: APPROVED`.
- Do not proceed with any tool use or file edits before effective onboarding
  authorization (normally that approval), except read-only onboarding/bootstrap tools.

Rules
- Only request still-required approval after completing the effective reads from:
  - `context_compass/config/context_compass_config.yaml`
  - `context_compass/SKILLS.MD`
  - `context_compass/agent_onboarding/default/general/SKILLS.MD`
  - selected role `SKILLS.MD` path from `context_compass/SKILLS.MD`
- Before requesting approval, complete role-driven onboarding reads from:
  - `context_compass/config/context_compass_config.yaml`
  - `context_compass/SKILLS.MD`
  - the resolved role `SKILLS.MD` chain
  - include read-integrity proof in the ONBOARD/REONBOARD attestation
  - include `AGENT_NAME` in the ONBOARD/REONBOARD attestation
  (concrete rule callouts -> behavior implications; not tool logs).
- Do not request approval based on onboarding dump artifacts; approval requires
  source-document read completion.
- On each fresh session or recovery event, re-resolve project instructions and
  complete the effective readset before requesting any still-required approval.
- With an applicable explicit project replacement/waiver (Project Instructions
  Bootstrap), effective onboarding authorization is reached through the
  specified replacement, if any, plus all remaining requirements. A waiver with
  no replacement removes the named requirement; do not ask for a substitute token.
  Effective authorization governs the same subsequent steps; identity, mailbox, and
  counter rules still require a known owner-provided or project-instructed
  name and never permit guessing. Shared session-state writes follow
  `agent_session_state.md` in both communication modes.


