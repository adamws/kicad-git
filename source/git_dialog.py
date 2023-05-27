import wx


GIT_COMMIT_MESSAGE_COLUMNS = 80
GIT_COMMENT_CHAR = "#"


class GitDialog(wx.Dialog):
    def __init__(self, parent, commit_info) -> None:
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(GitDialog, self).__init__(parent, -1, "Git Commit", style=style)

        box = wx.BoxSizer(wx.VERTICAL)

        commit_message = wx.TextCtrl(self, style=wx.TE_MULTILINE)
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
