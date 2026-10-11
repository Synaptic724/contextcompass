"""An upgrade must update package text and preserve the agent's working areas.

This is the promise the boards make in their own contract block, so it is
tested end to end rather than at the function level only.
"""

from __future__ import annotations

import shutil

import pytest

from conftest import PKG_ROOT, TOOLS, run_tool, write
from cleanup_context_compass import user_regions

pytestmark = pytest.mark.integration

UPDATER = TOOLS / "update_context_compass.py"
MANIFEST = TOOLS / "package_manifest.py"
MIGRATE = TOOLS / "migrate_boards.py"

BOARD_V1 = """\
# Attention Board

<!-- BEGIN MANAGED: contract -->
V1 package prose.
<!-- END MANAGED: contract -->

## Active Items
| work_item | status |
| --- | --- |
<!-- BEGIN USER-DEFINED: active_items -->
<!-- END USER-DEFINED: active_items -->
"""

BOARD_V2 = """\
# Attention Board

<!-- BEGIN MANAGED: contract -->
V2 package prose, rewritten.
<!-- END MANAGED: contract -->

## How this board works
New explanatory section the package added.

## Active Items
| work_item | status | owner |
| --- | --- | --- |
<!-- BEGIN USER-DEFINED: active_items -->
<!-- END USER-DEFINED: active_items -->
"""

MY_ROWS = "| system_doc_recomposition | in_progress |\n| aetheric_mediator_core | review |\n"


@pytest.fixture
def install_and_new(tmp_path):
    install, new = tmp_path / "install", tmp_path / "new"
    for root, board in ((install, BOARD_V1), (new, BOARD_V2)):
        write(root / "AGENTS.MD", "# AGENTS\n")
        write(root / "attention_board.md", board)
        write(root / "templates" / "task_template.md",
              "# Task\n\n## Scope\n<scope>\n\n## Project-Specific Additions\n"
              "<!-- BEGIN USER-DEFINED: project_fields -->\n"
              "<!-- END USER-DEFINED: project_fields -->\n")
    # the install has done real work in its protected areas
    b = install / "attention_board.md"
    b.write_bytes(b.read_text().replace(
        "<!-- BEGIN USER-DEFINED: active_items -->\n",
        "<!-- BEGIN USER-DEFINED: active_items -->\n" + MY_ROWS).encode())
    t = install / "templates" / "task_template.md"
    t.write_bytes(t.read_text().replace(
        "<!-- BEGIN USER-DEFINED: project_fields -->\n",
        "<!-- BEGIN USER-DEFINED: project_fields -->\n- COMPLIANCE_REVIEWER: <name>\n").encode())

    run_tool(MANIFEST, "--root", install, "--version", "1.0.0")
    run_tool(MANIFEST, "--root", new, "--version", "2.0.0")
    return install, new


class TestBoardsUpdateAndPreserve:
    def test_package_prose_updates(self, install_and_new):
        install, new = install_and_new
        res = run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert res.returncode == 0, res.stdout
        text = (install / "attention_board.md").read_text()
        assert "V2 package prose, rewritten." in text
        assert "V1 package prose." not in text

    def test_the_boards_shape_can_finally_change(self, install_and_new):
        """Swapping only the managed block froze everything else forever. A new
        section and a new table column now actually arrive."""
        install, new = install_and_new
        run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        text = (install / "attention_board.md").read_text()
        assert "## How this board works" in text
        assert "| work_item | status | owner |" in text

    def test_my_rows_survive(self, install_and_new):
        install, new = install_and_new
        run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        text = (install / "attention_board.md").read_text()
        assert "| system_doc_recomposition | in_progress |" in text
        assert "| aetheric_mediator_core | review |" in text

    def test_the_carry_is_reported_before_it_happens(self, install_and_new):
        install, new = install_and_new
        res = run_tool(UPDATER, "--install", install, "--new", new, "--check")
        assert "regions" in res.stdout
        assert "attention_board.md: active_items" in res.stdout

    def test_check_writes_nothing(self, install_and_new):
        install, new = install_and_new
        before = (install / "attention_board.md").read_bytes()
        run_tool(UPDATER, "--install", install, "--new", new, "--check")
        assert (install / "attention_board.md").read_bytes() == before

    def test_upgrading_twice_does_not_duplicate_rows(self, install_and_new):
        install, new = install_and_new
        run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert (install / "attention_board.md").read_text().count(
            "| system_doc_recomposition | in_progress |") == 1


