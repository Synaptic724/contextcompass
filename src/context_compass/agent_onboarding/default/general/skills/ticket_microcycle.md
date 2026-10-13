

# ticket_microcycle

Purpose
- Define a compact, repeatable execution loop that survives context loss.

Strict mode loop
1. `Investigate`
2. `Document` (immediate notes entry)
   - If `CONTEXT_MANAGEMENT_REQUIRED: true`, update the linked context
     artifact when the finding changes the reread pack or active topics.
3. `Strategy/Plan`
4. `Document` (decision/plan note)
   - If `CONTEXT_MANAGEMENT_REQUIRED: true`, update the linked context
     artifact when the decision changes the required context or topic focus.
5. `Implement`
6. `Document` (implementation note)
   - If `CONTEXT_MANAGEMENT_REQUIRED: true`, update the linked context
     artifact when implementation changes what must be reread for safe
     continuation.
7. `Validate`
8. `Document` (measure/result note)
   - If `CONTEXT_MANAGEMENT_REQUIRED: true`, update the linked context
     artifact when validation changes the active context or next reread set.

Relaxed mode loop
- Use when strict mode is disabled by config.
- Still required:
  - Document each meaningful finding.
  - Document before implementation starts.
  - Document after validation.
  - If `CONTEXT_MANAGEMENT_REQUIRED: true`, keep the linked context artifact
    synchronized with those findings.
- Unknown-first evidence rules remain unchanged.

Document semantics in both modes
- Record each meaningful changed finding, decision or result once at appropriate ticket depth,
  before dependent work required by the configured microcycle. Keep concise claim, impact,
  material limits and next action inline with exact retrievable supporting comment/doc links.
- Do not copy full linked reports or create substantive Notes for unchanged checks/ACKs.
  Required in-body state/evidence and routing updates still apply; a link alone is not the record.
- Preserve all existing Notes/history/custom regions. Concision is not permission to compact or
  migrate historical tickets. Parent owners synthesize child outcomes and remaining work rather
  than copying tactical logs; child completion does not accept the parent.
- These semantics do not waive onboarding/reentry, strict/relaxed configuration, evidence timing,
  denied/uncertain-write handling, note fields or the configured note-quality requirement.

Config source
- `config/context_compass_config.yaml`
- Keys:
  - `workflow.ticket_microcycle.enabled`
  - `workflow.ticket_microcycle.mode`
  - `workflow.ticket_microcycle.require_note_before_continue`
  - `workflow.ticket_microcycle.minimum_note_score`

