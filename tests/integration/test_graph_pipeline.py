"""The graph pipeline end to end: extract, assemble, migrate.

The property that matters most here is that re-extraction does not destroy the
authored tier. `owns_lifecycle_of`, `uses` and `borrows` are the same syntax -
"A holds a reference to B" - so a fresh extraction produces a structurally
perfect graph with an empty authored layer, and nothing warns you, because an
empty authored layer is also what a brand new project looks like.
"""

from __future__ import annotations

import json

import pytest

from conftest import GRAPH_TOOLS, run_tool, write

pytestmark = pytest.mark.integration

EXTRACT = GRAPH_TOOLS / "extract_graph.py"
ASSEMBLE = GRAPH_TOOLS / "assemble_graph.py"
MIGRATE = GRAPH_TOOLS / "migrate_authored_graph.py"


@pytest.fixture
def descriptors(mock_source_tree, tmp_path):
    out = tmp_path / "desc"
    res = run_tool(EXTRACT, "--src", mock_source_tree, "--out", out)
    assert res.returncode == 0, res.stderr
    return out


def load(root, name):
    return json.loads((root / name).read_text())


class TestExtract:
    def test_one_descriptor_per_source_file(self, descriptors):
        produced = {p.relative_to(descriptors).as_posix()
                    for p in descriptors.rglob("*.json")}
        assert produced == {
            "app/__init__.json", "app/engine.json",
            "app/core/__init__.json", "app/core/iface.json", "app/core/kinds.json",
        }

    def test_init_files_are_included_by_default(self, descriptors):
        """In most projects `__init__.py` carries the package's public surface,
        so excluding it by default would drop the file that defines what a
        package exposes."""
        assert (descriptors / "app" / "__init__.json").is_file()

    def test_classes_are_extracted_with_ids_and_line_numbers(self, descriptors):
        nodes = load(descriptors, "app/engine.json")["nodes"]
        assert "app.engine.Engine" in nodes
        assert nodes["app.engine.Engine"]["label"] == "Engine"
        assert nodes["app.engine.Engine"]["lineno"] > 0

    def test_protocol_is_marked_an_interface(self, descriptors):
        nodes = load(descriptors, "app/core/iface.json")["nodes"]
        assert nodes["app.core.iface.IStore"]["kind"] == "interface"

    def test_abc_is_not_marked_an_interface(self, descriptors):
        """Deliberate: an abstract base and a Protocol play different roles in a
        graph - one is a supertype, the other a contract."""
        nodes = load(descriptors, "app/core/iface.json")["nodes"]
        assert nodes["app.core.iface.BaseWorker"]["kind"] == "abstract"

    def test_enum_is_marked(self, descriptors):
        nodes = load(descriptors, "app/core/kinds.json")["nodes"]
        assert nodes["app.core.kinds.Phase"]["kind"] == "enum"

    def test_inheritance_becomes_a_resolved_edge(self, descriptors):
        edges = load(descriptors, "app/engine.json")["edges_out"]
        assert {"from": "app.engine.Engine", "to_label": "BaseWorker",
                "relation": "specializes",
                "to": "app.core.iface.BaseWorker"} in edges

    def test_marker_bases_do_not_become_edges(self, descriptors):
        """`class IStore(Protocol)` specializes nothing. An edge to `Protocol`
        is a dangling reference to a node that will never exist."""
        edges = load(descriptors, "app/core/iface.json")["edges_out"]
        assert not any("Protocol" in str(e) or "ABC" in str(e) for e in edges)

    def test_instantiation_is_a_candidate_not_an_edge(self, descriptors):
        """Over-generated roughly 8x against the reference graph, so it is
        quarantined as a guess rather than asserted as an edge."""
        d = load(descriptors, "app/engine.json")
        assert any(c["to_label"] == "Stage" for c in d["edge_candidates"])
        assert not any(e.get("relation") == "creates" for e in d["edges_out"])

    # Broken on EVERY Python, which the first version of this fixture was not.
    # It used a PEP 701 f-string (nested quotes) because that was the real-world
    # case - but that syntax is *valid* from 3.12, so the test asserted a
    # SyntaxError that only happens on 3.10 and 3.11. Green on two versions of
    # the matrix and red on three, for a reason having nothing to do with the
    # code under test.
    UNPARSEABLE = "class Broken:\n    def s(self)\n        return 1\n"

    def test_an_unparseable_file_names_the_interpreter_version(self, mock_source_tree, tmp_path):
        """A file the running interpreter cannot parse gets no descriptor and
        every node in it silently vanishes. That is right when the file is
        broken and wrong when the file is simply NEWER than the interpreter -
        and the two look identical from here, so the message names the version
        that did the parsing.
        """
        write(mock_source_tree / "app" / "broken.py", self.UNPARSEABLE)
        res = run_tool(EXTRACT, "--src", mock_source_tree, "--out", tmp_path / "d")

        assert res.returncode == 0, "one bad file must not abort the run"
        assert "SKIP (syntax error)" in res.stderr
        assert "parsed with Python" in res.stderr
        assert "the interpreter is older than the code" in res.stderr

    def test_the_other_files_still_extract(self, mock_source_tree, tmp_path):
        write(mock_source_tree / "app" / "broken.py", self.UNPARSEABLE)
        out = tmp_path / "d"
        run_tool(EXTRACT, "--src", mock_source_tree, "--out", out)
        assert (out / "app" / "engine.json").is_file()

    def test_check_mode_writes_nothing(self, mock_source_tree, tmp_path):
        out = tmp_path / "desc2"
        run_tool(EXTRACT, "--src", mock_source_tree, "--out", out)
        before = {p: p.read_bytes() for p in out.rglob("*.json")}
        run_tool(EXTRACT, "--src", mock_source_tree, "--out", out, "--check")
        assert {p: p.read_bytes() for p in out.rglob("*.json")} == before


