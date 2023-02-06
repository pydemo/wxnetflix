import wx
import os, sys, time, json
from os.path import isfile, dirname, join, isdir
import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import reciever


from ui_layer.utils import exception
from pathlib import Path

from ui_layer.common import open_editor
#from ui_layer.module.controller.Searcheable_ListCtrl_Controller import Controller
from ui_layer.utils import exception, load_pipeline_module
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic
Controller        = load_pipeline_module(uic, 'Controller/FilterPanel_Controller')

import cli_layer.aws_pipeline_utils  as APU
import cli_layer.s3_utils  as S3U
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic

import cli_layer.config.app_config as app_config
apc = app_config.apc

USE_CUSTOMTREECTRL = False
DEFAULT_PERSPECTIVE = "Default Perspective"


#_treeList = []
#---------------------------------------------------------------------------
# Show how to derive a custom wxLog class

list_cache=join('ui_cache','NF', 'list_movies', 'List_Movies_Center_1.json')


    
    
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
class FilterPanel(wx.Panel, Controller):
    def __init__(self,  **kwargs):
        def EmptyHandler(evt): pass
        wx.Panel.__init__(self, kwargs['parent'])
        self.ReadConfigurationFile()
        self.rows=[]
        self.header=[]
        #self.slist = slist = Searcheable_ListCtrl(self)
        if 0:
            self.slist = slist = wx.ListCtrl(self, size=(-1,100), style=wx.LC_REPORT )
        else:
            self.slist = slist= kwargs['slist']
        self.header=slist.header
        if 1:
            listfont = slist.GetFont()
            headfont = listfont.MakeBold()
            
            font_bold = wx.Font(wx.FontInfo(11).Bold())
            head_txt_colr = wx.Colour('BLUE')
            head_bac_colr = wx.Colour('DARK GREY')
            slist.SetHeaderAttr(wx.ItemAttr(None, None, font_bold))
            

        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.ShowCancelButton(True)
        #self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN,
                         lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT, self.OnSearch) #EVT_TEXT_ENTER
        if 1:
            searchMenu = wx.Menu()
            item = searchMenu.AppendRadioItem(-1, "Current Page")
            self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
            item = searchMenu.AppendRadioItem(-1, "All Pages")
            self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
            self.filter.SetMenu(searchMenu)
            if 1:
                searchMenu = self.filter.GetMenu().GetMenuItems()
                self.fullSearch = searchMenu[1].IsChecked()
                print('FULL SEARCH:', self.fullSearch)
        self.treeMap = {}
        self.searchItems = []
        uic._itemList=[]
        uic.ppl={'name':'Select pipline'}
        #self.RecreateTree()
        #self.tree.SetExpansionState(self.expansionState)
        self.slist.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.slist.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.slist.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.slist.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
        # add the windows to the splitter and split it.
        leftBox = wx.BoxSizer(wx.VERTICAL)
        #leftBox.Add(self.slist, 1, wx.EXPAND|wx.ALL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        h_sizer.Add(wx.StaticText(self, label = "Movie/TV filter:"), 0, wx.ALIGN_CENTER|wx.LEFT, 5)
        h_sizer.Add(self.filter, 1, wx.EXPAND|wx.ALL, 5)
        h_sizer.Add((5,10), 0)

        leftBox.Add(h_sizer, 0, wx.EXPAND|wx.ALL)
        if 'wxMac' in wx.PlatformInfo:
            leftBox.Add((5,5))  # Make sure there is room for the focus ring
        #parent.SetSizer(leftBox)

        self.SetSizerAndFit(leftBox)
        leftBox.Layout()
        if 1:
            # Set up a log window
            self.log = wx.TextCtrl(self, -1,
                                  style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            self.log.Show(False)
            if wx.Platform == "__WXMAC__":
                self.log.MacCheckSpelling(False)

            # Set the wxWindows log target to be this textctrl
            #wx.Log.SetActiveTarget(wx.LogTextCtrl(self.log))

            # But instead of the above we want to show how to use our own wx.Log class
            wx.Log.SetActiveTarget(MyLog(self.log))
    def cacheData(self,header, rows):

        if not isfile(list_cache):
            dn = dirname(list_cache)
            if not isdir(dn):
                os.makedirs(dn)
        dump = json.dumps([header, rows], indent='\t', separators=(',', ': '))
        with open(list_cache,'w') as fh:
            fh.write(dump)


        
    def RecreateList(self, evt=None):
        self.flog('RecreateList: "%s"' % self.filter.GetValue())
        print('FULL SEARCH 3:', self.fullSearch)
        if self.fullSearch:
            _itemList =self.slist.data
        else:
            _itemList =self.slist.itemDataMap
        
        ppl=uic.ppl
        with wx.WindowDisabler():

            ret= apc.cfg[apc.env]['retrieving']
            info = wx.BusyInfo(
                 wx.BusyInfoFlags()
                     .Parent(self)
                     .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                  wx.ART_OTHER, wx.Size(128, 128)))
                     .Title(f"<b>{ret} from {apc.env}</b>")
                     .Text("Please wait...")
                     .Foreground(wx.WHITE)
                     .Background(wx.BLACK)
                     .Transparency(int(4 * wx.ALPHA_OPAQUE / 7))
             )
            #time.sleep(0.33)
            slist=self.slist
            slist.Freeze()
            #slist.DeleteAllItems()
            slist.DeleteAllColumns()
            if 1: #set header
                for cid, k in enumerate(self.header):

                    slist.InsertColumn(cid, k)
                    #slist.SetColumnWidth(cid, wx.LIST_AUTOSIZE_USEHEADER)
            #print(len(self.rows))
            for row in self.rows:
                slist.Append(row)

            #for cid, k in enumerate(self.header):
            #    slist.SetColumnWidth(cid, wx.LIST_AUTOSIZE_USEHEADER)
            try:
                # Catch the search type (name or content)
                searchMenu = self.filter.GetMenu().GetMenuItems()
                self.fullSearch = searchMenu[1].IsChecked()
                if 0:
                    if evt:
                        if self.fullSearch:
                            # Do not`scan all the demo files for every char
                            # the user input, use wx.EVT_TEXT_ENTER instead
                            return

                #expansionState = self.tree.GetExpansionState()



                slist.Freeze()
                slist.DeleteAllItems()


                firstChild = None
                selectItem = None
                filter = self.filter.GetValue()
                count = 0
                #print(123,len(self.searchItems))
                #pp(self.searchItems)
                items=_itemList.values()
                if 0:
                    for item in items:
                        pp(item)
                        break
                    e()
                #count += 1
                
                if filter:
                    items = [item for item in items if filter in ','.join([str(i) for i in item])]
                    self.flog('Filtered count: %s' % len(items))
                    if 0:
                        if self.fullSearch:
                            items = self.searchItems
                        else:
                            items = [item for item in items if filter in ','.join([str(i) for i in item])]
                #print(111, fullSearch, len(_treeList), len(items), len(self.searchItems.get('category', [])), category)
                #slist.Append(row)
                #pp(items)
                if 0:
                    if items:
                        child = self.slist.AppendItem(self.root, category, image=count)
                        self.slist.SetItemFont(child, catFont)
                        self.slist.SetItemData(child, count)
                        if not firstChild: firstChild = child
                        for childItem in items:
                            image = count
                            #if DoesModifiedExist(childItem):
                            #    image = len(_demoPngs)
                            theDemo = self.slist.AppendItem(child, childItem, image=image)
                            self.slist.SetItemData(theDemo, count)
                            self.treeMap[childItem] = theDemo

                if 1:
                    for item in items:
                        slist.Append(item)


                #elif expansionState:
                #    self.tree.SetExpansionState(expansionState)
                if selectItem:
                    self.skipLoad = True
                    self.slist.SelectItem(selectItem)
                    self.skipLoad = False

                self.slist.Thaw()
                self.searchItems = []
            finally:
                slist.Thaw()
            wx.GetApp().Yield() 
            self.searchItems=[]
            for c in range(len(self.header)):
                self.slist.SetColumnWidth(c, wx.LIST_AUTOSIZE)
            self.slist.SetColumnWidth(2, 130)
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

        