from dulwich.repo import Repo

import source.git as g


def test_toplevel_in_repo(tmpdir) -> None:
    Repo.init(tmpdir)
    assert tmpdir == g.toplevel(tmpdir)


def test_toplevel_in_repo_child_dir(tmpdir) -> None:
    Repo.init(tmpdir)
    child = tmpdir.mkdir("child")
    assert tmpdir == g.toplevel(child)


def test_toplevel_not_in_repo(tmpdir) -> None:
    assert None is g.toplevel(tmpdir)


def test_toplevel_non_exsisting_path(tmpdir) -> None:
    assert None is g.toplevel(tmpdir / "not_created_repo")
