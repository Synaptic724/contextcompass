

# agent_lifecycle

Purpose
- Define how session tracking and handoffs are handled in this repo.

Rules
- Track active routing in `attention_board.md` and detailed execution state in ticket notes/checklists.
- Use UNKNOWN as the default claim stance until evidence is recorded.
- Do not invent external lifecycle tooling or databases.
- By default, on every onboarding or re-onboarding cycle ask for `AGENT_NAME: <name>` as
  part of certification. Apply Project Instructions Bootstrap and use effective
  onboarding authorization for the actual gate, then
  sync that assigned name into active workflow state when the active ticket
  or board row is touched. When certification is replaced by an applicable
  explicit project replacement, obtain the name as that replacement directs
  (owner or project instructions); ask only when it is missing or ambiguous.

Worklists
- In local mode, use `tickets/epics/`, `tickets/stories/`, and `tickets/tasks/`
  for active work, moving to matching completed folders only after confirmation.
- In plugin mode, use configured Issue bodies and their Status/Notes for active work;
  claim agents locally in `issue_board.md` and close only after confirmation.


