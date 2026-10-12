# Choose where your tickets live

Context Compass supports two settings in `config/context_compass_config.yaml`.
`local` uses the existing Epic/Story/Task folders. `github_codex_plugin` uses
GitHub Issues through the connected GitHub plugin. Both keep your ticket format,
Notes, evidence, acceptance rules, and recovery process.

## Local tickets

```yaml
work_tracking:
  backend: local
```

This is the default. Your agent reads tickets in `tickets/epics/`,
`tickets/stories/`, and `tickets/tasks/`, and follows their backlog/completed
lanes as needed. You can leave the GitHub settings blank and work offline.

## GitHub Issues through the Codex plugin

```yaml
work_tracking:
  backend: github_codex_plugin
  github_codex_plugin:
    connection_nickname: "Work account"
    issues_repository: YOUR_OWNER/YOUR_REPO
    project_url: "" # optional
```

Connect the GitHub plugin in the agent's environment and grant it access to that
repository. The agent checks the available repository/Issue tools and reads the
exact destination before working. CLI installation, a PowerShell script, and a
token in YAML are not required for this backend. A missing connection or denied
Issue operation is reported as a blocker, with no automatic switch to local files.

Give the connected account a nickname in Codex, such as `Work account`, and put
that exact nickname in YAML. It selects the connection, not a GitHub username
or repository owner. The agent resolves its current connection ID and verifies
the authenticated profile before operating. A missing or ambiguous nickname
stops work rather than selecting your personal account or another connection.
Do not save tokens or connection IDs in this file.

Each Epic, Story, or Task is an Issue containing the matching Context Compass
template. Status and `## Notes` live in its body, including the existing note
fields and evidence. Issue updates preserve the full body and prior history;
the agent verifies the update by fetching it again. Parent/child and blocker
links remain explicit even if native hierarchy tools are unavailable.

Your local `issue_board.md` records agent claims and `attention_board.md` records
current focus using Issue URLs. Mailbox, artifacts, context packs, system docs,
and special instructions stay in your repository. Message transport follows the
independent `agent_communication.backend` selector (default `mailbox`); MCP
mode replaces transport only and preserves all state sections. A Project URL can identify a
related Project, but it is optional and does not replace Issue-body Status.

An agent onboarding or recovering from compaction reads the selected backend's
skills and ticket source. YAML selects a workflow; it does not connect a plugin
or grant write permission by itself. The agent can verify read access first;
the first requested write must also succeed and be verified.

## Existing installs and migrations

Changing the setting does not move your tickets. Review [`migration.md`](migration.md)
for a local-to-Issue move before switching an active project. Keep the old files
until the complete content and route mapping have been verified.

Older `backend: files` settings resolve to `local`. The earlier `backend: github`
selected a CLI/Project draft, so it requires an explicit change to
`github_codex_plugin` and the matching settings block; it is not silently converted.
Upgrade tools preserve your existing config values.
Older plugin configurations must add `connection_nickname` explicitly; an
upgrade cannot infer which connected account you intend to use.

Installed `agent_onboarding/user_defined/` roles are also preserved on upgrade.
Review an existing overlay's local-only workflow references when enabling the
plugin; the corrected shipped examples do not overwrite your installed copies.

The earlier [CLI command guide](commands.md), `setup.ps1`, `setup.sh`, and
`check_setup.py` remain optional standalone CLI helpers. They are outside the
plugin backend's required readset and do not enable or authenticate that plugin.
