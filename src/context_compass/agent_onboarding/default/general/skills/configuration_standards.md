

# Configuration Standards

Purpose
- Define formatting standards that are configurable, explicit, and shared
  across ticketing and workflow documents.
- Keep documentation readable while preserving compact, evidence-backed notes.

Canonical config source
- `context_compass/config/context_compass_config.yaml`
- Settings path: `documentation_format`
- Tool read-limit path: `reading.viewer_tool_read_limit`
- Manual chunking path: `reading.read_loc_max`

Tool read-limit semantics
- `reading.viewer_tool_read_limit` is measured in lines.
- It is not a token limit and not a character-count limit.
- `reading.read_loc_max` is measured in lines-of-code (LOC) per manual read chunk.
- Default values are both `500`.
- Use this as the upper bound for one read operation when chunking large docs.

Line-width contract
- Target range: 90-110 characters per line (about 12-18 words).
- Hard cap: 120 characters per line.
- Applies to prose lines in tickets, workflow notes, and policy docs.
- Exceptions:
  - Unbreakable tokens (paths, IDs, URLs, code snippets).
  - Table rows where splitting would reduce readability.
- If a prose line exceeds hard cap and is breakable, wrap it.

EVIDENCE field contract
- Preferred form for short evidence:
  - `EVIDENCE: path:start-end`
- Required form for long or multi-path evidence:
  - One path per line under a multi-line `EVIDENCE` block.
- The same one-path-per-line rule applies to `Artifact Links` path lists in
  tickets.

Accepted patterns
- Inline (single short path):
  - `EVIDENCE: context_compass/agent_onboarding/default/general/skills/workflow.md:78-85`
- Multi-line (recommended when path count >= 2 or line would exceed cap):
  - `EVIDENCE:`
    `- context_compass/agent_onboarding/default/general/skills/workflow.md:78-85`
    `- context_compass/attention_board.md:8-15`

Rule to select EVIDENCE style
- Use inline form only if both are true:
  - there is exactly one evidence path
  - the line stays within hard cap
- Otherwise use multi-line one-path-per-line form.

Enforcement surfaces
- Templates:
  - `context_compass/templates/epic_template.md`
  - `context_compass/templates/story_template.md`
  - `context_compass/templates/task_template.md`
- Process policy:
  - the YAML-selected backend workflow in `agent_onboarding/default/general/SKILLS.MD`
  - `context_compass/SKILLS.MD`
  - `context_compass/agent_onboarding/default/general/skills/ticketing.md`

Adoption policy
- Forward-looking by default:
  - all new or edited active docs should follow this standard.
- Archived/completed docs are not rewritten unless explicitly requested.





