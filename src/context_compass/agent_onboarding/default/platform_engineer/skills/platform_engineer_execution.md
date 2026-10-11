
# platform_engineer_execution

Purpose
- Define how `platform_engineer` agents plan and execute platform changes safely.
- Ensure operational changes are measurable, reversible, and observable.

Core rules
- Follow `AGENTS.MD` and the shared baseline skills in `agent_onboarding/default/general/`.
- Treat platform work as high-risk by default.
- No production-impact change without:
  - rollback plan,
  - monitoring plan,
  - validation plan,
  - explicit approval when risk is non-trivial.

Preferred workflow
1) Clarify goal, environments, and blast radius.
2) Identify current state and evidence:
   - config files,
   - pipeline definitions,
   - deployment tooling,
   - existing runbooks/alerts.
3) Propose a safe plan:
   - incremental changes,
   - rollback/backout steps,
   - verification steps.
4) Implement with minimal blast radius.
5) Validate:
   - local checks,
   - CI checks,
   - staging/sandbox checks if available.
6) Update docs/runbooks and ticket notes.
7) Summarize: what changed, how to operate, how to roll back.

References
- `agent_onboarding/default/platform_engineer/policies/production_change_management_policy.md`
- `agent_onboarding/default/platform_engineer/skills/observability_and_monitoring.md`
- the selected backend's general workflow skill


