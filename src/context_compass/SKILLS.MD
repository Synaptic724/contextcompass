
# SKILLS Role Map

Purpose
- This file is the **single registry of roles** in Context Compass.
- A role exists if and only if it has a row in the registry table below.
- Resolve the selected role to its `SKILLS.MD` entry point from this table.

## Registry contract (non-negotiable)

- This table is the only place roles are declared. No other file lists roles.
- `config/context_compass_config.yaml` holds **behaviour settings only**. It does
  not enumerate roles and is never consulted to discover or resolve a role.
- Adding a role is a two-step change: add one row here, and create the
  `SKILLS.MD` it points to. Nothing else needs editing.
- Role selection is **per agent, per session**. There is no stored or global
  active role. Multiple agents may hold different roles in the same repository
  at the same time, which is why no single value can represent "the" role.
- Work tracking is a separate project setting. The general role has shared
  baseline skills plus one backend baseline selected by `work_tracking.backend`
  in config; this does not create or select another role.

## Role registry

| role | skills path | extends | user-defined | selectable after onboarding | reads README |
| --- | --- | --- | --- | --- | --- |
| `new` | `agent_onboarding/default/new/SKILLS.MD` | - | no | no | yes |
| `general` | `agent_onboarding/default/general/SKILLS.MD` | - | no | yes | no |
| `engineer` | `agent_onboarding/default/engineer/SKILLS.MD` | `general` | no | yes | no |
| `design_engineer` | `agent_onboarding/default/design_engineer/SKILLS.MD` | `engineer` | no | yes | no |
| `platform_engineer` | `agent_onboarding/default/platform_engineer/SKILLS.MD` | `engineer` | no | yes | no |
| `qa_engineer` | `agent_onboarding/default/qa_engineer/SKILLS.MD` | `engineer` | no | yes | no |
| `security_engineer` | `agent_onboarding/default/security_engineer/SKILLS.MD` | `engineer` | no | yes | no |
| `story_designer` | `agent_onboarding/default/story_designer/SKILLS.MD` | `general` | no | yes | no |
| `story_novel_artist` | `agent_onboarding/default/story_novel_artist/SKILLS.MD` | `general` | no | yes | no |
| `researcher` | `agent_onboarding/default/researcher/SKILLS.MD` | `general` | no | yes | no |
| `draft_writer` | `agent_onboarding/default/draft_writer/SKILLS.MD` | `general` | no | yes | no |
| `developmental_editor` | `agent_onboarding/default/developmental_editor/SKILLS.MD` | `general` | no | yes | no |
| `line_copy_editor` | `agent_onboarding/default/line_copy_editor/SKILLS.MD` | `general` | no | yes | no |
| `continuity_fact_checker` | `agent_onboarding/default/continuity_fact_checker/SKILLS.MD` | `general` | no | yes | no |
| `proofreader` | `agent_onboarding/default/proofreader/SKILLS.MD` | `general` | no | yes | no |
| `synaptic_finishing_developer` | `agent_onboarding/user_defined/synaptic_finishing_developer/SKILLS.MD` | `engineer` | yes | yes | no |
| `synaptic_python_developer` | `agent_onboarding/user_defined/synaptic_python_developer/SKILLS.MD` | `engineer` | yes | yes | no |
| `data_engineer` | `agent_onboarding/user_defined/data_engineer/SKILLS.MD` | `engineer` | yes | yes | no |

Column meanings
- **extends**: the parent role whose `SKILLS.MD` chain is read first. Must match
  the `INHERITS_SKILLS_FROM` header inside the role's own `SKILLS.MD`.
- **user-defined**: lives under `agent_onboarding/user_defined/` rather than
  `agent_onboarding/default/`. Project- or team-specific overlays.
- **selectable after onboarding**: may be chosen as a steady-state role once
  first-time onboarding is complete. `new` is entry-only and is never a
  steady-state role.
- **reads README**: whether this role reads role README files during onboarding.
  Only `new` does; every other role uses policy and skills docs. README files are
  user-facing.

Unregistered overlays
- `agent_onboarding/user_defined/<name>/SKILLS.MD` is the path convention for a
  new user-defined role, but a role at that path is **not selectable until it has
  a row in the table above**. A directory on disk with no row is not a role.

## Role selection directive (non-negotiable)

Apply `context_compass/AGENTS.MD` / Project Instructions Bootstrap before these
role-selection defaults. Explicit project overrides apply to all affected steps,
not only the question to the user; they do not create unregistered roles.

