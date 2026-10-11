"""Unit tests for the graph pipeline: extraction helpers and assembly."""

from __future__ import annotations

import pathlib

import pytest

import assemble_graph as ag
import extract_graph as eg

pytestmark = pytest.mark.unit


class TestExtractHelpers:
    @pytest.mark.parametrize("rel,expected", [
        ("app/engine.py", "app.engine"),
        ("app/core/iface.py", "app.core.iface"),
        ("app/__init__.py", "app"),
        ("app/core/__init__.py", "app.core"),
    ])
    def test_module_id(self, rel, expected):
        assert eg.module_id(rel) == expected

    @pytest.mark.parametrize("name,expected", [
        ("Engine", "engine"),
        ("AethericFrame", "aetheric_frame"),
        ("HTTPServer", "h_t_t_p_server"),
        ("A", "a"),
    ])
    def test_snake(self, name, expected):
        assert eg.snake(name) == expected

    def test_is_excluded_matches_any_path_component(self):
        assert eg.is_excluded(pathlib.Path("a/__pycache__/b.py")) is True
        assert eg.is_excluded(pathlib.Path("a/node_modules/x/y.py")) is True
        assert eg.is_excluded(pathlib.Path("a/b/c.py")) is False

    def test_nested_build_dir_is_excluded(self):
        assert eg.is_excluded(pathlib.Path("src/app/build/gen.py")) is True


class TestSplitBases:
    def test_markers_are_separated_from_real_supertypes(self):
        """A `Protocol` base declares what a class IS. Emitting an edge to it
        produces a dangling reference to a node that never exists - 13% of
        extracted edges on the reference codebase."""
        graph, markers = eg.split_bases(["BaseWorker", "Protocol"])
        assert graph == ["BaseWorker"]
        assert markers == ["Protocol"]

    def test_stdlib_bases_are_not_graph_edges(self):
        graph, markers = eg.split_bases(["ValueError", "MyBase"])
        assert graph == ["MyBase"]
        assert "ValueError" in markers

    def test_noise_bases_are_markers(self):
        graph, markers = eg.split_bases(["object", "Generic"])
        assert graph == []
        assert set(markers) == {"object", "Generic"}

    def test_no_bases(self):
        assert eg.split_bases([]) == ([], [])


class TestClassKind:
    def test_protocol_is_an_interface(self):
        assert eg.class_kind(["Protocol"]) == "interface"

    def test_abc_is_abstract_not_interface(self):
        """Deliberate. A codebase commonly has both an abstract base that gets
        inherited and a Protocol mirroring the same surface. They play different
        roles in a graph, so only the Protocol is `interface`."""
        assert eg.class_kind(["ABC"]) == "abstract"

    def test_enum_variants(self):
        for m in ("Enum", "IntEnum", "StrEnum", "Flag"):
            assert eg.class_kind([m]) == "enum"

    def test_record_variants(self):
        for m in ("NamedTuple", "TypedDict", "dataclass"):
            assert eg.class_kind([m]) == "record"

    def test_noise_markers_carry_no_kind(self):
        assert eg.class_kind(["object", "Generic"]) == "class"

    def test_no_markers_is_a_plain_class(self):
        assert eg.class_kind([]) == "class"


