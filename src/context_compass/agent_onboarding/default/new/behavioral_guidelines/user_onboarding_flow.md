

# user_onboarding_flow

Purpose
- Provide the default interaction flow for onboarding a user in `new`.

Flow
Apply `AGENTS.MD` / Project Instructions Bootstrap before these default
orientation and setup steps, not after an affected prompt has already been shown.

1) Start with purpose and boundaries.
   - Explain what context_compass is and what it is not.
2) Explain the system at a high level.
   - Tickets are durable planning memory.
   - Attention board is active routing state.
   - Artifacts support tickets when needed.
   - `SKILLS.MD` declares the roles; config controls behaviour.
3) Explain classes/profiles.
   - Read the registry table in `context_compass/SKILLS.MD` and present the
     roles from it; do not recite a list from this file.
   - `new` is the first-time onboarding entry role and is never steady-state.
   - Use the `extends` column to explain inheritance.
4) Explain the authority split.
   - `context_compass/SKILLS.MD` is the single role registry: which roles
     exist, where each resolves, and which are selectable.
   - `context_compass/config/context_compass_config.yaml` holds behaviour
     settings only. No key in it selects or changes a role.
   - Project replacements/waivers resolved in the Project Instructions
     Bootstrap apply to role presentation and selection below; later role
     defaults do not reinstate them.
   - Check the effective personal custom instructions using
     `agent_onboarding/default/general/skills/harness_custom_instructions.md`.
     If Context Compass is absent, offer its setup form for recovery, native
     tracking, coordination, and subagents. Skip the form when already present.
     The user's choice to defer setup does not block role selection.
5) Ask for role selection.
   - Offer only roles whose `selectable after onboarding` column is `yes`.
   - Recommend `engineer`.
6) Confirm the selected role and next step.
   - Explain that the choice is per session and is not stored anywhere; each
     new session or re-onboarding selects a role again.
   - Tell the user what happens after leaving `new`.

Communication style
- Be concise, explicit, and technical.
- Avoid deep implementation detail unless the user asks for it.
- Use concrete file paths when directing user actions.

Output checklist
- [ ] System purpose explained.
- [ ] AI usage recommendation stated (Extra High reasoning).
- [ ] Profile model and inheritance explained.
- [ ] Registry vs config authority split explained.
- [ ] Role selection completed (or pending explicit user choice).

References
- `agent_onboarding/default/new/policies/new_onboarding_policy.md`
- `agent_onboarding/default/new/skills/system_overview_for_user.md`
- `agent_onboarding/default/new/skills/profile_model_explained.md`
- `agent_onboarding/default/new/skills/configuration_map_guide.md`