class TestAuthoredTierSurvivesReExtraction:
    """The single most important property in the pipeline."""

    def test_authored_node_fields_are_preserved(self, descriptors, mock_source_tree):
        path = descriptors / "app" / "engine.json"
        d = json.loads(path.read_text())
        d["nodes"]["app.engine.Engine"]["role"] = "drives the run loop"
        d["nodes"]["app.engine.Engine"]["responsibilities"] = ["schedule stages"]
        d["nodes"]["app.engine.Engine"]["owns_state"] = ["stages"]
        path.write_text(json.dumps(d, indent=2))

        res = run_tool(EXTRACT, "--src", mock_source_tree, "--out", descriptors)
        assert res.returncode == 0

        after = json.loads(path.read_text())["nodes"]["app.engine.Engine"]
        assert after["role"] == "drives the run loop"
        assert after["responsibilities"] == ["schedule stages"]
        assert after["owns_state"] == ["stages"]

    def test_authored_edges_are_preserved(self, descriptors, mock_source_tree):
        path = descriptors / "app" / "engine.json"
        d = json.loads(path.read_text())
        d["edges_authored"] = [{
            "from": "app.engine.Engine", "relation": "owns_lifecycle_of",
            "to": "app.engine.Stage", "cardinality": "one_to_many",
            "why": "Engine constructs its stages and is the only thing that "
                   "can release them.",
        }]
        path.write_text(json.dumps(d, indent=2))

        run_tool(EXTRACT, "--src", mock_source_tree, "--out", descriptors)
        after = json.loads(path.read_text())
        assert len(after["edges_authored"]) == 1
        assert after["edges_authored"][0]["relation"] == "owns_lifecycle_of"

    def test_mechanical_fields_do_refresh(self, descriptors, mock_source_tree):
        """Authored is preserved; mechanical is re-derived. Otherwise a moved
        class keeps a stale line number forever."""
        path = descriptors / "app" / "engine.json"
        d = json.loads(path.read_text())
        d["nodes"]["app.engine.Engine"]["lineno"] = 9999
        path.write_text(json.dumps(d, indent=2))

        run_tool(EXTRACT, "--src", mock_source_tree, "--out", descriptors)
        assert json.loads(path.read_text())["nodes"]["app.engine.Engine"]["lineno"] != 9999


