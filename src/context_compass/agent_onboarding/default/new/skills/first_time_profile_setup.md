
# first_time_profile_setup

Purpose
- Define first-time onboarding steps before steady-state profile execution.
- Centralize setup guidance for user orientation, profile selection, and default class assignment.

First-time setup sequence
1) Start from `AGENTS.MD` bootstrap rules, including project
   replacements/waivers already resolved in the Project Instructions Bootstrap.
2) Read `SKILLS.MD` - the single role registry - and the behaviour settings in
   `config/context_compass_config.yaml`.
3) Explain the system purpose and onboarding model using:
   - `system_overview_for_user.md`
   - `profile_model_explained.md`
   - `configuration_map_guide.md`
4) Offer role selection for post-onboarding:
   - Read the registry table in `context_compass/SKILLS.MD`.
   - Offer only roles whose `selectable after onboarding` column is `yes`.
   - Use the `extends` column to explain what each role builds on.
   - Recommend `engineer` for most code-development execution.
   - Describe an unfamiliar role from the Purpose section of its own
     `SKILLS.MD` rather than from a list held in this document.
5) Confirm first-time completion and switch to selected default profile path map.

Describing roles to the user
- The registry table is the list; each role's own `SKILLS.MD` is the
  description. Read the role's Purpose section when the user asks what a role
  does.
- Do not maintain a role-description list in this file. Earlier versions did,
  and it silently went stale every time a role was added.
- Shape of the model, which is stable even as roles change:
  - `general` is the shared system, ticketing, policy, and workflow baseline.
  - `engineer` layers implementation practice on top of `general`.
  - The specialized software roles layer deeper posture on top of `engineer`.
  - The fiction-authoring roles layer on top of `general`.
  - User-defined roles are project or team overlays, usually on `engineer`.

User-facing recommendation
- This system is designed for code development and supports any language.
- It enhances AI-assisted workflows by enforcing durable context.
- Use the strongest reasoning setting your runtime offers.
- Other reasoning modes are currently untested in this repo.

Rules
- Keep role README reads scoped to first-time setup (`new` profile).
- Do not require role README reads for non-new profile onboarding paths. This
  does not exclude project Markdown under `special_instructions/` from bootstrap reads.
- Treat the `SKILLS.MD` registry table as authoritative for which roles exist
  and which are selectable.
- Treat config YAML as authoritative for onboarding and workflow behaviour only;
  it does not enumerate roles.
- Treat skill-map `INHERITS_SKILLS_FROM` headers as authoritative for
  inheritance order.

References
- `context_compass/AGENTS.MD`
- `context_compass/SKILLS.MD` (role registry - the current role list)
- `context_compass/config/context_compass_config.yaml` (behaviour settings)
- `agent_onboarding/default/general/SKILLS.MD`
- `agent_onboarding/default/new/SKILLS.MD`
- `agent_onboarding/default/new/policies/new_onboarding_policy.md`
