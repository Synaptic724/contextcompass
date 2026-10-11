

# repo_topology

Purpose
- Define the standard repo layout for this project.
- Keep onboarding/certification focused on documentation and ticket routing.

Repository layout
- Repo root is the project root (this checkout).
- Primary code lives under `src/` and tests under `tests/`.
- Onboarding and templates live under `agent_onboarding/` and `templates/`.
- Local mode stores tickets under `tickets/epics/`, `tickets/stories/`, and
  `tickets/tasks/`, with completed items in matching completed folders.
- Plugin mode stores tickets in configured GitHub Issue bodies and keeps local
  `issue_board.md` responsibility claims beside `attention_board.md`.

Collaboration note
- Certification in this repo is token-based (`CERTIFY: APPROVED`).
- Code-management workflows are user-directed and out of onboarding policy
  scope.

References
- `README.md`
- `AGENTS.MD`


