# testing_discipline

Purpose
- The engineer testing discipline: what makes a test valuable, how to choose unit,
  component and integration tests, the coverage policy, and truthful reporting.
- Lazy: read it in full before you write, change or review tests, or report test or
  coverage results. `engineer/AGENTS.MD` keeps the always-on testing rules.

## Unit first, component second, integration third

We are building confidence, not just coverage. **All changes must be accompanied by tests** unless explicitly exempted.

### 1) What We Value in Tests Ranked

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

### 2) Rules Unit Tests First Mock and Isolated

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

### 3) Integration Tests Second Only When Needed

Integration tests are required when behavior cannot be proven safely via mocks/unit tests.

Use integration tests when at least one is true:

* Correctness depends on real interactions across multiple components (e.g., concurrency scheduling, orchestration behavior, serializer/codec correctness across layers).
* Mocking would require re-implementing the system under test or would make the test meaningless.
* The integration is the contract (e.g., plugin wiring, adapter boundaries, real concurrency primitives).

Rules for integration tests:

* Keep them **scoped**: integrate only the minimal set of real components needed.
* Make them **explicit**: use clear naming and markers (e.g., `@pytest.mark.integration`) if the repo uses them.
* Ensure they remain **repeatable** and not environment-dependent unless explicitly documented.

### 4) Coverage Target 95 Percent or Higher Non-Negotiable

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

### 5) Truthful Validation Reporting

When reporting validation status:

* Only claim unit/integration/coverage runs if you actually ran them.
* If not run, say **"Not run."**
* If recommending commands, be specific and repo-consistent. Do not invent a workflow that contradicts repository docs.

### 6) Fixing Broken Base Code While Writing Tests

If you find mistakes while writing tests (bugs, incorrect docstrings, missing cleanup, race conditions):

* Raise them as issues rather than fixing them silently.
* If you have explicit permission to fix them, follow all rules in this document (docstrings, cleanup, scope control, tests).
* Do not fix unrelated mistakes outside your declared scope.
* If the mistakes block your work, explain the situation and ask for guidance.
