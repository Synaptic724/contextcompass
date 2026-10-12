"""The `contextcompass` CLI, run the way a user runs it.

These go through `main()` with real argv rather than calling the command
functions, because the argparse wiring is where the first version broke: it
declared `--apply` and not `--check`, so the documented default invocation
failed with "unrecognized arguments".
"""

from __future__ import annotations

import pathlib
import shutil
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import contextcompass_cli as contextcompass  # noqa: E402
from contextcompass_cli.__main__ import main  # noqa: E402

from conftest import TOOLS, run_tool  # noqa: E402

pytestmark = pytest.mark.integration

MANIFEST = TOOLS / "package_manifest.py"


@pytest.fixture(scope="session")
def golden_install(tmp_path_factory):
    """One real `init`, reused as the source for every test that needs a copy.

    `init` copies ~440 files, and on a network-mounted checkout that is ~3s per
    call - sixteen tests doing their own would take a minute of pure I/O.
    Copying once and then locally is ~300x faster and tests the same thing,
    since what is under test is the CLI's behaviour, not copytree's.
    """
    root = tmp_path_factory.mktemp("golden")
    assert main(["init", "--into", str(root)]) == 0
    return root / "context_compass"


@pytest.fixture
def installed(golden_install, tmp_path):
    """A fresh, writable install per test."""
    dst = tmp_path / "context_compass"
    shutil.copytree(golden_install, dst)
    return dst


class TestPayloadResolution:
    def test_payload_is_found_in_a_source_checkout(self):
        """Without the source fallback the CLI only works after a build, so
        every test would exercise a different path from the one users get."""
        assert contextcompass.PAYLOAD.is_dir()
        assert (contextcompass.PAYLOAD / "AGENTS.MD").is_file()

    def test_payload_carries_the_whole_package(self):
        n = sum(1 for p in contextcompass.PAYLOAD.rglob("*")
                if p.is_file() and "__pycache__" not in p.parts)
        assert n > 400, f"payload has only {n} files - the Markdown is the product"

    def test_version_matches_the_payload_manifest(self):
        """Two places record a version. A test is what keeps them honest."""
        manifest = (contextcompass.PAYLOAD / "MANIFEST.md").read_text(encoding="utf-8")
        recorded = next(l.split("|")[2].strip() for l in manifest.splitlines()
                        if l.startswith("| package_version |"))
        assert contextcompass.__version__ == recorded

    def test_the_source_directory_mirrors_the_install_directory(self):
        """`src/context_compass/` is what lands as `context_compass/`.

        Deliberately identical, so there is no translation step between what a
        contributor reads in the repository and what a user gets. These two are
        the pair that SHOULD match.
        """
        assert contextcompass.SOURCE_DIRNAME == contextcompass.INSTALL_DIRNAME
        assert contextcompass.INSTALL_DIRNAME == "context_compass"

    def test_the_module_name_matches_neither_directory(self):
        """This is the one that must never collide.

        A module sharing a name with the directory sitting in the user's repo
        resolves differently depending on how Python was invoked - the local
        folder wins from the repo root, the installed package wins from
        anywhere else. Same machine, same venv, different answer.
        """
        assert contextcompass.__name__ == "contextcompass_cli"
        assert contextcompass.__name__ != contextcompass.INSTALL_DIRNAME
        assert contextcompass.__name__ != contextcompass.SOURCE_DIRNAME


class TestInit:
    def test_init_creates_the_install(self, tmp_path, capsys):
        assert main(["init", "--into", str(tmp_path)]) == 0
        target = tmp_path / "context_compass"
        assert (target / "AGENTS.MD").is_file()
        assert (target / "SKILLS.MD").is_file()
        assert sum(1 for p in target.rglob("*") if p.is_file()) > 400

    def test_the_result_validates_against_its_own_manifest(self, tmp_path):
        main(["init", "--into", str(tmp_path)])
        res = run_tool(MANIFEST, "--root", tmp_path / "context_compass", "--check")
        assert res.returncode == 0, res.stdout
        assert "OK: manifest is current" in res.stdout

    def test_no_bytecode_is_copied_into_the_repo(self, tmp_path):
        """Importing the payload's tools compiles bytecode into the installed
        package. Copying that in puts untracked binaries in someone's first
        commit and makes the install disagree with its own manifest."""
        import compileall
        compileall.compile_dir(str(contextcompass.PAYLOAD / "tools"), quiet=2)

        main(["init", "--into", str(tmp_path)])
        target = tmp_path / "context_compass"
        assert not list(target.rglob("__pycache__"))
        assert not list(target.rglob("*.pyc"))

    def test_init_check_writes_nothing(self, tmp_path, capsys):
        assert main(["init", "--into", str(tmp_path), "--check"]) == 0
        assert "WOULD CREATE" in capsys.readouterr().out
        assert not (tmp_path / "context_compass").exists()

    def test_init_refuses_to_overwrite(self, tmp_path, capsys):
        main(["init", "--into", str(tmp_path)])
        assert main(["init", "--into", str(tmp_path)]) == 2
        out = capsys.readouterr().out
        assert "REFUSED" in out and "upgrade" in out

    def test_refusal_leaves_the_existing_install_intact(self, tmp_path):
        main(["init", "--into", str(tmp_path)])
        marker = tmp_path / "context_compass" / "tickets" / "tasks" / "MY_TICKET.md"
        marker.write_text("# mine\n")
        main(["init", "--into", str(tmp_path)])
        assert marker.read_text() == "# mine\n"


