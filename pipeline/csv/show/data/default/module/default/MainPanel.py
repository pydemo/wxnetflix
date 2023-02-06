#!/usr/bin/env python


import wx
import boto3
import os, sys, time, json
from os.path import isfile, dirname, join, isdir
import subprocess
from tempfile import gettempdir
from collections import OrderedDict
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import Base, reciever
from ui_layer.EditMenu import EditMenu
from ui_layer.module.FileCtrl import FileCtrl
from ui_layer.utils import ex
from pathlib import Path
from cli_layer.fmt import pfmtd, pfmtv, fmtv, pfmt, psql

import ui_layer.config.ui_layout as ui_layout 
uilyt = ui_layout.uilyt
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic
import cli_layer.config.app_config as app_config
apc = app_config.apc


from ui_layer.module.controller.ListCtrl import DoubleClick

import cli_layer.aws_pipeline_utils  as APU
e=sys.exit
#from ui_layer.module.Searcheable_ListPanel import Searcheable_ListPanel
from ui_layer.utils import exception, load_pipeline_module
FilterPanel     = load_pipeline_module(uic, 'FilterPanel')
ScanPanel       = load_pipeline_module(uic, 'ScanPanel')
NavigationPanel = load_pipeline_module(uic, 'NavigationPanel')
ListCtrl        = load_pipeline_module(uic, 'ListCtrl')
list_cache=join('ui_cache','GH', 'list_objects', 'List_Objects_Center_1.json')

def get_AWS_Pipeline_List():
    
    pd = APU.list_pipelines()
    #header
    #print('source,pipeline_name')
    rows=[]
    for ppl in sorted(pd):
        rows.append(['aws',pd[ppl]['name'], pd[ppl]['id']])
    header = ['source','name', 'id']
    return header, rows


#---------------------------------------------------------------------------
class MainPanel(wx.Panel, Base, EditMenu, DoubleClick):
    
    def __init__(self,  **kwargs):
        #pp(kwargs)
        #self.defaultUrl = kwargs.get('defaultUrl', '')
        self.parent=parent=kwargs['parent']
        wx.Panel.__init__(self, kwargs['parent'])
        
        self.kwargs=kwargs
        kwargs['parent']=self
        
        v_sizer = wx.BoxSizer(wx.VERTICAL)
        #h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bucket_name =bucket_name= uic.params[0]
        if 1:
            self.spnl = spnl = ScanPanel(self)
        if 0:
            self.slist = slist = wx.ListCtrl(self, size=(-1,100), style=wx.LC_REPORT )
        else:
            self.slist = slist = ListCtrl(parent=self )
            
        if 1:
            self.slp1 = slp = FilterPanel(parent=self, slist=slist)
            #self.slist=slist=slp.slist
            self.header=slp.header
            #self.slist =  slist =  wx.ListCtrl(list_panel, size=(-1,100), style=wx.LC_REPORT )
        if 1:
            self.npnl = npnl = NavigationPanel(parent=self)
        v_sizer.Add(spnl, 0, wx.EXPAND)
        v_sizer.Add(slist, 1, wx.EXPAND|wx.ALL)
        
        
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(slp, 1, wx.EXPAND|wx.ALL)
        h_sizer.Add((20,-1), 0)
        h_sizer.Add(npnl, 0)
        #h_sizer.Add(slp, 0, wx.EXPAND|wx.ALL)
        v_sizer.Add(h_sizer, 0, wx.EXPAND|wx.ALL)
        #self.SetSizerAndFit(leftBox)
        #self.Fit()
        #v_sizer.leftBox()        
        #leftBox.Fit(self)
        
        
        v_sizer.Layout()
        self.SetSizerAndFit(v_sizer)
        
        DoubleClick.__init__(self,self.showPipeline)
    def showPipeline(self,rid):
        print('--------------------------')
        slist=self.slist
        cols  = slist.GetColumnCount()

        row=OrderedDict()
        for col in range(cols):
            row[self.header[col]]=slist.GetItem(rid, col=col).GetText()
        #pp(row)
        self.send('showPipelineDetails', row)
        
    def _cacheData(self,header, rows):
        if not isfile(list_cache):
            dn = dirname(list_cache)
            if not isdir(dn):
                os.makedirs(dn)
        dump = json.dumps([header, rows], indent='\t', separators=(',', ': '))
        with open(list_cache,'w') as fh:
            fh.write(dump)
    def _load_data(self):
        self.header, self.rows=get_AWS_Pipeline_List()
        self.cacheData(self.header, self.rows)
    def _refresh_list(self, event):
        self.load_data()
        self.show_data()
        event.Skip()
    def _show_data(self):
        ret= apc.cfg[apc.env]['retrieving']
        with wx.WindowDisabler():
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
            
        
    def _updateList(self, dic):
        #self.data.InsertStringItem(0, 3)
        self.data.SetItem(0,0, f"{dic['Line count']:7,.0f}" )
        clipdata = wx.TextDataObject()
        clipdata.SetText(str(dic['Line count']))
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()        
    def _on_close(self, event):
        print('On close')
        if 0:
            logwin= self.logwin
            #self.MakeModal(logwin.Frame, False)
            logwin.this.disown()
            wx.Log.SetActiveTarget(None)
            event.Skip()
#---------------------------------------------------------------------------
def runTest(**kwargs):
    win = SearcheableListCtrl(**kwargs)
    #log.info(kwargs['name']+':runTest')
    return win
    


#---------------------------------------------------------------------------


overview = """\
File picker 

"""


if __name__ == '__main__':
    import sys
    import os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
