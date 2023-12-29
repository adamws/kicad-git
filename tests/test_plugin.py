import os
from pathlib import Path

import pcbnew
import pytest
from dulwich.repo import Repo

from source.git_plugin_action import (
    get_board,
    get_git_version,
    get_kicad_version,
    get_repo_dir,
)


def test_if_plugin_loads() -> None:
    dirname = Path(os.path.realpath(__file__)).parents[1]
    pcbnew.LoadPluginModule(dirname, "source", "")
    not_loaded = pcbnew.GetUnLoadableWizards()
    assert not_loaded == "", pcbnew.GetWizardsBackTrace()


def test_get_kicad_version() -> None:
    assert get_kicad_version().startswith("7")


def test_git_version() -> None:
    assert get_git_version().startswith("git version ")


def test_get_board() -> None:
    # can't use `pcbnew.GetBoard()` from test context so exception is always expected
    with pytest.raises(Exception):
        get_board()


def test_get_repo_dir(repo: Repo) -> None:
    board = f"{repo.path}/fake.kicad_pcb"
    assert get_repo_dir(board) == repo.path


def test_get_repo_dir_exception(tmpdir: Path) -> None:
    with pytest.raises(Exception, match="Could not locate git repository"):
        get_repo_dir(f"{tmpdir}/fake.kicad_pcb")