class TestUpgrade:
    def test_check_is_the_default_and_writes_nothing(self, installed, capsys):
        before = {p: p.read_bytes() for p in installed.rglob("*") if p.is_file()}
        assert main(["upgrade", "--install", str(installed)]) == 0
        assert {p: p.read_bytes() for p in installed.rglob("*") if p.is_file()} == before

    def test_check_flag_is_accepted(self, installed):
        """The first version declared --apply and not --check, so the
        documented default invocation errored out."""
        assert main(["upgrade", "--install", str(installed), "--check"]) == 0

    @pytest.mark.parametrize("flag", ["--keep-retired", "--preserve-local", "--seed-instance"])
    def test_passthrough_flags_are_accepted(self, installed, flag):
        assert main(["upgrade", "--install", str(installed), "--check", flag]) == 0

    def test_an_unknown_flag_is_rejected(self, installed):
        """Forwarding blindly would let a typo through to a tool that ignores
        it, and the run would look like it honoured a flag it never saw."""
        with pytest.raises(SystemExit):
            main(["upgrade", "--install", str(installed), "--seed-instanse"])

    def test_upgrade_from_an_older_install_applies_changes(self, installed):
        """The real path: an install a few versions back gets brought current.

        The file is made stale FIRST and the manifest regenerated after, so the
        install matches its own manifest and the package is the side that moved.
        That is the `replace` row of the three-hash table.
        """
        stale = installed / "agent_onboarding" / "default" / "engineer" / "SKILLS.MD"
        current = stale.read_bytes()
        stale.write_bytes(b"# an older version of this file\n")
        run_tool(MANIFEST, "--root", installed, "--version", "2.3.1")

        assert main(["upgrade", "--install", str(installed), "--apply"]) == 0
        assert stale.read_bytes() == current

    def test_a_local_edit_survives_when_the_package_did_not_move(self, installed):
        """The `keep` row, and the reason package_version is not the input: the
        install is stamped two versions back, but the file itself is unchanged
        upstream, so there is nothing to conform to and the edit stands."""
        run_tool(MANIFEST, "--root", installed, "--version", "2.3.1")
        mine = installed / "agent_onboarding" / "default" / "engineer" / "SKILLS.MD"
        mine.write_bytes(b"# locally edited\n")

        assert main(["upgrade", "--install", str(installed), "--apply"]) == 0
        assert mine.read_bytes() == b"# locally edited\n"

    def test_upgrade_preserves_the_repo_lanes(self, installed):
        ticket = installed / "tickets" / "tasks" / "T-1.md"
        ticket.write_text("# my ticket\n")
        run_tool(MANIFEST, "--root", installed, "--version", "2.3.1")

        main(["upgrade", "--install", str(installed), "--apply"])
        assert ticket.read_text() == "# my ticket\n"

    def test_not_an_install_is_reported(self, tmp_path, capsys):
        assert main(["upgrade", "--install", str(tmp_path)]) == 2
        assert "not a Context Compass install" in capsys.readouterr().out

    def test_upgrade_preserves_live_mailbox_without_counter_protocol(self, installed):
        from cleanup_context_compass import user_regions

        board = installed / "mailbox_board.md"
        current = board.read_text(encoding="utf-8")
        assert "## Request Tracking" not in current
        assert "prompt_id" not in current
        assert not (installed / "agent_onboarding/default/general/skills/request_tracking.md").exists()
        bodies = {
            "checked_in": "| worker | runtime | 2026-01-01T00:00:00Z | never | active |\n",
            "messages": "- TO: worker\n  FROM: lead\n  CLAIM: Keep this message.\n",
            "notes": "Keep this user's standing instructions.\n",
        }
        for name, body in bodies.items():
            marker = f"<!-- BEGIN USER-DEFINED: {name} -->\n"
            current = current.replace(marker, marker + body)
        board.write_bytes(current.encode("utf-8"))
        generated = run_tool(MANIFEST, "--root", installed, "--version", "2.15.4")
        assert generated.returncode == 0, generated.stdout + generated.stderr

        assert main(["upgrade", "--install", str(installed), "--apply"]) == 0
        updated = board.read_text(encoding="utf-8")
        regions = {name: updated[s:e] for name, s, e in user_regions(updated)}
        assert "request_tracking" not in regions
        for name, body in bodies.items():
            assert regions[name] == "\n" + body

        assert main(["upgrade", "--install", str(installed), "--apply"]) == 0
        final = board.read_text(encoding="utf-8")
        regions = {name: final[s:e] for name, s, e in user_regions(final)}
        assert "request_tracking" not in regions
        for name, body in bodies.items():
            assert regions[name] == "\n" + body

    def test_install_is_auto_detected_from_cwd(self, installed, monkeypatch):
        monkeypatch.chdir(installed.parent)
        assert main(["upgrade"]) == 0


class TestMigrateBoards:
    def test_a_fresh_install_needs_no_migration(self, installed, capsys):
        assert main(["migrate-boards", "--install", str(installed)]) == 0
        assert "already has USER-DEFINED regions" in capsys.readouterr().out

    def test_a_legacy_board_is_migrated(self, installed, capsys):
        install = installed
        (install / "attention_board.md").write_text(
            "# Attention Board\n\n## Active Items\n| work_item | status |\n"
            "|---|---|\n| my_work | in_progress |\n")

        assert main(["migrate-boards", "--install", str(install), "--apply"]) == 0
        text = (install / "attention_board.md").read_text()
        assert "BEGIN USER-DEFINED" in text
        assert "| my_work | in_progress |" in text


class TestVersionCommand:
    def test_reports_installed_and_payload(self, capsys):
        assert main(["version"]) == 0
        out = capsys.readouterr().out
        assert contextcompass.__version__ in out
        assert "payload manifest" in out
