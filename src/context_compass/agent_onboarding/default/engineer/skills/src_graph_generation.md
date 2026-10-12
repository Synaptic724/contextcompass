
# src_graph_generation

Purpose
- Define how to BUILD and MAINTAIN the assembled source graph.

## The pipeline

Two stages, two scripts, both stdlib-only:

```
tools/system_documents/python/extract_graph.py     source tree -> per-file descriptors
tools/system_documents/python/assemble_graph.py    descriptors -> src_graph.md + index
```

```bash
python context_compass/tools/system_documents/python/extract_graph.py \
    --src src --out context_compass/system_docs/graph

python context_compass/tools/system_documents/python/assemble_graph.py \
    --descriptors context_compass/system_docs/graph \
    --out context_compass/system_docs
```

`--check` on either script reports without writing. Run it before assuming the
graph is current.

## Resolving inheritance targets

The Python extractor resolves bases through their source expressions and import
bindings, without importing or executing the project's code.

- Plain imports, module aliases and `from` aliases preserve the qualified target.
  `import package.sub` binds `package`; `import package.sub as sub` binds `sub`.
- Each base expression is resolved independently. Two bases named `Base` from
  different modules remain separate relationships, even on the same class.
- A qualified base does not fall back to an unrelated import, local class or
  builtin with the same short name. Unknown roots and dynamic expressions such
  as `factory().Base` remain unresolved rather than receiving a guessed target.
- Eligible bare builtin classes resolve only after imports and local class
  definitions. Builtin functions are not class targets. Existing declaration
  markers and filtered stdlib bases remain markers, not new graph edges.
- `implements` follows the resolved interface ID, not a matching short label in
  another module. Generic base subscripts retain their underlying class target.

Descriptor layout and node IDs are unchanged. `to_label` remains the short
display name; resolved edges carry the qualified `to` ID. Temporary expression
metadata is not saved. Re-extraction still preserves authored fields and stamps,
including when an exact retired node ID returns.

## A file the interpreter cannot parse leaves the graph silently

`extract_graph.py` walks source with `ast.parse`. A file that raises `SyntaxError`
gets no descriptor, so every node in it disappears from the assembled document -
and the run still succeeds, because one unreadable file is not a reason to abandon
the other several hundred.

That is correct when the file is broken. It is wrong when the file is merely
**newer than the interpreter**, and the two are indistinguishable at the parse
site. Measured case: a PEP 701 f-string (nested quotes inside an f-string) parses
on 3.12+ and raises on 3.10, so a graph extracted with an older Python came out one
class short, every `Key Files (C1)` citation into that class stopped resolving, and
the summary said nothing was wrong.

Two defences, and use both:

- The run prints a **`SKIPPED - NOT IN THE GRAPH`** block naming every file and its
  reason, including the Python version that did the parsing. Read it. It is
  deliberately separate from the census, because the census counts nodes that exist
  and these do not.
- Pass **`--strict`** to exit non-zero when anything was skipped:

```bash
python context_compass/tools/system_documents/python/extract_graph.py \
    --src src --out context_compass/system_docs/graph --strict
```

`--strict` is opt-in rather than the default so existing invocations keep their exit
semantics, but an unattended or CI run should always set it. Without it the only
signal is a line of stdout that nobody is reading.

**Check the interpreter before concluding the file is broken.** Compare
`python -V` against the project's `requires-python`. If the interpreter is older,
the file is fine and the graph is not - re-run on the version the project targets.

Three more scripts exist for cases the pipeline alone cannot serve:

```
tools/system_documents/python/graph_walker.py             state of the authored tier
tools/system_documents/python/graph_semantics_tickets.py  turn unauthored areas into work
tools/system_documents/python/migrate_authored_graph.py   carry a retired-format graph in
```

## Keeping the authored tier honest

The mechanical tier self-heals - re-run the extractor and classes, bases and line
numbers are right again. **The authored tier does not.** It is written once, and
without help nothing says which parts are still true. Left alone that produces a
graph full of confident descriptions of code that no longer works that way.

Four states, and the walk through them is the maintenance loop:

| state | meaning | what to do |
| --- | --- | --- |
| `UNSEMANTIC` | no authored fields | author it, by reading the code |
| `AUTHORED` | authored, source unchanged since | nothing |
| `SEMANTICS_STALE` | authored, but **not verified against the source it describes** - either its source moved, or nobody ever checked it | read the source, then accept |

**An unstamped node is SEMANTICS_STALE.** The stamp means one thing: a human read
this prose against this source. Only `--accept` creates it. Authored prose with no
stamp has never had that done, so it is unverified, and unverified is stale.

