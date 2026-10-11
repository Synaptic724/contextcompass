
# design_validation_and_handoff

Purpose
- Define what "validated design" means and how to hand off to implementation.

Validation checklist
- Interfaces are explicit (API/schema/event contracts).
- Failure modes are identified with mitigations.
- Test strategy is explicit and covers core invariants.
- Rollout strategy is explicit and includes backout.
- Observability hooks are defined for the new behavior.
- Tickets are broken down into actionable units with dependencies.

Handoff rules
- If implementation is requested:
  - identify the minimal set of files/modules to change,
  - hand off to `engineer` execution discipline,
  - ensure each ticket has acceptance criteria and validation steps.

References
- `agent_onboarding/default/general/skills/ticketing.md`
- `agent_onboarding/default/engineer/behavioral_guidelines/task_execution_and_validation.md`