class TestTemplatesPreserveLocalFields:
    def test_a_project_field_survives_a_template_upgrade(self, install_and_new):
        """Templates are PACKAGE class, so before regions any local edit was
        conformed away on every upgrade."""
        install, new = install_and_new
        run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert "- COMPLIANCE_REVIEWER: <name>" in (
            install / "templates" / "task_template.md").read_text()


class TestUnmigratedBoards:
    @pytest.fixture
    def legacy_install(self, install_and_new):
        """A board predating regions: rows in open text.

        The separator is written unspaced (`|---|---|`), which is the style the
        real boards this migration was built for actually use. It matters: a
        spaced `| --- | --- |` happens to be a substring of the new board's
        three-column separator, so a different filter drops it and the
        separator check never runs. Written the spaced way, this fixture tested
        a path that could not fail.
        """
        install, new = install_and_new
        write(install / "attention_board.md",
              "# Attention Board\n\n"
              "<!-- BEGIN MANAGED: contract -->\nV1 package prose.\n"
              "<!-- END MANAGED: contract -->\n\n"
              "## Active Items\n| work_item | status |\n|---|---|\n" + MY_ROWS)
        run_tool(MANIFEST, "--root", install, "--version", "1.0.0")
        return install, new

    def test_a_board_without_regions_is_never_conformed(self, legacy_install):
        """Conforming it would delete every row, because nothing marks them as
        the install's."""
        install, new = legacy_install
        res = run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert res.returncode == 0
        text = (install / "attention_board.md").read_text()
        assert "| system_doc_recomposition | in_progress |" in text
        assert "## How this board works" not in text, "shape must NOT change yet"

    def test_it_is_named_with_the_command_that_fixes_it(self, legacy_install):
        install, new = legacy_install
        res = run_tool(UPDATER, "--install", install, "--new", new, "--check")
        assert "MIGRATE" in res.stdout
        assert "migrate  attention_board.md" in res.stdout
        assert "migrate_boards.py" in res.stdout

    def test_the_managed_block_still_updates(self, legacy_install):
        install, new = legacy_install
        run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert "V2 package prose, rewritten." in (install / "attention_board.md").read_text()

    def test_migrate_then_upgrade_gives_shape_and_rows(self, legacy_install):
        """The full path out: migrate once, then upgrades work normally."""
        install, new = legacy_install
        mig = run_tool(MIGRATE, "--install", install, "--new", new, "--apply")
        assert mig.returncode == 0, mig.stdout
        assert "active_items" in mig.stdout

        run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        text = (install / "attention_board.md").read_text()
        assert "## How this board works" in text, "shape now updates"
        assert "| work_item | status | owner |" in text
        assert "| system_doc_recomposition | in_progress |" in text, "rows preserved"

    def test_migration_does_not_carry_the_old_table_scaffolding(self, legacy_install):
        """The new board supplies its own header and separator. Carrying the old
        ones puts a second `| --- | --- |` inside the region, which renders as a
        row and quietly breaks the table."""
        install, new = legacy_install
        run_tool(MIGRATE, "--install", install, "--new", new, "--apply")

        import sys
        sys.path.insert(0, str(TOOLS))
        from cleanup_context_compass import user_regions
        text = (install / "attention_board.md").read_text()
        bodies = {n: text[s:e] for n, s, e in user_regions(text)}

        assert "| system_doc_recomposition | in_progress |" in bodies["active_items"]
        assert "---" not in bodies["active_items"], "separator leaked into the region"
        assert "| work_item | status |" not in bodies["active_items"], "header leaked in"

        # Count whole separator LINES, not substrings: "| --- |" occurs twice
        # inside "| --- | --- | --- |", so a substring count can never balance.
        import re as _re
        separators = [l for l in text.split("\n") if _re.match(r"^\s*\|[\s|:-]+\|\s*$", l)]
        assert len(separators) == 1, f"expected one separator, found {separators}"

    def test_migration_check_writes_nothing(self, legacy_install):
        install, new = legacy_install
        before = (install / "attention_board.md").read_bytes()
        run_tool(MIGRATE, "--install", install, "--new", new, "--check")
        assert (install / "attention_board.md").read_bytes() == before

    def test_migration_refuses_without_apply(self, legacy_install):
        install, new = legacy_install
        res = run_tool(MIGRATE, "--install", install, "--new", new)
        assert res.returncode == 2
        assert "Refusing to act without --apply" in res.stdout

    def test_content_with_no_matching_region_is_parked_not_dropped(self, legacy_install):
        """A section the new board has no region for must survive somewhere."""
        install, new = legacy_install
        b = install / "attention_board.md"
        b.write_bytes((b.read_text() + "\n## Local Conventions\n- we do X before Y\n").encode())
        write(new / "attention_board.md",
              BOARD_V2.rstrip("\n") + "\n\n## Notes\n"
              "<!-- BEGIN USER-DEFINED: notes -->\n<!-- END USER-DEFINED: notes -->\n")
        run_tool(MANIFEST, "--root", new, "--version", "2.0.0")

        run_tool(MIGRATE, "--install", install, "--new", new, "--apply")
        text = b.read_text()
        assert "- we do X before Y" in text
        assert "Local Conventions" in text


