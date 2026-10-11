# Preparing a Release

A version bump prepares the working tree. It does not publish anything, and it
does not require an immediate push. Release approval is a separate decision.

## Bump the Local Version

1. Change `__version__` in `src/contextcompass_cli/__init__.py`. A compatible bug
   fix increments the last number, for example `2.16.0` to `2.16.1`. Version
   components are numbers, not single-digit slots.
2. Leave `pyproject.toml`'s dynamic version configuration in place. Hatch reads
   that Python file; do not add a second literal project version.
3. Run `uv lock` to refresh project metadata. Inspect `git diff -- uv.lock` and
   keep unrelated dependency upgrades out of a version-only change.
4. Regenerate the manifest with the new version, then regenerate the review dump.

Replace `X.Y.Z` below with the version just written in the Python file:

```sh
uv lock
uv run python -B src/context_compass/tools/package_manifest.py --root src/context_compass --version X.Y.Z
uv run python -B src/context_compass/tools/build_llm_full.py --root src/context_compass --out llm_full.md
uv run contextcompass version
```

`manifest_version` describes the manifest format, not the package release. Do not
increment it for an ordinary package change. The manifest's `package_version`
must match `__version__` and the distribution version.

Keep local or unreleased version numbers out of examples that tell people to
install from PyPI. A pin must refer to a published release. Human-facing release
notes should explain new features, fixes, compatibility, and any action users
need to take; internal commit IDs are not a substitute for that explanation.

## Check the Candidate

Review the source for private content and live state before generating hashes.
Retain the intentional example roles and templates. Follow the cleanliness and
ownership rules in [Maintaining the repository](maintaining.md).

```sh
uv lock --check
uv run python -B -m pytest -p no:cacheprovider
uv run python -B src/context_compass/tools/package_manifest.py --root src/context_compass --check
uv run python -B src/context_compass/tools/build_llm_full.py --root src/context_compass --out llm_full.md --check
git diff --check
git status --short
git ls-files -- '*.pyc' '*.pyo' '**/__pycache__/*'
```

Also inspect untracked/ignored cache directories under `src/`, especially after
the CLI bytecode test. Regenerate outputs again if any payload content changes
during review. Do not edit the source during an active test run.

## Build Without Publishing

The build backend and payload mapping live in `pyproject.toml`. A local build is
safe to perform without releasing:

```sh
uv build --sdist --wheel
```

The workflow uses the equivalent `python -m build --sdist --wheel` after
installing the `build` frontend. These commands create files under `dist/`; they
do not upload them. Keep build output out of Git and out of the payload.

Inspect both archives, not just the build exit code. Neither should contain local
workspaces, harness configuration such as `.codex/`, virtual environments, or
bytecode. Git's local exclude file is not proof that the build backend excludes
those paths; check the archive member names. A leaking source archive blocks
publishing even when the wheel is clean.

The wheel must contain the CLI entry
point and the Markdown payload under one `_package/` root, including `AGENTS.MD`,
`SKILLS.MD`, and `MANIFEST.md`. Preserve the workflow's payload checks when changing
the build mapping. A wheel containing only Python scripts is not this product.

Install that wheel into a separate temporary environment and run
`contextcompass version`, then `contextcompass init` against an empty temporary
directory. Check the newly installed payload with its own
`tools/package_manifest.py --root context_compass --check`. Do not use a real
project as the build smoke-test target.

## Publishing Is Explicit

The source of truth is
[python-publish.yml](../.github/workflows/python-publish.yml). Its current triggers
are a GitHub release becoming published and a manual workflow dispatch.

**Manual dispatch is not a test-only mode.** If its checks succeed, the workflow
continues to the PyPI publishing job. There is no dry-run dispatch in the current
workflow. Do not dispatch it while preparing an unpublished local version.

For an approved release, the release tag, built distribution version, and
manifest `package_version` must agree; the release-triggered workflow checks
this after stripping an optional leading `v` from the tag. That tag check is
conditional on a release event and does not run on manual dispatch.

The pipeline checks case-colliding Git paths, runs the Python/OS test matrix,
builds the wheel and source distribution, verifies the payload, and smoke-tests
the installed wheel before the publish job. It transfers those checked
distributions through the `release-dists` artifact.

Publishing uses the `prod` GitHub environment. Without `PYPI_TOKEN`, it uses
trusted publishing with OIDC; when that secret is configured, the workflow uses
the token path instead. Keep authentication in the configured environment or
repository secrets, never in these documents, source files, or command arguments.
Do not change authentication merely to prepare a patch version.

Only after approval should the release owner commit/push the intended changes,
create the matching tag/release, and verify the published package and install.
Until then, keep the version local and report what has actually been tested.
