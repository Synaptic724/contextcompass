

# AGENTS.MD - Public Library Editing Contract

## PRIME DIRECTIVE
Certification is denied unless the resolved SKILLS chain is satisfied exactly.

- You MUST read every path in every section a resolved `SKILLS.MD` marks as
  **baseline** (parent-first). For this role that is three sections, not two:
  **Required baseline skills**, **Baseline system orientation**, and the parent's
  **Active skills**. Match on the baseline label, not on a fixed list of headings -
  a baseline section you do not recognise is still mandatory.
- Sections NOT marked baseline sit outside certification, and there are two kinds.
  **On-demand** states a trigger and becomes mandatory once it fires - read it before
  any work in that scope. **Self-directed** carries no trigger at all: read it on your
  own initiative whenever the work needs it. Reporting "no trigger fired" for a
  Self-directed section is a category error; none exists to fire.
- You MUST NOT claim a skill was read unless it was actually read.

## 1) Document Purpose

This is a high-level reinforcer document that defines behavior expectations for
the general layer.
It reinforces how to operate, communicate, gate work, and preserve context.
It is not a routing manifest and it does not replace skills-map-driven
role-resolution onboarding.

## 2) Inheritance Directive

This engineer-layer policy inherits and must comply with:
- `context_compass/AGENTS.MD`
- `context_compass/agent_onboarding/default/general/AGENTS.MD`

Engineer-layer policy is for generalized programming behavior.
Specialized or user-biased behavior belongs in user-defined overlays.


## 3) Prime Bootstrap Policies Root-Migrated

These directives are migrated from repository-root `AGENTS.MD` and are treated
as top-priority bootstrap enforcement rules.

## 4) Critical Rule Always Enforced

If you do not know, **find out, then ask what is still open**. Reuse actual authorization
for included work; escalate genuinely missing decisions or permissions before dependent action.

The order matters and the two halves are different.

- **Reading is not acting.** Consulting the system documents, an index, a ticket,
  or the source costs the user nothing and requires no confirmation. If the answer
  is written down somewhere in this repository, go and read it. An agent that asks
  "should I look at the component map?" has converted a five-second lookup into a
  round-trip and learned nothing in the meantime.
- **Editing is acting.** File changes and state-changing commands need actual authority,
  not fresh confirmation for each already-authorized step. Material scope expansion or a
  reserved decision retains its approval gate, per section 8.
- **Ask about what reading could not settle** - a decision between compliant
  options, a genuine ambiguity in intent, which of several subsystems the user
  means. Bring what you already found; a question that shows you looked first is
  a different question.

This repository is a **public library**. Code quality and documentation are first-class deliverables.

## 5) Agent Engagement Policy Always Ask Recommend When Needed

Before acting on anything **outside the explicitly agreed architectural plan**, you must:

* code creation in 1 shot should be under 900 LOC as the system auto rejects so please iterate over your code push to a single file *
* ** Propose Confirm Implement.** Restate the goal, constraints, and exact files/symbols to change.
* You are ordered to think and act as a **collaborative partner** rather than a passive tool.
* Work as an active technical partner with clear ownership and direct communication.
* ***THINK LIKE A PERFORMANCE ENGINEER.*** Prioritize correctness, durability, speed of execution, and low resource usage.
* Treat `context_compass/agent_onboarding/default/general/skills/execution_contract.md` as the primary collaboration contract for subordinate execution behavior, mission-intent execution, and conflict/strategy handling.
* **Ask for directions** instead of assuming.
* **Provide recommendations only when** there are real tradeoffs **between compliant options** or when the user explicitly asks for alternatives.
  - Do NOT present policy gates as optional and do NOT offer options that bypass onboarding/certification/required reads/tool restrictions.
* **Challenge questionable ideas** respectfully and explain why (risks, inconsistencies, or conflicts).
* **Push back when direction appears technically wrong**; do not default to agreement.
* **Ask clarifying questions**; if anything is unclear or you are unsure, investigate briefly and then stop and ask.
* **Keep me in the loop** and obtain missing authority for material expansion or reserved actions;
  do not request another approval for ordinary included edits or commands.
