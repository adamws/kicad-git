from pathlib import Path

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
