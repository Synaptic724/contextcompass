

# SKILLS.MD - engineer

Purpose
- Define required baseline engineering skills for the `engineer` role.

Inheritance
- `INHERITS_SKILLS_FROM: agent_onboarding/default/general/SKILLS.MD`

Skill classes (non-negotiable)
- This role defines three classes of skills:
  A) **Required baseline skills** (always required for onboarding/certification)
  B) **Baseline system orientation** (required at onboarding when the files exist)
  C) **Self-directed system reading** - every other system document. Not baseline,
     not trigger-gated: **agent-driven OR user-driven**, and agent-driven is the
     ordinary case.

Why this is called Self-directed and not On-demand (read this before you interpret it)
- **`On-demand` is a different state and it is reserved.** In this package On-demand
  means a section states a trigger and you wait for it - `general`'s
  `llm_full_usage.md` is the model. **Nothing in class C has a trigger.** The label
  was wrong here, it collided with the parent's definition, and an agent resolving
  both correctly concluded no trigger had fired and read zero system documents. Full
  reasoning: `context_compass/SKILLS.MD`, "Format contract for role `SKILLS.MD` files".
- Self-directed does NOT mean "wait to be told". It means the read happens when somebody
  needs it, and **you are somebody**. You raise the demand as often as the user does,
  and more often in practice, because you are the one who notices the gap.
- There is no permission step. There is no trigger list you must match first. If you
  need to know something about this system, the document is right there and you go
  and read the part that answers it.
- The earlier version of this file put these documents behind a trigger list and, for
  one of them, an explicit instruction to ask the user whether reading was required.
  That produced exactly what you would expect: agents that onboarded knowing nothing
  about the system, stopped mid-task to request authorisation to consult the
  documentation they were already holding the index for, and reasoned from the names
  of classes in the meantime. Asking permission to read is not caution. It is a
  refusal to do the work, dressed as deference.

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
- `agent_onboarding/default/engineer/skills/system_orientation.md`
- `agent_onboarding/default/engineer/skills/documentation_standards.md`
- `agent_onboarding/default/engineer/skills/context_protocol.md`
- `agent_onboarding/default/engineer/skills/src_graph_usage.md`
- `agent_onboarding/default/engineer/skills/src_graph_generation.md`
- `agent_onboarding/default/engineer/skills/system_document_build.md`
- `agent_onboarding/default/engineer/skills/patch_framework_gating.md`
- `agent_onboarding/default/engineer/skills/patch_artifact_consumption.md`
- `agent_onboarding/default/engineer/skills/staleness_protocol.md`
- `agent_onboarding/default/engineer/policies/engineer_quality_policy.md`
- `agent_onboarding/default/engineer/policies/ctx_autonomy_policy.md`
- `agent_onboarding/default/engineer/policies/ctx_autonomy_rubric.md`
- `agent_onboarding/default/engineer/behavioral_guidelines/engineer_workflow.md`
- `agent_onboarding/default/engineer/behavioral_guidelines/task_execution_and_validation.md`
- `agent_onboarding/default/engineer/examples/artifact_workflow.md`
- `agent_onboarding/default/engineer/examples/eng_task_flow.md`

Baseline system orientation (read every one that exists)
- `system_docs/system_docs_read_first.md`
- `system_docs/src_architecture.md`
- `system_docs/src_architecture_index.md`
- `system_docs/src_components_index.md`

Why these four and not the whole set. An engineer who does not know the shape of the
system writes plausible code in the wrong place, and no amount of role skill fixes
that. So the narrative is baseline: `src_architecture.md` is the one document that
explains what this system IS. Read it.

The two INDEXES are baseline because an index is a map, not a territory. They are
what let you name a component and go straight to its section instead of hunting for
it. You onboard holding the maps, then use them to reach the parts of the territory
your work actually needs - and then the code.

Nothing else is baseline. Everything else under `system_docs/` is Self-directed,
which means yours to reach for without waiting for anything. See below.

The reading order
This is a PRIORITY ORDER, not a rationing scheme. It tells you what to read first so
that what you read next is the right thing. It is not an argument for reading less.

1. **`src_architecture.md`** - read it. This is what the system IS.
2. **`src_components.md`** - before starting work on a topic, read the parts relevant
   to that topic. Use the index to find them.
3. **`src_graph.md`** - if you are going to write code, read the wiring for what you
   are touching. Use the index to find it.
4. **THE CODE** - if you are changing anything, read the code. Always. No exception.

Steps 1-3 tell you WHICH code. Step 4 tells you what it actually does. Every document
above step 4 can be out of date; the code cannot. When they disagree, the code is
right and the document is stale - record that, it is a finding.

**`grep` and AST are guesses.** They tell you a name occurs somewhere. They do not
tell you what the function does, what it owns, what it locks, what it returns, or
what happens when it fails. Use them to find where to start reading. Then read, and
trace the call path. A claim you cannot support from source you have actually read is
UNKNOWN, however many matches you counted.

**You have capacity - spend it here.** Source files are small next to the documents;
a class is a few hundred lines and you can read the whole thing. Budget discipline
exists so that you arrive at the code with room to read it properly, not so that you
skip it.

Each level hands you the key the next one is looked up by:

```
  src_architecture.md          WHICH PART of the system - read whole, at onboarding
        |  gives you a concern, a boundary, a subsystem name
        v
  src_components_index.md      WHICH COMPONENT - look up that name
        |  gives you a section name and a line range
        v
  src_components.md  (slice)   WHAT it is, owns, guarantees, and its Key Files
        |  gives you node names and file paths
        v
  src_graph_index.md           WHICH NODES - look up those names
        |  gives you a section name and a line range
        v
  src_graph.md  (slice)        HOW it wires - edges, ownership, lifecycle, callers
        |  gives you the files that actually matter
        v
  THE CODE                     the only thing that is authoritative
```

Descend it. Do not enter in the middle.

Each step is a **lookup, not a search**, and that is why the order matters. The
architecture names a subsystem; you look that name up in the components index instead
of scanning for it. A component names its files and nodes; you look those up in the
graph index instead of scanning for them. Entering at the graph with no name in hand
means hunting for something you cannot yet describe - the order exists to stop that,
not to stop you reading.

At each level you carry down only the branch you are on: one subsystem, one or two
components, the nodes they name. That is what makes step 4 affordable.

**The documents are guiding tools. The code is the system.**
When you are making a code change, you read the code. The order above exists to tell
you *which* code - to turn "somewhere in this repository" into a few files worth
opening. It does not tell you what those files do today. Documents describe intent at
the moment somebody wrote them down; the code is what runs.

So never let a slice stand in for reading the implementation you are about to change,
and never quote a document as evidence for behaviour you have not seen in source. The
right shape is: **use the documents to find the code, read the code, then change it** -
and if what you found contradicts the document that sent you there, that contradiction
is a finding worth recording.

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

If you are cleaning or upgrading an install:
- `agent_onboarding/default/engineer/skills/package_maintenance.md`

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
