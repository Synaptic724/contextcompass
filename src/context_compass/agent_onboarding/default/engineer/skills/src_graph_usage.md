
# src_graph_usage

Purpose
- Define how to READ the assembled source graph without loading all of it.

## What the graph is

Two files under `system_docs/`:

- `src_graph.md` - one section per source file, each delimited by an HTML
  comment naming that file.
- `src_graph_index.md` - the exact line range of every section, plus a
  staleness proof.

Both are generated. Never hand-edit either one; see
`agent_onboarding/default/engineer/skills/src_graph_generation.md`.

## The read order (non-negotiable)

1. Read `src_graph_index.md`. It is small - about 3% of the document's lines,
   6% of its bytes.
2. **Verify it is current** (next section).
3. Find the row for the source file you care about.
4. Read only that line range out of `src_graph.md`.

Do not read `src_graph.md` in full. On the reference codebase it is 20,261
lines against a 602-line index; a single file's section is typically 20-40
lines. Reading the whole document to answer a question about one file costs
roughly 500x what the answer needs.

Do not scan the document for `BEGIN FILE` markers instead of using the index.
The index is authoritative, it was emitted by the same pass that wrote the
document, and scanning defeats the entire point of having ranges.

## Verify before you slice

The index records what the document was when it was generated:

| field | how to verify |
|---|---|
| `line_count` | recount the document's lines |
| `content_sha256` | rehash the document's exact bytes |
| `line_ending` | split on THAT terminator, always `lf` here |

On any mismatch the document was hand-edited or the pipeline was interrupted.
**STOP. Do not slice.** Regenerate, or read the file directly and say which you
did. A range from an unverified index is a guess wearing a line number.

```python
import hashlib, pathlib, re

doc = pathlib.Path("context_compass/system_docs/src_graph.md")
idx = pathlib.Path("context_compass/system_docs/src_graph_index.md").read_text(encoding="utf-8")

raw = doc.read_bytes()
claimed_lines = int(re.search(r"line_count \| (\d+)", idx).group(1))
claimed_hash = re.search(r"content_sha256 \| `([0-9a-f]{64})`", idx).group(1)

lines = raw.decode("utf-8").split("\n")
if lines and lines[-1] == "":
    lines.pop()

if len(lines) != claimed_lines or hashlib.sha256(raw).hexdigest() != claimed_hash:
    raise SystemExit("INDEX STALE - refusing to slice; regenerate the graph")
```

## Selecting what to read

Each index row is `| lines | source | nodes | edges |`. The `edges` count covers
both derived and authored edges, matching what that section's `Edges out` table
renders. Edge candidates are not counted - they are guesses, not edges.

- **Working one file**: match `source` against its path, read that range.
- **Working a subsystem**: match `source` against the directory prefix and read
  each matching range. Rows are ordered by source path, so a subsystem's files
  are contiguous.
- **Following a relationship**: a section's `Edges out` table gives fully
  qualified target ids. Map the id back to a path and look that row up.
- **Finding what points AT something**: the per-file sections carry outbound
  edges only. Inbound edges are not answerable from one section - you must
  either scan the index-selected sections you care about, or accept that
  reverse lookup is the one query this layout does not make cheap.

## What each section contains

- `source_sha256` of the source file at generation time. If you are reasoning
  about current code, check it against the file on disk, hashed the way the
  extractor hashes it: with CRLF turned into LF, so the answer is the same on
  every checkout.

  ```python
  import hashlib, pathlib

  raw = pathlib.Path("src/app/engine.py").read_bytes()
  current = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
  ```
- **Nodes**: id, kind (`module`, `class`, `interface`, `abstract`, `enum`,
  `record`), definition line, bases, markers, public methods, and the authored
  fields (`role`, `responsibilities`, `owns_state`, `phases`) when present.
- **Edges out**: one table, six columns - `from`, `relation`, `to`,
  `cardinality`, `phase`, `origin`. Derived edges (`specializes`, `implements`)
  carry `-` in the two authored columns, because those are design facts the
  extractor cannot produce. A row of dashes is not missing data; it is the graph
  telling you nobody has authored that relationship's semantics yet.
- **Why lines**: beneath the table, one per authored edge that carries a `why`.
  This is the justification for a claim the syntax tree cannot support - an
  authored `owns_lifecycle_of` asserts ownership where the AST shows only a
  reference. Read it before relying on the edge.
- **Edge candidates**: AST instantiation guesses. **Unconfirmed.** These
  over-generate roughly 8x against a hand-authored graph. Treat them as leads,
  never as evidence.
- **Published aliases**: module-level `Alias = Class` bindings, which are the
  names consumers actually import.

## Trust boundaries

Read every section with this in mind:

- Node identity, `bases`, and `specializes` are **mechanical** - derived from
  the syntax tree, measured at 94-98% agreement with a hand-authored graph.
- `role`, `responsibilities`, `owns_state`, `phases`, and any edge marked
  `authored` are **authored** by an agent or human who read the code.
- A node marked **UNSEMANTIC** has scaffold only. Its structure is trustworthy;
  its meaning has not been established. Do not infer purpose from a name.
- **`AUTHORED` measures field PRESENCE, not quality.** A node counts as authored
  the moment `role`, `responsibilities` or `owns_state` is non-empty - nothing
  inspects what is in them. Fields scraped from docstrings clear that bar while
  reading as fragments: sentences split mid-clause, bare section headers
  (`Attributes:`, `It ensures:`), clauses ending in a comma. Measured on one real
  graph, **158 of 502 nodes** were `AUTHORED` and unreadable in exactly this way.
  So "100% authored" can be true as measured and still overstate what you will
  find. Judge the prose, not the state.
- Edge candidates are **guesses**.

**Authored does not mean current.** The mechanical tier is rebuilt on every
extraction and is as fresh as the last run. Authored prose is written once and
stays exactly as written while the code underneath it moves. A node can carry a
confident, well-written `role` describing behaviour the class no longer has.

Two states exist to tell you which is which, and neither appears in the document
itself - ask the walker:

```bash
python context_compass/tools/system_documents/python/graph_walker.py \
    --descriptors <dir> --src src --report
```

| state | what it means for a reader |
| --- | --- |
| `AUTHORED` | the source has not changed since the prose was written |
| `SEMANTICS_STALE` | **unverified against the source it describes** - the source moved, or nobody ever checked it. Treat the prose as a lead, not a fact |
| `RETIRED` | the node is gone from source; its prose is kept for adjudication |

If a claim matters and the node is stale, **read the code**. Full loop:
`agent_onboarding/default/engineer/skills/src_graph_generation.md`.

Cite what you read with `path:start_line-end_line` against `src_graph.md`, the
same evidence convention used everywhere else in this repository.

## Anti-patterns

- Reading `src_graph.md` in full when the index would answer the question.
- Slicing without verifying `line_count` and `content_sha256` first.
- Treating an edge candidate as a real relationship.
- Treating an UNSEMANTIC node's name as a description of its purpose.
- Quoting a `source_sha256` as proof the code is current without comparing it
  to the file on disk.
- Relying on authored prose for a decision without checking whether the node is
  `SEMANTICS_STALE`. Well-written prose about code that has since changed reads
  exactly like well-written prose about code that has not.
- Filling in a node's semantics from its name because a generated ticket asked
  you to. `UNSEMANTIC` is honest; invented semantics read as verified.

References
- `agent_onboarding/default/engineer/skills/src_graph_generation.md`
- `agent_onboarding/default/engineer/skills/context_protocol.md`
- `agent_onboarding/default/general/skills/configuration_standards.md`
