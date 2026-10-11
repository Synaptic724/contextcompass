

# system_overview_for_user

Purpose
- Give first-time users a concise explanation of what this system does.

What context_compass is
- A workflow and context system for structured AI work.
- A structure for planning, execution, and handoff consistency.
- A way to improve quality and continuity when working with AI agents.

What it is for
- Durable ticket-based planning (`epic`, `story`, `task`).
- Deterministic active routing via `attention_board.md`.
- Controlled artifact linkage via `artifact_board.md`.
- Profile-based onboarding paths via config + skill maps.

Language support
- Designed for code development in any language and policy-driven fiction
  authoring workflows.
- The profile model allows domain specialization without changing the shared
  core process.

AI usage model
- Primary target: AI-assisted development workflows, any runtime.
- Compatible with other AI agents when they follow the same policy contracts.
- Recommended execution mode in this repo:
  - the strongest reasoning setting your runtime offers.
  - Other reasoning modes are currently untested in this repo context.

Core system anchors
- `AGENTS.MD`
- `config/context_compass_config.yaml`
- `SKILLS.MD`
- `tickets/` for `local`, or configured GitHub Issue bodies for `github_codex_plugin`
- `issue_board.md` for plugin-mode agent claims
- `attention_board.md`
- `artifact_board.md`

Outcome for user
- You should understand:
  - why the system exists,
  - where state lives,
  - how onboarding and profile routing work.

References
- `agent_onboarding/default/new/skills/profile_model_explained.md`
- `agent_onboarding/default/new/skills/configuration_map_guide.md`



