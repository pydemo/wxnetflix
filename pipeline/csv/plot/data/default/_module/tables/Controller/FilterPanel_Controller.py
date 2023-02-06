import wx
import os
from os.path import isfile, dirname, join
import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import reciever


from ui_layer.utils import exception
from pathlib import Path
from ui_layer.Base import reciever, Base
from ui_layer.common import open_editor
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic


#---------------------------------------------------------------------------
class FilterPanel_Controller(Base):
    def __init__(self):
       pass

    def OnSearchMenu(self, event):

        # Catch the search type (name or content)
        searchMenu = self.filter.GetMenu().GetMenuItems()
        self.fullSearch = searchMenu[1].IsChecked()
        print('FULL SEARCH 2:', self.fullSearch)
        if self.fullSearch:
            self.send('filterlog','Filter: OnSearchMenu: Full search')
            self.OnSearch()
            
        else:
            self.send('filterlog','Filter: OnSearchMenu: Recreate list')
            self.RecreateList()

    def _search(self, item, keyword):
        self.send('filterlog','_search')
        if 0:
            """ Returns whether a Item contains the search keyword or not. """
            fid = open(GetOriginalFilename(item), "rt")
            fullText = fid.read()
            fid.close()

            if six.PY2:
                fullText = fullText.decode("iso-8859-1")

            if fullText.find(keyword) >= 0:
                return True
        else:
            fullText = ','.join(item)
            #print(555, fullText, keyword, fullText.find(keyword))
            if fullText.find(keyword) >= 0:
                return True
        return False
    
    def OnSearch(self, event=None):
        value = self.filter.GetValue()
        self.send('filterlog','OnSearch: "%s"' % value)
        #_itemList=uic._itemList
        
        if not value:
            self.RecreateList()
            return
        if 0:
            wx.BeginBusyCursor()
            self.searchItems=[]
            for item in _itemList:
                
                
                if self._search(item, value):
                        self.searchItems.append(item)
            #pp(self.searchItems)
            wx.EndBusyCursor()
        self.RecreateList()

    #---------------------------------------------
    def OnItemExpanded(self, event):
        item = event.GetItem()
        wx.LogMessage("OnItemExpanded: %s" % self.slist.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnItemCollapsed(self, event):
        item = event.GetItem()
        wx.LogMessage("OnItemCollapsed: %s" % self.slist.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnTreeLeftDown(self, event):
        # reset the overview text if the tree item is clicked on again
        pt = event.GetPosition()
        item, flags = self.slist.HitTest(pt)
        #if item == self.slist.GetSelection():
        #    #self.SetOverview(self.tree.GetItemText(item)+" Overview", self.curOverview)
        #    pass
        event.Skip()

    #---------------------------------------------
    def OnSelChanged(self, event):


        #self.StopDownload()

        item = event.GetItem()
        itemText = self.slist.GetItemText(item)
        print('selection changed')
        #self.LoadDemo(itemText)

        #self.StartDownload()
        