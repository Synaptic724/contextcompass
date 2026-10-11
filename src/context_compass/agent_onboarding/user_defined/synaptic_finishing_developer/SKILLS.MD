# SKILLS.MD - synaptic_finishing_developer

Purpose
- Define active user-defined overlay skills for the
  `synaptic_finishing_developer` role.
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
- This role declares no **On-demand** and no **Self-directed** section of its own.
  It still inherits `engineer`'s Self-directed system reading - `src_components.md`
  and `src_graph.md`, sliced through their indexes at your own initiative, with no
  trigger to wait for. The three read states are defined in
  `context_compass/SKILLS.MD`, "Format contract for role `SKILLS.MD` files".

Active skills
- `agent_onboarding/user_defined/synaptic_finishing_developer/AGENTS.MD`
- `agent_onboarding/user_defined/synaptic_finishing_developer/WORKFLOWS.MD`
- `agent_onboarding/user_defined/synaptic_finishing_developer/profile_overrides.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/policies/synaptic_finishing_developer_policy_overrides.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/synaptic_finishing_developer_skill_overrides.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/behavioral_guidelines/synaptic_finishing_developer_behavior_overrides.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/documentation/docstring_craft.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/documentation/comment_craft.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/documentation/system_aware_docstrings.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/documentation/docstring_test_alignment.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/testing_overview.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/pytest_unit.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/component_tests.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/pytest_integration.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/mocking.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/regression_tests.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/skills/testing/evidence_reporting.md`
- `agent_onboarding/user_defined/synaptic_finishing_developer/examples/python/docstring_finishing_examples.py`
- `agent_onboarding/user_defined/synaptic_finishing_developer/examples/python/comment_finishing_examples.py`
- `agent_onboarding/user_defined/synaptic_finishing_developer/examples/python/pytest_unit_finishing_examples.py`
- `agent_onboarding/user_defined/synaptic_finishing_developer/examples/python/pytest_component_finishing_examples.py`
- `agent_onboarding/user_defined/synaptic_finishing_developer/examples/python/pytest_integration_finishing_examples.py`
