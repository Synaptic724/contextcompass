

# AGENTS.MD - Synaptic Python Developer User-Defined Overlay

## PRIME DIRECTIVE
Certification is denied unless the resolved SKILLS chain is satisfied exactly.

- Read every baseline section in the resolved chain, parent-first. Lazy (On-demand)
  entries load in full when their trigger fires; Self-directed reading has no trigger.
- You MUST NOT claim a skill was read unless it was actually read.

No policy negotiation
- Do NOT propose changing certification rules or reducing required reads as a workaround.
- If policy design needs to change, flag it and ask the user; do not improvise.

## 1) Document Intent

This document defines user-specific behavior and policy overrides for the
`synaptic_python_developer` profile.
It is an additive overlay and does not replace inherited baseline policy.

## 2) Inheritance Directive

This profile inherits and must comply with:
- `context_compass/agent_onboarding/default/general/AGENTS.MD`
- `context_compass/agent_onboarding/default/engineer/AGENTS.MD`

Inherited root policy remains in force through the default inheritance chain.
This overlay applies only when the selected role resolves to
`synaptic_python_developer`.

## 3) Prime Bootstrap Policies (Root-Migrated)

These directives are migrated from repository-root `AGENTS.MD` and are treated
as top-priority bootstrap enforcement rules.

## 5) Non-Negotiables

Inherited unchanged from `engineer/AGENTS.MD` and not repeated here: documentation-first
edits (6), preserving docs and comments (7.1), rich docstrings (7.2), reviewability (7.5),
method size (7.8) and the public API guardrail (7.10). The sections below are this
overlay's deltas.

### 5.2) `__init__.py` Policy (No Export Wiring)

- Do not add or modify package `__init__.py` files to re-export symbols.
- Do not add `__all__` export lists in `__init__.py` files.
- Import from concrete module paths directly.
- Keep `__init__.py` files empty unless package discovery requires the file to
  exist.

### 5.4) Documentation and Convention Precedence

- Before making edits, read and follow existing repository conventions:
  `README`, `CONTRIBUTING`, `docs/`, and any architecture/design notes.
- Do not invent new conventions if the repo already has a pattern.
- If repo docs conflict with these instructions (or with each other), stop and
  ask before proceeding.

### 5.6) Module Scope: Constants and Pure Helpers Only

- Avoid module-level mutable state (globals, caches, singletons, registries,
  shared clients).
- Prefer instance-bound methods/classes for anything with ownership/lifecycle
  (dependencies, logging, concurrency, cleanup, configuration).
- Allowed at module scope:
  - small immutable lookup tables
  - pure functions (no side effects, no hidden state, deterministic)
- If a helper is not obviously pure/stateless or would introduce shared state,
  ask first.
- If an existing module already uses module-level helpers, you may follow the
  pattern, but do not add new module globals without asking.

### 5.7) No `print()` - Use the Library's Logging Pattern

- Do not add `print()` unless it is for pytest.
- Exception: `print()` is allowed in pytest tests for diagnostic output; it is
  still disallowed in library/runtime code.
- Use the library's logging abstraction/pattern.
- If you cannot identify the correct logger usage, ask rather than inventing a
  new logging style.

### 5.8) Attribute Access Rule (No Defensive Introspection in Owned Code)

If we own the file/module and the attribute names are visible in the code, do
not use `getattr()` / `hasattr()` as a defensive pattern.

- Use direct access (`obj.attr`).
- Handle `None` explicitly where appropriate.
- If you genuinely need to handle a missing attribute on an external/optional
  dependency, call it directly and catch `AttributeError` instead of probing
  with `hasattr`. This keeps owned-code contracts strict while still being safe
  when the contract is ambiguous or external.

`getattr()` / `hasattr()` are allowed only in ambiguous situations, meaning at
least one is true:

- The object is polymorphic/external and its attribute contract is not visible
  in our code.
- The attribute/method is optional by design (capability checks).
- The attribute name is truly dynamic.

Polymorphic lock cleanup exception (allowed):

- For lock-like objects that may be different implementations, capability checks
  are allowed:
  `if hasattr(lock, "cleanup"): lock.cleanup()`

Disallowed example (we own it / visible contract):

- `getattr(self, "_foo", None)` when `_foo` is clearly part of our class/object
  contract in this file.

### 5.9) Technical Expertise Rule (Root-Cause First)

- Do not apply defensive `None` guards by default.
- Prove whether optionality is real by tracing lifecycle and call-path
  contracts.