The extractor used to auto-stamp those nodes against current source so they would
report AUTHORED - asserting, on nobody's behalf, that prose it never read matched
code it never compared. That made `SEMANTICS_STALE: 0` reachable without a single
node having been checked, so an epic with that success metric could pass having
verified nothing. Removed.

The first run after upgrading an existing graph will report a large stale count.
That count is correct, and it is the number being told to you for the first time -
not a regression.
| `RETIRED` | gone from source, prose retained | adjudicate: move it or drop it |

```bash
python context_compass/tools/system_documents/python/graph_walker.py \
    --descriptors context_compass/system_docs/graph --src src --report
```

Read-only. It aggregates by package rather than by node, because per-node output
on a real codebase is thousands of lines nobody reads, and a subsystem is the
unit an agent actually works in.

Staleness is tracked **per node**, not per file: a file-level hash would mark all
forty classes in a module stale because one changed, and a census that cries wolf
gets ignored.

Once you have RE-READ a stale node and confirmed its semantics still hold:

```bash
python context_compass/tools/system_documents/python/graph_walker.py \
    --descriptors <dir> --accept app.mod.Alpha --apply
```

That re-stamps; it changes no prose. **Accepting without reading is how a graph
becomes confidently wrong** - the stamp is meant to record that someone checked,
and it cannot tell the difference.

### Nothing deletes authored prose automatically

A node that disappears from source keeps its authored fields under
`nodes_retired` in the same descriptor, and is reported. Earlier this was a real
defect: the note said `ORPHANED - resolve by hand` while the same pass wrote the
prose out of the file, so the only copy was in git and only if you noticed.

The walker also reports **stranded descriptors** - ones whose source file is gone
entirely. The extractor walks source, so it never opens those and their nodes
count as live forever; only a pass starting from the descriptors can see it.
Pass `--src` to enable that check.

Possible cross-file moves are **suggested, never applied**. A same-label match is
evidence, not proof, and attaching someone's authored prose to the wrong class is
worse than leaving it retired where they can see it.

### Deleting for real: `--reconcile`

When a retirement is genuinely a deletion - the thing is gone and its meaning is
not coming back - clear it:

```bash
python context_compass/tools/system_documents/python/graph_walker.py \
    --descriptors <dir> --reconcile
```

**This is the only sanctioned path for structural deletion, and the only verb in
the subsystem that destroys authored work.** It lists every node and its prose,
then asks. Without a terminal it refuses rather than assuming - a prompt that
silently self-answers in CI is not a prompt. `--yes` answers it deliberately.

Before running it, check `--report` for possible moves. If a retirement is really
a rename, copy the authored fields onto the new node first; afterwards the only
copy is in version control.

## Turning the backlog into work - ON DEMAND

Resolve the ticket backend first. The `--create` command below writes local
ticket files and applies only to `local`. With `github_codex_plugin`, use the
dry-run findings to compose the existing Epic/Story/Task bodies through the
plugin instead; keep local ticket folders inactive for that work.

The helper reads `config/context_compass_config.yaml` beside the selected ticket
lane. It refuses `--create` in plugin mode and previews only the graph census,
without reading local ticket archives. Its dependency-free selector supports
the published YAML block format; ambiguous, merged, or flow-form selectors stop
the helper before it can write. Missing legacy config still means local.

```bash
python context_compass/tools/system_documents/python/graph_semantics_tickets.py \
    --descriptors <dir> --tickets context_compass/tickets            # dry run
    ... --create --yes                                               # write them
```

**Off by default and prompted.** Nothing generates tickets as part of extraction
or assembly. A tool that writes into someone's board without being asked is doing
something hostile, so this is a separate command, a dry run unless you say
`--create`, and a question unless you say `--yes`.

**Aggregated at the package**, and that is a hard constraint rather than a
preference. Measured against a real 575-file, 1,188-node graph with 657 nodes
unauthored:

| granularity | stories | outcome |
| --- | --- | --- |
| per node | 657 | destroys the board |
| per file | 575 | destroys the board |
| per directory (default) | 146 | still too many |
| `--depth 4` | **36** | usable |
| `--min-nodes 5` | **46** | usable |

The attention board is a routing surface carrying about a dozen active rows. A
package is also the unit an agent actually works in - a subsystem at a time - so
it is the natural granularity as well as the survivable one.

**The default is the containing directory, and on a deep tree that is still too
many.** `--depth N` groups at a shallower level; `--min-nodes N` skips the
scraps. Once the count passes 50 the tool prints both levers with the counts
they would produce, rather than emitting 146 stories and letting you discover it
afterwards. Neither loses work - the nodes stay in the census either way, only
the packaging changes.

