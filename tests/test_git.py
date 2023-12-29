import pytest
from dulwich.repo import Repo

import source.git as g


@pytest.fixture()
def repo(tmpdir) -> Repo:
    repo = Repo.init(tmpdir)
    config = repo.get_config()
    config.set("user", "email", "test@pytest")
    config.set("user", "name", "pytest")
    config.write_to_path()
    return repo


def test_toplevel_in_repo(repo) -> None:
    assert repo.path == g.toplevel(repo.path)


def test_toplevel_in_repo_child_dir(repo) -> None:
    child = repo.path.mkdir("child")
    assert repo.path == g.toplevel(child)


def test_toplevel_not_in_repo(tmpdir) -> None:
    assert None is g.toplevel(tmpdir)


def test_toplevel_non_exsisting_path(tmpdir) -> None:
    assert None is g.toplevel(tmpdir / "not_created_repo")
