import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pcbnew
import pytest
import wx
from dulwich.repo import Repo

from source.git_plugin_action import (
    GitPluginAction,
    get_board,
    get_git_version,
    get_kicad_version,
    get_repo_dir,
    setup_logging,
)


def test_if_plugin_loads() -> None:
    dirname = Path(os.path.realpath(__file__)).parents[1]
    pcbnew.LoadPluginModule(dirname, "source", "")
    not_loaded = pcbnew.GetUnLoadableWizards()
    assert not_loaded == "", pcbnew.GetWizardsBackTrace()


def test_setup_logging(tmpdir: Path) -> None:
    setup_logging(str(tmpdir))
    assert Path(f"{tmpdir}/kicadgit.log").exists()


def test_get_kicad_version() -> None:
    assert get_kicad_version()[0] in ["7", "8"]


@patch("pcbnew.Version")
def test_get_kicad_version_unsupported(mock_pcbnew_version: MagicMock) -> None:
    mock_pcbnew_version.return_value = "6.0.11"
    with pytest.raises(Exception, match="KiCad version 6.0.11 is not supported"):
        get_kicad_version()


def test_git_version() -> None:
    assert get_git_version().startswith("git version ")


@patch("source.git.version", side_effect=Exception("Mocked exception"))
def test_git_version_executable_missing(mock_git_version: MagicMock) -> None:
    _ = mock_git_version
    with pytest.raises(
        Exception, match="Could not find git executable: Mocked exception"
    ):
        get_git_version()


@patch("source.git.version")
def test_git_version_unexpected_value(mock_git_version: MagicMock) -> None:
    mock_git_version.return_value = "git: 'xxx' is not a git command"
    with pytest.raises(
        Exception,
        match="Could not find git executable: "
        f"Unexpected git version: {mock_git_version.return_value}",
    ):
        get_git_version()


@patch("pcbnew.GetBoard")
def test_get_board(mock_get_board: MagicMock) -> None:
    mock_board = MagicMock()
    mock_get_board.return_value = mock_board
    mock_board.GetFileName.return_value = "test_board.kicad_pcb"

    result_board, result_board_file = get_board()

    assert result_board == mock_board
    assert result_board_file == "test_board.kicad_pcb"


@patch("pcbnew.GetBoard", return_value=None)
def test_get_board_no_board(mock_get_board: MagicMock) -> None:
    _ = mock_get_board
    with pytest.raises(Exception, match="Could not load board"):
        get_board()


@patch("pcbnew.GetBoard")
def test_get_board_no_board_file(mock_get_board: MagicMock) -> None:
    mock_board = MagicMock()
    mock_get_board.return_value = mock_board
    mock_board.GetFileName.return_value = None

    with pytest.raises(
        Exception, match="Could not locate .kicad_pcb file, open or create it first"
    ):
        get_board()


def test_get_repo_dir(repo: Repo) -> None:
    board = f"{repo.path}/fake.kicad_pcb"
    assert get_repo_dir(board) == repo.path


def test_get_repo_dir_exception(tmpdir: Path) -> None:
    with pytest.raises(Exception, match="Could not locate git repository"):
        get_repo_dir(f"{tmpdir}/fake.kicad_pcb")


@patch("wx.GetActiveWindow")
@patch("source.git_plugin_action.setup_logging")
@patch("source.git_plugin_action.get_kicad_version", return_value="KiCad 7.0.0")
@patch("source.git_plugin_action.get_git_version", return_value="git version 2.0.0")
@patch(
    "source.git_plugin_action.get_board",
    return_value=(MagicMock(), "test_board.kicad_pcb"),
)
@patch("source.git_plugin_action.get_repo_dir", return_value="/path/to/repo")
@patch("source.git.citool")
def test_run_success(
    mock_citool: MagicMock,
    mock_get_repo_dir: MagicMock,
    mock_get_board: MagicMock,
    mock_get_git_version: MagicMock,
    mock_get_kicad_version: MagicMock,
    mock_setup_logging: MagicMock,
    mock_get_active_window: MagicMock,
) -> None:
    action = GitPluginAction()

    with patch.object(
        wx, "MessageDialog", side_effect=wx.MessageDialog
    ) as mock_message_dialog:
        action.Run()

    mock_get_active_window.assert_called_once()
    mock_setup_logging.assert_called_once()
    mock_get_kicad_version.assert_called_once()
    mock_get_git_version.assert_called_once()
    mock_get_board.assert_called_once()
    mock_get_repo_dir.assert_called_once()
    mock_citool.assert_called_once_with("/path/to/repo")
    mock_message_dialog.assert_not_called()
