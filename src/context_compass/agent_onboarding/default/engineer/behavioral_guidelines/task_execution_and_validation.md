

# task_execution_and_validation

Purpose
- Define the execution and validation flow for a single task.

Story steps
1) Read the ticket
   - Confirm scope, acceptance criteria, and files in scope.
   - Treat unknowns as UNKNOWN by default.
2) Investigate and document
   - Investigate until one meaningful finding, then append a `## Notes` entry before more investigation.
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
   - Ask whether acceptance criteria are met before closing the ticket in the
     selected backend.

References
- `AGENTS.MD`
- `SKILLS.MD`
- the selected backend's general workflow skill




