

# SKILLS.MD - engineer

Purpose
- Define the eager and lazy readsets for the `engineer` role.

Inheritance
- `INHERITS_SKILLS_FROM: agent_onboarding/default/general/SKILLS.MD`

Skill classes (non-negotiable)
- This role defines four classes of skills:
  A) **Required baseline skills** (eager: always required for onboarding/certification)
  B) **Baseline system orientation** (eager: required at onboarding when the files exist)
  C) **Self-directed system reading** - every other system document. Not baseline,
     not trigger-gated: **agent-driven OR user-driven**, and agent-driven is the
     ordinary case.
  D) **On-demand skills (lazy readset index)** - the system-document guides, patch
     gates and maintenance procedures, each read in full when its trigger fires.
     The index is at the end of this file.

Why Self-directed is not On-demand
- On-demand entries wait for a trigger; class C has none. Self-directed means the
  read happens when somebody needs it, and **you are somebody**: raise the demand
  yourself, with no permission step and no trigger list to match first. Labelling
  these reads On-demand once produced agents that read no system documents at all.
  Full reasoning: `context_compass/SKILLS.MD`, "Format contract for role `SKILLS.MD` files".

Rules
- Inherited `general` reads include shared baseline skills and only the
  backend baseline selected by YAML; inactive backend paths are not required.
- You MUST read **all** paths listed under **Required baseline skills** for this role
  to be considered onboarded/certifiable as `engineer`.
- You MUST read every file under **Baseline system orientation** that exists in this
  repository. A missing one is skipped, not blocked on - a fresh install has none.
- Everything else under `system_docs/` is **Self-directed** in the sense defined
  above: yours to reach for, unprompted, whenever the work needs it. It is not
  baseline and it is not trigger-gated.
- You MUST NOT claim you read a document you only sliced. Say which sections.
- Large documents are read **by slice through their index**, never whole. That is a
  rule about HOW, not WHETHER.
- **Slice the DOCUMENTS to the topic; read the CODE whole.** These two rules point in
  opposite directions on purpose. Documents grow with the repository and are entered
  through their indexes. A source file is a few hundred lines - open it and read it.
  - This rule is about the large system documents ONLY. It has never applied to
    source, and reading it that way is how an agent ends up describing code from
    `grep` output. If you are about to change an implementation, you read that
    implementation in full.
- Ask the user for **guidance** when you cannot tell where to look - which subsystem,
  which component, which of four similar names. Do not ask for **permission** to look.
  Guidance is a real question; permission is a stall.
- **Descend the hierarchy; do not enter in the middle.** architecture -> components
  index -> component slice -> graph index -> graph slice -> the code. Each level
  hands you the name the next one is keyed on. See the section below.
- **These documents guide you to the code. They are not the code.** Before changing
  an implementation you read that implementation. Where a document and the source
  disagree, the source is what runs.
- **A search is not a read, and a document is not the source.** `grep`/`rg` narrows
  the shortlist; it never closes a behaviour question. Citing a doc section, or a
  single line where a symbol matched, is not evidence that code does what you say.
  Full rule: `agent_onboarding/default/general/skills/unknowns_gate_reference.md`.

Required baseline skills
- `agent_onboarding/default/engineer/AGENTS.MD`
- `agent_onboarding/default/engineer/WORKFLOWS.MD`
- `agent_onboarding/default/engineer/skills/engineer_execution.md`
- `agent_onboarding/default/engineer/skills/technical_expertise.md`
- `agent_onboarding/default/engineer/skills/documentation_standards.md`
- `agent_onboarding/default/engineer/skills/staleness_protocol.md`
- `agent_onboarding/default/engineer/policies/engineer_quality_policy.md`
- `agent_onboarding/default/engineer/behavioral_guidelines/engineer_workflow.md`
- `agent_onboarding/default/engineer/behavioral_guidelines/task_execution_and_validation.md`
- `agent_onboarding/default/engineer/examples/eng_task_flow.md`

Baseline system orientation (read every one that exists)
- `system_docs/system_docs_read_first.md`
- `system_docs/src_architecture.md`
- `system_docs/src_architecture_index.md`
- `system_docs/src_components_index.md`

Why these four: `src_architecture.md` is the one document that explains what this
system IS, and the two indexes are the maps that take you straight to a component's
section and its nodes. Everything else under `system_docs/` is Self-directed (below).

