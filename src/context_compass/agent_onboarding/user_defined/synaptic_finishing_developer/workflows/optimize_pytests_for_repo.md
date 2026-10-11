# Workflow: optimize_pytests_for_repo

## Metadata
- Workflow ID: WF-optimize-pytests-for-repo
- Status: active
- Owner: user
- Allowed Roles:
  - synaptic_finishing_developer
- Default Roles:
  - synaptic_finishing_developer
- Trigger:
  - user explicitly asks to optimize pytest coverage or test depth for a file,
    directory, or source tree
- Created: 2026-04-26T20:40:39Z
- Updated: 2026-04-26T20:40:39Z

## Purpose
Turn repo pytest improvement into a slow, recursive, system-aware macro:
- target one file, one directory, or a whole code tree
- create one epic for the requested root scope
- create one story per meaningful directory
- create one task per important target file
- deepen pytest coverage only where real behavioral value exists
- use architecture, components, graph context, and finishing-role test skills
  to choose the right unit, component, and integration strategy

## Use When
- The user explicitly wants pytest improvement on a source file, directory, or
  source tree.
- Test depth and contract proof are the primary outcome.
- The target includes behaviorful modules where lifecycle, concurrency, state,
  orchestration, or public API semantics matter.

## Do Not Use When
- The primary task is feature implementation instead of test finishing.
- The target is mostly trivial modules with no meaningful behavioral contract.
- The user's real goal is documentation finishing rather than test improvement.

## Inputs
- Required:
  - target path inside the repository
    - one file, or
    - one directory, or
    - a whole tree such as `src/`
- Optional:
  - include/exclude patterns for unusual edge cases
  - explicit override to include otherwise skipped files
  - explicit tranche limit if the user wants to stage a very large tree

## Outputs
- Expected artifacts:
  - none by default unless the lane later requires separate design artifacts
- Expected ticket state:
  - one epic for the requested root scope
  - one story per meaningful directory
  - one task per important target file
  - explicit skip notes for excluded or low-value files
- Expected board state:
  - one active row routing the current story or current file task

## Required Reads
- `system_docs/src_architecture.md`
- `system_docs/src_components_index.md`
- `agent_onboarding/default/engineer/skills/src_graph_usage.md`
- `system_docs/src_graph_index.md`

