import wx
from pprint import pprint as pp
class DoubleClick():
    def __init__(self, method):
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClick)
        self.method=method
    def OnClick(self, event):
        print ('OnClick', event.GetText())

        self.method(event.Index)
