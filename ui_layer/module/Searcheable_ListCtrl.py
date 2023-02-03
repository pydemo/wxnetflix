import wx
import ui_layer.module.images as images

_demoPngs = ["overview", "recent", "frame", "dialog", "moredialog", "core",
             "book", "customcontrol", "morecontrols", "layout", "process",
             "clipboard", "images", "miscellaneous"]
             
             
USE_CUSTOMTREECTRL = False
DEFAULT_PERSPECTIVE = "Default Perspective"
from wx.lib.mixins.listctrl import ListRowHighlighter
if 0:
    if USE_CUSTOMTREECTRL:
        import wx.lib.agw.ultimatelistctrl as CT
        ListBaseClass = CT.UltimateustomListCtrl
    else:
        ListBaseClass = wx.ListCtrl
else:
    ListBaseClass = wx.ListCtrl

class Searcheable_ListCtrl(ListRowHighlighter, ListBaseClass):
    def __init__(self, parent):
        ListBaseClass.__init__(self, parent)
        self.BuildTreeImageList()
        if USE_CUSTOMTREECTRL:
            self.SetSpacing(10)
            self.SetWindowStyle(self.GetWindowStyle() & ~wx.TR_LINES_AT_ROOT)

        self.SetInitialSize((100,80))
        
        


    def AppendItem(self, parent, text, image=-1, wnd=None):
        if USE_CUSTOMTREECTRL:
            item = ListBaseClass.AppendItem(self, parent, text, image=image, wnd=wnd)
        else:
            item = ListBaseClass.AppendItem(self, parent, text, image=image)
        return item

    def BuildTreeImageList(self):
        imgList = wx.ImageList(16, 16)
        for png in _demoPngs:
            imgList.Add(images.catalog[png].GetBitmap())

        # add the image for modified demos.
        imgList.Add(images.catalog["custom"].GetBitmap())

        self.AssignImageList(imgList, wx.IMAGE_LIST_NORMAL)


    def GetItemIdentity(self, item):
        return self.GetItemData(item)
        
        
        