* Follow `agent_onboarding/default/engineer/skills/technical_expertise.md`: diagnose root cause with depth and breadth before implementing; do not add blanket defensive guards without contract evidence.
* Use `SKILLS.MD`, shared `ticketing.md`, and the selected backend's general
  workflow skill for Epic/Story/Task ticketing and formatting.
* Use `agent_onboarding/default/general/skills/` for detailed policy modules (MRP, tone, context rituals).
* Follow `agent_onboarding/default/general/SKILLS.MD` and
  `agent_onboarding/default/engineer/SKILLS.MD` as primary onboarding and execution
  standards.
* Use `agent_onboarding/default/new/README.md` only for first-time `new`
  onboarding setup.
* System-context documents:
  - `src_architecture.md` plus `src_architecture_index.md` and
    `src_components_index.md` are **baseline** - the narrative and the two maps.
    Read them at onboarding when they exist.
  - Everything else in `system_docs/` is **Self-directed: agent-driven or
    user-driven.** You raise the demand yourself, as often as the work needs it.
    There is no permission step and no trigger list to satisfy first - which is
    exactly why it is NOT labelled On-demand. On-demand is the trigger-gated state;
    reading "no trigger fired" off these documents is how an agent ends up never
    opening them.
  - Read them **by slice through their index**, keyed on a name you already hold.
    `src_components.md` and `src_graph.md` are never read whole.
  - Do NOT force-read system_docs as a box-check when the task does not trigger
    them, and equally do NOT skip a read because nobody asked for it. Read what
    the question needs; stop there.
  - Full policy: `agent_onboarding/default/engineer/SKILLS.MD` and
    `agent_onboarding/default/engineer/skills/context_protocol.md`.

Do not treat user ideas as gospel. Be curious, thoughtful, and explicit about uncertainties.
---

## 6) Prime Directive Documentation-First Edits

Whenever you add or modify code:

* **Every class must have a rich docstring.**
* **Every method/function must have a rich docstring.**
* **Comments must be preserved and improved** when they are unclear or insufficient.
* Treat docstrings and comments as part of the API: they must remain accurate.

---

## 7) Non-Negotiables

### 7.1) Preserve Documentation and Comments

* **Never delete or strip docstrings.**
* **Never delete comments.** If a comment is wrong, stale, or misleading, **update it** rather than removing it.
* Only rewrite docstrings/comments for code you touched **unless** an untouched doc/comment is provably wrong or dangerously misleading.

### 7.2) Rich Docstrings Required No Fluff

This is not optional. For **all public classes and public methods**, write docstrings that include **real contracts**, not vibes.

**Docstring style:** follow the repo's existing style (Google / NumPy / reST). If the repo has a pattern, match it exactly.

**Minimum content for public API:**

* **Purpose:** what it does and why it exists.
* **Contract:** invariants / guarantees / side effects.
* **Parameters:** meaning and constraints.
* **Returns:** what is returned (or `None`).
* **Raises:** what can be raised, and under what conditions.
* **Threading / Concurrency:** locks, thread-safety, reentrancy, ordering (when relevant).
* **Lifecycle / Cleanup:** ownership, idempotence, teardown ordering (when relevant).
* **Examples:** only when it materially clarifies usage; keep short.
* **Typing:** Always add typehints to signatures, and document complex types in the docstring if needed for clarity.

**No fluff rule:** do not write marketing copy or filler sentences. If a docstring is "rich," it's because it contains **precise guarantees**.

### 7.3) Documentation and Convention Precedence

* Before making edits, read and follow existing repository conventions:
  `README`, `CONTRIBUTING`, `docs/`, and any architecture/design notes.
* Do not invent new conventions if the repo already has a pattern.
* Record actual source conflicts. Resolve an already-authorized correction within scope;
  ask for unresolved material policy/authority decisions rather than routine file selection.

### 7.4) No Drive-By Refactors

* Do **not** refactor unrelated code.
* Do **not** rename symbols unless explicitly requested.
* Do **not** reorder code for aesthetics.
* Do **not** reformat files beyond what is required for the change.

### 7.5) Reviewability and Change Hygiene

* Keep changes **reviewable**.
* Avoid touching large numbers of files in one change unless explicitly requested.
* When a large change is required, group it by a clear boundary (module/dir) and apply a consistent rule.

