# Special Instructions

Purpose
- Users can place project-specific instruction documents in this folder.
- Agents must read and follow every Markdown document in `context_compass/special_instructions/`.

Rules
- Use relative repo paths only.
- Keep project-specific instructions here instead of embedding them directly in `AGENTS.MD` when possible.

Delegated authority
- `context_compass/AGENTS.MD` (Project Instructions Bootstrap) grants named
  onboarding scopes to explicit project replacements or waivers stated here.
  Within a stated scope, an explicit replacement/waiver prevails over the
  conflicting default; later MUST statements restate defaults and do not
  reinstate it.
- State the scope of every override: which named requirement it replaces or
  waives, and any session or lane limit (see the clarification rule below).
- A confirmed absent or empty folder means no overrides. Unreadable content
  or irreconcilable contradictions mean the agent stops and asks; priority
  is never guessed from filenames and unreadable instructions are never
  silently skipped.
- This mechanism changes default onboarding only where it explicitly says so.
  Fresh installs without project files keep the shipped defaults untouched.
- This README does not activate any override itself; overrides need explicit
  stated scope in a project instruction file. An override without a stated
  scope cannot be applied; ask the owner for clarification rather than
  ignoring an explicit project instruction.

Registration
- Documents here are picked up by a directory sweep, not by a named entry in a
  `SKILLS.MD` readset. Adding a file here is enough; nothing needs to be
  registered, and an unreferenced file in this folder is not an orphan.
- That is deliberate: project instructions are the user's to add, and requiring
  a registry edit would make the package own something it should not.
