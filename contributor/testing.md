# Testing Changes

## Set Up Locally

The shipped tools use the standard library and support Python 3.10 and newer.
Development uses pytest, declared in the `dev` dependency group. From the root:

```sh
uv sync --group dev
```

Use the resulting environment for commands in these guides. To avoid routine
Python imports leaving bytecode in the source tree, set this before test runs:

```powershell
# PowerShell
$env:PYTHONDONTWRITEBYTECODE = '1'
```

```sh
# bash / zsh
export PYTHONDONTWRITEBYTECODE=1
```

Then run the suite:

```sh
uv run python -B -m pytest -p no:cacheprovider
```

With an already prepared environment, `python -B -m pytest -p no:cacheprovider`
is equivalent; no environment reinstall is needed for each change. If a command
cannot access its cache or temporary directory, report that environment failure
rather than treating it as a test result. Do not weaken repository permissions.

## Match Tests to the Change

Start with the affected files, then broaden to the full suite before release.
These are entry points, not separate release gates:

| Change | Start with |
| --- | --- |
| CLI, payload lookup, or version agreement | `tests/integration/test_cli.py` |
| Board structure, regions, and user-owned content | `tests/integration/test_preserved_areas.py`, `tests/unit/test_user_regions.py` |
| Upgrades and cleanup | `tests/integration/test_update_three_hash.py`, `tests/integration/test_cleanup_modes.py`, `tests/unit/test_update_units.py`, `tests/unit/test_cleanup_units.py` |
| Manifest ownership, hashing, or compatibility | `tests/integration/test_manifest_lifecycle.py`, `tests/integration/test_version_tolerance.py`, `tests/unit/test_manifest_units.py` |
| Graph extraction and authored-data preservation | `tests/integration/test_authoring_lifecycle.py`, `tests/integration/test_graph_pipeline.py`, `tests/unit/test_graph_units.py` |
| Graph-generated tickets | `tests/integration/test_semantics_tickets.py` |
| Document indexes and review dumps | `tests/integration/test_index_lifecycle.py`, `tests/integration/test_llm_full.py`, `tests/unit/test_index_units.py` |
| Previously reported failures | `tests/regression/test_known_failures.py` |

For example:

```sh
uv run python -B -m pytest -p no:cacheprovider tests/integration/test_authoring_lifecycle.py tests/unit/test_graph_units.py
```

For a bug fix, first show that the new regression fails on the old behavior.
Assert the result that matters: exact preserved content, correct exit codes, and
unchanged user data. A success message or a node ID still existing is not enough.

Tests use temporary fixtures. The session guard in `tests/conftest.py` rejects
changes to the real payload while tests run. Finish source edits and generation
before starting a run; do not regenerate files while that guard is active.

One CLI test deliberately invokes `compileall` to prove that initialization does
not copy bytecode. It can create source `__pycache__` directories even with the
environment setting above. After testing, inspect and remove only those generated
cache directories under `src/`. Do not disable the test or redirect its bytecode
away from the payload: that would stop it testing the failure it exists to catch.

## Mutation Checks

The mutation runner changes a scratch copy, never the working tree. It first
requires the unmodified suite to pass, then checks that each deliberate defect
causes a failure:

```sh
uv run python -B tests/mutation_check.py --list
uv run python -B tests/mutation_check.py
```

For a bounded batch, use `--start 0 --count 5`; `--keep` retains its scratch copy
for investigation. A surviving mutation means coverage missed a defect. A
skipped mutation means its source anchor no longer matches. Neither is a passing
mutation check. Update anchors deliberately when the corresponding code changes.

## Before Calling It Verified

Record which suites ran, their results, and any skips or unavailable checks. A
local run on one interpreter is not the release matrix. The current workflow
runs Python 3.10 through 3.14 on Ubuntu and Windows, then builds distributions,
checks the wheel payload, and installs it into a separate smoke-test environment.

That workflow runs on a published release or manual dispatch, not every push or
pull request. Manual dispatch also reaches publishing: do not use it merely to
get a test run. See [Preparing a release](releasing.md).