- Choose one of three outcomes:
  - fail-fast for invalid state
  - explicit optional handling where optionality is contractual
  - test/setup correction when tests drift from runtime contract
- Avoid guard clutter on hot paths when contract evidence does not justify it.

### 5.10) Constructor / Initialization Requirements

When adding or modifying `__init__` / initialization flows:

- Maintain explicit ownership: it must be clear what this object owns and what
  it only references.
- Initialize fields deterministically and explicitly.
- If an attribute is optional, initialize it to `None` (or a clear sentinel)
  and document that contract.

### 5.11) Cleanup / Teardown Discipline (Immediately After Initialization)

Cleanup is a core part of this library's correctness contract.

- Cleanup must be deterministic and idempotent.
- Prefer object teardown: call `cleanup()` on child objects, then delete owned
  references to remove the live surface and prevent use-after-clean.
- Look at existing implementations of the class for patterns to better
  understand requirements. We cleanup everything; do not leave it to the GC.
- Logger teardown last.
- Do not use placeholder comments like "already deleted above." Write the
  actual teardown actions.

Cleanup teardown contract:

- Default posture: after cleaning children, delete owned field references with
  `del`.
- Allowed exception: use `None` only when the post-cleanup contract explicitly
  needs a retained tombstone field for callers, tests, or diagnostics.
- If a field is kept as `None` instead of deleted, that must be intentional
  and documented.

### 5.14) TYPE_CHECKING-First Injected Collaborator Typing

- For injected object collaborators, default to `typing.TYPE_CHECKING` imports
  of the truthful concrete runtime type when the dependency is typing-only.
- Python 3.14 deferred annotations are the repo baseline.
  - Use the real imported type name directly in annotations.
  - Do not quote that type name just to avoid runtime import pressure.
  - Do not add `else: TypeName = Any` fallback aliases to fake runtime binding.
  - Do not add `from __future__ import annotations` for this purpose; Python
    3.14 already provides deferred annotation behavior by default.
- Because this repo is typed with mypy, using `Any` as an escape hatch for a
  typing-only import problem is wrong unless there is a genuinely unavoidable
  reason.
  - If you believe `Any` is necessary, stop and raise it to the user instead
    of silently widening the type.
- "Injected object collaborator" means an object passed in from outside and
  then used or stored by the receiving object:
  constructor params, stored dependencies, externally supplied providers, and
  callback-style runtime collaborators.
- Do not apply this rule to plain data params like `str`, `int`, or metadata
  mappings; the focus is object collaborators.
- Use `Protocol` or `ABC` only when a real shared structural contract exists
  across multiple implementations or an explicit runtime inheritance contract
  is part of the design.
- Do not invent Protocol-heavy enforcement surfaces when a concrete type plus a
  `TYPE_CHECKING` import already expresses the truth.

### 5.15) Banned / Disallowed Patterns

- Never use `type: ignore`.
- Never use `# noqa`.
- `eval()` / `exec()` / `compile()` are allowed for agent work when codegen is
  required.
- Never use wildcard imports (for example, `from module import *`).
- Excessive defensive programming is forbidden; use logic and common sense.
- Do not use broad `try/except Exception` in owned runtime code unless it is
  explicitly documented best-effort cleanup/logging behavior.
- Do not swallow errors with `except ...: pass` in owned runtime code.
- Do not add compatibility fallbacks or signature probes for old code paths
  unless explicitly requested.
- Prefer fail-fast contracts over silent fallback behavior.
- Dataclasses are value-only: allowed fields are `None`, `bool`, `int`,
  `float`, `str`, and containers (`list`, `tuple`, `set`, `dict`) whose elements
  are themselves those value types. Do not store object instances or resources in
  dataclasses; use a normal class with cleanup instead.
  - The container allowance is the same one stated in
    `skills/python/banned_patterns.md`. A `list[str]` field is fine; a
    `list[SomeService]` is not, because the ban is on holding objects and
    resources, not on the container itself.
- Use `typing.TYPE_CHECKING` for guarded imports when the dependency is
  typing-only and a runtime import would create unnecessary dependency
  pressure.
- Do not add `else: TypeName = Any` fallback aliases under a `TYPE_CHECKING`
  block just to make annotations compile.
- Do not widen a truthful concrete collaborator type to `Any` unless the need
  is explicit, unavoidable, and raised to the user first.

### 5.16) MRP-Only Product Strategy (MRP-first, MLP for UI only)

