

# onboarding_summary

Purpose
- Provide a concise onboarding checklist for agents.

Checklist (short form)
1) Confirm repo root + policy sources
   - Read `AGENTS.MD` and any directory-local `AGENTS.MD` in scope.
2) Read onboarding entrypoints
   - `config/context_compass_config.yaml`
   - `context_compass/SKILLS.MD`
3) First-time user path only (`new` profile)
   - Read `agent_onboarding/default/new/skills/first_time_profile_setup.md`
   - Read `agent_onboarding/default/new/README.md`
4) Select working role
   - Read the registry table in `context_compass/SKILLS.MD` for the current
     role list. Do not rely on a role list copied into any other document.
   - Read `agent_onboarding/default/general/SKILLS.MD` first.
   - Read the selected role `SKILLS.MD` chain after baseline, parent-first.
5) Certification gate
   - Request approval before any tool usage or edits.
   - Approval must include the exact token `CERTIFY: APPROVED`.
6) Post-cert work execution
   - Use ticket folders when `work_tracking.backend` resolves to `local`; use
     the configured plugin to fetch Issue bodies and local `issue_board.md`
     when it is `github_codex_plugin`.
   - Route from `attention_board.md` and resume from linked ticket notes.
   - Orient from `system_docs/src_architecture.md` plus the architecture and
     component indexes, then descend: index -> slice -> the code. Slice
     `src_components.md` and `src_graph.md` through their indexes whenever the
     work needs them - your call, no permission required, and never whole.
   - Keep `attention_board.md` current for routing and ticket notes current for
     durable findings.

References
- `AGENTS.MD`
- `config/context_compass_config.yaml`
- `context_compass/SKILLS.MD`


