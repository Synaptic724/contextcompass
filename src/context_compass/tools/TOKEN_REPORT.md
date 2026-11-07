# See What Your Agent Loads

A short file is not always cheap. An artifact board can have a few hundred lines
and still contain more tokens than a long architecture document. This tool counts
the actual text and shows how your role and routing choices change the reading map.

It does not shorten anything, change your settings, or tell the agent to skip instructions.
Running a report is optional, not another onboarding step.

## Install The Optional Counter

For a pip-installed Context Compass:

```sh
python -m pip install "contextcompass[tokens]"
```

For a copied `context_compass/` folder, install `tiktoken` in the Python environment
you use to run the script. The tool never installs packages automatically. On its
first use, tiktoken may download its public vocabulary. Your project text is counted
locally, not sent to a model or token-counting API.

## Make A Report

From a repository with an installed `context_compass/` folder:

```sh
contextcompass token-report --role engineer --out-dir context_compass_report
```

Or run the Python tool directly:

```sh
python context_compass/tools/token_report.py --root context_compass --role engineer --out-dir context_compass_report
```

`--role` selects the route to explain in the report. It does not select or change
an agent's role: you still ask the agent to onboard as the role you want.

Without `--role`, the tool assumes no role and shows the full comparison instead.
Without `--out-dir`, it prints Markdown without writing report files.
For large projects, prefer `--out-dir` so the full inventory does not flood a chat or terminal.

## Compare Your Choices

The report includes every registered role from `SKILLS.MD`, its inherited parents,
both ticket backends, both message transports, and onboarding versus recovery.
The selected detail view uses your current YAML settings unless you explicitly
choose alternatives for the report:

```sh
contextcompass token-report --role engineer --ticket-backend github_codex_plugin --communication-backend codex_mcp --event reonboard --out-dir context_compass_report
```

These flags do not edit YAML or enable a connector. They let you compare declared
reading routes before making a separate configuration decision.

`--reading-mode lean|full` does the same for `reading.mode`. In `lean`, the default,
each role reads its eager readset and loads lazy (On-demand) entries when their
trigger fires; in `full`, it also reads every lazy entry at onboarding and recovery:

```sh
contextcompass token-report --role engineer --reading-mode full --out-dir context_compass_report
```

## What The Numbers Mean

- **Known tokens:** one copy of the declared full reads plus any precisely identified
  partial text, with shared paths counted once per route.
- **Lazy tokens:** the full size of the lazy files a route can load by trigger. `lean`
  reads them only when needed; `full` moves them into the known total.
- **Session-specific text:** extra material whose size depends on the agent/session.
  The mailbox roster is measurable; relevant Notes and addressed messages are not
  assumed to mean the whole mailbox. A trailing `+` means this extra cost is unresolved.
- **Full-file reference size:** the size of a file containing a required read. It
  is not automatically the amount the agent should read. MCP attention-board costs
  exclude the Message Alerts section.
- **Conditional and self-directed paths:** shown separately, not added to the
  baseline. Their full sizes do not establish the cost of a topic-specific slice.
- **UNKNOWN:** a path was missing, unreadable, binary, too large, excluded, or its
  declaration could not be resolved. It is not silently counted as zero.

The encoding is explicit: `o200k_base` by default. Use `--encoding` to select another
tiktoken encoding. The report does not claim that a model alias uses that encoding.
These are source-text counts, not cumulative chat usage, billing, cached-input or
reasoning/output measurements.

## Files And Privacy

The output contains:

- `report.md`: route comparisons, the selected inherited paths, optional choices,
  ranked source sizes and diagnostics.
- `report.json`: the complete per-route map, reasons, source declaration lines,
  hashes and inventory metadata.
- `files.csv`: every inventoried path with its full-file size and measurement status.

CSV protects formula-like filenames when opened in a spreadsheet; JSON retains exact path values.

Keep reports local when their filenames or paths describe private work. The tool
does not publish them or register them on your boards. Agents should associate any
retained report with the ticket that needed it under the project's existing rules.

The scan stays inside the selected Context Compass root. It excludes environment,
cache, Git and harness directories, known credential filenames and generated output
directories. Individual excluded files remain visible as unmeasured. Files above
10 MiB are visible but not tokenized; change `--max-file-bytes` if needed, or use `0`
for no per-file limit. Large scans can still take time and memory.

Select an empty output directory, or reuse one already created by this generator.
Reporting refuses to overwrite an unrelated directory or replace the input root.

## Reading Rules Remain The Authority

This is a report of the existing registry and declared skill lists, not a new
onboarding engine. It validates inheritance and documented backend choices but
does not interpret arbitrary natural-language overrides in `special_instructions/`.
Those files are included and their possible effect is explicitly disclosed. Global
harness instructions and task-specific code reads are outside the default scope.

Missing system-orientation documents are skipped only where the manifest says to
read them when they exist. Other missing baseline paths are reported as unresolved.
When declarations are unsupported, the report retains diagnostics instead of
guessing an effective route or pretending the agent is certified.