1. During role selection, list the roles from the registry table.
2. Ask the user which role to take on, unless they already selected one,
   subject to any project role-prompt replacement resolved in the Project
   Instructions Bootstrap (`context_compass/AGENTS.MD`).
3. Resolve the selected role to its `SKILLS.MD` path from the table.
4. Read that `SKILLS.MD`, then walk `INHERITS_SKILLS_FROM` upward and read the
   whole chain **parent-first**.
5. Treat the resolved chain as the routing manifest:
   - You MUST read every path in every section a `SKILLS.MD` in the chain marks
     as **baseline**. Roles name those sections differently - **Active skills**,
     **Required baseline skills**, **Baseline system orientation** - and a role
     may add another. Match on the baseline label, never on a fixed list of
     headings; a section you fail to recognise is still mandatory.
   - `Local backend baseline` applies to `local`; `GitHub Codex plugin baseline`
     applies to `github_codex_plugin` in `work_tracking.backend`.
     A missing key means `local`; resolve legacy values through the shared
     `work_tracking_backend.md` skill. Read the selected backend's paths before
     certification; never apply the inactive backend's storage instructions.
   - **On-demand** skills are conditional. Do NOT read them for certification
     unless a trigger condition is met. When the trigger is met, those paths
     become mandatory and MUST be read before proceeding in that scope.
   - **Self-directed** skills are also outside certification, but they carry no
     trigger. Read them on your own initiative whenever the work needs them.
     Waiting for permission there is the failure the state exists to prevent.

## Format contract for role `SKILLS.MD` files

Every role `SKILLS.MD` uses one dialect so a single parser reads them all:

- Inheritance header: ``- `INHERITS_SKILLS_FROM: <path|none>` ``
- Skill entries: ``- `<path>` `` — one backticked path per list item.

**There is one entry form, not two.** Baseline and on-demand entries look
identical; the section heading a path sits under is what classifies it. Do not
prefix on-demand entries with `Read:` or any other marker — a second form means
a second parser, and the parser written for the first one silently returns an
empty on-demand readset instead of failing.

**There are three read states, not two, and the section a path sits under
declares which one applies.** Roles name their sections to suit what they hold, so
match on the STATE, never on a list of headings:

| state | required for certification? | when it is read |
| --- | --- | --- |
| **baseline** | yes | at onboarding, every time |
| **On-demand** | no | only when the section's stated trigger fires |
| **Self-directed** | no | at the agent's own initiative, no trigger, no permission |

Baseline sections are named for what they hold — `general` uses **Shared baseline skills**,
`engineer` uses both **Required baseline skills** and **Baseline system
orientation**. A role may introduce another; it is still baseline.

`general` also names backend-specific baseline sections. Their paths are
required only for the selected backend, after the config has been read. This is
a conditional baseline, not an On-demand skill and not a new role.

**On-demand and Self-directed are both outside certification, and they are not the
same thing.** On-demand is gated: the section states a trigger, and reading before
it fires teaches a procedure with nothing to apply it to — `general`'s
`llm_full_usage.md` is the model, useless on an install with no `llm_full.md`.
Self-directed is the opposite failure being guarded against: the document is
relevant *now*, you hold its index, and there is nothing to wait for. `engineer`'s
system-document reading is Self-directed for exactly that reason.

Collapsing the two is not cosmetic. It shipped: `engineer` labelled its
self-directed reads "On-demand" while `general` defined that label as trigger-gated
with false-attestation language, and an agent resolving both found no trigger had
fired, read zero system documents, and defended the choice with sound reasoning
from the document it was handed. Two definitions, one word, no override marker.

So: classify by state, leave the heading free, and never label a self-directed
section On-demand to mean "optional". Optional is not one of the three.

Bare (unbackticked) paths are not valid, and a backticked path must be a list
item. A path indented under a sentence is prose, not an entry, and a parser will
not see it. If a path must be read, it is a list item; if it is illustration,
name the file without making it look like an entry.

A parser written for this dialect must be able to read every role file in the
package. If it cannot, the role file is wrong, not the parser.

## Notes

- This file is a routing manifest, not a license to read the whole repo.
- Baseline and on-demand triggers are defined in the resolved role `SKILLS.MD`
  files and enforced by `AGENTS.MD` and
  `agent_onboarding/default/general/skills/compaction_requirements.md`.
- The roles are delta layers, not separate systems:
  - `general` is the shared baseline for all work.
  - `engineer` extends `general` for implementation-focused engineering.
  - `design_engineer`, `platform_engineer`, `qa_engineer`, and
    `security_engineer` extend `engineer` for specialized software workflows.
  - The fiction-authoring roles extend `general`.
  - The `user_defined` roles extend `engineer`.