class TestMergeRestoration:
    @pytest.mark.parametrize("candidate_file", ["src/demo.py", "src/other.py"])
    def test_exact_retired_id_precedes_live_rename_candidates(self, candidate_file):
        nid = "demo.Resource"
        retired = {"id": nid, "label": "Resource", "file": "src/demo.py",
                   "role": "returning resource", "semantics_authored_against": "old-span"}
        candidate = {"id": "old.Resource", "label": "Resource", "file": candidate_file,
                     "role": "different resource"}
        unrelated = {"id": "demo.Absent", "role": "still retired"}
        edges = [{"from": nid, "relation": "uses", "to": "demo.Absent",
                  "why": "Retain the authored relationship"}]
        old = {"nodes": {"old.Resource": candidate},
               "nodes_retired": {nid: retired, "demo.Absent": unrelated},
               "edges_authored": edges}
        new = {"nodes": {nid: {"id": nid, "label": "Resource", "file": "src/demo.py",
                               "span_sha256": "new-span"}}}

        merged, notes = eg.merge(new, old)

        assert merged["nodes"][nid]["role"] == "returning resource"
        assert merged["nodes"][nid]["semantics_authored_against"] == "old-span"
        assert merged["nodes"][nid]["span_sha256"] == "new-span"
        assert nid not in merged["nodes_retired"]
        assert merged["nodes_retired"]["old.Resource"] == {
            **candidate, "retired_reason": "gone from source"}
        assert merged["nodes_retired"]["demo.Absent"] == unrelated
        assert merged["edges_authored"] == edges
        assert old["nodes_retired"] == {nid: retired, "demo.Absent": unrelated}
        assert not any(note.startswith(f"RECOVERED node {nid}") for note in notes)

    @pytest.mark.parametrize("authored", [{}, {"role": "live", "semantics_authored_against": "live-span"}])
    def test_exact_live_id_precedes_a_duplicate_retired_entry(self, authored):
        nid = "demo.Resource"
        old = {"nodes": {nid: {"id": nid, **authored}},
               "nodes_retired": {nid: {"id": nid, "role": "retired",
                                       "responsibilities": ["Do not resurrect this"],
                                       "semantics_authored_against": "retired-span"}}}
        mechanical = {"id": nid, "span_sha256": "live-span"}

        merged, _ = eg.merge({"nodes": {nid: dict(mechanical)}}, old)

        assert merged["nodes"][nid] == {**mechanical, **authored}
        assert nid not in merged.get("nodes_retired", {})

    def test_retired_nodes_are_not_matched_by_file_or_label(self):
        retired = {"id": "old.Resource", "label": "Resource", "file": "src/demo.py",
                   "role": "not the returning node"}
        old = {"nodes": {}, "nodes_retired": {"old.Resource": retired}}
        mechanical = {"id": "demo.Resource", "label": "Resource", "file": "src/demo.py"}

        merged, notes = eg.merge({"nodes": {"demo.Resource": dict(mechanical)}}, old)

        assert merged["nodes"]["demo.Resource"] == mechanical
        assert merged["nodes_retired"] == old["nodes_retired"]
        assert not any(note.startswith("RESTORED") for note in notes)


class TestFmtCell:
    @pytest.mark.parametrize("value", [None, "", []])
    def test_absent_renders_a_dash(self, value):
        assert ag.fmt_cell(value) == "-"

    def test_list_is_comma_joined(self):
        assert ag.fmt_cell(["init", "runtime"]) == "init,runtime"

    def test_scalar_is_stringified(self):
        assert ag.fmt_cell("one_to_many") == "one_to_many"
        assert ag.fmt_cell(3) == "3"

    def test_tuple_behaves_like_a_list(self):
        assert ag.fmt_cell(("a", "b")) == "a,b"


def descriptor(source: str, **extra) -> dict:
    base = {
        "source": source,
        "source_sha256": "0" * 64,
        "nodes": {
            f"{source}.Thing": {
                "id": f"{source}.Thing", "label": "Thing", "kind": "class",
                "file": source, "lineno": 1,
            }
        },
    }
    base.update(extra)
    return base


