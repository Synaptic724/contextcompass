"""Reconcile and on-demand ticket generation.

Two destructive-ish verbs, both gated. `--reconcile` is the only sanctioned path
for deleting authored prose; ticket generation writes into somebody's board. Both
are off by default and both ask.
"""

from __future__ import annotations

import json
import re

import pytest

from conftest import GRAPH_TOOLS, run_tool, write

pytestmark = pytest.mark.integration

EXTRACT = GRAPH_TOOLS / "extract_graph.py"
WALKER = GRAPH_TOOLS / "graph_walker.py"
TICKETS = GRAPH_TOOLS / "graph_semantics_tickets.py"

TWO = "class Alpha:\n    def run(self): ...\n\n\nclass Beta:\n    def go(self): ...\n"
ONE = "class Alpha:\n    def run(self): ...\n"


@pytest.fixture
def retired(tmp_path):
    """A descriptor tree with one retired node carrying authored prose."""
    src, desc = tmp_path / "src", tmp_path / "desc"
    write(src / "app" / "thing.py", TWO)
    run_tool(EXTRACT, "--src", src, "--out", desc)

    p = desc / "app" / "thing.json"
    d = json.loads(p.read_text())
    d["nodes"]["app.thing.Beta"]["role"] = "Beta coordinates widget teardown"
    p.write_text(json.dumps(d, indent=2))

    write(src / "app" / "thing.py", ONE)
    run_tool(EXTRACT, "--src", src, "--out", desc)
    assert "nodes_retired" in json.loads(p.read_text())
    return src, desc, p


class TestReconcile:
    def test_refuses_without_a_terminal_or_yes(self, retired):
        """A prompt that silently self-answers in CI is not a prompt, and this is
        the one verb that destroys authored work."""
        _, desc, p = retired
        res = run_tool(WALKER, "--descriptors", desc, "--reconcile")
        assert res.returncode == 1
        assert "REFUSED" in res.stdout
        assert "nodes_retired" in json.loads(p.read_text())

    def test_lists_what_it_would_delete_before_asking(self, retired):
        _, desc, _ = retired
        res = run_tool(WALKER, "--descriptors", desc, "--reconcile")
        assert "app.thing.Beta" in res.stdout
        assert "Beta coordinates widget teardown" in res.stdout
        assert "not recoverable" in res.stdout

    def test_yes_deletes_the_retired_nodes(self, retired):
        _, desc, p = retired
        res = run_tool(WALKER, "--descriptors", desc, "--reconcile", "--yes")
        assert res.returncode == 0
        assert "nodes_retired" not in json.loads(p.read_text())

    def test_live_nodes_are_untouched(self, retired):
        _, desc, p = retired
        run_tool(WALKER, "--descriptors", desc, "--reconcile", "--yes")
        assert "app.thing.Alpha" in json.loads(p.read_text())["nodes"]

    def test_nothing_retired_is_a_clean_no_op(self, tmp_path):
        src, desc = tmp_path / "src", tmp_path / "desc"
        write(src / "app" / "thing.py", ONE)
        run_tool(EXTRACT, "--src", src, "--out", desc)
        res = run_tool(WALKER, "--descriptors", desc, "--reconcile", "--yes")
        assert res.returncode == 0
        assert "nothing to reconcile" in res.stdout


@pytest.fixture
def scanned(tmp_path):
    """An unauthored graph plus an empty tickets lane."""
    src, desc = tmp_path / "src", tmp_path / "desc"
    write(src / "app" / "core" / "a.py", "class A:\n    def x(self): ...\n")
    write(src / "app" / "core" / "b.py", "class B:\n    def x(self): ...\n")
    write(src / "app" / "edge" / "c.py", "class C:\n    def x(self): ...\n")
    run_tool(EXTRACT, "--src", src, "--out", desc)

    lane = tmp_path / "tickets"
    (lane / "stories").mkdir(parents=True)
    (lane / "epics").mkdir(parents=True)
    return src, desc, lane


def story_files(lane):
    return sorted((lane / "stories").glob("*.md"))


