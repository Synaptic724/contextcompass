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
  - ticket `Owner` is the accountable person, coordinator, or team
  - roster `owner` identifies the runtime owner; it is not technical authorship
  - `agent_name` is the user-facing assigned name or names
- `Agent Name` / `agent_name` may contain one name or multiple assigned names
  in a comma-separated list.
- After effective onboarding authorization and before planned implementation or validation work,
  sync the chosen name into the active ticket metadata and active
  `attention_board.md` row when those surfaces are touched in the current lane.
  When the certification token is waived by an applicable explicit project
  replacement, the name must still be known from owner or project
  instructions; ask only when it is missing or ambiguous, and never guess it.

Visible identity
- Ticket bodies, Notes and ticket comments must identify the full assigned
  name and actual role/function. Use the current known identity, not the model
  name, runtime UUID, publishing account, or ticket Owner.
- Ordinary chat messages do not require a name/role prefix.
- If the applicable naming rule has not established a name, record ticket
  attribution as `unassigned` and resolve it through that rule. Do not invent a name or role.
- Sign each authored ticket post, comment, and structured Note with that same
  name and role/function. A ticket's executor field does not identify every
  past contributor. New structured Notes include `AUTHOR` and `AUTHOR_ROLE`.
- Preserve native hosting-account attribution. Record actual prose, design,
  implementation, test, and evidence contributions by actor, scope, and revision;
  never infer authorship from Owner, executor, assignee, or publishing account.
- Public posts use an approved project-visible identity, not private session
  identifiers or restricted rosters. Existing scope and tool permissions apply;
  this rule creates neither a per-post approval gate nor a posting cadence.
- Do not fabricate names or authorship for historical records. Apply these
  fields to new contributions and preserve earlier evidence.

Non-goals
- This skill does not define long-term persistence of names across sessions.
- This skill grants no waiver itself. The default `CERTIFY: APPROVED` gate and
  any applicable project override are governed by Project Instructions Bootstrap.

References
- `agent_onboarding/default/general/skills/self_certification.md`
- `agent_onboarding/default/general/skills/user_approved_certification.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/general/skills/ticketing.md`