The reading order
Read `src_architecture.md` at onboarding. Before work on a topic, slice the relevant
`src_components.md` sections through its index; before writing code, slice the
`src_graph.md` wiring for what you touch; then read that code in full. Each level
hands you the name the next is looked up by - descend it, do not enter in the middle.
The documents tell you WHICH code; only the code tells you what it does. Where they
disagree, the code is right and the document is stale - record that as a finding.
`grep` and AST find names, not behaviour. The full protocol is `context_protocol.md`
in the lazy index below.

Self-directed system reading - agent-driven or user-driven
Every system document that is not one of the four above, including any this role
does not name:
- `system_docs/src_components.md` - via `src_components_index.md`, sliced
- `system_docs/src_graph.md` - via `src_graph_index.md`, sliced
- `system_docs/tests_architecture.md`
- `system_docs/tests_components.md`
- anything else present in `system_docs/`

None of these ship with the package, so a fresh install has nothing here to read.
That is expected and is not a blocked onboarding.

**Either party can raise the demand, and usually it is you.** You do not ask whether
you are allowed, you do not wait for a ticket to authorise it, and you do not treat
the user's silence as a reason not to look. You hold the indexes from onboarding;
that is what they are for.

**Read what you need. Not everything.**
This is the other half of the rule and it matters just as much. These documents scale
with the repository, and on a large one they are enormous - a component map runs to
tens of thousands of lines and a graph larger still. "Self-directed" is permission to
be surgical, never a licence to pull the whole set into context. An agent that reads
everything has not been thorough; it has spent its context before starting, and it
will be vague about all of it instead of precise about the part that mattered.

So: name the question first, find the section in the index, slice that section, stop.
One component, one call path, one edge - then go back for the next one if the work
actually needs it. Two targeted slices beat a whole document every time.

**Ask for guidance, not for permission.** The two are different requests and only one
of them is an imposition:
- "May I read `src_components.md`?" - do not ask this. Read it.
- "This repository has 140 components. I need the ones handling retry and backoff -
  is that `scheduler`, or somewhere else?" - ask this, early and without
  embarrassment. The user knows their system's vocabulary and can point you at the
  right five sections in one line, which is cheaper for both of you than you reading
  eighty to find them.

Ask when the scope is genuinely unclear: the repository is large and you cannot tell
which subsystem owns the behaviour, several components have plausible-sounding names,
or the task description does not map onto anything you can see in the index. Say what
you are looking for and what you already ruled out. That is a real question with a
real answer, and it is nothing like asking whether you are permitted to look.

Go and read when any of this is true, which is most of the time:
- you are about to describe what a component does, owns, or is responsible for
- you are about to assume a relationship - who constructs what, who owns a
  lifecycle, what a call path actually is
- you are about to touch a file and do not already know what depends on it
- a name looks self-explanatory. `EngineManager` tells you nothing; the descriptor
  for it tells you whether it owns its stages or borrows them, and those are
  different bugs
- you are about to write "presumably", "likely", or "appears to" about this codebase
- you are about to say a document was not required, when reading it would have
  taken one slice

And the mirror of that list - do NOT read when:
- you already know the answer from a slice you took earlier this session
- the section is adjacent to what you need but not what you need
- you are reading "to be thorough" with no question in hand. Thoroughness is
  answering the right question completely, not loading the most text

The user drives it too, and their demand is not narrower than yours: an explicit
request for a deep dive, a ticket that needs architecture work, a task touching
`system_docs/`, a cross-cutting change, an install clean or upgrade. These are
examples of demand, not a gate on it. A condition list that fails to fire is not
permission to work uninformed.

**Slice these two through their indexes**, always - `src_components.md` and
`src_graph.md` are the large ones. The tests pair is small enough to read directly.
None of this applies to source: read the code you are changing, in full. Verify an index before trusting a range - an
index that lags its document still returns line numbers, they are simply the wrong
ones. See `agent_onboarding/default/engineer/skills/src_graph_usage.md`.

Read the tests pair when the work concerns the suite. Do not skip it because nobody
asked, and do not drag it in because you happened to be reading the src pair - they
describe different things.

Note on a fresh install
- **`system_docs/` ships empty.** The package does not seed architecture,
  component, test or graph documents, because a shipped placeholder in a live
  lane gets read as repository truth no matter what banner sits on top of it.
- `examples/` is where the shape and quality bar live. Read the examples to learn
  the format; write `system_docs/` from your own repository.
