import logging
import os
import sys

import pcbnew
import wx

from .git import git_toplevel, git_commit_info, git_add, git_commit
from .git_dialog import GitDialog


logger = logging.getLogger(__name__)


class GitPluginAction(pcbnew.ActionPlugin):
    def defaults(self) -> None:
        self.name = "Git Plugin"
        self.category = ""
        self.description = ""
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "icon.png")

    def Initialize(self) -> None:
        version = pcbnew.Version()
        if int(version.split(".")[0]) < 6:
            msg = f"KiCad version {version} is not supported"
            raise Exception(msg)
        self.board = pcbnew.GetBoard()

        self.board_file = self.board.GetFileName()
        if not self.board_file:
            msg = "Could not locate .kicad_pcb file, open or create it first"
            raise Exception(msg)

        self.board_dir = os.path.dirname(os.path.abspath(self.board_file))

        self.repo_dir = git_toplevel(self.board_dir)
        if self.repo_dir == "":
            msg = "Could not locate git repository"
            raise Exception(msg)

        # Remove all handlers associated with the root logger object.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # set up logger
        logging.basicConfig(
            level=logging.DEBUG,
            filename=f"{self.board_dir}/kicadgit.log",
            filemode="w",
            format="%(asctime)s %(name)s %(lineno)d: %(message)s",
            datefmt="%H:%M:%S",
        )
        logger.info("Plugin executed with KiCad version: " + version)
        logger.info("Plugin executed with python version: " + repr(sys.version))
        logger.info("Repository top directory: {}".format(self.repo_dir.strip()))

    def Run(self) -> None:
        self.Initialize()

        git_add(self.repo_dir, self.board_file)
        commit_info = git_commit_info(self.repo_dir, self.board_file)

        dlg = GitDialog(wx.GetActiveWindow(), commit_info)
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.get_commit_message()
            if message:
                git_commit(self.repo_dir, self.board_file, message)

        dlg.Destroy()
        logging.shutdown()