class TestAssemble:
    def test_writes_document_and_index(self, descriptors, tmp_path):
        out = tmp_path / "system_docs"
        out.mkdir()
        res = run_tool(ASSEMBLE, "--descriptors", descriptors, "--out", out)
        assert res.returncode == 0, res.stderr
        assert (out / "src_graph.md").is_file()
        assert (out / "src_graph_index.md").is_file()

    def test_every_range_is_verified_before_writing(self, descriptors, tmp_path):
        out = tmp_path / "system_docs"
        out.mkdir()
        res = run_tool(ASSEMBLE, "--descriptors", descriptors, "--out", out)
        assert "verified" in res.stdout.lower()

    def test_index_ranges_land_on_their_own_delimiters(self, descriptors, tmp_path):
        """The index is a byproduct of assembly, so it cannot disagree with the
        document - this test is what proves that claim rather than assuming it."""
        out = tmp_path / "system_docs"
        out.mkdir()
        run_tool(ASSEMBLE, "--descriptors", descriptors, "--out", out)

        import re
        doc = (out / "src_graph.md").read_text().split("\n")
        index = (out / "src_graph_index.md").read_text()

        # Match the row shape, not "contains a dash" - the table separator
        # `| --- | --- |` also contains dashes and parses as a bogus range.
        rows = re.findall(r"^\| (\d+)-(\d+) \| `([^`]+)` \|", index, re.MULTILINE)
        assert len(rows) == 5, f"expected one row per source file, got {len(rows)}"
        for start, end, source in rows:
            assert doc[int(start) - 1] == f"<!-- BEGIN FILE: {source} -->"
            assert doc[int(end) - 1] == f"<!-- END FILE: {source} -->"

    def test_staleness_proof_matches_the_document(self, descriptors, tmp_path):
        import hashlib
        out = tmp_path / "system_docs"
        out.mkdir()
        run_tool(ASSEMBLE, "--descriptors", descriptors, "--out", out)

        raw = (out / "src_graph.md").read_bytes()
        index = (out / "src_graph_index.md").read_text()
        assert f"| content_sha256 | `{hashlib.sha256(raw).hexdigest()}` |" in index

    def test_authored_edges_render_with_why(self, descriptors, tmp_path):
        why = "Engine constructs its stages and is the only thing that can release them."
        path = descriptors / "app" / "engine.json"
        d = json.loads(path.read_text())
        d["edges_authored"] = [{
            "from": "app.engine.Engine", "relation": "owns_lifecycle_of",
            "to": "app.engine.Stage", "cardinality": "one_to_many",
            "phase": ["init", "cleanup"], "why": why,
        }]
        path.write_text(json.dumps(d, indent=2))

        out = tmp_path / "system_docs"
        out.mkdir()
        run_tool(ASSEMBLE, "--descriptors", descriptors, "--out", out)
        doc = (out / "src_graph.md").read_text()
        assert "| from | relation | to | cardinality | phase | origin |" in doc
        assert "one_to_many | init,cleanup | authored |" in doc
        assert why in doc

    def test_reassembly_is_idempotent(self, descriptors, tmp_path):
        out = tmp_path / "system_docs"
        out.mkdir()
        run_tool(ASSEMBLE, "--descriptors", descriptors, "--out", out)
        first = (out / "src_graph.md").read_bytes()
        run_tool(ASSEMBLE, "--descriptors", descriptors, "--out", out)
        assert (out / "src_graph.md").read_bytes() == first


class TestMigrate:
    @pytest.fixture
    def legacy(self, tmp_path):
        """A graph in the retired JSON format, carrying an authored tier."""
        p = tmp_path / "src_graph.expanded.json"
        p.write_text(json.dumps({
            "nodes": {
                "app.engine.Engine": {
                    "id": "app.engine.Engine", "label": "Engine",
                    "file": "src/app/engine.py",
                    "role": "drives the run loop",
                    "responsibilities": ["schedule stages"],
                },
            },
            "edges": [{
                "from": "app.engine.Engine", "to": "app.engine.Stage",
                "relation": "owns_lifecycle_of", "cardinality": "one_to_many",
                "why": "Engine constructs its stages.",
            }],
        }, indent=2))
        return p

    def test_check_reports_the_plan_and_writes_nothing(self, descriptors, legacy):
        before = {p: p.read_bytes() for p in descriptors.rglob("*.json")}
        res = run_tool(MIGRATE, "--legacy", legacy, "--descriptors", descriptors, "--check")
        assert res.returncode == 0
        assert "matched by id            : 1" in res.stdout
        assert {p: p.read_bytes() for p in descriptors.rglob("*.json")} == before

    def test_apply_writes_the_authored_tier_in(self, descriptors, legacy):
        res = run_tool(MIGRATE, "--legacy", legacy, "--descriptors", descriptors, "--apply")
        assert res.returncode == 0

        d = load(descriptors, "app/engine.json")
        assert d["nodes"]["app.engine.Engine"]["role"] == "drives the run loop"
        assert d["edges_authored"][0]["relation"] == "owns_lifecycle_of"
        assert d["edges_authored"][0]["why"] == "Engine constructs its stages."

    def test_refuses_without_apply(self, descriptors, legacy):
        res = run_tool(MIGRATE, "--legacy", legacy, "--descriptors", descriptors)
        assert res.returncode == 2
        assert "Refusing to act without --apply" in res.stdout

    def test_unmatched_nodes_are_reported_never_guessed(self, descriptors, tmp_path):
        """A node that cannot be located keeps its authored prose in the report
        so a human can place it. Guessing would silently attach someone's design
        rationale to the wrong class."""
        legacy = tmp_path / "legacy.json"
        legacy.write_text(json.dumps({
            "nodes": {"gone.Removed": {"id": "gone.Removed", "label": "Removed",
                                       "file": "src/gone.py", "role": "was a thing"}},
            "edges": [],
        }))
        res = run_tool(MIGRATE, "--legacy", legacy, "--descriptors", descriptors, "--check")
        assert "UNMATCHED                : 1" in res.stdout
        assert "gone.Removed" in res.stdout

    def test_migrated_graph_then_assembles(self, descriptors, legacy, tmp_path):
        """The round trip that actually matters: legacy JSON in, rendered
        document with why lines out."""
        run_tool(MIGRATE, "--legacy", legacy, "--descriptors", descriptors, "--apply")
        out = tmp_path / "system_docs"
        out.mkdir()
        res = run_tool(ASSEMBLE, "--descriptors", descriptors, "--out", out)
        assert res.returncode == 0

        doc = (out / "src_graph.md").read_text()
        assert "Engine constructs its stages." in doc
        assert "| authored |" in doc
        assert "- role: drives the run loop" in doc


