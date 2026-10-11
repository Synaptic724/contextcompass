"""The authoring lifecycle: retention, staleness, and the walker.

The mechanical tier self-heals. The authored tier does not, and before this
there was no state for "this node still exists, its source changed, and its
authored meaning may now be wrong". These tests cover the four states and the
one defect that was losing prose outright.
"""

from __future__ import annotations

import json

import pytest

from conftest import GRAPH_TOOLS, run_tool, write

pytestmark = pytest.mark.integration

EXTRACT = GRAPH_TOOLS / "extract_graph.py"
WALKER = GRAPH_TOOLS / "graph_walker.py"

TWO_CLASSES = """\
class Alpha:
    def run(self):
        return 1


class Gamma:
    def go(self): ...
"""


@pytest.fixture
def graph(tmp_path):
    """A source tree with two authored classes, both accepted against source.

    The stamps are earned via `--accept`, which is now the ONLY thing that mints
    one. This fixture used to get them for free from the extractor's grandfathering
    - it auto-stamped unverified prose so it would read as AUTHORED. That is gone,
    so the setup has to do what a human would: author, then accept.
    """
    src, desc = tmp_path / "src", tmp_path / "desc"
    write(src / "app" / "thing.py", TWO_CLASSES)
    assert run_tool(EXTRACT, "--src", src, "--out", desc).returncode == 0

    p = desc / "app" / "thing.json"
    d = json.loads(p.read_text())
    for label in ("Alpha", "Gamma"):
        d["nodes"][f"app.thing.{label}"]["role"] = f"authored for {label}"
    p.write_text(json.dumps(d, indent=2))

    run_tool(EXTRACT, "--src", src, "--out", desc)
    for label in ("Alpha", "Gamma"):
        assert run_tool(WALKER, "--descriptors", desc,
                        "--accept", f"app.thing.{label}", "--apply").returncode == 0
    return src, desc, p


def nodes(p):
    return json.loads(p.read_text())["nodes"]


class TestOrphanRetention:
    def test_authored_prose_survives_deletion_from_source(self, graph):
        """The defect: `merge()` reported ORPHANED and then returned a descriptor
        built from the new node set, so the prose was written out of the file in
        the same pass. It said "resolve by hand" after removing the thing you
        would resolve with."""
        src, desc, p = graph
        write(src / "app" / "thing.py", "class Alpha:\n    def run(self):\n        return 1\n")
        res = run_tool(EXTRACT, "--src", src, "--out", desc)
        assert res.returncode == 0

        d = json.loads(p.read_text())
        assert "app.thing.Gamma" not in d["nodes"], "must leave the live node set"
        retired = d["nodes_retired"]["app.thing.Gamma"]
        assert retired["role"] == "authored for Gamma"
        assert retired["retired_reason"] == "gone from source"

    def test_retirement_is_reported(self, graph):
        src, desc, p = graph
        write(src / "app" / "thing.py", "class Alpha:\n    def run(self):\n        return 1\n")
        res = run_tool(EXTRACT, "--src", src, "--out", desc)
        assert "ORPHANED" in res.stdout
        assert "RETAINED" in res.stdout

    @pytest.mark.parametrize("changed", [False, True], ids=["unchanged", "changed"])
    @pytest.mark.parametrize("stamped", [False, True], ids=["unverified", "accepted"])
    def test_a_node_that_comes_back_retains_its_authored_content(self, graph, changed, stamped):
        src, desc, p = graph
        nid = "app.thing.Gamma"
        d = json.loads(p.read_text())
        before = d["nodes"][nid]
        authored = {
            "include": False,
            "role": "authored for Gamma",
            "responsibilities": ["Keep the authored explanation"],
            "owns_state": [],
            "phases": ["runtime"],
        }
        before.update(authored)
        if stamped:
            authored["semantics_authored_against"] = before["semantics_authored_against"]
        else:
            del before["semantics_authored_against"]
        p.write_text(json.dumps(d, indent=2))

        write(src / "app" / "thing.py", "class Alpha:\n    def run(self):\n        return 1\n")
        res = run_tool(EXTRACT, "--src", src, "--out", desc)
        assert res.returncode == 0, res.stderr
        retired = json.loads(p.read_text())["nodes_retired"][nid]
        assert {field: retired[field] for field in authored} == authored

        source = "\n" + TWO_CLASSES
        if changed:
            source = source.replace("def go(self): ...", "def resume(self):\n        return 2")
        write(src / "app" / "thing.py", source)
        res = run_tool(EXTRACT, "--src", src, "--out", desc)
        assert res.returncode == 0, res.stderr

        d = json.loads(p.read_text())
        restored = d["nodes"][nid]
        assert {field: restored[field] for field in authored} == authored
        assert "retired_reason" not in restored
        assert nid not in d.get("nodes_retired", {}), "no duplicate"
        assert restored["lineno"] == before["lineno"] + 1
        assert restored["public_methods"] == (["resume"] if changed else ["go"])
        assert (restored["span_sha256"] != before["span_sha256"]) == changed
        assert f"RESTORED node {nid}" in res.stdout
        assert f"NEW node {nid}" not in res.stdout
        assert f"UNSEMANTIC node {nid}" not in res.stdout
        if not stamped:
            assert "semantics_authored_against" not in restored
            assert f"UNVERIFIED node {nid}" in res.stdout
        elif changed:
            assert f"SEMANTICS_STALE node {nid}" in res.stdout
        else:
            assert f"SEMANTICS_STALE node {nid}" not in res.stdout
            assert f"UNVERIFIED node {nid}" not in res.stdout

        res = run_tool(EXTRACT, "--src", src, "--out", desc)
        assert res.returncode == 0, res.stderr
        assert json.loads(p.read_text()) == d, "subsequent extraction must preserve the result"

    def test_a_node_with_no_semantics_is_just_removed(self, graph):
        """Retention is for authored work. Quarantining mechanical scaffold would
        fill the file with noise."""
        src, desc, p = graph
        write(src / "app" / "extra.py", "class Plain:\n    def x(self): ...\n")
        run_tool(EXTRACT, "--src", src, "--out", desc)
        write(src / "app" / "extra.py", "class Other:\n    def x(self): ...\n")
        run_tool(EXTRACT, "--src", src, "--out", desc)

        d = json.loads((desc / "app" / "extra.json").read_text())
        assert "nodes_retired" not in d or "app.extra.Plain" not in d["nodes_retired"]