- An empty `system_docs/` is the expected state of a new install, not a defect,
  and not something to fill with invented content.
- `system_docs/system_docs_read_first.md` is the entry point and explains the
  order to build these in when the repository is ready.

Note on the source graph
- `system_docs/src_graph.md` and `system_docs/src_graph_index.md` are generated
  per project by `tools/system_documents/python/` and are NOT shipped with this
  package. A fresh install has neither.
- If they are absent, that is expected. Do not treat their absence as a blocked
  onboarding or a missing required read.
- NEVER read `src_graph.md` in full. Read `src_graph_index.md`, verify it, and
  slice only the sections you need. See
  `agent_onboarding/default/engineer/skills/src_graph_usage.md`.
- "Never read it in full" is a rule about HOW, not WHETHER, and it applies to this
  DOCUMENT - not to the code it describes. Slice it freely and often; that is what it
  is for. Reading none of it is not the safe reading of this rule, it is the failure
  the rule was written to prevent.

On-demand skills (lazy readset index)
These files are not in the eager readset. Once a trigger fires, the file is mandatory:
read the whole file before proceeding in that scope. `design_engineer` adds its own
triggers for the system-document entries below.

- `agent_onboarding/default/engineer/skills/context_protocol.md`
  - Covers: navigating the system documents to the code worth opening.
  - Trigger: before you read or slice `src_architecture.md`, `src_components.md`,
    `src_graph.md` or their indexes. At onboarding this fires whenever
    `system_docs/src_architecture.md` exists.
- `agent_onboarding/default/engineer/skills/src_graph_usage.md`
  - Covers: reading the generated source graph through its index.
  - Trigger: before you read `src_graph_index.md` or slice `src_graph.md`.
- `agent_onboarding/default/engineer/skills/system_document_build.md`
  - Covers: the authoring format for `src_architecture.md` and `src_components.md`,
    and how their indexes are built.
  - Trigger: you are asked to create or update those documents or their indexes,
    or your change requires updating them.
- `agent_onboarding/default/engineer/skills/src_graph_generation.md`
  - Covers: building and maintaining the generated source graph with the
    extraction tools.
  - Trigger: you are asked to generate, regenerate or refresh the source graph, or
    your change requires refreshing it.
- `agent_onboarding/default/engineer/policies/ctx_autonomy_rubric.md`
  - Covers: ranking context quality across file, directory, component and
    architecture layers.
  - Trigger: you create or refresh any layer of system context.
- `agent_onboarding/default/engineer/policies/ctx_autonomy_policy.md`
  - Covers: applying that ranking to engineer context work.
  - Trigger: the same as `ctx_autonomy_rubric.md`.
- `agent_onboarding/default/engineer/skills/patch_framework_gating.md`
  - Covers: the patch gates for system-impacting changes.
  - Trigger: the task changes architecture or component boundaries, lifecycle
    behavior, policy or gating behavior, or cross-component contracts, or it
    requires updating `src_architecture.md`, `src_components.md` or `src_graph.md`.
- `agent_onboarding/default/engineer/skills/patch_artifact_consumption.md`
  - Covers: consuming architecture, component and code-description patches during
    implementation.
  - Trigger: `patch_framework_gating.md` applies to the task, or the task points at
    a patch under `system_docs/patches/active/`.
- `agent_onboarding/default/engineer/skills/testing_discipline.md`
  - Covers: test-value ranking, unit-first rules, when integration tests are required,
    the coverage policy, and fixing base code found while testing.
  - Trigger: before you write, change or review tests, or report test or coverage
    results.
- `agent_onboarding/default/engineer/skills/system_orientation.md`
  - Covers: explaining this repository's workflow and documents to the user.
  - Trigger: the user asks how the system works or how to interact with it, or
    wants a walkthrough before work begins.
- `agent_onboarding/default/engineer/examples/artifact_workflow.md`
  - Covers: a worked example of scratch capture and an artifact moving through a
    ticket.
  - Trigger: before you create or link an artifact for the first time in a session.
- `agent_onboarding/default/engineer/skills/package_maintenance.md`
  - Covers: cleaning an install back to shipping state, upgrading one, and
    preparing the package for distribution.
  - Trigger: you are preparing the package for distribution, one project's content
    has ended up inside another install, or a newer Context Compass version needs
    rolling into a repository.
