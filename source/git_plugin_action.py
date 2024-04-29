import logging
import os
import sys
from pathlib import Path
from typing import Tuple

import pcbnew
import wx

from . import git

logger = logging.getLogger(__name__)


class PluginError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


def setup_logging(destination: str) -> None:
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # set up logger
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"{destination}/kicadgit.log",
        filemode="w",
        format="%(asctime)s %(name)s %(lineno)d: %(message)s",
        datefmt="%H:%M:%S",
    )


def get_kicad_version() -> str:
    version = pcbnew.Version()
    if int(version.split(".")[0]) < 7:
        msg = f"KiCad version {version} is not supported"
        raise PluginError(msg)
    logger.info(f"Plugin executed with KiCad version: {version}")
    logger.info(f"Plugin executed with python version: {repr(sys.version)}")
    return version


def get_git_version() -> str:
    try:
        git_version = git.version()
        if not git_version.startswith("git version "):
            msg = f"Unexpected git version: {git_version}"
            raise PluginError(msg)
    except Exception as e:
        msg = f"Could not find git executable: {e}"
        raise PluginError(msg)
    logger.info(f"Plugin executed with {git_version}")
    return git_version


def get_board() -> Tuple[pcbnew.BOARD, str]:
    board = pcbnew.GetBoard()
    if not board:
        msg = "Could not load board"
        raise PluginError(msg)
    board_file = board.GetFileName()
    if not board_file:
        msg = "Could not locate .kicad_pcb file, open or create it first"
        raise PluginError(msg)
    logger.info(f"Board file: {board_file}")
    return board, board_file


def get_repo_dir(board_file: str) -> Path:
    board_dir = Path(board_file).parent
    repo_dir = git.toplevel(board_dir)
    if repo_dir is None:
        msg = "Could not locate git repository"
        raise PluginError(msg)
    logger.info(f"Repository top directory: {repo_dir}")
    return repo_dir


class GitPluginAction(pcbnew.ActionPlugin):
    def defaults(self) -> None:
        self.name = "Git Plugin"
        self.category = ""
        self.description = ""
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "icon.png")

    def Initialize(self) -> None:
        self.window = wx.GetActiveWindow()
        self.plugin_path = os.path.dirname(__file__)
        setup_logging(self.plugin_path)

        _ = get_kicad_version()
        _ = get_git_version()

        self.board, self.board_file = get_board()
        self.repo_dir = get_repo_dir(self.board_file)

    def Run(self) -> None:
        try:
            self.Initialize()
            self.board.Save(self.board_file)
            git.guitool(self.repo_dir)
        except PluginError as e:
            error = wx.MessageDialog(self.window, e.message, style=wx.ICON_ERROR)
            error.ShowModal()

        logging.shutdown()
