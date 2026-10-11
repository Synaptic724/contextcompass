

# Engineer Example: Task Execution Flow

Context
- The user asks for a small refactor with tests.
- Follow `SKILLS.MD` and the selected backend's general workflow skill for
  ticketing and execution rules.

Example flow (concise)
1) Confirm scope and list files to be changed.
2) Read the relevant module and docstrings.
3) Propose a minimal plan (2-4 steps) and confirm.
4) Implement the change with docstrings and tests.
5) Run `pytest` and report results or say "Not run."

Expected output format (sample)
- Plan:
  - Update `module_x.py` to split helper function.
  - Add unit test for the new behavior.
  - Run `pytest -q`.
- Changes:
  - `module_x.py`: refactored helper, updated docstrings.
  - `tests/unit/test_module_x.py`: new coverage for split helper.
- Tests:
  - `pytest -q` (pass)




