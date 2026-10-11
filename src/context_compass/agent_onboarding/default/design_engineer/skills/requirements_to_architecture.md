
# requirements_to_architecture

Purpose
- Turn ambiguous requests into explicit requirements and constraints.
- Prevent "design drift" by anchoring design choices to stated needs.

Method
1) Extract the user goal (what success looks like).
2) Define non-goals (what is explicitly out of scope).
3) Identify constraints:
   - compatibility (API, schema, behavior),
   - performance/SLA expectations,
   - operational constraints (deployments, observability),
   - security/privacy constraints,
   - timeline and risk tolerance.
4) Capture assumptions and UNKNOWNs:
   - label UNKNOWN explicitly,
   - define the minimal verification path (what doc/code to read).
5) Define acceptance criteria:
   - functional,
   - non-functional,
   - testability criteria.

Output format (recommended)
- Goal:
- Non-goals:
- Constraints:
- Assumptions:
- UNKNOWNs + verification plan:
- Acceptance criteria:
- Proposed next step (design draft / source reads / ticket creation):

References
- `agent_onboarding/default/general/skills/unknowns_gate_reference.md`
- `agent_onboarding/default/general/skills/ticketing.md`
- `agent_onboarding/default/design_engineer/skills/system_design_method.md`


