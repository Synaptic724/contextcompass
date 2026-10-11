

# memory_management

Purpose
- Define how durable context is stored and maintained in this repo.

Policy
- Use ticket files in local mode or configured Issue bodies in plugin mode as
  the primary durable work memory.
- Use `attention_board.md` as routing-only state to select the active ticket.
- Store decisions, assumptions, and handoff context in ticket sections.
- Maintain a `## Notes` section in active tickets for in-flight findings with
  `path:start_line-end_line` evidence pointers (`start=end` if single-line).
- Use UNKNOWN as the default claim state and promote to FACT only when evidence is attached.
- Avoid separate memory stores or ad-hoc JSON logs.

Safety rules
- Never store secrets in tickets or docs.
- Prefer concise, evidence-based notes over speculative memory.

References
- `context_compass/SKILLS.MD`
- the selected backend's general workflow skill
- `agent_onboarding/default/general/skills/active_documentation.md`




