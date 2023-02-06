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
from ui_layer.module.controller.Searcheable_ListCtrl_Controller import Controller
from ui_layer.module.Searcheable_ListCtrl import Searcheable_ListCtrl

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

list_cache=join('ui_cache','GH', 'list_objects', 'List_Objects_Center_1.json')

def get_S3_File_List():
    bucket_name= 'gh-package-pdf'
    pd = S3U.list_s3_files(bucket_name)
    #header
    #print('source,pipeline_name')
    rows=[]
    for ppl in sorted(pd):
        pp(pd[ppl])
        rows.append([bucket_name,pd[ppl]['Key'], pd[ppl]['ETag']])
    header = ['Bucket','Key', 'ETag']
    return header, rows
    
    
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
class Search_Panel(wx.Panel, Controller):
    def __init__(self,  **kwargs):
        def EmptyHandler(evt): pass
        wx.Panel.__init__(self, kwargs['parent'])
        self.ReadConfigurationFile()
        self.rows=[]
        self.header=[]
        self.slist = slist = Searcheable_ListCtrl(self)
        self.slist = slist = wx.ListCtrl(self, size=(-1,100), style=wx.LC_REPORT )
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
            item = searchMenu.AppendRadioItem(-1, "Sample Name")
            self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
            item = searchMenu.AppendRadioItem(-1, "Sample Content")
            self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
            self.filter.SetMenu(searchMenu)
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
        leftBox.Add(self.slist, 1, wx.EXPAND|wx.ALL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        h_sizer.Add(wx.StaticText(self, label = "Filter list:"), 0, wx.TOP|wx.LEFT, 5)
        h_sizer.Add(self.filter, 1, wx.EXPAND|wx.ALL, 5)
        h_sizer.Add((10,10), 0)
        if 1:
            
            self.refresh=refresh = wx.Button(self, -1, f'Refresh AWS pipeline list', size=(-1,30))
            refresh.Bind(wx.EVT_BUTTON, self.refresh_list) 
            #h_sizer.Add(new, 0, wx.ALIGN_TOP)
            
            

            #new.Bind(wx.EVT_BUTTON, self.onNew)
            self.refresh.Show(True)
            h_sizer.Add(refresh, 0, wx.LEFT)
        leftBox.Add(h_sizer, 0, wx.EXPAND|wx.ALL)
        if 'wxMac' in wx.PlatformInfo:
            leftBox.Add((5,5))  # Make sure there is room for the focus ring
        #parent.SetSizer(leftBox)
        if 1:
            #print(list_cache)
            if isfile(list_cache):
                self.header, self.rows= json.loads(open(list_cache).read())
                #self.show_data()
        #pp(self.header)
        #self.RecreateList()
        self.show_data()
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

    def load_data(self):
        self.header, self.rows=get_S3_File_List()
        self.cacheData(self.header, self.rows)
    def refresh_list(self, event):
        self.load_data()
        self.show_data()
        event.Skip()
    def _show_data(self):
        with wx.WindowDisabler():
            info = wx.BusyInfo(
                 wx.BusyInfoFlags()
                     .Parent(self)
                     .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                  wx.ART_OTHER, wx.Size(128, 128)))
                     .Title("<b>Retrieving movie details</b>")
                     .Text("Please wait...")
                     .Foreground(wx.WHITE)
                     .Background(wx.BLACK)
                     .Transparency(4 * wx.ALPHA_OPAQUE / 7)
             )
            data=self.slist
            #pp(dir(data))
            data.DeleteAllItems()
            data.DeleteAllColumns()
            if 1: #set header
                for cid, k in enumerate(self.header):

                    data.InsertColumn(cid, k)
                    #data.SetColumnWidth(k,150)
            #data.SetToolTip('test')
            for row in self.rows:
                data.Append(row)
            data.Freeze()
            try: #set header
                for cid,k in enumerate(self.header):
                    data.SetColumnWidth(cid, wx.LIST_AUTOSIZE_USEHEADER) #wx.LIST_AUTOSIZE)
                #data.AutoSizeColumns()
            finally:
                data.Thaw()
            #pp(data[0])
            #print(data)
            wx.GetApp().Yield()
            #self.updateList({'Line count':cnt})
            
    def show_data(self):
 
        itemList=[]
        
        for row in self.rows:
            itemList.append(row)
        uic._itemList=itemList
        self.RecreateList()
        
    def RecreateList(self, evt=None):
        #global _treeList
        
        #for x in treeList:
        #    _treeList.append(x)
        _itemList =uic._itemList
        ppl=uic.ppl
        with wx.WindowDisabler():

            ret= apc.cfg[apc.env]['retrieving']
            info = wx.BusyInfo(
                 wx.BusyInfoFlags()
                     .Parent(self)
                     .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                  wx.ART_OTHER, wx.Size(128, 128)))
                     .Title(f"<b>{ret}</b>")
                     .Text("Please wait...")
                     .Foreground(wx.WHITE)
                     .Background(wx.BLACK)
                     .Transparency(4 * wx.ALPHA_OPAQUE / 7)
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
            print(len(self.rows))
            for row in self.rows:
                slist.Append(row)
            for cid, k in enumerate(self.header):
                slist.SetColumnWidth(cid, wx.LIST_AUTOSIZE_USEHEADER)
            try:
                # Catch the search type (name or content)
                searchMenu = self.filter.GetMenu().GetMenuItems()
                fullSearch = searchMenu[1].IsChecked()

                if evt:
                    if fullSearch:
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
                items=_itemList
                    
                #count += 1
                
                if filter:
                    if fullSearch:
                        items = self.searchItems
                    else:
                        items = [item for item in items if filter in ','.join(item)]
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

        