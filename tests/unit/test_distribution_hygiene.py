"""Keep local operating state out of the release source archive."""

from __future__ import annotations

import ast
import re

import pytest

from conftest import PKG_ROOT

pytestmark = pytest.mark.unit


def sdist_section():
    text = (PKG_ROOT.parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r"(?ms)^\[tool.hatch.build.targets.sdist\]\n(.*?)(?=^\[|\Z)", text)
    assert match is not None
    return match.group(1)


def test_sdist_explicitly_selects_product_and_maintainer_files():
    section = sdist_section()
    selected = re.search(r"(?ms)^only-include\s*=\s*(\[[^\]]*\])", section)
    assert selected is not None, "Broad globs can include private README/LICENSE copies"
    assert set(ast.literal_eval(selected.group(1))) == {
        "src/context_compass", "src/contextcompass_cli", "tests", "contributor",
        "AGENTS.md", "README.md", "LICENSE", "NOTICE", "pyproject.toml",
        ".github/workflows/python-publish.yml",
    }


def test_sdist_excludes_nested_harness_state_and_bytecode():
    section = sdist_section()
    for pattern in ("**/.codex/**", "**/.agents/**", "**/__pycache__/**", "**/*.pyc", "**/*.pyo"):
        assert pattern in section
