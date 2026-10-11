# Maintaining the Repository

Agents maintaining this repository start at [the maintainer-agent
entrypoint](AGENTS.md), which routes the read path, work state, recovery, and
delegation rules. The sections below are the referenced detail.

## Where Changes Belong

| Path | Purpose |
| --- | --- |
| `src/context_compass/` | The payload installed as `context_compass/` in a user's repository |
| `src/contextcompass_cli/` | The installer and command-line interface |
| `tests/` | Unit, integration, regression, and mutation coverage |
| `pyproject.toml` | Package metadata, build mapping, development dependencies, and pytest configuration |
| `uv.lock` | Resolved development environment and project metadata |
| `README.md` | The public introduction and user setup guide |
| `contributor/` | Instructions for maintaining this repository |
| `.github/workflows/python-publish.yml` | Release checks, distribution builds, and publishing |
| `llm_full.md`, `llm_full_index.md` | Generated review copy of the payload and its file-range index |

The distribution is named `contextcompass`, the Python module is
`contextcompass_cli`, and the installed directory is `context_compass`. Keep those
names distinct. The wheel maps the payload to `contextcompass_cli/_package/`;
editing a built wheel or an installed copy does not change the source package.
The contributor guides belong in the source distribution, not the installed
payload. Keep `contributor/` in the sdist include list when changing packaging.

## Changing Instructions and Roles

The Markdown is part of the product. A policy edit can change agent behavior even
when no Python changes. Follow its references through the entrypoint, shared
skills, role skills, templates, and examples before deciding the change is done.

- Keep [AGENTS.MD](../src/context_compass/AGENTS.MD) as the runtime entrypoint.
- Keep [SKILLS.MD](../src/context_compass/SKILLS.MD) as the role registry. Roles
  are selected per agent/session, not through a shared active-profile setting.
- Use the existing [profile creation guide](../src/context_compass/PROFILE_CLASS_CREATION_GUIDE.md)
  for role layout and registration. Keep registry parents and
  `INHERITS_SKILLS_FROM` headers consistent.
- Follow the registry's skill-entry format and preserve the distinction between
  baseline, on-demand, and self-directed reads. Do not silently change a skill's
  read requirement while editing its wording.
- Configuration defaults belong in
  `src/context_compass/config/context_compass_config.yaml`; installed user values
  must survive upgrades.
- Keep examples generic and usable. A reference to a relative project path is
  different from a contributor's concrete home directory or private repository.

For system-document work, use the existing
[system-document authoring guide](../src/context_compass/agent_onboarding/default/engineer/skills/system_document_build.md)
and [graph generation guide](../src/context_compass/agent_onboarding/default/engineer/skills/src_graph_generation.md).
Architecture/component prose is authored; its indexes are generated. Graph
extraction refreshes mechanical facts but must preserve authored content and
review stamps, including when a retired node returns.

Harness-specific instructions are maintained in the shared
[custom-instruction skill](../src/context_compass/agent_onboarding/default/general/skills/harness_custom_instructions.md).
Check vendor documentation when changing its paths or behavior. Package tools
must not silently edit a user's global instructions.

## Preserve the User's Work

The ownership rules come from
[package_manifest.py](../src/context_compass/tools/package_manifest.py), with
upgrade behavior in
[update_context_compass.py](../src/context_compass/tools/update_context_compass.py).
Use the code and preservation tests when changing these rules; a folder name
alone does not establish what a tool may replace.

| Class | Upgrade behavior to preserve |
| --- | --- |
| `PACKAGE` | Compare shipped, current, and incoming content; keep local edits when the package has not changed, otherwise conform with explicit reporting |
| `RESET` | Leave installed tickets, artifacts, system docs, context management, and special instructions alone |
| `INSTANCE` | Do not replace existing user-defined files or undo deliberate deletions; newly introduced missing files can be seeded |
| `LIVE` | Update board structure while carrying `USER-DEFINED` regions intact; legacy boards need migration |
| `CONFIG` | Add new defaults without overwriting values already chosen by the user |

Region names are compatibility keys. Removing or renaming one can strand user
content. Test upgrades with old populated regions and new empty templates, not
with identical user data already present on both sides. Preserve routing rows,
switch/resume details, mailbox checkpoints, and artifact associations.

Unmanifested files in strict package areas may be swept during upgrades;
permissive user-owned areas are different. Keep that distinction covered by tests.

Cleanup is not a harmless formatting step. `cleanup_context_compass.py` defaults
to `reset`, which can remove project work. Use `--check` to inspect a named target
and reference first. Use `--mode repair` when preserving an active instance, and
do not apply a reset or purge as part of routine maintenance. The existing
user-defined example roles are intentional; do not remove them as contamination.

## Keep the Shipping Copy Clean

- Leave shipped board user regions empty. Do not check in agent registrations,
  live requests, personal tickets, or another project's system maps.
- Put reusable examples in `examples/`, not in a live work area. Keep required
  scaffolding and instructions rather than deleting entire directories.
- Inspect new text for credentials, absolute personal paths, private repository
  names, and copied project-specific claims. Preserve legitimate license notices.
- Keep caches, bytecode, virtual environments, build output, and local workspaces
  out of the payload. `.gitignore` does not remove files already tracked by Git.
- Preserve filename case, especially `AGENTS.MD` and `SKILLS.MD`. Check for paths
  that differ only by case before adding or renaming files.
- Follow `.gitattributes`: text ships with LF endings. Avoid formatting churn
  unrelated to the requested change.

## Refresh Generated Files

Do not hand-edit hashes, line ranges, or the review dump. The version comes from
`src/contextcompass_cli/__init__.py`; when it changes, follow the
[release guide](releasing.md#bump-the-local-version) so the manifest agrees.

For a payload edit without a version change, the manifest tool retains the
version already recorded in the manifest:

```sh
uv run python -B src/context_compass/tools/package_manifest.py --root src/context_compass
uv run python -B src/context_compass/tools/build_llm_full.py --root src/context_compass --out llm_full.md
uv run python -B src/context_compass/tools/package_manifest.py --root src/context_compass --check
uv run python -B src/context_compass/tools/build_llm_full.py --root src/context_compass --out llm_full.md --check
```

Generate the manifest before the review dump because the dump includes it. The
dump covers the payload, not the root README, contributor guides, or CLI module.
Use `llm_full_index.md` to find a file and `--slice context_compass/AGENTS.MD` to
read a verified slice; `--slice` reads existing output, it does not regenerate it.

Neither a matching manifest nor a clean dump proves the content is appropriate
for a public release. Review the source before recording its hashes.