class TestTicketGeneration:
    def test_dry_run_is_the_default(self, scanned):
        _, desc, lane = scanned
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane)
        assert res.returncode == 0
        assert "DRY RUN" in res.stdout
        assert story_files(lane) == []

    def test_create_refuses_without_a_terminal_or_yes(self, scanned):
        """Writing tickets into somebody's board unasked is hostile."""
        _, desc, lane = scanned
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create")
        assert res.returncode == 1
        assert "REFUSED" in res.stdout
        assert story_files(lane) == []

    def test_creates_one_story_per_package_plus_one_epic(self, scanned):
        """Per node would be 1,188 tickets on a real codebase and per file 575.
        The board carries about a dozen active rows."""
        _, desc, lane = scanned
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane,
                       "--create", "--yes")
        assert res.returncode == 0
        # Two packages, not three: `package` is the directory holding the file,
        # and nothing lives directly in `src/app`.
        assert len(story_files(lane)) == 2          # app/core, app/edge
        assert len(list((lane / "epics").glob("*.md"))) == 1

    def test_no_tasks_are_generated(self, scanned):
        """Task granularity is the working agent's judgement."""
        _, desc, lane = scanned
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        assert not list((lane / "tasks").glob("*.md")) if (lane / "tasks").is_dir() else True

    def test_stories_follow_the_repos_template_contract(self, scanned):
        _, desc, lane = scanned
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        text = story_files(lane)[0].read_text()
        for section in ("## Metadata", "## Ticket Contract", "## Acceptance Criteria",
                        "## Requirements (Functional)", "## Context / Handoff Summary"):
            assert section in text, f"missing {section}"
        assert "ENTRY_GATE" in text and "EXIT_GATE" in text

    def test_a_story_says_semantics_must_be_read_not_inferred(self, scanned):
        """A generated ticket that omits this gets filled with invented prose by
        the first agent in a hurry, and invented semantics read as verified."""
        _, desc, lane = scanned
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        text = story_files(lane)[0].read_text()
        assert "READING THE CODE" in text
        # Match on unwrapped fragments - the prose is hard-wrapped, so
        # "worse than none" straddles a line break in the rendered ticket.
        assert "Invented semantics are worse" in text
        assert "read as verified" in text

    def test_a_story_lists_the_nodes_it_covers(self, scanned):
        _, desc, lane = scanned
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        core = next(p for p in story_files(lane) if "core" in p.name)
        assert "app.core.a.A" in core.read_text()
        assert "app.core.b.B" in core.read_text()

    def test_the_board_is_never_touched(self, scanned, tmp_path):
        """A generated ticket claiming an active row is a row nobody agreed to."""
        _, desc, lane = scanned
        board = write(tmp_path / "attention_board.md", "# Attention Board\n")
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        assert board.read_text() == "# Attention Board\n"


class TestTicketBackend:
    def test_plugin_backend_refuses_local_create_and_preserves_existing_files(self, scanned):
        _, desc, lane = scanned
        write(lane.parent / "config/context_compass_config.yaml",
              "work_tracking:\n  backend: github_codex_plugin\n")
        write(lane / "epics/keep.md", "# Keep\n\nAuthored decision and Notes.\n")
        before = {p.relative_to(lane): p.read_bytes() for p in lane.rglob("*") if p.is_file()}
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        assert res.returncode == 1
        assert "REFUSED" in res.stdout and "github_codex_plugin" in res.stdout
        after = {p.relative_to(lane): p.read_bytes() for p in lane.rglob("*") if p.is_file()}
        assert after == before

    def test_plugin_preview_ignores_local_archive_ids(self, scanned):
        _, desc, lane = scanned
        write(lane.parent / "config/context_compass_config.yaml",
              "work_tracking:\n  backend: github_codex_plugin\n")
        archived = write(lane / "epics/completed/old.md",
                         "- Epic ID: ARCHIVE-author-graph-semantics\n\nDo not read as active work.\n")
        before = archived.read_bytes()
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane)
        assert res.returncode == 0
        assert "github_codex_plugin" in res.stdout and "DRY RUN" in res.stdout
        assert "ARCHIVE-author-graph-semantics" not in res.stdout
        assert archived.read_bytes() == before and story_files(lane) == []

    def test_plugin_preview_does_not_call_local_ticket_lookup(self, scanned, monkeypatch):
        import graph_semantics_tickets as generator

        _, desc, lane = scanned
        write(lane.parent / "config/context_compass_config.yaml",
              "work_tracking:\n  backend: github_codex_plugin\n")
        monkeypatch.setattr(generator.sys, "argv", [str(TICKETS), "--descriptors", str(desc),
                                                    "--tickets", str(lane)])

        def no_local_reads(*args):
            pytest.fail("Plugin preview read inactive local ticket state")

        monkeypatch.setattr(generator, "find_existing", no_local_reads)
        assert generator.main() == 0

    @pytest.mark.parametrize("value", ["", "unknown", "github", "null"])
    def test_ambiguous_backend_blocks_creation_without_writes(self, scanned, value):
        _, desc, lane = scanned
        write(lane.parent / "config/context_compass_config.yaml",
              f"work_tracking:\n  backend: {value}\n")
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        assert res.returncode == 2
        assert "ERROR" in res.stdout
        assert story_files(lane) == []
        assert list((lane / "epics").glob("*.md")) == []

    def test_legacy_files_setting_preserves_local_generation(self, scanned):
        _, desc, lane = scanned
        write(lane.parent / "config/context_compass_config.yaml",
              "work_tracking:\n  backend: 'files' # older install\n")
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        assert res.returncode == 0
        assert len(story_files(lane)) == 2
        assert len(list((lane / "epics").glob("*.md"))) == 1


