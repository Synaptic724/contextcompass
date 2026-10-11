# context_management

Purpose
- Define the context-management system for reusable reread packs.
- Make context-heavy tickets able to point at one derived context document
  instead of embedding long read lists inline.
- Keep the skill itself baseline-readable in the general role while keeping
  ticket-level use optional.

Canonical surfaces
- Board:
  - `context_management/context_board.md`
- Artifact root:
  - `context_management/artifacts/`
- Optional artifact template:
  - `context_management/context_artifact_template.md`

Ticket contract
- Tickets may include an optional `Context Management` section.
- Required fields for that section:
  - `CONTEXT_MANAGEMENT_REQUIRED: true | false`
  - `CONTEXT_IDS:` (0 or more `Context ID` values from
    `context_management/context_board.md`)
  - `CONTEXT_TOPICS:` (0 or more topic bullets)
  - `IF_UNKNOWN:` (`UNKNOWN` | `ask user before implementation` | `none`)
- Default posture:
  - `CONTEXT_MANAGEMENT_REQUIRED: false`
- When a required context-management field is not yet known, write
  `UNKNOWN` explicitly instead of leaving it blank.

Baseline read vs ticket use
- The general role always reads:
  - `agent_onboarding/default/general/skills/context_management.md`
  - `context_management/context_board.md`
- Ticket-level use remains optional and only activates when the ticket opts in.

When context management is active
- If a ticket sets `CONTEXT_MANAGEMENT_REQUIRED: true`, the agent must:
  1. resolve every `CONTEXT_ID` through `context_management/context_board.md`
  2. read every linked context artifact before implementation or validation
  3. treat those artifacts as derived reread packs, not as canonical policy
  4. keep the ticket section and `context_management/context_board.md`
     synchronized
  5. if the required context is not concretely known yet, write `UNKNOWN`
     and ask the user before implementation
  6. update the linked context artifact during the Ticket Microcycle whenever
     meaningful findings change required rereads or active topics

When context management is inactive
- No context artifact is required.
- Normal ticket, note, and board flow remains sufficient.

What belongs in a context artifact
- Explicit file paths to reread
- Explicit topics or questions the ticket is about
- Optional reread order
- Explicit exclusions when useful

What does not belong
- Ticket history replay
- Artifact-board-style retention policy for unrelated work
- Generic statements like "understand the system"

Unknown handling
- Do not default lazily to unknown context requirements.
- If a ticket wants context management and the required context cannot be
  defined concretely, ask the user before implementation.

Board rules
- `attention_board.md` stays ticket-routing-only.
- Context artifacts are indexed in `context_management/context_board.md`.
- Tickets point at context entries by `Context ID`, not by board-row position.
- Use the board only when at least one active ticket opted into context
  management.

References
- `agent_onboarding/default/general/skills/ticketing.md`
- the selected backend's general workflow skill
- `context_management/context_board.md`
