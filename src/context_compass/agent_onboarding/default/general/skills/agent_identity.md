# agent_identity

Purpose
- Define how an agent receives and carries a user-facing name through
  onboarding, certification, tickets, and board routing.

Rules
- Apply `context_compass/AGENTS.MD` / Project Instructions Bootstrap first.
- By default, on every ONBOARD and REONBOARD cycle ask for
  `AGENT_NAME: <name>` with the certification message. If an applicable project
  override changes naming or certification, resolve the name from the explicit
  owner/project instructions and ask only when it is missing or ambiguous.
- Attestation must include an `AGENT_NAME` line.
  - If no name is known under the applicable naming rule for this trigger event, use:
    `AGENT_NAME: REQUIRED_FROM_USER`
  - If a name is already provided under that rule, use that exact name.
- By default, certification requests must ask for both:
  - `AGENT_NAME: <name>`
  - `CERTIFY: APPROVED`
- By default, treat agent naming as cycle-local:
  - do not assume the previous session name is still valid
  - ask again on every onboarding or re-onboarding cycle
- `owner` and `agent_name` are different fields:
  - `owner` is the current executor/runtime owner
  - `agent_name` is the user-facing assigned name or names
- `Agent Name` / `agent_name` may contain one name or multiple assigned names
  in a comma-separated list.
- After effective onboarding authorization and before planned implementation or validation work,
  sync the chosen name into the active ticket metadata and active
  `attention_board.md` row when those surfaces are touched in the current lane.
  When the certification token is waived by an applicable explicit project
  replacement, the name must still be known from owner or project
  instructions; ask only when it is missing or ambiguous, and never guess it.

Non-goals
- This skill does not define long-term persistence of names across sessions.
- This skill grants no waiver itself. The default `CERTIFY: APPROVED` gate and
  any applicable project override are governed by Project Instructions Bootstrap.

References
- `agent_onboarding/default/general/skills/self_certification.md`
- `agent_onboarding/default/general/skills/user_approved_certification.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/general/skills/ticketing.md`
