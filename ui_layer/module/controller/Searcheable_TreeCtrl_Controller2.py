import wx
import os
from os.path import isfile, dirname, join
import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import reciever


from ui_layer.utils import exception
from pathlib import Path

from ui_layer.common import open_editor
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic


#---------------------------------------------------------------------------
class Controller2(object):
    def __init__(self):
       pass

    def OnSearchMenu(self, event):

        # Catch the search type (name or content)
        searchMenu = self.filter.GetMenu().GetMenuItems()
        fullSearch = searchMenu[1].IsChecked()

        if fullSearch:
            self.OnSearch()
        else:
            self.RecreateTree()

    def _search(self, name, keyword):
        if 0:
            """ Returns whether a Item contains the search keyword or not. """
            fid = open(GetOriginalFilename(name), "rt")
            fullText = fid.read()
            fid.close()

            if six.PY2:
                fullText = fullText.decode("iso-8859-1")

            if fullText.find(keyword) >= 0:
                return True
        else:
            fullText = ','.join(name)
            
            if fullText.find(keyword) >= 0:
                return True
        return False
    
    def OnSearch(self, event=None):
        _treeList=uic._treeList

        value = self.filter.GetValue()
        if not value:
            self.RecreateTree()
            return

        wx.BeginBusyCursor()
        self.searchItems={}
        for category, items in _treeList:
            self.searchItems[category] = []
            for childItem in items:
                if self._search([category, childItem], value):
                    self.searchItems[category].append(childItem)
        #pp(self.searchItems)
        wx.EndBusyCursor()
        self.RecreateTree()

    #---------------------------------------------
    def OnItemExpanded(self, event):
        item = event.GetItem()
        wx.LogMessage("OnItemExpanded: %s" % self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnItemCollapsed(self, event):
        item = event.GetItem()
        wx.LogMessage("OnItemCollapsed: %s" % self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnTreeLeftDown(self, event):
        # reset the overview text if the tree item is clicked on again
        pt = event.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item == self.tree.GetSelection():
            #self.SetOverview(self.tree.GetItemText(item)+" Overview", self.curOverview)
            pass
        event.Skip()

    #---------------------------------------------
    def OnSelChanged(self, event):


        #self.StopDownload()

        item = event.GetItem()
        itemText = self.tree.GetItemText(item)
        print('selection changed')
        #self.LoadDemo(itemText)

        #self.StartDownload()
        