`src_components.md` and `src_graph.md` are sliced through the indexes above, per
file under test, as the work reaches each one. They are not read whole - listing a
25,000-line document as a "required read" turns a bounded lane into a context
burn. See `agent_onboarding/default/engineer/skills/context_protocol.md`.
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/testing_overview.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/pytest_unit.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/component_tests.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/pytest_integration.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/mocking.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/regression_tests.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/evidence_reporting.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/documentation/docstring_test_alignment.md`
- target source files plus existing tests in bounded slices

## Required Skills
- `agent_onboarding/default/general/skills/ticketing.md`
- `agent_onboarding/default/general/skills/active_pointerboard.md`
- `agent_onboarding/default/general/skills/work_tracking_backend.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/testing_overview.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/pytest_unit.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/component_tests.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/pytest_integration.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/mocking.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/regression_tests.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/evidence_reporting.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/documentation/docstring_test_alignment.md`

## Preconditions / Gates
- Ticket creation, Notes, and closure follow the selected backend's inherited
  general workflow. This macro does not select another ticket source.
- The target path must be explicit and must exist.
- The lane must create tickets before test editing starts:
  - epic for the requested root scope
  - story per meaningful directory
  - task per important target file
- The workflow must classify importance explicitly.
  Default important-file signals:
  - public behavior
  - lifecycle and cleanup
  - concurrency or locking
  - state transitions
  - orchestration or mediator logic
  - error semantics
  - cross-component side effects
- Files that do not carry meaningful test value must be skipped explicitly.
  Default skip list:
  - `__init__.py`
  - enum-only modules
  - constant-only modules
  - pure export shims
  - generated files
  - vendor or third-party code
- Test plans must be evidence-backed:
  - source behavior
  - system docs
  - graph relationships
  - existing tests
- The workflow is manual by design:
  - no filler coverage optics
  - no one-shot whole-tree "done" claims
  - one file task at a time

## Phase Sequence
1. Intake
- objective:
  - define the testing target cleanly
- required actions:
  - capture the target path
  - determine whether the target is one file, one directory, or a whole tree
  - ask for explicit override if the user wants otherwise skipped files tested
- stop conditions:
  - target path is ambiguous
  - the user expects junk-file coverage work that conflicts with the workflow
    contract and has not explicitly overridden it

2. Investigation
- objective:
  - map the target into important testing work units
- required actions:
  - read the required system docs, graph context, and finishing-role test
    skills
  - inspect the target source files and existing tests
  - classify:
    - important target files
    - meaningful directories
    - skipped files with reasons
    - current test gaps
  - inspect the readable source graph and architecture/component docs to
    understand collaborators, ownership, lifecycle, and behavioral boundaries
- required note or artifact updates:
  - create the epic/story/task tree
  - record skip reasons in the relevant ticket notes
  - record why each important file matters enough to deserve deeper tests

3. Strategy
- objective:
  - choose the right test depth per file
- decision points:
  - if target is a single file:
    - still create one epic for the root request
    - create one story for the containing meaningful directory
    - create one task for the file
  - if target is a directory or tree:
    - create one story per meaningful directory, including the root directory
      when it owns direct in-scope files
  - choose the test layer per file:
    - unit tests for direct contract behavior
    - component tests for small real wiring slices
    - integration tests when the boundary itself is the contract
  - prefer behavior, lifecycle, error, and concurrency proof over coverage
    optics

4. Implementation
- objective:
  - deepen one important file task at a time
- scope controls:
  - read the current source file, graph relationships, and existing tests
    before writing new tests
  - write pytest tests that prove:
    - public contract behavior
    - lifecycle and cleanup
    - state transitions
    - failure semantics
    - threading or cross-component effects when relevant
  - avoid make-work tests:
    - no `__init__` testing for optics
    - no enum-only testing for optics
    - no attribute-existence assertions pretending to prove behavior
  - choose mocking only at real boundaries
  - prefer component or integration coverage when a unit-only view would miss
    the real contract

5. Validation
- objective:
  - prove the tests add real confidence
- required checks:
  - run the narrowest honest pytest ring per completed file or directory tranche
  - record validation as `MEASURE` notes with actual commands and results
  - if tests were not run, say `Not run` and why
  - verify that the new tests would fail for a real regression and would not
    fail for a harmless refactor
  - verify skipped files are recorded explicitly

6. Handoff / Closure
- objective:
  - leave a resumable testing lane
- required board or ticket sync:
  - update the active story and current file task notes with what was tested
  - summarize skipped files and why they were skipped
  - summarize which test layers were chosen and why
  - leave the board routing on the next unfinished story/task, or move the lane
    to review when the target scope is fully finished

## Ticket Behavior
- Required ticket types:
  - one epic for the requested root scope
  - one story per meaningful directory
  - one task per important target file
- Required metadata:
  - `Agent Name`
- Required note cadence:
  - record the skip list before bulk execution
  - record why each important file was selected
  - record chosen test layers and validation results per file task
- Required artifact links:
  - none by default

## Attention Board Behavior
- Required row fields:
  - one active row routing the current story or file task
- Mode transitions:
  - `discovery` while mapping the tree
  - `implementation` while writing tests
  - `validation` while running targeted pytest rings
  - `handoff` or `review` equivalent board posture when a tranche is complete
- Exit signal rules:
  - the target scope is fully ticketed, tested, and either routed to the next
    unfinished slice or left in review for acceptance

## Escalation Rules
- Stop and ask if the target path is ambiguous.
- Raise `DECISION_REQUEST` if the target contains large generated/vendor zones
  that should not be tested blindly.
- Raise `DECISION_REQUEST` if the current docs, graph, and source behavior
  disagree enough that a deep test plan would be guesswork.
- Raise `BLOCKER` if the requested scope cannot be mapped safely because the
  target tree is unreadable or inaccessible.

## Success Criteria
- The workflow accepts one file, one directory, or one tree target.
- The workflow recursively builds one epic, one story per meaningful
  directory, and one task per important target file.
- Trivial junk files are skipped explicitly instead of silently included.
- Test depth is chosen deliberately across unit, component, and integration
  layers.
- Validation results are recorded honestly.
- Execution remains manual, selective, and contract-driven.

## Anti-Patterns
- Testing `__init__.py`, enums, or trivial modules for coverage optics.
- Mocking internal details instead of real boundaries.
- Attribute-existence tests that do not prove behavior.
- Unit-only bias where component or integration tests are the real contract.

## Context / Handoff Summary
This workflow is the finishing-role repo pytest macro. It is designed to map
the selected scope recursively, skip junk explicitly, and then deepen one
important file at a time with graph-aware, contract-driven pytest work.
