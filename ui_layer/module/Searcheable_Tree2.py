import wx
import os, time
from os.path import isfile, dirname, join
import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import reciever


from ui_layer.utils import exception
from pathlib import Path

from ui_layer.common import open_editor
from ui_layer.module.controller.Searcheable_TreeCtrl_Controller2 import Controller2
from ui_layer.module.Searcheable_TreeCtrl2 import Searcheable_TreeCtrl2


import ui_layer.config.ui_config as ui_config
uic = ui_config.uic



USE_CUSTOMTREECTRL = False
DEFAULT_PERSPECTIVE = "Default Perspective"


#_treeList = []
#---------------------------------------------------------------------------
# Show how to derive a custom wxLog class

class MyLog(wx.Log):
    def __init__(self, textCtrl, logTime=0):
        wx.Log.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime

    def DoLogText(self, message):
        if self.tc:
            self.tc.AppendText(message + '\n')
            
def GetDataDir():
    """
    Return the standard location on this platform for application data
    """
    sp = wx.StandardPaths.Get()
    return sp.GetUserDataDir()
    
def GetConfig():
    if not os.path.exists(GetDataDir()):
        os.makedirs(GetDataDir())

    config = wx.FileConfig(
        localFilename=os.path.join(GetDataDir(), "options"))
    return config
    
def DoesModifiedExist(name):
    """Returns whether the specified demo has a modified copy"""
    if os.path.exists(GetModifiedFilename(name)):
        return True
    else:
        return False