class TestAssemble:
    def test_sections_bracket_their_own_delimiters(self):
        doc, sections = ag.assemble([descriptor("src/a.py"), descriptor("src/b.py")])
        assert ag.verify(doc, sections) == []

    def test_ranges_are_one_based_and_inclusive(self):
        doc, sections = ag.assemble([descriptor("src/a.py")])
        lines = doc.split("\n")
        s = sections[0]
        assert lines[s["start"] - 1] == "<!-- BEGIN FILE: src/a.py -->"
        assert lines[s["end"] - 1] == "<!-- END FILE: src/a.py -->"

    def test_edge_count_includes_authored_edges(self):
        """The index column must match what the section renders. Counting only
        `edges_out` undercounts exactly the edges that carry design meaning -
        68% of relationships are not derivable."""
        d = descriptor(
            "src/a.py",
            edges_out=[{"from": "A", "relation": "specializes", "to": "B"}],
            edges_authored=[{"from": "A", "relation": "owns_lifecycle_of", "to": "C"},
                            {"from": "A", "relation": "borrows", "to": "D"}],
        )
        _, sections = ag.assemble([d])
        assert sections[0]["edges"] == 3

    def test_authored_edges_render_six_columns(self):
        d = descriptor("src/a.py", edges_authored=[{
            "from": "A", "relation": "owns_lifecycle_of", "to": "B",
            "cardinality": "one_to_many", "phase": ["init", "runtime"],
            "why": "A constructs B and is the only thing that can release it.",
        }])
        doc, _ = ag.assemble([d])
        assert "| from | relation | to | cardinality | phase | origin |" in doc
        assert "| `A` | owns_lifecycle_of | `B` | one_to_many | init,runtime | authored |" in doc

    def test_why_renders_beneath_the_table(self):
        why = "A constructs B and is the only thing that can release it."
        d = descriptor("src/a.py", edges_authored=[
            {"from": "A", "relation": "owns_lifecycle_of", "to": "B", "why": why}])
        doc, _ = ag.assemble([d])
        assert f"- `A` -> `B`: {why}" in doc
        table_at = doc.index("| from | relation |")
        assert doc.index(why) > table_at, "why belongs below the table, not in it"

    def test_derived_edges_carry_dashes_in_the_authored_columns(self):
        """Not missing data: the graph saying nobody has authored that
        relationship's semantics yet."""
        d = descriptor("src/a.py",
                       edges_out=[{"from": "A", "relation": "specializes", "to": "B"}])
        doc, _ = ag.assemble([d])
        assert "| `A` | specializes | `B` | - | - | derived |" in doc

    def test_footer_carries_the_source_path_not_a_node_id(self):
        """Regression shape: naming the why-loop variable `src` shadowed the
        section's source path and emitted a node id into the footer."""
        d = descriptor("src/a.py", edges_authored=[
            {"from": "pkg.mod.Alpha", "relation": "uses", "to": "pkg.mod.Beta",
             "why": "because"}])
        doc, sections = ag.assemble([d])
        assert doc.split("\n")[sections[0]["end"] - 1] == "<!-- END FILE: src/a.py -->"
        assert ag.verify(doc, sections) == []

    def test_unsemantic_marker_on_nodes_with_no_authored_meaning(self):
        doc, _ = ag.assemble([descriptor("src/a.py")])
        assert "**UNSEMANTIC**" in doc

    def test_authored_node_suppresses_the_unsemantic_marker(self):
        d = descriptor("src/a.py")
        d["nodes"]["src/a.py.Thing"]["role"] = "does a thing"
        doc, _ = ag.assemble([d])
        assert "**UNSEMANTIC**" not in doc

    def test_preamble_does_not_contain_a_parseable_delimiter(self):
        """A file's own documentation must not be parseable as its own data. An
        earlier version spelled the marker inline and a validator counted 576
        sections where 575 existed."""
        doc, sections = ag.assemble([descriptor("src/a.py")])
        preamble = doc[:doc.index("<!-- BEGIN FILE:")]
        assert "BEGIN FILE:" not in preamble
        assert doc.count("<!-- BEGIN FILE:") == len(sections)

    def test_assemble_preserves_input_order(self):
        """Sorting is `load_descriptors`' job, not `assemble`'s. Keeping the
        split means a caller can assemble a deliberate subset in a chosen order
        without the renderer second-guessing it."""
        _, sections = ag.assemble([descriptor("src/b.py"), descriptor("src/a.py")])
        assert [s["source"] for s in sections] == ["src/b.py", "src/a.py"]


class TestVerify:
    def test_wrong_start_is_caught(self):
        doc, sections = ag.assemble([descriptor("src/a.py")])
        sections[0]["start"] += 1
        assert any("start" in p for p in ag.verify(doc, sections))

    def test_wrong_end_is_caught(self):
        doc, sections = ag.assemble([descriptor("src/a.py")])
        sections[0]["end"] -= 1
        assert any("end" in p for p in ag.verify(doc, sections))

    def test_overlapping_sections_are_caught(self):
        doc, sections = ag.assemble([descriptor("src/a.py"), descriptor("src/b.py")])
        sections[0]["end"] = sections[1]["start"]
        assert any("overlap" in p for p in ag.verify(doc, sections))


class TestRenderIndex:
    def test_staleness_proof_matches_the_document(self):
        import hashlib
        doc, sections = ag.assemble([descriptor("src/a.py")])
        index = ag.render_index(doc, sections)
        assert f"| content_sha256 | `{hashlib.sha256(doc.encode()).hexdigest()}` |" in index
        assert f"| line_count | {len(doc.split(chr(10))) - 1} |" in index
        assert f"| sections | {len(sections)} |" in index

    def test_rows_are_keyed_by_source_path_not_by_number(self):
        """No index in this system uses a bare number as identity: a row keyed
        by a number tells a reader nothing about whether to read it."""
        doc, sections = ag.assemble([descriptor("src/a.py")])
        index = ag.render_index(doc, sections)
        assert "| `src/a.py` |" in index
