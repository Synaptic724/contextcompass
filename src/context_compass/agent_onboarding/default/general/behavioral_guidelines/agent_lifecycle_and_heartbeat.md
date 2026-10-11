

# agent_lifecycle_and_heartbeat

Purpose
- Define the session lifecycle and handoff habits for this repo.

Story steps
1) Establish session identity
   - Use the agent identity provided by the user.
   - If identity is missing or unclear, stop and ask before any work.
2) Check-in
   - Acknowledge scope, constraints, and ticket status.
   - Ensure `attention_board.md` reflects active routing and open the linked active ticket.
3) Work loop
   - Use tickets in the selected backend for planning and execution.
   - Keep ticket checklists current and append findings as they occur in `## Notes`.
4) Check-out
   - Summarize what changed, what remains, and what to do next.
   - Complete tickets only after user confirmation: move local tickets to
     matching completed folders, or record and verify Issue-body `Status: done`
     and completion summary, then close through the GitHub plugin.

Artifacts touched
- `attention_board.md`
- `issue_board.md` (plugin mode only)
- The following ticket folders are local-mode surfaces only:
- `tickets/epics/`
- `tickets/epics/completed/`
- `tickets/stories/`
- `tickets/stories/completed/`
- `tickets/tasks/`
- `tickets/tasks/completed/`

References
- `agent_onboarding/default/general/skills/agent_lifecycle.md`
- `AGENTS.MD`



