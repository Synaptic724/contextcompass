# Context Compass™

[![PyPI](https://img.shields.io/pypi/v/contextcompass.svg)](https://pypi.org/project/contextcompass/)
[![Python](https://img.shields.io/pypi/pyversions/contextcompass.svg)](https://pypi.org/project/contextcompass/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Synaptic724/context_compass?style=social)](https://github.com/Synaptic724/context_compass/stargazers)

**Working memory for coding agents, stored in your repo instead of a chat window.**

```bash
cd my-repo
uvx contextcompass init
```

That writes a `context_compass/` directory into your project. Point an agent at
`context_compass/AGENTS.MD` and its tickets, decisions, evidence and handoff state
live in files you own — surviving compaction, new chats, model swaps, and the next
agent.

> **⭐ If this is useful, please star the repo — it's how people find it.**

## Why It Exists

Agent work falls apart the second the chat stops being fresh. The context gets
long, compaction happens, the model forgets half the reasoning, another agent
takes over, or you switch from GPT to Claude to Gemini — and suddenly the work has
no memory of why it looks the way it looks.

The failures are boring and repetitive:

- the agent forgot what it was doing
- the next chat lost the reasoning
- the important decisions stayed in chat instead of in the project
- compaction wiped the context
- a new agent took over with no reliable handoff
- the platform kept the task state, but you wanted to keep the task state

Context Compass moves the working memory into the repo. Not a prompt pack, not a
documentation template — a persistence and control layer: an onboarding contract,
role maps with routed skill chains, ticket-first execution, durable notes and
evidence, artifact tracking, mailbox handoffs, and re-entry rules after
compaction.

The point is simple. Chat memory is weak, repository state is durable, and
process should be recoverable from files rather than vibes.

## Install

Three ways in. They produce the **same `context_compass/` directory** in your
repo — pick whichever fits how you work.

### 1. uvx — nothing installed, nothing cloned (recommended)

```bash
cd my-repo
uvx contextcompass init
```

`uvx` fetches the package into a throwaway environment, runs it, and discards it.
Nothing lands in your project's dependency tree, because a repo-scaffolding tool
has no business there.

Pin a published version for reproducibility, or track the latest. Replace
`X.Y.Z` with the release you want:

```bash
uvx contextcompass@X.Y.Z init      # exact, published release
uvx contextcompass@latest init     # whatever is newest
```

<details>
<summary>Don't have uv yet?</summary>

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
wget -qO- https://astral.sh/uv/install.sh | sh     # if you have no curl
```

```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

uv also installs Python itself, which is the other reason to have it:

```bash
uv python install 3.14        # or 3.12, 3.13 - whichever you want
uv python install 3.14t       # the `t` suffix is the free-threaded build
uv venv --python 3.14         # creates .venv using that interpreter
```
</details>

### 2. pip / pipx — if you would rather not use uv

```bash
pipx install contextcompass && contextcompass init    # isolated, preferred
pip install --user contextcompass && contextcompass init
```

### 3. Clone — no Python needed at all

The package is **Markdown**. If all you want is the system, copy the folder:

```bash
git clone https://github.com/Synaptic724/context_compass
cp -r context_compass/src/context_compass my-repo/
```

```powershell
# Windows
git clone https://github.com/Synaptic724/context_compass
Copy-Item -Recurse context_compass\src\context_compass my-repo\
```

Clone when you want to read the source first, work offline, vendor a specific
commit, or modify the package before adopting it.

### What actually needs Python

Only `tools/` — the scripts that build the manifest, index documents, generate the
source graph, and upgrade an install. **Python 3.10+, stdlib only, no dependencies
ever.** An agent that has to `pip install` before it can read a document is an
agent that cannot read the document on a fresh clone.

The release workflow runs the suite on Python 3.10 through 3.14 on Linux and
Windows. Verify an install any time:

```bash
python context_compass/tools/package_manifest.py --root context_compass --check
```

## Quickstart

1. Point your agent at `context_compass/AGENTS.MD` and ask it to onboard as an
   `engineer`.
2. Under the default onboarding flow, approve the certification step it asks
   for: `CERTIFY: APPROVED`.
3. Work normally. The agent routes through `attention_board.md` and the active
   ticket, and writes findings into ticket `## Notes`.
4. Commit `context_compass/`. It is your repository's memory now, and it is meant
   to be reviewed and diffed like any other source.
5. **After every compaction or handoff, the agent must re-onboard.** Add the
   recovery reminder to your tool's custom instructions as described below. If
   you skip that setup, remind the agent yourself.

### Set up recovery once

During onboarding, the agent checks whether your personal custom instructions
already include Context Compass. If they do, it keeps your existing setup. If
they do not, it offers a short setup form for Codex, Claude Code, or Gemini CLI.

You choose whether Context Compass should own all tickets, plans, and working
notes; whether agents can coordinate; when subagents may be created; and whether
those subagents should complete their own onboarding. The agent shows the exact
addition and asks before editing your personal instructions. You can also add
the text yourself or skip setup. Existing preferences stay in place.

The reminder sends the agent back to the repo's onboarding and recovery rules
after compaction. It lives in your tool's personal configuration, while your
project's work stays in Context Compass. Package installs and upgrades do not
edit those personal files automatically.

### Project-specific onboarding

If your project needs a different onboarding routine, put explicit instructions
in `context_compass/special_instructions/`. Agents read that folder before
applying onboarding or re-onboarding defaults, so you do not need to fork the
package's `AGENTS.MD` to change a particular requirement.

State which requirement changes, where the override applies, and what should
happen instead. Everything you do not override remains in force. Later role or
skill documents do not undo the override, and agents reload it after compaction.
Conflicting project instructions need clarification rather than a filename-based
winner. The shipped folder contains no active override; normal onboarding is
unchanged until you add one.

These are project-policy overrides, not changes to the agent platform's system
instructions or tool permissions.

### Follow the request count

Responses now carry a marker such as `prompt_id: compact_0_turn_3`. The turn
advances once for each user request, including follow-up messages. Several
progress updates and a final answer to that request all carry the same marker;
tool calls do not advance it.

After compaction, the next segment starts at `compact_1_turn_0`. Each agent
session keeps its own counter checkpoint in the mailbox, so it can recover the
count during re-onboarding. A missing checkpoint is reported as unknown instead
of being silently reset. The marker helps you follow continuity alongside the
agent's actual ticket notes and recovery work.

## Core Features

### 1) Compaction durability

Compaction is treated as a reliability event, not a convenience step. Action after
it is **blocked** until re-onboarding completes: the agent re-reads the policy
anchors, re-resolves its role chain, reopens the board and active tickets, and
posts a `REONBOARD: COMPLETE` attestation carrying read-integrity proof before it
may touch anything.

### 2) Certification gate

Under the default onboarding rules, before tools or edits the agent posts what it read and
what each document changes about its behavior, then waits for a message containing
`AGENT_NAME: <name>` and the exact token `CERTIFY: APPROVED`. Proof is a
comprehension claim, not a tool log — "I ran `cat`" is not evidence of reading.

### 3) Evidence and the Unknowns Gate

`UNKNOWN` is the default state for every claim. Promotion to `FACT` requires an
evidence pointer (`path:start_line-end_line`). Inferring behavior from a class
name, a folder layout, or what a framework usually does is explicitly rejected as
proof. Documents are evidence of *intent*; only source is evidence of *behavior*.

### 4) Ticket microcycle

A strict loop: investigate → document → plan → document → implement → document →
validate → document. No second investigation tranche before the current finding is
written down. Notes are not side output; they are the execution memory that makes
compaction survivable.

### 5) Three read states

Every section of a role's skill map is exactly one of these, and the section
heading declares which:

| state | required to certify? | when it is read |
| --- | --- | --- |
| **baseline** | yes | at onboarding, every time |
| **On-demand** | no | only when the section's stated trigger fires |
| **Self-directed** | no | at the agent's initiative — no trigger, no permission |

The third state exists because collapsing it into On-demand produces a specific
failure: an agent finds no trigger has fired, reads none of the system documents,
and reasons from class names instead — with sound-looking justification. Waiting
for permission to read is not caution.

### 6) The understanding hierarchy

Large system documents are entered through indexes and sliced, never read whole.
Each level hands you the key the next is looked up by:

```
  src_architecture.md        WHICH PART  - read whole, at onboarding
        v
  src_components_index.md    WHICH COMPONENT - look up that name
        v
  src_components.md (slice)  WHAT it owns, its Key Files
        v
  src_graph_index.md         WHICH NODES
        v
  src_graph.md (slice)       HOW it wires - ownership, lifecycle, callers
        v
  THE CODE                   the only authoritative account
```

Enter at the graph with no name in hand and you are searching tens of thousands of
lines for something you cannot describe. Descend it instead.

### 7) Role overlays and inheritance

Roles are delta layers, not separate systems. A role names its parent with
`INHERITS_SKILLS_FROM`, the chain is read parent-first, and a custom role extends
`engineer` or `general` without forking core behavior.

### 8) Mailbox handoffs

Not every handoff should be broadcast. `mailbox_board.md` carries point-to-point
messages between named agents — handoff, notice, question, ack — so directed
communication does not turn the routing board into noise.

## Roles

`SKILLS.MD` is the **single role registry**. A role exists if and only if it has a
row in that table; adding one is two steps — add the row, create the `SKILLS.MD`
it points to.

### Shared foundation

| role | extends | what it is |
| --- | --- | --- |
| `general` | — | process, ticketing, evidence discipline, compaction contract |
| `new` | — | first-time onboarding only; never a steady-state role |

### Software roles

| role | extends | choose it for |
| --- | --- | --- |
| `engineer` | `general` | most coding: debugging, refactors, repo changes |
| `design_engineer` | `engineer` | architecture plans, component boundaries, ADRs |
| `platform_engineer` | `engineer` | CI/CD, deployment, observability, production safety |
| `qa_engineer` | `engineer` | test strategy, quality gates, release signoff |
| `security_engineer` | `engineer` | threat modeling, security review, hardening |

### Fiction and editorial roles

| role | extends | choose it for |
| --- | --- | --- |
| `story_designer` | `general` | premise, arcs, chapter purpose, story bibles |
| `story_novel_artist` | `general` | style systems, scene art briefs, cover direction |
| `researcher` | `general` | source-backed constraints, confidence labels |
| `draft_writer` | `general` | chapter-complete prose under architecture constraints |
| `developmental_editor` | `general` | pacing, stakes, arc diagnosis, rewrite planning |
| `line_copy_editor` | `general` | clarity, style consistency, mechanical correctness |
| `continuity_fact_checker` | `general` | canon, timeline, contradiction detection |
| `proofreader` | `general` | final typo, punctuation and format lock |

### User-defined overlays

Live under `agent_onboarding/user_defined/` and are **never touched by an
upgrade**. The package ships three as working examples —
`synaptic_python_developer`, `synaptic_finishing_developer`, and `data_engineer`,
all extending `engineer`.

A directory there is not a role until it has a registry row. That is deliberate:
a folder on disk with no row is scaffolding, not a selectable role.

## How A Session Actually Runs

**Onboard.** The agent starts with `AGENTS.MD` and reads `special_instructions/`
before applying onboarding defaults. It then follows the effective requirements
for the execution contract, config, and `SKILLS.MD`. Normally it lists the roles
and asks which to take. It walks the chain
parent-first and reads every baseline section — for `engineer` that is its own
required skills, the parent's active skills, and the system-orientation set
(`src_architecture.md` plus the architecture and component indexes).

**Certify (default).** It posts what it read and what each document changes about its
behavior. You reply with `AGENT_NAME: helper_1` and `CERTIFY: APPROVED`.

**Route.** It opens `attention_board.md` and picks up the active row:

```
| work_item | status | mode | owner | agent_name | blocker | next | ... | ticket |
| parser_retry_fix | in_progress | implementation | claude | helper_1 | none |
  finish the backoff branch | ... | tickets/tasks/2026-08-01_parser_retry_task.md |
```

**Work the microcycle.** It opens the linked ticket, investigates until it has one
meaningful finding, and writes it to `## Notes` *before* continuing:

```
DATETIME: 2026-08-01T14:22:10Z
TYPE: FACT
CLAIM: retry backoff is computed but never applied on the 429 path
EVIDENCE: src/client/retry.py:88-104
IMPACT: every 429 retries immediately; the ceiling is never reached
NEXT: apply the computed delay before the recursive call
REREAD: REQUIRED
SCORE_0_TO_10: 8
```

**Close.** The ticket moves to `tickets/tasks/completed/`, the board row is
updated in the same pass, and an anchor row records where it went.

**Re-enter.** After compaction the next agent re-onboards, reopens the board and
that ticket, reads the notes, and continues — from evidence, not from memory.

## The Boards

Three default boards, each with one job. All carry `USER-DEFINED` regions that no
tool writes to in any mode, so your rows survive upgrades while the surrounding
structure improves.

**`attention_board.md`** — routing only. What is active, who owns it, what mode it
is in, what comes next, and which ticket holds the detail. Not for narrative, not
for analysis, not for artifact paths. Durable history belongs in ticket notes.

**`artifact_board.md`** — artifact associations by ticket, with disposition:
`delete_on_close`, `retain_as_reference`, or `promote_to_documentation`.

**`mailbox_board.md`** — point-to-point messages plus a checked-in roster, so
concurrent agents can see who is live and hand work to a named recipient.

**`issue_board.md`** — optional GitHub-mode responsibility map. It records which
Context Compass agent owns or reviews each Issue without copying Issue content.

## Repository Anatomy

```
context_compass/
  AGENTS.MD                     entrypoint - onboarding and execution policy
  SKILLS.MD                     the single role registry
  CONTEXT_COMPACTION.md         compaction and handoff contract
  config/                       behaviour settings (never a role list)
  attention_board.md            routing
  issue_board.md                optional GitHub-mode agent claims
  artifact_board.md             artifact lifecycle
  mailbox_board.md              agent-to-agent messages
  agent_onboarding/
    default/                    the shipped roles
    user_defined/               YOURS - never touched by upgrade
  tickets/epics|stories|tasks/  work, each with backlog/ and completed/
  templates/                    ticket and workflow templates
  artifacts/                    ticket-linked supporting files
  context_management/           optional reusable reread packs
  system_docs/                  SHIPS EMPTY - your architecture maps
  special_instructions/         project-specific rules
  user_defined/                 free space, never written to
  examples/                     the quality bar - read these, don't edit them
  tools/                        stdlib-only Python
```

Five directories are yours outright and an upgrade never touches them:
`system_docs/`, `tickets/`, `artifacts/`, `special_instructions/`, and both
`user_defined/` trees.

`system_docs/` ships empty on purpose. A seeded placeholder in a live lane gets
read as repository truth no matter what banner sits on it, so the package does not
put one there. Build the maps when your repo has real structure to describe;
`system_docs/system_docs_read_first.md` explains the order.

## Configuration

`config/context_compass_config.yaml` holds **behaviour settings only**. It never
enumerates roles and is never consulted to resolve one — that is `SKILLS.MD`'s job
alone. Notable keys:

| key | effect |
| --- | --- |
| `system_of_record.enforce` | when `true`, agents may not use harness task lists, plans or session memory to track work. This package is the only tracking surface. |
| `work_tracking.backend` | `local` reads ticket folders; `github_codex_plugin` uses the connected GitHub plugin's Issues |
| `workflow.ticket_microcycle.*` | strict or relaxed loop, note score floor, expansion gate |
| `workflow.note_behavior.*` | append-only notes, required evidence ranges, per-ticket focus |
| `artifacts.*` | store root, disposition defaults, ticket-link requirements |
| `reading.read_loc_max` | chunk size for manual reads of large documents |

Config is merged key by key on upgrade. New keys arrive with their comments; a
value you set is never reset.

### Optional GitHub Mode

Choose where your agent reads and updates tickets in YAML:

```yaml
work_tracking:
  backend: local
```

`local` is the default and uses the existing epic, story, and task folders. To
use Issues through the connected GitHub plugin, choose:

```yaml
work_tracking:
  backend: github_codex_plugin
  github_codex_plugin:
    connection_nickname: "Work account"
    issues_repository: YOUR_OWNER/YOUR_REPO
    project_url: "" # optional
```

Connect the GitHub plugin with access to that repository. Each Issue keeps the
matching Epic/Story/Task template, including Status and Notes in its body.
Agents read the selected backend's skills during onboarding and recovery.
Agent claims, active focus, mailbox, artifacts, special instructions, and system
docs stay in your repo. This mode uses plugin authentication and does not require
CLI setup or a token in YAML.

Give your connected GitHub account a nickname in Codex, such as `Work account`,
and copy that exact nickname into YAML. It tells the agent which connection to
use, independently of the target repository owner. The agent verifies the
selected profile and stops if the nickname is missing or ambiguous; it does
not fall back to another account. Connection IDs and credentials stay out of
the config. Existing plugin configs must add this setting explicitly.

The YAML choices, plugin capabilities, and existing-config migration are in
[the GitHub setup guide](src/context_compass/agent_onboarding/default/general/skills/github/README.md).
Existing file tickets are not published or migrated just because you enable the
mode; review their content and destination first.

## Upgrading An Existing Install

```bash
uvx contextcompass@latest upgrade --check     # exactly what would change
uvx contextcompass@latest upgrade --apply     # do it
```

Every tool refuses to act without `--apply` and prints a full plan under `--check`.
**Read the plan.**

### How it decides what is safe to replace

One hash tells you a file changed. It cannot tell you *who* changed it, which is
the only question that matters. So three are compared — what shipped, what is on
disk, and what is incoming:

| on disk | incoming | what happens |
| --- | --- | --- |
| unchanged | changed | **replace** — clean update |
| unchanged | unchanged | skip |
| **you edited it** | unchanged | **keep yours** — nothing to conform to |
| **you edited it** | changed | **conform**, and say so by name |

### Boards keep your rows

Everything inside a `USER-DEFINED` region is yours; everything outside is package
structure that gets conformed, so a board's shape can improve over time.

Boards created before those regions existed hold their rows in open text, where
nothing distinguishes them from stale package headings. The updater refuses to
conform such a board and names the fix:

```bash
uvx contextcompass@latest migrate-boards --check --diff
uvx contextcompass@latest migrate-boards --apply
```

Anything with no matching region is parked under `## Notes` rather than dropped.
Migrating three real boards carrying 277 lines of live agent state moved every line
and lost **zero**, verified line-by-line against a pre-migration snapshot.

### The tools

All under `context_compass/tools/`, all stdlib-only, all `--check` before `--apply`.

| tool | what it does |
| --- | --- |
| `package_manifest.py` | what ships, who owns it, its hash. Everything else reads this. |
| `update_context_compass.py` | upgrade an install to a newer package |
| `migrate_boards.py` | one-time board migration into `USER-DEFINED` regions |
| `cleanup_context_compass.py` | repair a broken install, or reset lanes for a release |
| `build_llm_full.py` | concatenate the package into one file, plus a line-range index |
| `system_documents/index_document.py` | line-range index over an authored document |
| `system_documents/python/extract_graph.py` | derive the source graph from code |
| `system_documents/python/assemble_graph.py` | render the graph and its index |
| `system_documents/python/graph_walker.py` | state of the graph's authored tier |
| `system_documents/python/graph_semantics_tickets.py` | turn unauthored areas into tickets |
| `system_documents/python/migrate_authored_graph.py` | carry a graph out of the retired JSON format |

## Feed The Whole System To A Model

Sometimes you want a model to see everything at once — reviewing a change to the
onboarding contract, working out why two policies disagree, handing the system to
something that cannot browse a filesystem.

```bash
python context_compass/tools/build_llm_full.py \
    --root context_compass --out llm_full.md --slice context_compass/AGENTS.MD
```

That writes `llm_full.md` (every file concatenated, ~30,000 lines) and
`llm_full_index.md` (483 lines saying which lines each file occupies).

**Read the index, slice what you need, never load the document whole.** The index
carries `line_count` and `content_sha256`, and `--slice` recomputes both before
returning anything, so a hand-edited document makes the next slice refuse rather
than confidently hand back the wrong file.

## Design Notes

The package installs into repositories that agents actively write to, so the
tooling is built around not destroying that work.

- **Ownership classes.** Every shipped file is PACKAGE, RESET, INSTANCE, LIVE or
  CONFIG, recorded with its hash in a generated `MANIFEST.md` — derived from the
  files themselves, so it cannot drift the way a hand-bumped stamp does.
- **Nothing deletes authored work automatically.** Every tool that can remove
  something refuses without `--apply`, and the one that deletes authored prose
  refuses without a terminal to ask at.
- **Line-range indexes carry staleness proofs**, and every consumer refuses on
  mismatch rather than returning confidently wrong content.
- **Regression tests, plus mutation testing.** A green suite is equally consistent with
  "the code is correct" and "the tests assert nothing", so
  `tests/mutation_check.py` applies 49 deliberate defects and requires at least
  one test to fail for each. Several survived their first run; each named a real
  gap.

Local setup, test commands, and mutation checks are covered in the
[contributor testing guide](contributor/testing.md).

### The source graph is honest about what it cannot know

Context Compass can derive a **source graph** from your code — one node per class
and module, with the relationships between them. Half of it derives cleanly. The
other half cannot:

```python
self._pool = pool   # borrows
self._pool = pool   # uses
self._pool = pool   # owns_lifecycle_of
```

Three different relationships, identical syntax. That difference is design intent
appearing nowhere in the source text — measured against a hand-authored graph,
**68% of all edges**. So the graph has an authored tier, and nodes without one are
marked `UNSEMANTIC` rather than guessed at.

Authored prose is also the tier that rots: the mechanical half self-heals on
re-extraction, while prose stays exactly as written while the code moves under it.
A read-only walker reports each node as `UNSEMANTIC`, `AUTHORED`,
`SEMANTICS_STALE`, or `RETIRED` — tracked per node, because a file-level hash
would mark all forty classes in a module stale because one changed, and a census
that cries wolf gets ignored.

## Common Failure Modes This Prevents

- "The agent started coding before onboarding."
- "It claimed it read the docs but could not say what changed about its behavior."
- "Critical decisions vanished after compaction."
- "The new chat had no reliable re-entry path."
- "Two agents did the same work because neither could see the other's state."
- "Role responsibilities blurred and the quality gates quietly disappeared."

## Practical Adoption

1. Start with `general` + `engineer`.
2. Enforce board and ticket routing first.
3. Then evidence and unknowns discipline.
4. Then certification and compaction re-entry gates.
5. Add specialized roles as the workflow matures.
6. Add user-defined overlays once baseline behavior is stable.

This sequence keeps adoption fast without weakening the core controls.

## Final Word

You own the state. You can review it, diff it, commit it, hand it to another
agent, and come back in three months and still know what happened.

If you want project memory that stays with the repo, survives branch work, handles
handoffs, resists drift, and still makes sense when another agent shows up later —
that is exactly what this system is for.

## Contributing

If you are changing Context Compass itself, start with the
[contributor guide](contributor/README.md). It covers repository maintenance,
preserving user content, testing, generated files, version bumps, and releases.

## License and Trademarks

The software is licensed under **Apache License 2.0** — see [LICENSE](LICENSE).
Copyright 2026 Mark Thomas Geleta.

**Context Compass™** is a trademark of Mark Thomas Geleta. The Apache 2.0 licence
covers the code and documentation; **Section 6 of that licence expressly does not
grant trademark rights**. You are free to use, fork and redistribute the software
under Apache 2.0, including describing your work as based on Context Compass™ —
what the licence does not give you is permission to use the name or logo to brand
your own product, or in any way suggesting endorsement or official status.

The distribution name `contextcompass` and the command `contextcompass` are
technical identifiers, not the mark. Full statement: [NOTICE](NOTICE).