class TestInstanceLaneSeeding:
    def test_a_lane_the_new_version_introduces_arrives(self, install_and_new):
        """An older install's manifest listed `user_defined/` files absent on disk,
        because the updater skipped INSTANCE before it could ever create one."""
        install, new = install_and_new
        write(new / "user_defined" / "README.md", "# user_defined\n\nYour space.\n")
        run_tool(MANIFEST, "--root", new, "--version", "2.0.0")

        res = run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert res.returncode == 0
        assert (install / "user_defined" / "README.md").is_file()

    def test_existing_instance_content_is_never_replaced(self, install_and_new):
        install, new = install_and_new
        write(new / "user_defined" / "README.md", "# PACKAGE VERSION\n")
        run_tool(MANIFEST, "--root", new, "--version", "2.0.0")
        mine = write(install / "user_defined" / "README.md", "# MY VERSION\n")

        run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert mine.read_text() == "# MY VERSION\n"

    def test_seed_instance_repairs_a_lane_recorded_but_never_written(self, install_and_new):
        """The state an install was left in by the pre-2.5.0 skip: the manifest
        listed `user_defined/README.md` and the file had never existed.

        Absent AND in `shipped` is indistinguishable from a deletion, so the
        repair is opt-in rather than a guess.
        """
        install, new = install_and_new
        write(new / "user_defined" / "README.md", "# user_defined\n")
        run_tool(MANIFEST, "--root", new, "--version", "2.0.0")
        # manifest records it; disk never got it
        (install / "MANIFEST.md").write_bytes((new / "MANIFEST.md").read_bytes())

        plain = run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert plain.returncode == 0
        assert not (install / "user_defined" / "README.md").exists(), \
            "without the flag it must not guess"

        res = run_tool(UPDATER, "--install", install, "--new", new,
                       "--seed-instance", "--apply")
        assert res.returncode == 0
        assert (install / "user_defined" / "README.md").is_file()

    def test_seed_instance_still_never_replaces_existing_content(self, install_and_new):
        install, new = install_and_new
        write(new / "user_defined" / "README.md", "# PACKAGE\n")
        run_tool(MANIFEST, "--root", new, "--version", "2.0.0")
        mine = write(install / "user_defined" / "README.md", "# MINE\n")

        run_tool(UPDATER, "--install", install, "--new", new,
                 "--seed-instance", "--apply")
        assert mine.read_text() == "# MINE\n"

    def test_a_file_the_user_deleted_is_not_resurrected(self, install_and_new):
        """Seeding acts on absence, so it needs the three-hash rule to tell a
        lane that never arrived from a file someone removed on purpose."""
        install, new = install_and_new
        write(install / "user_defined" / "README.md", "# mine\n")
        write(new / "user_defined" / "README.md", "# package\n")
        run_tool(MANIFEST, "--root", install, "--version", "1.0.0")
        run_tool(MANIFEST, "--root", new, "--version", "2.0.0")
        (install / "user_defined" / "README.md").unlink()

        run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert not (install / "user_defined" / "README.md").exists()


