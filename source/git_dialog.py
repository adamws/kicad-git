import wx
from wx.stc import StyledTextCtrl

GIT_COMMIT_MESSAGE_COLUMNS = 80
GIT_COMMENT_CHAR = "#"


class GitDialog(wx.Dialog):
    def __init__(self, parent, commit_info) -> None:
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(GitDialog, self).__init__(parent, -1, "Git Commit", style=style)

        box = wx.BoxSizer(wx.VERTICAL)

        commit_message = StyledTextCtrl(self, style=wx.TE_MULTILINE)
        commit_message.SetLexer(wx.stc.STC_LEX_PYTHON)

        commit_message.StyleSetSpec(
            wx.stc.STC_STYLE_DEFAULT, "face:Courier New,size:10"
        )
        commit_message.StyleSetSpec(
            wx.stc.STC_P_COMMENTLINE, "fore:#a8a8a8,face:Courier New,size:10"
        )

        commit_message.AppendText(commit_info)

        font = commit_message.GetFont()
        line_height = commit_message.GetCharHeight()
        commit_message.SetMinSize(
            (GIT_COMMIT_MESSAGE_COLUMNS * font.GetPixelSize()[0], 20 * line_height)
        )

        box.Add(commit_message, 0, wx.EXPAND | wx.ALL, 5)

        buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        box.Add(buttons, 0, wx.EXPAND | wx.ALL, 5)

        commit_message.SetFocus()
        commit_message.SetInsertionPoint(0)

        self.SetSizerAndFit(box)

        self.__commit_message = commit_message

    def get_commit_message(self) -> str:
        message = ""
        for line in self.__commit_message.GetValue().splitlines(keepends=True):
            if line.startswith(GIT_COMMENT_CHAR):
                continue
            message += line
        return message


if __name__ == "__main__":
    import os
    import sys
    import threading
    from pathlib import Path

    from . import git

    _ = wx.App(False)

    commit_info = git.commit_info(Path(os.path.realpath(__file__)).parent)
    dlg = GitDialog(None, commit_info)

    if "PYTEST_CURRENT_TEST" in os.environ:
        # use stdin for gracefully closing GUI when running
        # from pytest. This is required when measuring
        # coverage and process kill would cause measurement to be lost
        def listen_for_exit():
            while True:
                input("Press any key to exit: ")
                dlg.Close(wx.ID_CANCEL)
                sys.exit()

        input_thread = threading.Thread(target=listen_for_exit)
        input_thread.daemon = True
        input_thread.start()

    dlg.ShowModal()