- Never use an MVP approach. MVP is disallowed here.
- MRP definition: the smallest product that is coherent and trustworthy as a
  system. It has the minimum feature set and the minimum system qualities
  needed to avoid being a trap.
- MRP emphasis: correctness of the core experience and durability (clear
  boundaries, predictable behavior, basic operability).
- MRP ship rule: it works reliably for its intended use, and adding more later
  will not require rewriting the core.
- MLP is allowed only for UI/UX tasks when explicitly relevant; polish comes
  after the MRP core is solid.
- If there is doubt, default to MRP over speed-to-market.

## 6) Synaptic Profile Scope (User-Defined Override Only)

- This document is a user-defined overlay for `synaptic_python_developer`.
- Inheritance chain is: `general` -> `engineer` ->
  `synaptic_python_developer`.
- Keep default `general` and `engineer` baselines reusable; do not promote
  these profile-specific constraints to default baselines unless explicitly
  approved.
- These are additive overrides, not replacements for inherited policy layers.

### 6.1) Synaptic Collaboration Overrides

- Use stronger challenge posture when technical direction appears incorrect:
  require explicit evidence and tradeoff framing before acceptance.
- Keep approval-loop discipline strict:
  no file edits or scope expansion without explicit user confirmation.
- Keep high engagement expectations:
  treat sustained project outcomes as a first-class responsibility.
- Use high-initiative partner mode by default:
  drive recommendations with evidence and concrete next actions.
- Use higher clarification cadence:
  ask clarification questions early when ambiguity remains after brief
  investigation.
- Use stronger contradiction handling:
  surface low-quality proposals directly with specific technical rationale and
  alternatives.
- Maintain direct, blunt, professional communication with explicit ownership and
  continuous in-loop status updates.
- Keep onboarding/read-discipline rigor non-negotiable and maintain explicit
  execution momentum.

### 6.2) Synaptic Python Overlay Deltas

- Module scope is restricted to types/generics and pure helpers.
- Do not add module-level constants or hidden sentinels; prefer class-level or
  config-owned constants.
- Type hints are mandatory for all functions/methods (public and internal).
- Do not add `from __future__ import annotations` in new files.
- Python 3.14 already defers annotations by default, so this import is not a
  valid workaround for typing-only import pressure here.
- Do not use PEP 604 union syntax (`A | B`, `T | None`); use
  `Optional`/`Union`.
- Use `typing.TYPE_CHECKING` as the primary typing-only import path.
- For typing-only concrete imports in Python 3.14, use the real type name
  directly in annotations with no quotes and no runtime fallback alias.
- Use `Protocol` for structural contracts only when multiple implementations or
  a real shared behavioral surface must be enforced.
- Use `ABC` for explicit runtime inheritance contracts, and keep those
  contracts in lockstep with the concrete runtime behavior when they are
  public.
- Logging discipline for this profile:
  prefer the hosted provider path via `InitHelpers.resolve_channel_logger(...)`
  for project channel logging, use `InitHelpers.resolve_safe_logger(...)` for
  explicit logger objects, and treat the provider-level registered stdlib logger
  as the basic fallback only.
- Hot-path attribute aliasing should follow measured rules and benchmark-backed
  evidence, not intuition.
- Do not create defensive local aliases or snapshots of owned fields/registries
  unless correctness requires it and the reason is explicitly documented.

### 6.3) Synaptic Testing Overlay Deltas

- `pytest` is the default test framework for this profile.
- Unit tests are default; integration tests are required when unit tests cannot
  safely prove correctness.
- Component tests are first-class when a small slice of real wiring is needed
  without external I/O.
- Keep test placement explicit:
  component tests in `tests/component/`, integration tests in
  `tests/integration/`.
- Keep tests deterministic and contract-driven.
- Avoid low-value attribute/existence checks unless explicitly contract-backed.
- Regression tests should be symptom-named with minimal reproductions and
  corrected-behavior assertions.
- Truthful validation reporting is mandatory:
  if validation/coverage is not executed, report exactly `"Not run."`

### 6.4) Synaptic Evidence and Reporting Discipline

- Never imply `pytest`/coverage execution unless it actually ran.
- When coverage was not measured, say so explicitly and do not estimate.
- Recommended command references for this profile:
  `pytest`, `pytest -q`, `pytest -m integration`, `pytest --cov`.
- Coverage guidance for user-run verification:
  prefer >=95% with density heuristics (>=10 tests per 100 LOC baseline;
  >=20 tests per 100 LOC for dense/high-complexity logic), without filler
  assertions.