DETAIL_T1 = ("- WORK_ITEM: parser_retry\n"
             "  SWITCH_TRIGGER: backoff branch lands and the 429 path is covered\n"
             "  RESUME_HIERARCHY:\n"
             "    - tickets/stories/2026-09-29_retry_story.md\n"
             "    - tickets/tasks/2026-09-29_parser_retry_task.md\n")
DETAIL_T2 = ("- WORK_ITEM: cache_refresh\n"
             "  SWITCH_TRIGGER: review lane signals acceptance\n"
             "  RESUME_HIERARCHY:\n"
             "    - tickets/stories/2026-09-29_cache_story.md\n"
             "    - tickets/tasks/2026-09-29_cache_refresh_task.md\n")

# Older already-regioned board: regions present, details section absent.
# This is the install side everywhere below; user content lives ONLY here.
OLD_BOARD = """\
# Attention Board

<!-- BEGIN MANAGED: contract -->
V1 package prose.
<!-- END MANAGED: contract -->

## Active Items
| work_item | status |
| --- | --- |
<!-- BEGIN USER-DEFINED: active_items -->
| parser_retry | in_progress |
<!-- END USER-DEFINED: active_items -->

## Recently Closed Anchors
| work_item | status |
| --- | --- |
<!-- BEGIN USER-DEFINED: closed_anchors -->
| nightly_cleanup | done |
<!-- END USER-DEFINED: closed_anchors -->

## Notes
<!-- BEGIN USER-DEFINED: notes -->
Standing instructions.
<!-- END USER-DEFINED: notes -->
"""

# Incoming package board: V1 prose replaced, details section declared, and
# every USER-DEFINED region EMPTY, so a broken carry cannot pass by copying
# package data identical to the install's.
PACKAGE_BOARD = """\
# Attention Board

<!-- BEGIN MANAGED: contract -->
V2 package prose, rewritten.
<!-- END MANAGED: contract -->

## Active Items
| work_item | status |
| --- | --- |
<!-- BEGIN USER-DEFINED: active_items -->
<!-- END USER-DEFINED: active_items -->

## Active Attention Details
<!-- BEGIN USER-DEFINED: active_attention_details -->
<!-- END USER-DEFINED: active_attention_details -->

## Recently Closed Anchors
| work_item | status |
| --- | --- |
<!-- BEGIN USER-DEFINED: closed_anchors -->
<!-- END USER-DEFINED: closed_anchors -->

## Notes
<!-- BEGIN USER-DEFINED: notes -->
<!-- END USER-DEFINED: notes -->
"""


def write_manifested_pair(tmp_path, install_board, new_board):
    install, new = tmp_path / "install", tmp_path / "new"
    for root, board in ((install, install_board), (new, new_board)):
        write(root / "AGENTS.MD", "# AGENTS\n")
        write(root / "attention_board.md", board)
    for root, version in ((install, "1.0.0"), (new, "2.0.0")):
        res = run_tool(MANIFEST, "--root", root, "--version", version)
        assert res.returncode == 0, res.stdout + res.stderr
    return install, new


@pytest.fixture
def detail_install_and_new(tmp_path):
    return write_manifested_pair(tmp_path, OLD_BOARD, PACKAGE_BOARD)


def regions_of(board_path):
    text = board_path.read_text(encoding="utf-8")
    return {name: text[s:e] for name, s, e in user_regions(text)}


