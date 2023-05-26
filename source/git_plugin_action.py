import logging
import os
import sys

import pcbnew
import wx

from .git_dialog import GitDialog


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

        board_file = self.board.GetFileName()
        if not board_file:
            msg = f"Could not locate .kicad_pcb file, open or create it first"
            raise Exception(msg)

        # go to the project folder - so that log will be in proper place
        os.chdir(os.path.dirname(os.path.abspath(board_file)))

        # Remove all handlers associated with the root logger object.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # set up logger
        logging.basicConfig(
            level=logging.DEBUG,
            filename="kicadgit.log",
            filemode="w",
            format="%(asctime)s %(name)s %(lineno)d: %(message)s",
            datefmt="%H:%M:%S",
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Plugin executed with KiCad version: " + version)
        self.logger.info("Plugin executed with python version: " + repr(sys.version))

    def Run(self) -> None:
        self.Initialize()

        pcb_frame = [x for x in wx.GetTopLevelWindows() if x.GetName() == "PcbFrame"][0]

        dlg = GitDialog(pcb_frame, "git")
        if dlg.ShowModal() == wx.ID_OK:
            pass

        dlg.Destroy()
        logging.shutdown()