A design brief for this feature estimated ~33 stories from
`_package_candidates.json`. That file counts directories whose files share a
naming *suffix* - a different concept from the directory a file lives in - so the
real directory-level figure was 146. Worth knowing before you trust an estimate
from either source.

You get **one epic and one story per package with work**. Tasks are deliberately
not generated: task granularity is the working agent's judgement, and
pre-generating it presumes an approach to work nobody has started.

Re-running **updates** rather than duplicating - ticket ids derive from the
package path, and completed lanes are searched too. A package that gets fully
authored is reported `SATISFIED` so you can close its story. The loop closes in
both directions or it is just a different kind of noise.

Generated tickets are **drafts** and touch no board. Route them yourself: a
generated ticket claiming an active row is a row nobody agreed to take.

### What a generated story must not become

Every generated story states that semantics are authored **by reading the code**.
Take that literally. `owns_lifecycle_of`, `uses` and `borrows` are the same
syntax - `self._x = x` in all three - and the difference is design intent that
appears nowhere in the source text. A cleanup-contract heuristic was tested
against a labelled corpus and discriminated at 21% versus 21%: no signal at all.

Filling a generated ticket with plausible prose inferred from class names is
worse than leaving those nodes unsemantic, because `UNSEMANTIC` is honest and
invented semantics read as verified.

The layout is `tools/system_documents/<language>/`. The descriptor contract is
language-neutral; only the extractor is Python-specific. A sibling directory can
implement the same contract for another language.

## Why per-file descriptors

The unit is the source file, because that is the unit that changes.

Earlier drafts sharded a single generated blob by namespace and bin-packed it to
a line budget. That produced unstable boundaries - adding one node reflowed the
packer and silently moved unrelated nodes between shards - and meaningless
names. Anchoring to the source path fixes both: a file is a file, its descriptor
mirrors its path, and touching one file dirties exactly one descriptor.

It also makes the size problem disappear. Source files are already
human-sized, so descriptors are too: median 43 lines, p90 83, none over 400,
with no budget parameter anywhere.

## The three tiers, and who owns them

This is the contract that makes regeneration safe.

| tier | owner | fields |
|---|---|---|
| mechanical | the script | `id`, `label`, `kind`, `file`, `lineno`, `bases`, `markers`, `public_methods`, `shape`, `source_sha256`, `specializes`/`implements` edges |
| curation | authored | `include` |
| semantics | authored | `role`, `responsibilities`, `owns_state`, `phases`, `edges_authored` |

**On re-run the script refreshes tier 1 and never touches tiers 2 and 3.** That
is verified behaviour, not an intention - inject an authored field, re-run, and
it survives.

## The authored schema

These are the fields you may populate. Nothing generates them and nothing
validates them, so this list is the contract.

### Node fields

| field | shape | meaning |
|---|---|---|
| `include` | bool | belongs in the composed graph. Absent means "not triaged", which is not the same as `false`. |
| `role` | prose, one line | what this object is for. |
| `responsibilities` | list of short phrases | what it is on the hook for. |
| `owns_state` | list of attribute names | fields whose lifecycle it controls. |
| `phases` | list | when in its life it matters: `init`, `validation`, `runtime`, `refresh`, `cleanup`. Open set - add one if your system needs it, but reuse these first. |

### Edge fields, under `edges_authored`

| field | shape | rendered |
|---|---|---|
| `from` | node id | yes, table |
| `to` | node id | yes, table |
| `relation` | `owns_lifecycle_of`, `uses`, `borrows`, `holds`, `owns`, `used_by` | yes, table |
| `cardinality` | `one_to_one`, `one_to_many`, `many_to_one` | yes, table |
| `phase` | list, same vocabulary as node `phases` | yes, table |
| `why` | prose, one or two sentences | yes, beneath the table |
| `strength` | `hard`, `borrowed`, `soft` | **no - see below** |

**`strength` is stored and deliberately not rendered.** Measured against a
hand-authored graph of 997 edges it is ~97% recoverable from `relation`:
`hard` is the ownership relations, `borrowed` is the reference relations. A
column that restates the column beside it costs space and adds nothing. Keep
populating it if your tooling consumes it; the document will not show it.

**`why` is rendered because it is the justification for a claim the extractor
says it cannot make.** An authored `owns_lifecycle_of` asserts ownership where
the syntax tree shows only a reference. Recording why, and showing it, is the
difference between evidence and assertion. It sits beneath the table so the
table stays scannable.