class TestQualifiedResolution:
    def _extract(self, tmp_path, files):
        from conftest import write
        src = tmp_path / "src"
        for rel, text in files.items():
            write(src / rel, text)
        out = tmp_path / "desc"
        res = run_tool(EXTRACT, "--src", src, "--out", out)
        assert res.returncode == 0, res.stderr
        return out

    def _edges(self, out, name):
        import json
        return json.loads((out / name).read_text())["edges_out"]

    def test_qualified_plain_imports_resolve_independently(self, tmp_path):
        out = self._extract(tmp_path, {
            "left.py": "class Base:\n    pass\n",
            "right.py": "from typing import Protocol\n\n\nclass Base(Protocol):\n    def get(self) -> None: ...\n",
            "main.py": "import left\nimport right\n\n\nclass Foo(left.Base):\n    pass\n\n\nclass Bar(right.Base):\n    pass\n",
        })
        edges = self._edges(out, "main.json")
        foo = next(e for e in edges if e["from"] == "main.Foo")
        bar = next(e for e in edges if e["from"] == "main.Bar")
        assert foo["to_label"] == "Base"
        assert bar["to_label"] == "Base"
        assert foo["to"] == "left.Base"
        assert bar["to"] == "right.Base"
        assert foo["relation"] == "specializes"
        assert bar["relation"] == "implements"
        assert all("_to_dotted" not in e for e in edges)

    def test_qualified_unknown_and_shortname_not_redirected(self, tmp_path):
        out = self._extract(tmp_path, {
            "x.py": "class Base:\n    pass\n",
            "main.py": "from x import Base\n\n\nclass Local:\n    pass\n\n\nclass Foo(other.Base):\n    pass\n\n\nclass Bar(unknown.Base):\n    pass\n",
        })
        edges = self._edges(out, "main.json")
        assert all("to" not in e for e in edges)
        assert {e["to_label"] for e in edges} == {"Base"}

    def test_bare_builtin_resolves_but_function_and_qualified_root_do_not(self, tmp_path):
        out = self._extract(tmp_path, {
            "main.py": "class Good(ReferenceError):\n    pass\n\n\nclass BadLen(len):\n    pass\n\n\nclass BadQual(mystery.ReferenceError):\n    pass\n",
        })
        edges = self._edges(out, "main.json")
        good = next(e for e in edges if e["from"] == "main.Good")
        bad_len = next(e for e in edges if e["from"] == "main.BadLen")
        bad_qual = next(e for e in edges if e["from"] == "main.BadQual")
        assert good.get("to") == "builtins.ReferenceError"
        assert "to" not in bad_len
        assert "to" not in bad_qual

    def test_aliased_interface_implements_via_target(self, tmp_path):
        out = self._extract(tmp_path, {
            "pkg/__init__.py": "",
            "pkg/iface.py": "from typing import Protocol\n\n\nclass IStore(Protocol):\n    def get(self) -> None: ...\n",
            "pkg/main.py": "from pkg.iface import IStore as MyStore\n\n\nclass Foo(MyStore):\n    pass\n",
        })
        edges = self._edges(out, "pkg/main.json")
        assert len(edges) == 1
        assert edges[0]["to"] == "pkg.iface.IStore"
        assert edges[0]["relation"] == "implements"

    def test_dynamic_qualified_bases_do_not_fall_back_to_short_names(self, tmp_path):
        out = self._extract(tmp_path, {
            "other.py": "class Base:\n    pass\n",
            "main.py": (
                "from other import Base\n\n"
                "class DynamicImport(factory().Base):\n    pass\n\n"
                "class DynamicBuiltin(factory().ReferenceError):\n    pass\n"
            ),
        })
        edges = self._edges(out, "main.json")
        assert len(edges) == 2
        assert {edge["to_label"] for edge in edges} == {"Base", "ReferenceError"}
        assert all("to" not in edge for edge in edges)
        assert all("_to_dotted" not in edge for edge in edges)


