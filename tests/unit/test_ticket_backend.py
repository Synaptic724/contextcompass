"""Literal backend selection for tools that must not guess before writing."""

from __future__ import annotations

import pathlib

import pytest

from conftest import PKG_ROOT
from ticket_backend import BackendConfigError, backend_from_yaml, read_backend

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("text,expected", [
    ("", "local"),
    ("version: 2\n", "local"),
    ("work_tracking:\n", "local"),
    ("work_tracking:\n  github_codex_plugin:\n    issues_repository: team/app\n", "local"),
    ("work_tracking:\n  backend: local\n", "local"),
    ("work_tracking:\n  backend: files # legacy\n", "local"),
    ("work_tracking:\n  backend: 'files'\n", "local"),
    ('"work_tracking":\n  "backend": "github_codex_plugin" # comment\n', "github_codex_plugin"),
    ("work_tracking: # settings\n    backend: github_codex_plugin\n", "github_codex_plugin"),
    ("---\nwork_tracking:\n  backend: local\n...\n", "local"),
    ("\ufeffwork_tracking:\n  backend: github_codex_plugin\n", "github_codex_plugin"),
    ("work_tracking:\n  backend: local\n  other:\n    backend: github_codex_plugin\n", "local"),
])
def test_literal_backend_settings(text, expected):
    assert backend_from_yaml(text) == expected


@pytest.mark.parametrize("text", [
    "work_tracking:\n  backend:\n",
    'work_tracking:\n  backend: ""\n',
    "work_tracking:\n  backend: null\n",
    "work_tracking:\n  backend: unknown\n",
    "work_tracking:\n  backend: github\n",
    "work_tracking:\n  backend: local#not-a-comment\n",
    "work_tracking:\n  backend: local\n  backend: github_codex_plugin\n",
    "work_tracking:\n  backend: local\nwork_tracking:\n  backend: local\n",
    "work_tracking: {backend: github_codex_plugin}\n",
    "work_tracking: *defaults\n",
    "work_tracking:\n  <<: *defaults\n",
    "<<: *defaults\n",
    "work_tracking:\n  backend: &choice local\n",
    "work_tracking:\n  backend: !!str local\n",
    "work_tracking:\n\tbackend: local\n",
    "work_tracking:\n  backend:local\n",
    "  work_tracking:\n    backend: local\n",
    "work_tracking:\n  backend: local\n---\nwork_tracking:\n  backend: local\n",
])
def test_ambiguous_or_unsupported_selectors_stop(text):
    with pytest.raises(BackendConfigError):
        backend_from_yaml(text)


def test_missing_legacy_config_defaults_local(tmp_path):
    assert read_backend(tmp_path / "config/context_compass_config.yaml") == "local"


def test_unreadable_config_does_not_default_local(tmp_path, monkeypatch):
    def denied(*args, **kwargs):
        raise PermissionError("test denial")

    monkeypatch.setattr(pathlib.Path, "read_text", denied)
    with pytest.raises(BackendConfigError):
        read_backend(tmp_path / "config.yaml")


def test_invalid_encoding_stops(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_bytes(b"\xff")
    with pytest.raises(BackendConfigError):
        read_backend(path)


def test_published_yaml_resolves_with_the_standard_library_helper():
    assert read_backend(PKG_ROOT / "config/context_compass_config.yaml") == "local"