class TestSemanticsStale:
    def test_changing_one_class_stales_only_that_class(self, graph):
        """Per node, not per file. A file-level hash marks all 40 classes in a
        module stale because one changed, which is a census nobody can act on."""
        src, desc, p = graph
        write(src / "app" / "thing.py", TWO_CLASSES.replace("return 1", "return 999"))
        res = run_tool(EXTRACT, "--src", src, "--out", desc)

        assert "SEMANTICS_STALE node app.thing.Alpha" in res.stdout
        assert "SEMANTICS_STALE node app.thing.Gamma" not in res.stdout

    def test_semantics_are_never_altered_by_staleness(self, graph):
        """The flag is a question, not an edit. Prose stays exactly as written."""
        src, desc, p = graph
        write(src / "app" / "thing.py", TWO_CLASSES.replace("return 1", "return 999"))
        run_tool(EXTRACT, "--src", src, "--out", desc)
        assert nodes(p)["app.thing.Alpha"]["role"] == "authored for Alpha"

    def test_unchanged_source_stays_authored(self, graph):
        src, desc, p = graph
        res = run_tool(EXTRACT, "--src", src, "--out", desc)
        assert "SEMANTICS_STALE" not in res.stdout

    def test_unstamped_prose_is_reported_unverified_and_never_auto_stamped(self, tmp_path):
        """Authored prose with no stamp is UNVERIFIED, and the extractor must not
        invent a stamp for it.

        This inverts the original assertion. That test encoded "grandfathering":
        the extractor auto-stamped pre-existing prose against current source so it
        would report AUTHORED, on the reasoning that flagging everything stale on
        day one makes the census useless.

        The cost was the census meaning nothing. The stamp claims a human read this
        prose against this source; minting one on nobody's behalf made
        `SEMANTICS_STALE: 0` reachable with zero nodes checked, and once written the
        assumed stamp was indistinguishable from an earned one. A large stale count
        on first run is the truth surfacing, not a regression.
        """
        src, desc = tmp_path / "src", tmp_path / "desc"
        write(src / "app" / "thing.py", TWO_CLASSES)
        run_tool(EXTRACT, "--src", src, "--out", desc)
        p = desc / "app" / "thing.json"
        d = json.loads(p.read_text())
        d["nodes"]["app.thing.Alpha"]["role"] = "pre-existing prose"
        p.write_text(json.dumps(d, indent=2))

        res = run_tool(EXTRACT, "--src", src, "--out", desc)
        assert "UNVERIFIED" in res.stdout
        # the defining assertion: no stamp was invented
        assert "semantics_authored_against" not in nodes(p)["app.thing.Alpha"]

    def test_the_stamp_is_preserved_across_extractions(self, graph):
        src, desc, p = graph
        before = nodes(p)["app.thing.Alpha"]["semantics_authored_against"]
        run_tool(EXTRACT, "--src", src, "--out", desc)
        assert nodes(p)["app.thing.Alpha"]["semantics_authored_against"] == before