class TestIdempotency:
    def test_rerunning_updates_rather_than_duplicates(self, scanned):
        """A scan that doubles the board every run gets switched off in a day."""
        _, desc, lane = scanned
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        first = story_files(lane)
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        assert story_files(lane) == first

    def test_a_nested_package_slug_does_not_match_its_parents_story(self, scanned):
        """`GRAPH-SEM-app` is a prefix of `GRAPH-SEM-app-core`. A substring match
        made the parent find the child's story and overwrite it."""
        _, desc, lane = scanned
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        for p in story_files(lane):
            ids = set(re.findall(r"GRAPH-SEM-[a-z0-9-]+", p.read_text()))
            assert len(ids) == 1, f"{p.name} carries {ids}"

    def test_a_completed_story_is_found_not_recreated(self, scanned):
        """Completed lanes are searched too, or the scan re-creates work
        somebody already finished."""
        _, desc, lane = scanned
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        core = next(p for p in story_files(lane) if "core" in p.name)
        done = lane / "stories" / "completed"
        done.mkdir(parents=True)
        moved = done / core.name
        moved.write_text(core.read_text())
        core.unlink()

        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane)
        assert "UPDATE" in res.stdout
        assert moved.name in res.stdout

    def test_an_authored_package_is_reported_satisfied(self, scanned):
        """The loop has to close in both directions or it becomes noise."""
        src, desc, lane = scanned
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")

        for p in (desc / "app" / "edge").glob("*.json"):
            d = json.loads(p.read_text())
            for n in d["nodes"].values():
                n["role"] = "authored"
            p.write_text(json.dumps(d, indent=2))
        run_tool(EXTRACT, "--src", src, "--out", desc)
        # Authoring alone no longer completes the work. An unstamped node is
        # SEMANTICS_STALE, which this tool counts as needing work - correctly, since
        # nobody has checked that prose against its source. SATISFIED now requires
        # the verification too, which is the loop the epic claims to close.
        for p in (desc / "app" / "edge").glob("*.json"):
            for nid in json.loads(p.read_text())["nodes"]:
                run_tool(WALKER, "--descriptors", desc, "--accept", nid, "--apply")

        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane)
        assert "SATISFIED" in res.stdout
        assert "app/edge" in res.stdout

    def test_a_satisfied_story_is_not_rewritten(self, scanned):
        src, desc, lane = scanned
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        edge = next(p for p in story_files(lane) if "edge" in p.name)
        before = edge.read_bytes()

        for p in (desc / "app" / "edge").glob("*.json"):
            d = json.loads(p.read_text())
            for n in d["nodes"].values():
                n["role"] = "authored"
            p.write_text(json.dumps(d, indent=2))
        run_tool(EXTRACT, "--src", src, "--out", desc)
        # Authoring alone no longer completes the work. An unstamped node is
        # SEMANTICS_STALE, which this tool counts as needing work - correctly, since
        # nobody has checked that prose against its source. SATISFIED now requires
        # the verification too, which is the loop the epic claims to close.
        for p in (desc / "app" / "edge").glob("*.json"):
            for nid in json.loads(p.read_text())["nodes"]:
                run_tool(WALKER, "--descriptors", desc, "--accept", nid, "--apply")
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--create", "--yes")
        assert edge.read_bytes() == before

    def test_min_nodes_filters_small_packages(self, scanned):
        _, desc, lane = scanned
        # Each file contributes a module node plus its class, so the
        # single-file `app/edge` package holds 2 nodes, not 1.
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane,
                       "--min-nodes", "3")
        assert "app/edge" not in res.stdout, "2-node package should be filtered"
        assert "app/core" in res.stdout, "4-node package should survive"