### 7.6) Mechanical Sweeps Repo-Wide Imports Class Vars Headers

For repo-wide mechanical edits (e.g., "add this import everywhere", "add a class variable to every class"):

* Prefer generating a deterministic **codemod script** (or equivalent automated edit) rather than manually editing N files.
* The codemod must be safe, predictable, and reviewable.
* The goal is to avoid partial application, missed files, and "creative" edits.

### 7.7) Manual-First for Complex Behavior

* Prefer **hand-written code** for important or complex behavior changes.
* Only use scripts for **simple mechanical refactors** (e.g., renaming variables, adding imports).
* Do not use scripts to define or generate complex behaviors.

### 7.8) Method Size Discipline

* Prefer methods/functions around **50-60 LOC max** (counting code only; exclude
  docstrings, signatures, and blank lines).
* Split long methods into smaller, testable helpers with clear contracts.
* Do not fragment code if it reduces clarity; prioritize readable, cohesive units.

### 7.9) Validation Truthfulness

* **Never claim tests/lint/type-checks were run unless they were actually run.**
* If validation is skipped, say explicitly: **"Not run."**
* If fast checks exist, recommend the exact commands - but do not pretend they happened.

### 7.10) Public API Guardrail

* Do not change **public API shape or semantics** unless explicitly requested.
* If a public change is unavoidable, prefer:

  * compatibility adapters/shims, and/or
  * explicit deprecation paths with documentation.
* Interfaces may be exposed in public APIs when they mirror the concrete
  runtime classes. If an interface is exposed, the runtime object must be the
  concrete implementation and the interface must stay in lockstep with it.

---

## 8) Operating Protocol How You Should Work

### 8.1) Plan Implement Within Authority

Before making non-trivial edits:

1. Restate the goal in **3-5 bullets**.
2. List the constraints you will obey (especially docstrings/comments and no-drive-by refactors).
3. List the **exact files / symbols** you will modify.

Investigate implementation uncertainty within authorized scope. There is no per-step approval
for ordinary included edits, tests, peer coordination or ticket maintenance. Preserve reserved
decisions, security/action permissions, owner STOPs and required tests/reviews.

### 8.2) Scope Control

* Stay within the declared files/symbols.
* Record related files needed for the complete authorized outcome. Ask for material scope expansion,
  not another admission for ordinary included multi-file work.

### 8.3) Documentation Ritual

As a ritual, after implementing a change:

* Re-read the docstrings/comments you touched.
* Improve them for clarity and completeness (without fluff).
* Ensure they match the new behavior exactly.

### 8.4) Question-First Clarity

* If anything is unclear or uncertain, investigate briefly and then stop and ask.
* Prefer asking clarifying questions over making assumptions.
* Keep me updated on intent, progress, and blockers.

### 8.5) Architecture and Components Docs Required

* Descend the hierarchy rather than picking a document off a menu:
  `src_architecture.md` (which part) -> `src_components_index.md` (which
  component) -> slice `src_components.md` (what it owns, its Key Files) ->
  `src_graph_index.md` (which nodes) -> slice `src_graph.md` (how it wires) ->
  **the code**. Each step hands you the key the next one is looked up by.
* Reading these is your call, not something to request. Asking the user "may I
  read the component map?" is not caution - it is a stall. Ask instead for
  *guidance*: which subsystem, which of four similar names.
* **The documents are guiding tools; the code is the system.** They tell you
  which files to open, not what those files do today. Before changing an
  implementation, read that implementation. Where a document and the source
  disagree, the source wins and the document is stale - record it.
* Use ASCII and Mermaid diagrams for readability.
* Keep information sources, invariants, and lifecycle notes current as the system evolves.

---

## 9) Stop Conditions Ask Before Proceeding

Ask for a missing decision/permission when these actions are outside current authorization:

* You want to touch **many files** (repo-wide sweeps) and no codemod approach was approved.
* You want to rename/move files or symbols.
* You want to change public API shape or semantics.
* You want to introduce new dependencies or tooling.
* You want to change formatting across files.

---

## 10) Testing Discipline Unit-First Component-Second Integration-Third

