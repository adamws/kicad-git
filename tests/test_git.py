from textwrap import dedent

import pytest
from dulwich import porcelain
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


def test_unmodified_in_fresh_repo(repo) -> None:
    assert g.check_unmodified(repo.path)


def test_unmodified_in_repo_with_staged_content(repo) -> None:
    with open(f"{repo.path}/foo", "w") as f:
        f.write("bar")
    repo.stage(["foo"])
    assert not g.check_unmodified(repo.path)


def test_unmodified_specific_file_in_repo_with_staged_content(repo) -> None:
    for name in ["foo", "bar"]:
        with open(f"{repo.path}/{name}", "w") as f:
            f.write("baz")
    repo.stage(["foo"])
    repo.do_commit(b"message")
    assert g.check_unmodified(repo.path, "foo")


def test_add_content(repo) -> None:
    with open(f"{repo.path}/foo", "w") as f:
        f.write("bar")
    g.add(repo.path, "foo")
    assert porcelain.status(repo.path).staged["add"] == [b"foo"]


def test_get_commit_info(repo) -> None:
    with open(f"{repo.path}/foo", "w") as f:
        f.write("bar")
    g.add(repo.path, "foo")

    expected = """
    # Please enter the commit message for your changes. Lines starting
    # with '#' will be ignored, and an empty message aborts the commit.
    """
    assert g.commit_info(repo.path).startswith(dedent(expected))


def test_commit_content(repo) -> None:
    with open(f"{repo.path}/foo", "w") as f:
        f.write("bar")
    g.add(repo.path, "foo")
    g.commit(repo.path, "foo", "test message")
