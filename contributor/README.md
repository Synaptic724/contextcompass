# Contributing to Context Compass

This folder is for maintaining Context Compass itself: changing the shipped
documents and tools, checking that upgrades preserve people's work, and preparing
a release. If you want to use Context Compass in another project, start with the
[main README](../README.md#quickstart).

## Find What You Need

| Guide | What it covers |
| --- | --- |
| [Maintaining the repository](maintaining.md) | Where changes belong, document wiring, user-owned content, and generated files |
| [Maintainer-agent entrypoint](AGENTS.md) | Read path, work state, recovery, and delegation for agents maintaining this repo |
| [Testing changes](testing.md) | Local setup, regression suites, mutation tests, and package checks |
| [Preparing a release](releasing.md) | Version changes, final checks, packaging, and what actually publishes |

Commands in these guides run from the repository root, beside `pyproject.toml`,
unless a command explicitly changes directories. Paths are relative to that
root, not to a particular contributor's machine.

## The Important Distinction

`src/context_compass/` is the clean package that other people copy into their
repositories. It is not this repository's live workspace. Do not use its boards,
tickets, mailbox, or system-document directories to track maintenance work.
That would ship our working state to everyone who installs the next version.

Use a separate local Context Compass instance for maintenance work. Keep personal
instructions, machine paths, private repository references, and live agent records
out of the public package. Keep the shipped examples; they are not live records.

These guides explain repository maintenance. Agents start with
[the maintainer-agent entrypoint](AGENTS.md), which routes them to the working
instance's normal policy and the contributor materials. The shipped entrypoint
under `src/context_compass/` remains product source, not a place to write live state.

## A Normal Change

1. Read the current implementation and the documents that describe its behavior.
2. Make the requested change without folding in unrelated cleanup.
3. Add a regression test for a bug, then run the relevant existing tests.
4. Refresh the manifest and review dump if the package changed.
5. Review the complete diff for user-data loss, stale instructions, and accidental
   private content before handing it back for review.

A local version bump is not permission to commit, push, tag, or publish. Keep
release preparation separate from release approval.
