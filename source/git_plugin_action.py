import logging
import os
import sys
from pathlib import Path

import pcbnew
import wx

from . import git

logger = logging.getLogger(__name__)


class PluginException(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


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

        version = pcbnew.Version()
        if int(version.split(".")[0]) < 7:
            msg = f"KiCad version {version} is not supported"
            raise PluginException(msg)

        self.board = pcbnew.GetBoard()
        self.board_file = self.board.GetFileName()
        if not self.board_file:
            msg = "Could not locate .kicad_pcb file, open or create it first"
            raise PluginException(msg)

        try:
            git_version_str = git.version()
            if not git_version_str.startswith("git version "):
                msg = "Could not find git executable"
                raise PluginException(msg)
        except Exception as e:
            msg = f"Could not find git executable: {e}"
            raise PluginException(msg)

        self.board_dir = Path(self.board_file).parent

        self.repo_dir = git.toplevel(self.board_dir)
        if self.repo_dir is None:
            msg = "Could not locate git repository"
            raise PluginException(msg)

        # Remove all handlers associated with the root logger object.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # set up logger
        logging.basicConfig(
            level=logging.DEBUG,
            filename=f"{self.plugin_path}/kicadgit.log",
            filemode="w",
            format="%(asctime)s %(name)s %(lineno)d: %(message)s",
            datefmt="%H:%M:%S",
        )
        logger.info(f"Plugin executed with KiCad version: {version}")
        logger.info(f"Plugin executed with python version: {repr(sys.version)}")
        logger.info(f"Repository top directory: {self.repo_dir}")
        logger.info(f"Board file: {self.board_file}")

    def Run(self) -> None:
        initialized = False
        try:
            self.Initialize()
            initialized = True
        except PluginException as e:
            error = wx.MessageDialog(self.window, e.message, style=wx.ICON_ERROR)
            error.ShowModal()

        if initialized and self.repo_dir:
            self.board.Save(self.board_file)
            git.citool(self.repo_dir)

        logging.shutdown()