class TestShippedDetailsRegion:
    def test_shipped_template_declares_an_empty_details_region(self):
        """The real template, not a synthetic stand-in: a purely synthetic
        fixture would pass while the shipped package still lacked the region.
        """
        text = (PKG_ROOT / "attention_board.md").read_text(encoding="utf-8")
        assert "## Active Attention Details" in text
        bodies = regions_of(PKG_ROOT / "attention_board.md")
        assert "active_attention_details" in bodies
        assert bodies["active_attention_details"] == "\n"


class TestDetailsRegionUpgrade:
    def test_upgrade_adds_the_region_and_preserves_content(
            self, detail_install_and_new):
        install, new = detail_install_and_new
        before = regions_of(install / "attention_board.md")
        res = run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert res.returncode == 0, res.stdout + res.stderr
        text = (install / "attention_board.md").read_text(encoding="utf-8")
        assert "V2 package prose, rewritten." in text
        after = regions_of(install / "attention_board.md")
        assert after["active_attention_details"] == "\n"
        for name in ("active_items", "closed_anchors", "notes"):
            assert after[name] == before[name]

    def test_populated_details_survive_a_second_upgrade(self, tmp_path):
        populated = PACKAGE_BOARD.replace(
            "<!-- BEGIN USER-DEFINED: active_attention_details -->\n",
            "<!-- BEGIN USER-DEFINED: active_attention_details -->\n"
            + DETAIL_T1 + DETAIL_T2)
        install, new = write_manifested_pair(tmp_path, populated, PACKAGE_BOARD)
        before = regions_of(install / "attention_board.md")
        first = run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert first.returncode == 0, first.stdout + first.stderr
        mid = regions_of(install / "attention_board.md")
        assert mid["active_attention_details"] == before["active_attention_details"]
        second = run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert second.returncode == 0, second.stdout + second.stderr
        after = regions_of(install / "attention_board.md")
        assert after["active_attention_details"] == before["active_attention_details"]

    def test_notes_held_details_are_preserved_not_relocated(self, tmp_path):
        """Details already protected inside Notes must survive with text
        identical and must NOT be silently moved into the new region: carry
        maps same-name regions only, so relocation needs an explicit step."""
        noted = OLD_BOARD.replace(
            "Standing instructions.\n", "Standing instructions.\n" + DETAIL_T1)
        install, new = write_manifested_pair(tmp_path, noted, PACKAGE_BOARD)
        before = regions_of(install / "attention_board.md")
        res = run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert res.returncode == 0, res.stdout + res.stderr
        after = regions_of(install / "attention_board.md")
        assert after["notes"] == before["notes"]
        assert DETAIL_T1 in after["notes"]
        assert after["active_attention_details"] == "\n"


class TestLegacyDetailsMigration:
    def test_open_text_details_map_into_the_new_region(self, tmp_path):
        legacy = ("# Attention Board\n\n"
                  "<!-- BEGIN MANAGED: contract -->\nV1 package prose.\n"
                  "<!-- END MANAGED: contract -->\n\n"
                  "## Active Items\n| work_item | status |\n|---|---|\n"
                  "| parser_retry | in_progress |\n\n"
                  "## Active Attention Details\n" + DETAIL_T1)
        install, new = write_manifested_pair(tmp_path, legacy, PACKAGE_BOARD)

        res = run_tool(UPDATER, "--install", install, "--new", new, "--check")
        assert res.returncode == 0, res.stdout + res.stderr
        assert "MIGRATE" in res.stdout

        mig = run_tool(MIGRATE, "--install", install, "--new", new, "--apply")
        assert mig.returncode == 0, mig.stdout + mig.stderr
        bodies = regions_of(install / "attention_board.md")
        assert bodies["active_attention_details"] == "\n" + DETAIL_T1
        assert bodies["active_items"] == "\n| parser_retry | in_progress |\n"
        assert "---" not in bodies["active_attention_details"]

        final = run_tool(UPDATER, "--install", install, "--new", new, "--apply")
        assert final.returncode == 0, final.stdout + final.stderr
        bodies = regions_of(install / "attention_board.md")
        assert "V2 package prose, rewritten." in (install / "attention_board.md").read_text()
        assert bodies["active_attention_details"] == "\n" + DETAIL_T1
        assert bodies["active_items"] == "\n| parser_retry | in_progress |\n"
