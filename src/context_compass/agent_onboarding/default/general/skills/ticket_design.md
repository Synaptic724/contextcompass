# Ticket design and optional Agile metadata

Applies to new/future tickets and new contributions. This is not a migration
procedure, role selector, permission grant or replacement for onboarding.

## Choose the design

Read `ticket_design` in `config/context_compass_config.yaml` before creating a
new ticket. Its `instructions` are project guidance. Its `templates` map Epic,
Story and Task to context-compass-relative files. Users can point those paths
at their own templates under `user_defined/`; keep the full ticket composition,
required gates, Notes, evidence and handoff. Do not overwrite an existing ticket
to apply a new design.

Agile metadata is optional **by ticket design**. Do not add it merely because a
GitHub plugin exists or an agent holds a particular role. Non-Agile designs
retain their ordinary Status authority. A selected Agile design adds one
`AGILE_METADATA` JSON block inside the existing `project_fields` region.

## Canonical definition

Read `templates/ticket_contract.json` for the versioned fields, values,
invariants and attribution policy. That file is the source-owned definition;
tools and portable bundles derive from it rather than another handwritten
ticket rulebook. Read the full selected template as well.

When metadata is present, its workflow is canonical. The visible Status is
`phase / execution / resolution`, derived from that object, not an old-status
compatibility mapping. Native hosting state and Projects cannot override it.
Metadata evidence references point to existing body Notes by `EVENT_ID` or
`DATETIME`; they do not create another evidence store. Retain the configured
note-quality requirement. Unknown evidence is not an acceptable transition ref.

Accepted resolution additionally references Notes with the explicit conclusions
specified by `accepted_note_fields` in the canonical definition. These record
authorized acceptance, validation, child dispositions and reconciled routing;
the presence of a passing test or a closed Issue cannot supply those conclusions.
The checker validates declarations, not their authenticity or truth.

Each state event has a logical event identity. Reusing that identity for a
different payload is a conflict. A revision/hash check is a client safeguard,
not an atomic lock supplied by GitHub. Read, preserve, write, fetch and reconcile
uncertain effects under the primary writer's custody.

## Names, authors and review

`Owner` is accountable custody. `Agent Name` and `Agent Role` describe the actual
executor. Each new authored Note, post or comment identifies its own full author
name and actual role/function under `agent_identity.md`. Do not treat the current
executor as the author of all earlier contributions.

`TICKET_ATTRIBUTION`, when used, records contribution-scoped authors, the
observed publishing service/account and exact review targets. It is not an
identity registry. Public examples use generic project actors; public work must
not disclose restricted rosters or runtime identifiers. Native created-by
attribution stays intact. No per-post approval gate or posting cadence is added.
Its readable Contribution Attribution labels are generated from the canonical
definition and JSON object; do not maintain another editable copy of those facts.

Both optional objects use this exact wrapper inside `project_fields`, replacing
the example name with `AGILE_METADATA` or `TICKET_ATTRIBUTION`:

````text
<!-- BEGIN OBJECT_NAME -->
```json
{ "fields": "from the canonical definition" }
```
<!-- END OBJECT_NAME -->
````

State-event Notes include an `EVENT_ID` matching `last_event_id`. This identifies
one actual workflow change; it is not emitted on each assistant response. The
Python helpers `initial_metadata`, `render_new` and `transition` construct/check
these wrappers while retaining the complete ticket and prior Notes.

Passing validation, entering acceptance phase, or closing an Issue does not
establish authorized acceptance. A reviewer who authored or materially edited
the target is not independent by changing a role label. Historical unknown
authorship stays unknown; this feature does not repair old records.

## Helpers and portable delivery

`tools/ticket_design.py` validates the chosen new-format metadata and attribution,
performs preserving in-memory transitions, and produces source-derived bundles.
It never writes to GitHub or updates boards, credentials, global instructions or
installed projects. New-file output refuses an existing target.

For local agents, read the installed canonical definition and selected template.
For a cloud reader, create one complete ticket-contract bundle for the selected
type/backend, with its source hashes and explicit versioned note-score binding.
Do not load both that bundle and an independently maintained copy of its rules.
It is a ticket-contract delivery unit, not proof that onboarding was completed
or permission to skip other actual runtime/coordination gates.

Custom template content may be project-private. Generating a bundle is not
publication authorization. Check its audience before sharing it. No token-saving
or adherence claim is made without actual read/behavior measurements.
