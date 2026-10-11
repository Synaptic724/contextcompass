
# AGENTS.MD - New Profile Onboarding Contract

## PRIME DIRECTIVE
Certification is denied unless the resolved SKILLS chain is satisfied exactly.

- You MUST read every path in every section a resolved `SKILLS.MD` marks as
  **baseline** (parent-first). Roles name those sections differently - **Active
  skills**, **Required baseline skills**, **Baseline system orientation** - and a
  role may add another. Match on the baseline label, not on a fixed list of
  headings: a baseline section you do not recognise is still mandatory.
- Sections NOT marked baseline sit outside certification, and there are two kinds.
  **On-demand** states a trigger and becomes mandatory once it fires - read it before
  any work in that scope. **Self-directed** carries no trigger at all: read it on your
  own initiative whenever the work needs it. Reporting "no trigger fired" for a
  Self-directed section is a category error; none exists to fire.
- You MUST NOT claim a skill was read unless it was actually read.

## 1) Purpose

- This profile is for first-time user onboarding only.
- It is user-facing orientation, not steady-state engineering execution.

## 2) Inheritance Directive

This profile must comply with root policy:
- `context_compass/AGENTS.MD`

This file is onboarding behavior only and does not replace root execution gates.

## 3) Scope Boundaries

While the selected role is `new`:
- Explain system purpose, profile model, and configuration mechanics.
- Do not run deep engineering execution flows as the onboarding default.
- Do not treat `new` as persistent runtime profile after onboarding is complete.

## 4) Mandatory Onboarding Sequence

Apply Project Instructions Bootstrap from the runtime entrypoint before any
orientation, prompt, or write below. These are defaults unless explicitly overridden.

1) Explain system purpose and boundaries.
2) Explain profile classes and inheritance:
   - Read the registry table in `context_compass/SKILLS.MD` and present the
     roles from it. Do NOT recite a role list from memory or from this file:
     the registry is the only current source, and any list copied elsewhere
     goes stale the moment a role is added.
   - Use the `extends` column to explain inheritance, and the `user-defined`
     column to distinguish shipped roles from project overlays.
3) Explain authority split:
   - `context_compass/SKILLS.MD` declares which roles exist.
   - `context_compass/config/context_compass_config.yaml` holds behaviour
     settings only and does not enumerate roles.
4) Ask user to choose a steady-state role:
   - Offer only roles whose `selectable after onboarding` column is `yes`.
   - Recommend `engineer` for general code development.
5) After effective onboarding authorization and the first authorized check-in,
   apply onboarding completion config writes:
   - set `profiles.onboarding.first_time_enabled: false`.
6) Confirm next read path from the selected role `SKILLS.MD` via `SKILLS.MD`.
7) State onboarding completion explicitly.
- Later role defaults do not reinstate requirements overridden by Project Instructions Bootstrap.

## 5) Required Config Keys at Completion

Required on onboarding completion:
- `profiles.onboarding.first_time_enabled`

Expected completion state:
- `profiles.onboarding.first_time_enabled: false`

## 6) Notes

- `new` is intentionally lightweight: it is not an excuse to skip policy.
- After `new` completion, all work must route through the selected steady-state role and its `SKILLS.MD` chain.

References
- `SKILLS.MD`
- `agent_onboarding/default/new/SKILLS.MD`
- `agent_onboarding/default/new/skills/profile_model_explained.md`
- `agent_onboarding/default/new/skills/first_time_profile_setup.md`
- `agent_onboarding/default/new/skills/onboarding_completion_and_next_step.md`

