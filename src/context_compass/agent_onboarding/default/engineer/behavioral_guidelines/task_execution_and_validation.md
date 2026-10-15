

# task_execution_and_validation

Purpose
- Define the execution and validation flow for a single task.

Story steps
1) Read the ticket
   - Confirm scope, acceptance criteria, and files in scope.
   - Treat unknowns as UNKNOWN by default.
2) Investigate and document
   - Record each meaningful finding before dependent work in supported Notes, attributed
     comments or authorized linked evidence under shared `ticketing.md`.
   - Multiple meaningful comments may carry findings directly; no forced body copy is
     required before ordinary continuation. Preserve historical Notes and author attribution.
   - Include evidence (`path:start_line-end_line`; use `start=end` for single-line evidence) and a concrete NEXT action.
3) Implement
   - Make minimal, reviewable changes.
   - Update docstrings/comments for touched code.
4) Validate
   - Run tests when possible; otherwise report "Not run" and why.
   - Prefer pytest for new tests per `AGENTS.MD`.
5) Report
   - Summarize changes and reference relevant files.
   - List remaining risks or follow-ups.
6) Close
   - Authorized agents close routine completed work after criteria, required tests and required
     reviews are satisfied, without another owner ping. Reserved owner decisions still wait.
   - Review is proportionate to actual consequence, uncertainty and contract; self-checks are
     not independent review. Use shared `ticketing.md` for qualified reviewer acceptance and
     the selected backend's verified closure sequence.

References
- `AGENTS.MD`
- `SKILLS.MD`
- the selected backend's general workflow skill




