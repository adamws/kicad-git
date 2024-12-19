import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from dulwich.repo import Repo

import source.git as g


def test_get_version() -> None:
    assert g.version().startswith("git version ")


def test_toplevel_in_repo(repo: Repo) -> None:
    assert repo.path == g.toplevel(repo.path)


def test_toplevel_in_repo_child_dir(repo: Repo) -> None:
    child = repo.path.mkdir("child")
    assert repo.path == g.toplevel(child)


def test_toplevel_not_in_repo(tmpdir: Path) -> None:
    assert None is g.toplevel(tmpdir)


def test_toplevel_non_exsisting_path(tmpdir: Path) -> None:
    assert None is g.toplevel(tmpdir / "not_created_repo")


@pytest.mark.skipif(
    "DISPLAY" not in os.environ,
    reason="No DISPLAY variable defined on Unix-like system",
)
@pytest.mark.skipif("CI" in os.environ, reason="Not running on CI")
def test_default_guitool(tmpdir: Path) -> None:
    process = g.guitool(tmpdir)
    assert process
    process.terminate()


@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
def test_missing_guitool(tmpdir: Path) -> None:
    with patch("source.git.git_gui", "git gui-but-wrong"):
        with pytest.raises(RuntimeError, match="Error: Failed to run"):
            g.guitool(tmpdir)