#---------------------------------------------------------------------------
class Searcheable_Tree2(Controller2):
    def __init__(self, parent):
        def EmptyHandler(evt): pass
        self.parent=parent
        self.ReadConfigurationFile()
        
        self.tree = Searcheable_TreeCtrl2(parent)

        self.filter = wx.SearchCtrl(parent, style=wx.TE_PROCESS_ENTER)
        self.filter.ShowCancelButton(True)
        #self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN,
                         lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT, self.OnSearch) #EVT_TEXT_ENTER
        if 1:
            searchMenu = wx.Menu()
            item = searchMenu.AppendRadioItem(-1, "Caseless")
            parent.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
            item = searchMenu.AppendRadioItem(-1, "Exact")
            parent.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
            self.filter.SetMenu(searchMenu)
        self.treeMap = {}
        self.searchItems = {}
        uic._treeList=[]
        uic.ppl={'name':'Select pipline'}
        self.RecreateTree()
        self.tree.SetExpansionState(self.expansionState)
        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
        # add the windows to the splitter and split it.
        leftBox = wx.BoxSizer(wx.VERTICAL)
        leftBox.Add(self.tree, 1, wx.EXPAND)
        leftBox.Add(wx.StaticText(parent, label = "Filter details:"), 0, wx.TOP|wx.LEFT, 5)
        leftBox.Add(self.filter, 0, wx.EXPAND|wx.ALL, 5)
        if 'wxMac' in wx.PlatformInfo:
            leftBox.Add((5,5))  # Make sure there is room for the focus ring
        #parent.SetSizer(leftBox)
        
        parent.SetSizerAndFit(leftBox)
        leftBox.Layout()
        if 1:
            # Set up a log window
            self.log = wx.TextCtrl(parent, -1,
                                  style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            self.log.Show(False)
            if wx.Platform == "__WXMAC__":
                self.log.MacCheckSpelling(False)

            # Set the wxWindows log target to be this textctrl
            #wx.Log.SetActiveTarget(wx.LogTextCtrl(self.log))

            # But instead of the above we want to show how to use our own wx.Log class
            wx.Log.SetActiveTarget(MyLog(self.log))
            

    def RecreateTree(self, evt=None):
        #global _treeList
        
        #for x in treeList:
        #    _treeList.append(x)
        _treeList =uic._treeList
        ppl=uic.ppl
        with wx.WindowDisabler():


            info = wx.BusyInfo(
                 wx.BusyInfoFlags()
                     .Parent(self.parent)
                     .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                  wx.ART_OTHER, wx.Size(128, 128)))
                     .Title("<b>Retrieving pipeline details from AWS</b>")
                     .Text("Please wait...")
                     .Foreground(wx.WHITE)
                     .Background(wx.BLACK)
                     .Transparency(4 * wx.ALPHA_OPAQUE / 7)
             )
            #time.sleep(0.33)
            tree=self.tree
            tree.Freeze()
            try:
                # Catch the search type (name or content)
                searchMenu = self.filter.GetMenu().GetMenuItems()
                fullSearch = searchMenu[1].IsChecked()

                if evt:
                    if fullSearch:
                        # Do not`scan all the demo files for every char
                        # the user input, use wx.EVT_TEXT_ENTER instead
                        return

                expansionState = self.tree.GetExpansionState()

                current = None
                item = self.tree.GetSelection()
                if item:
                    prnt = self.tree.GetItemParent(item)
                    if prnt:
                        current = (self.tree.GetItemText(item),
                                   self.tree.GetItemText(prnt))

                self.tree.Freeze()
                self.tree.DeleteAllItems()
                self.root = self.tree.AddRoot(ppl['name'])
                self.tree.SetItemImage(self.root, 0)
                self.tree.SetItemData(self.root, 0)

                treeFont = self.tree.GetFont()
                catFont = self.tree.GetFont()

                # The native treectrl on MSW has a bug where it doesn't draw
                # all of the text for an item if the font is larger than the
                # default.  It seems to be clipping the item's label as if it
                # was the size of the same label in the default font.
                if USE_CUSTOMTREECTRL or 'wxMSW' not in wx.PlatformInfo:
                    treeFont.SetPointSize(treeFont.GetPointSize()+2)

                treeFont.SetWeight(wx.FONTWEIGHT_BOLD)
                catFont.SetWeight(wx.FONTWEIGHT_BOLD)
                self.tree.SetItemFont(self.root, treeFont)

                firstChild = None
                selectItem = None
                filter = self.filter.GetValue()
                count = 0
                for category, items in _treeList:
                    #print('1'*20)
                    #pp(items)
                    count += 1
                    
                    if filter:
                        if fullSearch:
                            #print('full search')
                            items = self.searchItems[category]
                        else:
                            #print('Caseless')
                            objs = {obj:[] for obj in items if filter.lower() in obj.lower()}
                            for obj, fields  in {itm:fields for itm,fields in items.items() if itm in objs}.items():
                                objs[obj]=[fld for fld in fields if filter.lower() in fld.lower()]
                            for obj, fields  in {itm:fields for itm,fields in items.items() if itm not in objs}.items():
                                flds= [fld for fld in fields if filter.lower() in fld.lower()]
                                if flds:
                                    objs[obj]=flds
                            items=objs
                                
                    #print('2'*20)
                    #pp(items)
                    if items:
                        child = self.tree.AppendItem(self.root, category, image=count)
                        self.tree.SetItemFont(child, catFont)
                        self.tree.SetItemData(child, count)
                        if not firstChild: firstChild = child
                        for childItem in items:
                            image = count

                            theDemo = self.tree.AppendItem(child, childItem, image=image)
                            self.tree.SetItemData(theDemo, count)
                            self.treeMap[childItem] = theDemo
                            for field in items[childItem]:
                                self.tree.AppendItem(theDemo, field, image=image)
                            #if current and (childItem, category) == current:
                            #    selectItem = theDemo


                self.tree.Expand(self.root)
                if firstChild:
                    self.tree.Expand(firstChild)
                if filter:
                    self.tree.ExpandAll()
                elif expansionState:
                    self.tree.SetExpansionState(expansionState)
                else:
                    self.tree.ExpandAll()
                if selectItem:
                    self.skipLoad = True
                    self.tree.SelectItem(selectItem)
                    self.skipLoad = False

                self.tree.Thaw()
                self.searchItems = {}
            finally:
                tree.Thaw()
            wx.GetApp().Yield() 
            self.searchItems={}
    def ReadConfigurationFile(self):

        self.auiConfigurations = {}
        self.expansionState = [0, 1]

        config = GetConfig()
        val = config.Read('ExpansionState')
        if val:
            self.expansionState = eval(val)

        val = config.Read('AUIPerspectives')
        if val:
            self.auiConfigurations = eval(val)

        val = config.Read('AllowDownloads')
        if val:
            self.allowDocs = eval(val)

        val = config.Read('AllowAUIFloating')
        if val:
            self.allowAuiFloating = eval(val)

        