The prose does not cost you a whole-document read, because there is no such
thing here: you read the index and slice one section. A few extra lines inside
the one section you asked for is not a cost worth optimising against.

## What the script cannot do, and why

Do not expect the extractor to produce a finished graph. Measured against a
hand-authored graph of 535 nodes and 997 edges:

- node identity: **94%** recovered (matching on file + label)
- `specializes` edges: **94%** recovered with fully-qualified ids on both ends
- edge target resolution via imports: **99%**
- **68% of all edges are not derivable at all**

`owns_lifecycle_of` (205 edges), `uses` (323), and `borrows` (119) are
syntactically identical. Every one is "A holds a reference to B". Whether A owns
B's lifecycle, merely uses it, or borrows it without owning is a design fact
that does not appear anywhere in the source text. The same is true of every
`role`, `why`, `cardinality`, and `strength`.

Curation is equally underivable. The best syntactic significance rule tested
would have suppressed 419 nodes while wrongly dropping 63 that the reference
graph deliberately includes. So the script emits inventory and records `shape`
signals; the `include` field is authored. Emitting a node the author can reject
is recoverable. Silently withholding one they wanted is not.

## Maintenance loop

When you change a source file:

1. Re-run `extract_graph.py`. Only that file's descriptor changes.
2. Read the drift report. It names nodes that are `NEW`, `ORPHANED` (gone from
   source but still carrying authored semantics), or `UNSEMANTIC`.
3. Author the semantics for anything new. Resolve orphans by hand - the script
   will not delete authored prose on your behalf.
4. Re-run `assemble_graph.py` to rebuild the document and index together.

Never regenerate one without the other. They are only guaranteed consistent
because a single pass emits both.

## The index is a byproduct

`assemble_graph.py` knows each section's line range because it emitted those
lines. It does not re-parse the document to find headings.

That removes a whole class of drift. An index generated by re-walking a
document can disagree with the document, and the only defence is a hash. Here
they cannot disagree. The hash is still recorded, but it guards a different
failure: someone hand-editing the assembled file.

Every range is verified against its own header on every run. An off-by-one here
silently corrupts every downstream read, so it is checked rather than trusted.

## What this replaced

The two generated JSON graph files - a readable graph of 776 KB and a raw graph
of 768 KB - are retired. Together they were 1,544 KB that had to be read whole
or not at all, because a JSON object has no addressable interior.

The replacement is 972 KB of Markdown plus a 62 KB index, and a typical query
reads a 20-40 line slice.

**If you arrive holding a graph in the retired format, do not run the two-command
sequence and hope.** Only `specializes` and `implements` are mechanical, so a
naive re-extraction marks every node `UNSEMANTIC` and drops every authored edge.
Measured on a mature graph that was 84% of its edges. The rule generalises: the
better your existing graph, the more the naive path destroys, because a mature
graph is edge-richer than a young one. Carry the authored tier across by node id
first, then by `(file, label)`, before you assemble anything.

## Anti-patterns

- Hand-editing `src_graph.md` or `src_graph_index.md`. Edit descriptors, reassemble.
- Regenerating the document without the index, or the reverse.
- Deleting a descriptor whose node still carries authored semantics.
- Filtering descriptor files by filename prefix. An earlier version of the
  assembler skipped anything starting with `_` to avoid manifests, and silently
  swallowed 14 real files including `__init__.py` and every dunder module. A
  prefix is a naming convention, not a type.
- Promoting an edge candidate to an edge without reading the code.
- **Reading `skipped=N` in the summary as harmless.** A skipped file is not a
  partial result, it is an absent one: the graph is wrong rather than incomplete,
  and nothing downstream can tell. Run with `--strict` so it cannot pass silently.
- **Treating a `SyntaxError` from the extractor as a defect in the source file.**
  Check `python -V` against the project's `requires-python` first; an interpreter
  older than the code produces exactly this signature.
- **Writing `context_compass/...` into a descriptor's authored prose.** The
  generated document is clean today - it cites the source tree constantly and
  names this package nowhere - and that is only true because nothing has typed a
  tool path into a `role`, `responsibilities`, or `why` field. Those fields flow
  straight through the assembler into `src_graph.md`, which ships with the
  codebase to readers who do not have Context Compass. Cite the source; if a
  reader needs the regeneration command, they are in this skill already.
- Absolute paths in a descriptor. Repo-relative, or the document is correct on
  one machine.

References
- `agent_onboarding/default/engineer/skills/src_graph_usage.md`
- `agent_onboarding/default/engineer/skills/staleness_protocol.md`
- `agent_onboarding/default/engineer/skills/context_protocol.md`
