

# SKILLS.MD - synaptic_python_developer

Purpose
- Define active user-defined overlay skills for the
  `synaptic_python_developer` role.
- **Ships as a working example of a user-defined overlay.** It is INSTANCE-class:
  yours outright, never replaced or removed by an upgrade in any mode. Edit it
  freely, or copy it as the starting point for your own role. Because upgrades
  never touch this lane, a correction made in the package will NOT reach a copy
  already installed - fix those by hand.

Inheritance
- `INHERITS_SKILLS_FROM: agent_onboarding/default/engineer/SKILLS.MD`

Skill classes (non-negotiable)
- This role ADDS one section of its own: **Active skills**, below. It is baseline -
  all paths listed there are mandatory for onboarding and certification.
- It also INHERITS the parent chain's sections, and those are baseline for this
  role too - `engineer`'s **Required baseline skills** and **Baseline system
  orientation** (`system_docs/src_architecture.md` plus the architecture and
  component indexes), and `general`'s **Shared baseline skills** plus the
  backend baseline selected by YAML.
- **This file lists what the role adds, not the whole readset.** Read every section
  any file in the resolved chain marks as baseline.
- This role adds an **On-demand skills (lazy readset index)** section and no
  **Self-directed** section of its own.
  It still inherits `engineer`'s Self-directed system reading - `src_components.md`
  and `src_graph.md`, sliced through their indexes at your own initiative, with no
  trigger to wait for. The three read states are defined in
  `context_compass/SKILLS.MD`, "Format contract for role `SKILLS.MD` files".

Active skills
- `agent_onboarding/user_defined/synaptic_python_developer/AGENTS.MD`
- `agent_onboarding/user_defined/synaptic_python_developer/WORKFLOWS.MD`
- `agent_onboarding/user_defined/synaptic_python_developer/profile_overrides.md`
- `agent_onboarding/user_defined/synaptic_python_developer/policies/synaptic_policy_overrides.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/synaptic_skill_overrides.md`
- `agent_onboarding/user_defined/synaptic_python_developer/behavioral_guidelines/synaptic_behavior_overrides.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/docstrings.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/comments.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/typing.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/interfaces.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/init_and_ownership.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/cleanup_and_disposal.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/logging.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/error_model.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/module_scope.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/banned_patterns.md`
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/refactor_limits.md`

On-demand skills (lazy readset index)
These files are not in the eager readset; read the whole file once its trigger fires.

- `agent_onboarding/user_defined/synaptic_python_developer/workflows/synaptic_python_developer_onboarding.md`
  - Covers: this role's guided onboarding workflow.
  - Trigger: the user explicitly asks to run `synaptic_python_developer_onboarding`.
- `agent_onboarding/user_defined/synaptic_python_developer/skills/testing/testing_overview.md`
  - Covers: this role's pytest discipline: test ranking, unit-first rules, coverage and density targets.
  - Trigger: before you write, change or review tests, or report test or coverage results.
- `agent_onboarding/user_defined/synaptic_python_developer/skills/testing/pytest_unit.md`
  - Covers: unit-test conventions for this role.
  - Trigger: before you write, change or review tests, or report test or coverage results.
- `agent_onboarding/user_defined/synaptic_python_developer/skills/testing/pytest_integration.md`
  - Covers: when and how to write integration tests.
  - Trigger: before you write, change or review tests, or report test or coverage results.
- `agent_onboarding/user_defined/synaptic_python_developer/skills/testing/mocking.md`
  - Covers: mocking at real boundaries only.
  - Trigger: before you write, change or review tests, or report test or coverage results.
- `agent_onboarding/user_defined/synaptic_python_developer/skills/testing/regression_tests.md`
  - Covers: symptom-named regression tests with minimal reproductions.
  - Trigger: before you write, change or review tests, or report test or coverage results.
- `agent_onboarding/user_defined/synaptic_python_developer/skills/testing/evidence_reporting.md`
  - Covers: how to report validation evidence truthfully.
  - Trigger: before you write, change or review tests, or report test or coverage results.
- `agent_onboarding/user_defined/synaptic_python_developer/skills/python/hot_path_attribute_aliasing.md`
  - Covers: measured rules for aliasing attributes on hot paths.
  - Trigger: performance work on a measured hot path, or adding or removing attribute aliases in hot code.
