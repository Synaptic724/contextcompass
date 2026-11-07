"""Real tokenizer and both supported entrypoints, using disposable report output."""

import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys

import pytest

from conftest import PKG_ROOT, REPO_ROOT, TOOLS, run_tool

pytestmark = pytest.mark.integration


def snapshot():
    return {p.relative_to(PKG_ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in PKG_ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts}


def test_standalone_report_counts_real_tokens_and_every_route(tmp_path):
    import tiktoken
    before = snapshot()
    out = tmp_path / "report"
    result = run_tool(TOOLS / "token_report.py", "--root", PKG_ROOT, "--role", "engineer", "--out-dir", out)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((out / "report.json").read_text())
    assert len(report["routes"]) == len(report["roles"]) * 8
    assert all(row["status"] == "resolved_declarations" for row in report["routes"])
    row = next(row for row in report["files"] if row["path"] == "AGENTS.MD")
    expected = len(tiktoken.get_encoding("o200k_base").encode_ordinary((PKG_ROOT / "AGENTS.MD").read_bytes().decode("utf-8")))
    assert row["tokens"] == expected
    assert (out / "files.csv").is_file() and (out / "report.md").is_file()
    assert snapshot() == before


def test_cli_delegates_to_same_engine_and_uses_explicit_choices(tmp_path):
    env = dict(os.environ, PYTHONPATH=str(REPO_ROOT / "src"), PYTHONDONTWRITEBYTECODE="1")
    out = tmp_path / "cli_report"
    result = subprocess.run([sys.executable, "-m", "contextcompass_cli", "token-report",
        "--install", str(PKG_ROOT), "--role", "design_engineer", "--ticket-backend", "github_codex_plugin",
        "--communication-backend", "codex_mcp", "--event", "reonboard", "--out-dir", str(out)],
        cwd=tmp_path, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((out / "report.json").read_text())
    assert report["selected_route"] == "design_engineer/github_codex_plugin/codex_mcp/reonboard"
    selected = next(r for r in report["routes"] if r["id"] == report["selected_route"])
    assert selected["role_chain"] == ["general", "engineer", "design_engineer"]
    assert any(r["path"].endswith("github/codex_plugin.md") for r in selected["paths"])
    assert not any(r["path"].endswith("mailbox_protocol.md") for r in selected["paths"])


def test_unknown_role_and_encoding_fail_clearly(tmp_path):
    for flags in (("--role", "not_registered"), ("--encoding", "not_an_encoding")):
        result = run_tool(TOOLS / "token_report.py", "--root", PKG_ROOT, *flags, "--out-dir", tmp_path / "unused")
        assert result.returncode == 2
        assert "ERROR:" in result.stderr
        assert not (tmp_path / "unused").exists()


def test_missing_optional_tokenizer_does_not_install_anything(monkeypatch):
    from token_report import tokenizer
    from reading_routes import RouteError
    monkeypatch.setitem(sys.modules, "tiktoken", None)
    with pytest.raises(RouteError, match="Nothing was installed automatically"):
        tokenizer("o200k_base")


def test_cli_help_needs_no_tokenizer(monkeypatch, capsys):
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from contextcompass_cli.__main__ import main
    monkeypatch.setitem(sys.modules, "tiktoken", None)
    with pytest.raises(SystemExit) as exc:
        main(["token-report", "--help"])
    assert exc.value.code == 0
    assert "--role" in capsys.readouterr().out


def test_copied_tool_is_read_only_without_python_bytecode_flags(tmp_path):
    root = tmp_path / "context_compass"
    shutil.copytree(PKG_ROOT, root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    env = dict(os.environ)
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    result = subprocess.run([sys.executable, str(root / "tools/token_report.py"), "--root", str(root),
        "--role", "engineer", "--out-dir", str(tmp_path / "report")],
        cwd=tmp_path, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()} == before