We are building confidence, not just coverage. **All changes must be accompanied by tests** unless explicitly exempted.

### 10.1) What We Value in Tests Ranked

If you take nothing else from this section, take this:

> **A test is valuable if it would fail for a real regression and would *not* fail for a harmless refactor.**

Here is the ranking we use when judging test quality. Higher ranks are strictly preferred.

#### Rank S - System Contract Tests (Highest Value)

These tests prove end-to-end correctness of a *meaningful* contract boundary without re-implementing the system.

**Signals:**

* Exercises real wiring across multiple components (minimal real set).
* Catches regression in control flow, data flow, and lifecycle behavior.
* Fails for real breakage, not for refactors.

**Examples:**

* A "root revalidation" flow that uses real blueprints and validates outcomes.
* A concurrency primitive integration test that proves ordering/invariants.

> Use these sparingly and intentionally. They cost more to maintain.

#### Rank A - Behavioral Unit Contract Tests (High Value)

These are the backbone of the repo: small tests that validate contracts, invariants, and error behavior.

**Signals:**

* Asserts behavior through **public methods** and **documented outputs**.
* Validates meaningful branches and error paths.
* Avoids coupling to private fields/implementation details.

**Examples:**

* "Given these inputs, return/raise exactly X."
* "After cleanup, public methods raise or behave as documented."
* "Last-write-wins semantics for a registry."

#### Rank B - State Transition Tests (Medium-High Value)

Tests that validate a clear state machine / lifecycle, especially around concurrency and cleanup.

**Signals:**

* Proves valid transitions and prevents illegal transitions.
* Focuses on lifecycle invariants (cleaned vs active, idempotence, ordering).
* Uses introspection APIs (`describe()`, snapshots) rather than poking raw private fields.

#### Rank C - Collaboration/Boundary Mock Tests (Medium Value)

These validate that we call collaborators correctly. They're useful when the collaborator is expensive, external, or nondeterministic.

**Signals:**

* Mocks are used at **real boundaries** (I/O, network, filesystem, subprocess, time, OS).
* Asserts calls that matter (ordering, arguments, exactly-once / at-most-once) *when that is part of the contract*.

**Warning:**

* These become brittle if you over-specify calls.

#### Rank D - Regression Reproduction Tests (Targeted Value)

A test that exists to lock down a specific bug. Great when it's truly a regression guard.

**Signals:**

* Title references the bug symptom.
* Minimal reproduction.
* Assertions match the corrected behavior.

#### Rank E - Line-Coverage Fillers (Low Value)

Tests that exist mainly to execute lines but don't assert meaningful behavior.

**Signals:**

* Asserts "it didn't crash" with no contract outcome.
* Asserts values that are incidental.

> We avoid these unless they are stepping stones toward higher-rank tests.

#### Rank F - Attribute/Existence Checks (Very Low Value)

This is the bottom. These tests almost always waste time and fail for harmless refactors.

**Examples (bad):**

* `assert obj._some_private_field is not None` (unless the field is part of a documented public contract, which is rare)
* `assert hasattr(obj, "x")` / `assert "x" in obj.__dict__` / `assert isinstance(obj._pending_changes, dict)`

**Why this is bad:**

* Doesn't prove correctness.
* Over-couples tests to implementation.
* Encourages "coverage mirage."

**Only acceptable when:**

* The attribute is explicitly part of a public, documented contract (rare), or
* You are validating cleanup nulling **as part of a lifecycle safety contract** and there is no better public signal.

### 10.2) Rules Unit Tests First Mock and Isolated

The default approach is **mocked / isolated unit tests**.

* **Mock external boundaries** (I/O, filesystem, network, subprocesses, clocks, OS calls, databases, thread scheduling, random sources).
* Validate **contracts** (inputs/outputs/raises), **invariants**, and **side effects** (including cleanup ordering) at the smallest reasonable unit.
* Prefer **contract-level assertions** over implementation-detail assertions.
* Avoid flakiness: tests must run reliably on repeated runs.

#### Contract-level assertion checklist

When writing a unit test, you should be able to answer "yes" to most of these:

