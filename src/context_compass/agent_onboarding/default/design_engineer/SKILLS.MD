
# SKILLS.MD - design_engineer

Purpose
- Define the eager and lazy readsets for the `design_engineer` role.
- This role is optimized for designing software engineering projects with high-quality handoff.

Inheritance
- `INHERITS_SKILLS_FROM: agent_onboarding/default/engineer/SKILLS.MD`

Skill classes (non-negotiable)
- This role ADDS two classes of its own:
  A) **Required baseline skills** (eager: always required for onboarding/certification)
  B) **On-demand skills (lazy readset index)** - document and patch authoring
     material, each read in full when its trigger fires.
- It also INHERITS the parent chain's classes, which include `engineer`'s
  **Baseline system orientation** - `system_docs/system_docs_read_first.md`,
  `src_architecture.md`, `src_architecture_index.md`, `src_components_index.md`.
  Those are baseline for this role too. This section describes what this file adds;
  it is not the complete list of what you must read.

Rules
- You MUST read **all** paths listed under **Required baseline skills** for this role
  to be considered onboarded/certifiable as `design_engineer`, **plus** every
  baseline section in the inherited chain.
- You MUST NOT claim an on-demand skill was read unless:
  1) a trigger condition was met, AND
  2) you actually read it in full.
- When a trigger condition is met, the on-demand skills become mandatory and MUST be
  read **before** any work in that scope.

Required baseline skills
- `agent_onboarding/default/design_engineer/AGENTS.MD`
- `agent_onboarding/default/design_engineer/WORKFLOWS.MD`
- `agent_onboarding/default/design_engineer/skills/architecture_contexts.md`
- `agent_onboarding/default/design_engineer/skills/design_engineer_execution.md`
- `agent_onboarding/default/design_engineer/skills/requirements_to_architecture.md`
- `agent_onboarding/default/design_engineer/skills/system_design_method.md`
- `agent_onboarding/default/design_engineer/skills/decomposition_and_boundaries.md`
- `agent_onboarding/default/design_engineer/skills/api_and_interface_design.md`
- `agent_onboarding/default/design_engineer/skills/data_modeling.md`
- `agent_onboarding/default/design_engineer/skills/architecture_tradeoffs.md`
- `agent_onboarding/default/design_engineer/skills/adr_and_decision_hygiene.md`
- `agent_onboarding/default/design_engineer/skills/nonfunctional_requirements.md`
- `agent_onboarding/default/design_engineer/skills/design_review_protocol.md`
- `agent_onboarding/default/design_engineer/policies/design_quality_policy.md`
- `agent_onboarding/default/design_engineer/policies/decision_record_policy.md`
- `agent_onboarding/default/design_engineer/policies/design_review_policy.md`
- `agent_onboarding/default/design_engineer/behavioral_guidelines/design_engineer_workflow.md`
- `agent_onboarding/default/design_engineer/behavioral_guidelines/design_validation_and_handoff.md`
- `agent_onboarding/default/design_engineer/examples/design_task_flow.md`
- `agent_onboarding/default/design_engineer/examples/adr_example.md`

On-demand skills (lazy readset index)
These files are not in the eager readset; read the whole file once its trigger fires.
The `engineer` lazy index applies too: a full system design, an architecture plan, a
component boundary redesign, a change to a public contract, API, schema or lifecycle
boundary, or P0/P1 claims about architecture, components or tests load its
`context_protocol.md`, `system_document_build.md` and patch entries before work in
that scope, in addition to the entries below.

- `agent_onboarding/default/design_engineer/skills/src_architecture_instructions.md`
  - Covers: the exact build protocol for `system_docs/src_architecture.md`.
  - Trigger: you create, update or review `src_architecture.md`.
- `agent_onboarding/default/design_engineer/skills/src_components_instructions.md`
  - Covers: the exact build protocol for `system_docs/src_components.md`.
  - Trigger: you create, update or review `src_components.md`.
- `agent_onboarding/default/design_engineer/skills/tests_architecture_instructions.md`
  - Covers: the exact build protocol for `system_docs/tests_architecture.md`.
  - Trigger: you create, update or review `tests_architecture.md`.
- `agent_onboarding/default/design_engineer/skills/tests_components_instructions.md`
  - Covers: the exact build protocol for `system_docs/tests_components.md`.
  - Trigger: you create, update or review `tests_components.md`.
- `agent_onboarding/default/design_engineer/policies/system_document_quality_rubric.md`
  - Covers: scoring the four system documents on whether they say anything useful.
  - Trigger: you create, update, review or grade any of those four documents.
- `agent_onboarding/default/design_engineer/skills/patch_framework_design.md`
  - Covers: building and maintaining patch-framework contracts for system-impacting
    design changes.
  - Trigger: a design change is system-impacting, or you author or review a patch
    under `system_docs/patches/`.
- `agent_onboarding/default/design_engineer/skills/architecture_patch_contracts.md`
  - Covers: the authoring contract for architecture patches.
  - Trigger: you author or review an architecture patch.
- `agent_onboarding/default/design_engineer/skills/component_patch_contracts.md`
  - Covers: the authoring contract for component patches.
  - Trigger: you author or review a component patch.
- `agent_onboarding/default/design_engineer/skills/code_description_patch_contracts.md`
  - Covers: the conditional authoring contract for code-description patches.
  - Trigger: you author or review a code-description patch.