class TestWalkerReport:
    def test_reports_the_four_state_census(self, graph):
        src, desc, _ = graph
        res = run_tool(WALKER, "--descriptors", desc, "--report")
        for state in ("AUTHORED", "SEMANTICS_STALE", "UNSEMANTIC", "RETIRED"):
            assert state in res.stdout

    def test_report_writes_nothing(self, graph):
        src, desc, _ = graph
        before = {p: p.read_bytes() for p in desc.rglob("*.json")}
        run_tool(WALKER, "--descriptors", desc, "--report")
        assert {p: p.read_bytes() for p in desc.rglob("*.json")} == before

    def test_stale_nodes_are_named(self, graph):
        src, desc, _ = graph
        write(src / "app" / "thing.py", TWO_CLASSES.replace("return 1", "return 999"))
        run_tool(EXTRACT, "--src", src, "--out", desc)

        res = run_tool(WALKER, "--descriptors", desc, "--report")
        assert "app.thing.Alpha" in res.stdout

    def test_work_is_aggregated_by_package(self, graph):
        """Per-node output on a real codebase is thousands of lines nobody
        reads. A subsystem is the unit an agent actually works in."""
        src, desc, _ = graph
        res = run_tool(WALKER, "--descriptors", desc, "--report", "--by", "package")
        assert "BY PACKAGE" in res.stdout

    def test_a_deleted_source_file_is_detected_with_src(self, graph):
        """The extractor's blind spot: it walks SOURCE, so a descriptor whose
        file is gone is never opened and its nodes count as live forever."""
        src, desc, _ = graph
        write(src / "app" / "doomed.py", "class Doomed:\n    def x(self): ...\n")
        run_tool(EXTRACT, "--src", src, "--out", desc)
        (src / "app" / "doomed.py").unlink()

        without = run_tool(WALKER, "--descriptors", desc, "--report")
        assert "STRANDED" not in without.stdout

        with_src = run_tool(WALKER, "--descriptors", desc, "--src", src, "--report")
        assert "STRANDED" in with_src.stdout
        assert "doomed.py" in with_src.stdout

    def test_a_possible_move_is_suggested_not_applied(self, graph):
        """A same-label match is evidence, not proof. Moving prose onto the wrong
        class is worse than leaving it retired where it can be seen."""
        src, desc, p = graph
        write(src / "app" / "thing.py", "class Alpha:\n    def run(self):\n        return 1\n")
        run_tool(EXTRACT, "--src", src, "--out", desc)
        write(src / "app" / "elsewhere.py", "class Gamma:\n    def go(self): ...\n")
        run_tool(EXTRACT, "--src", src, "--out", desc)

        res = run_tool(WALKER, "--descriptors", desc, "--report")
        assert "POSSIBLE MOVES" in res.stdout
        assert "Suggested only" in res.stdout
        # the retired entry is untouched
        assert "app.thing.Gamma" in json.loads(p.read_text())["nodes_retired"]

    def test_missing_descriptor_root_is_reported(self, tmp_path):
        res = run_tool(WALKER, "--descriptors", tmp_path / "nope", "--report")
        assert res.returncode == 2


class TestWalkerAccept:
    def test_accept_clears_stale_after_re_verification(self, graph):
        src, desc, p = graph
        write(src / "app" / "thing.py", TWO_CLASSES.replace("return 1", "return 999"))
        run_tool(EXTRACT, "--src", src, "--out", desc)

        res = run_tool(WALKER, "--descriptors", desc,
                       "--accept", "app.thing.Alpha", "--apply")
        assert res.returncode == 0
        after = run_tool(WALKER, "--descriptors", desc, "--report")
        assert "SEMANTICS_STALE         0" in after.stdout

    def test_accept_without_apply_writes_nothing(self, graph):
        src, desc, p = graph
        write(src / "app" / "thing.py", TWO_CLASSES.replace("return 1", "return 999"))
        run_tool(EXTRACT, "--src", src, "--out", desc)
        before = p.read_bytes()

        res = run_tool(WALKER, "--descriptors", desc, "--accept", "app.thing.Alpha")
        assert "WOULD ACCEPT" in res.stdout
        assert p.read_bytes() == before

    def test_accept_never_changes_prose(self, graph):
        src, desc, p = graph
        write(src / "app" / "thing.py", TWO_CLASSES.replace("return 1", "return 999"))
        run_tool(EXTRACT, "--src", src, "--out", desc)
        run_tool(WALKER, "--descriptors", desc, "--accept", "app.thing.Alpha", "--apply")
        assert nodes(p)["app.thing.Alpha"]["role"] == "authored for Alpha"

    def test_accepting_an_unsemantic_node_is_refused(self, tmp_path):
        """There is nothing to accept. Stamping it would claim semantics exist."""
        src, desc = tmp_path / "src", tmp_path / "desc"
        write(src / "app" / "thing.py", TWO_CLASSES)
        run_tool(EXTRACT, "--src", src, "--out", desc)

        res = run_tool(WALKER, "--descriptors", desc,
                       "--accept", "app.thing.Alpha", "--apply")
        assert "nothing to accept" in res.stdout

    def test_an_unknown_id_is_reported(self, graph):
        src, desc, _ = graph
        res = run_tool(WALKER, "--descriptors", desc, "--accept", "no.such.Node", "--apply")
        assert "NOT FOUND" in res.stdout
        assert res.returncode == 1