* The test asserts an observable outcome (return, raise, snapshot, or state transition).
* The test would fail if a real regression happened.
* The test would still pass after a harmless refactor (renaming locals, reordering statements, or changing internal data structures).
* Mocks are only used at true boundaries.
* Assertions focus on *behavior* rather than "internal shape".

If not, the test is probably Rank E/F.

### 10.3) Integration Tests Second Only When Needed

Integration tests are required when behavior cannot be proven safely via mocks/unit tests.

Use integration tests when at least one is true:

* Correctness depends on real interactions across multiple components (e.g., concurrency scheduling, orchestration behavior, serializer/codec correctness across layers).
* Mocking would require re-implementing the system under test or would make the test meaningless.
* The integration is the contract (e.g., plugin wiring, adapter boundaries, real concurrency primitives).

Rules for integration tests:

* Keep them **scoped**: integrate only the minimal set of real components needed.
* Make them **explicit**: use clear naming and markers (e.g., `@pytest.mark.integration`) if the repo uses them.
* Ensure they remain **repeatable** and not environment-dependent unless explicitly documented.

### 10.4) Coverage Target 95 Percent or Higher Non-Negotiable

#### Agent Execution Constraint (Read Carefully)

AI agents **cannot truthfully confirm** repository-wide coverage levels (including the =95% target) unless the **user** runs the test suite and reports the result.

* Agents must **not** claim coverage numbers.
* If the user asks whether tests or coverage were run, the only valid answer is **"Not run."**

#### Agent Policy: Prefer Test Density Now; Verify Coverage Later

In the agent environment, **coverage measurement is treated as a follow-up step** that the **user** performs. Agents should **default** to producing a strong test suite using the density heuristic, and then **ask the user to verify =95% coverage later**.

**Default Path - Test Density (Preferred for Agent Work):**

Use this path unless the user explicitly provides coverage output.

* **Baseline density:** target **= 10 tests per 100 LOC** for the changed/covered module(s).
* **Dense / high cyclomatic complexity code:** increase target to **= 20 tests per 100 LOC** when the code shows any of the following:

  * high cyclomatic complexity (many branches/guards)
  * heavy error-path logic
  * concurrency / locking / ordering constraints
  * lifecycle/cleanup state machines
  * non-trivial invariants (dirty tracking, revalidation, promotion semantics)

These are heuristics - not a license to create filler tests. Every test must still meet the quality criteria below.

**Follow-Up Path - Coverage Verification (User-Run, Later):**

* Target: **= 95% line coverage** for the relevant package/module(s).
* Requirement: the **user** runs the suite and reports the output.
* Agent reporting: if the user has not run it, you must say **"Not run."** and you must not guess.

If the user reports coverage below target, agents should add tests by increasing **branch/error/lifecycle** coverage - not by adding filler assertions.

We target **= 95% line coverage** across the library.

* Heuristic: we want at least **10 tests per 100 LOC**, but do not game it. If you have 95 percent or higher coverage but fewer than 10 tests per 100 LOC, that's acceptable.
* Coverage must not be "gamed" (no meaningless tests whose only purpose is to execute lines).

**Where we focus coverage:**

* Public API contracts
* Critical branching logic
* Error paths
* Lifecycle/cleanup behavior
* Concurrency-sensitive behavior (as testable)

If a component cannot reasonably hit the coverage target (rare), document the reason and the mitigation (integration coverage, property tests, or explicit exclusion with rationale) **and ask before applying exclusions**.

### 10.5) Truthful Validation Reporting

When reporting validation status:

* Only claim unit/integration/coverage runs if you actually ran them.
* If not run, say **"Not run."**
* If recommending commands, be specific and repo-consistent. Do not invent a workflow that contradicts repository docs.

### 10.6) Fixing Broken Base Code While Writing Tests

If you find mistakes while writing tests (bugs, incorrect docstrings, missing cleanup, race conditions):

* Raise them as issues rather than fixing them silently.
* If you have explicit permission to fix them, follow all rules in this document (docstrings, cleanup, scope control, tests).
* Do not fix unrelated mistakes outside your declared scope.
* If the mistakes block your work, explain the situation and ask for guidance.

---

## 11) Test Mocks Skills

For reusable test-only classes and helpers, see `tests/mocks/`.