class TestScale:
    """Behaviour on a tree big enough for the design constraint to bite.

    The 11-node example proves correctness and nothing about scale. Measured on
    a real 575-file source tree the directory-level grouping produced **146**
    stories, not the ~33 the design brief estimated - that figure came from
    `_package_candidates.json`, which counts directories whose files share a
    naming suffix, a different thing entirely. These lock in the levers that
    close the gap.
    """

    @pytest.fixture
    def deep_tree(self, tmp_path):
        """60 packages nested four deep, one class each."""
        src, desc = tmp_path / "src", tmp_path / "desc"
        for top in ("alpha", "beta", "gamma"):
            for mid in ("one", "two", "three", "four"):
                for leaf in ("x", "y", "z", "w", "v"):
                    write(src / "pkg" / top / mid / leaf / "m.py",
                          f"class C_{top}_{mid}_{leaf}:\n    def go(self): ...\n")
        run_tool(EXTRACT, "--src", src, "--out", desc)
        lane = tmp_path / "tickets"
        (lane / "stories").mkdir(parents=True)
        (lane / "epics").mkdir(parents=True)
        return desc, lane

    def test_directory_grouping_gives_one_story_per_leaf(self, deep_tree):
        desc, lane = deep_tree
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane)
        assert "packages with work : 60" in res.stdout

    def test_a_large_count_prints_the_levers_rather_than_just_doing_it(self, deep_tree):
        """146 stories on a routing board carrying a dozen rows is not a plan.
        Show the way out instead of silently emitting them."""
        desc, lane = deep_tree
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane)
        assert "is a lot for a routing board" in res.stdout
        assert "--depth" in res.stdout
        assert "--min-nodes" in res.stdout
        assert "Neither loses work" in res.stdout

    @pytest.mark.parametrize("depth,expected", [(2, 1), (3, 3), (4, 12)])
    def test_depth_collapses_the_story_count(self, deep_tree, depth, expected):
        desc, lane = deep_tree
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane,
                       "--depth", str(depth))
        assert f"packages with work : {expected}" in res.stdout

    def test_depth_loses_no_nodes(self, deep_tree):
        """Grouping changes how work is packaged, never how much there is."""
        desc, lane = deep_tree
        flat = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane)
        deep = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--depth", "3")
        n = re.search(r"nodes to author\s+: (\d+)", flat.stdout).group(1)
        assert f"nodes to author    : {n}" in deep.stdout

    def test_the_levers_are_not_shown_once_the_count_is_reasonable(self, deep_tree):
        desc, lane = deep_tree
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane, "--depth", "3")
        assert "is a lot for a routing board" not in res.stdout

    def test_grouped_stories_still_carry_every_node(self, deep_tree):
        desc, lane = deep_tree
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane,
                 "--depth", "3", "--create", "--yes")
        listed = set()
        for p in story_files(lane):
            listed |= set(re.findall(r"`(pkg\.[\w.]+)`", p.read_text()))
        assert len(listed) == 60 * 2, f"expected 120 nodes across stories, got {len(listed)}"

    def test_grouping_stays_idempotent(self, deep_tree):
        desc, lane = deep_tree
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane,
                 "--depth", "3", "--create", "--yes")
        first = story_files(lane)
        run_tool(TICKETS, "--descriptors", desc, "--tickets", lane,
                 "--depth", "3", "--create", "--yes")
        assert story_files(lane) == first


class TestContract:
    def test_missing_descriptors_is_reported(self, tmp_path):
        res = run_tool(TICKETS, "--descriptors", tmp_path / "nope",
                       "--tickets", tmp_path)
        assert res.returncode == 2

    def test_missing_tickets_lane_is_reported(self, scanned):
        _, desc, lane = scanned
        res = run_tool(TICKETS, "--descriptors", desc, "--tickets", lane / "nope")
        assert res.returncode == 2