class TestQualifiedR1:
    def _extract(self, tmp_path, files):
        from conftest import write
        src = tmp_path / "src"
        for rel, text in files.items():
            write(src / rel, text)
        out = tmp_path / "desc"
        res = run_tool(EXTRACT, "--src", src, "--out", out)
        assert res.returncode == 0, res.stderr
        return out

    def _edges(self, out, name):
        import json
        return json.loads((out / name).read_text())["edges_out"]

    def test_one_class_two_qualified_same_label_bases(self, tmp_path):
        out = self._extract(tmp_path, {
            "left.py": "class Base:\n    pass\n",
            "right.py": "from typing import Protocol\n\n\nclass Base(Protocol):\n    def get(self) -> None: ...\n",
            "main.py": "import left\nimport right\n\n\nclass Both(left.Base, right.Base):\n    pass\n",
        })
        edges = self._edges(out, "main.json")
        assert len(edges) == 2
        first = edges[0]
        second = edges[1]
        assert first["from"] == "main.Both"
        assert second["from"] == "main.Both"
        assert first["to_label"] == "Base"
        assert second["to_label"] == "Base"
        assert first["to"] == "left.Base"
        assert second["to"] == "right.Base"
        assert first["relation"] == "specializes"
        assert second["relation"] == "implements"
        assert all("_to_dotted" not in e for e in edges)

    def test_module_import_forms_and_generic_bases(self, tmp_path):
        out = self._extract(tmp_path, {
            "left.py": "class Base:\n    pass\n",
            "pkg/__init__.py": "",
            "pkg/sub.py": "class Base:\n    pass\n",
            "main.py": "import pkg.sub\nimport pkg.sub as ps\nfrom pkg import sub as submod\nimport left\n\n\nclass A(pkg.sub.Base):\n    pass\n\n\nclass B(ps.Base):\n    pass\n\n\nclass C(submod.Base):\n    pass\n\n\nclass D(left.Base[T]):\n    pass\n\n\nclass E(pkg.sub.Base[T]):\n    pass\n",
        })
        edges = self._edges(out, "main.json")
        by_from = {e["from"]: e for e in edges}
        assert by_from["main.A"]["to"] == "pkg.sub.Base"
        assert by_from["main.B"]["to"] == "pkg.sub.Base"
        assert by_from["main.C"]["to"] == "pkg.sub.Base"
        assert by_from["main.D"]["to"] == "left.Base"
        assert by_from["main.D"]["to_label"] == "Base"
        assert by_from["main.E"]["to"] == "pkg.sub.Base"
        assert by_from["main.E"]["to_label"] == "Base"
        assert all(e["relation"] == "specializes" for e in edges)
        assert all("_to_dotted" not in e for e in edges)

    def test_known_qualified_vs_unrelated_and_local_builtin_shadow(self, tmp_path):
        out = self._extract(tmp_path, {
            "known.py": "class Base:\n    pass\n",
            "x.py": "class Base:\n    pass\n",
            "main.py": "import known\nfrom x import Base\n\n\nclass Base:\n    pass\n\n\nclass Foo(known.Base):\n    pass\n\n\nclass ReferenceError:\n    pass\n\n\nclass Bar(ReferenceError):\n    pass\n\n\nclass Baz(mystery.ReferenceError):\n    pass\n",
        })
        edges = self._edges(out, "main.json")
        by_from = {e["from"]: e for e in edges}
        assert by_from["main.Foo"]["to"] == "known.Base"
        assert by_from["main.Foo"]["relation"] == "specializes"
        assert by_from["main.Bar"]["to"] == "main.ReferenceError"
        assert "to" not in by_from["main.Baz"]
        assert all("_to_dotted" not in e for e in edges)
