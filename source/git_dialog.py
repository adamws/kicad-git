import wx


class GitDialog(wx.Dialog):
    def __init__(self, parent, title) -> None:
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(GitDialog, self).__init__(parent, -1, title, style=style)

        box = wx.BoxSizer(wx.VERTICAL)

        buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        box.Add(buttons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(box)
