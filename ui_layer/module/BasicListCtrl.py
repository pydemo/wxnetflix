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

s3c = boto3.client('s3')

from ui_layer.module.controller.ListCtrl import DoubleClick

import cli_layer.aws_pipeline_utils  as APU
e=sys.exit



list_cache=join('ui_cache','GH', 'basic_details', 'BasicListCtrl_Center_1.json')

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
class BasicListCtrl(wx.Panel, Base, EditMenu, DoubleClick):
    def __init__(self,  **kwargs):
        #pp(kwargs)
        #self.defaultUrl = kwargs.get('defaultUrl', '')
        self.parent=parent=kwargs['parent']
        wx.Panel.__init__(self, kwargs['parent'])
        
        self.kwargs=kwargs
        kwargs['parent']=self
        
        v_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bucket_name =bucket_name= uic.params[0]
        
        if 0:
            #kwargs['parent']=self
            self.fc=fc = wx.TextCtrl(self, id=wx.ID_ANY, value=uic.params[1], pos=wx.DefaultPosition,
                 size=(140, 30), style=wx.TE_CENTRE, validator=wx.DefaultValidator,
                 name='TextCtrlNameStr')
            
            #fc.BackgroundColour = 'sky blue'
            
        h_sizer.Add((10,10), 1)
        if 1:
            
            self.new=new = wx.Button(self, -1, f'Refresh AWS pipeline list', size=(-1,30))
            new.Bind(wx.EVT_BUTTON, self.refresh_list) 
            #h_sizer.Add(new, 0, wx.ALIGN_TOP)
            
            

            #new.Bind(wx.EVT_BUTTON, self.onNew)
            self.new.Show(True)
            h_sizer.Add(new, 0, wx.LEFT)
        v_sizer.Add(h_sizer, 0, wx.EXPAND)
        if 1:
            self.data =  data =  wx.ListCtrl(self, size=(-1,100), style=wx.LC_REPORT )
            #self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDataDD, data)
            #self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClick)
            listfont = data.GetFont()
            headfont = listfont.MakeBold()
            
            font_bold = wx.Font(wx.FontInfo(11).Bold())
            head_txt_colr = wx.Colour('BLUE')
            head_bac_colr = wx.Colour('DARK GREY')
            data.SetHeaderAttr(wx.ItemAttr(None, None, font_bold))
            if 0:
                self.data.InsertColumn(0, 'Line count')
                self.data.Append(('',))
                data.SetItemFont(0,wx.Font(wx.FontInfo(11)))
                data.SetColumnWidth(0,150)
                if 0:
                    self.data.InsertColumn(0, '1')
                    self.data.InsertColumn(1, '2')
                    self.data.InsertColumn(2, '3')
                
                    
                    
                    dt = [[1,2,3]]
                    for j in dt:
                        self.data.Append((j[0],j[1],j[2]))
            v_sizer.Add(data, 1, wx.EXPAND|wx.ALL)
        if 0:
            self.logwin = logwin = wx.LogWindow(parent, 'Log Window', show=False, passToOld=False)
            

        if isfile(list_cache):
            self.header, self.rows= json.loads(open(list_cache).read())
            self.show_data()
        self.SetSizerAndFit(v_sizer)
        v_sizer.Layout()
        EditMenu.__init__(self, globals())
        self.Fit()
        #self.Bind(wx.EVT_CLOSE, self._on_close)
        DoubleClick.__init__(self,self.showPipeline)
    def showPipeline(self,rid):
        print('--------------------------')
        data=self.data
        cols  = data.GetColumnCount()
        row=OrderedDict()
        for col in range(cols):
            row[self.header[col]]=data.GetItem(rid, col=col).GetText()
        #pp(row)
        self.send('showPipelineDetails', row)
        
    def cacheData(self,header, rows):
        if not isfile(list_cache):
            dn = dirname(list_cache)
            if not isdir(dn):
                os.makedirs(dn)
        dump = json.dumps([header, rows], indent='\t', separators=(',', ': '))
        with open(list_cache,'w') as fh:
            fh.write(dump)
    def load_data(self):
        self.header, self.rows=get_AWS_Pipeline_List()
        self.cacheData(self.header, self.rows)
    def refresh_list(self, event):
        self.load_data()
        self.show_data()
        event.Skip()
    def show_data(self):
        with wx.WindowDisabler():
            info = wx.BusyInfo(
                 wx.BusyInfoFlags()
                     .Parent(self)
                     .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                  wx.ART_OTHER, wx.Size(128, 128)))
                     .Title("<b>Retrieving pipeline list from AWS</b>")
                     .Text("Please wait...")
                     .Foreground(wx.WHITE)
                     .Background(wx.BLACK)
                     .Transparency(4 * wx.ALPHA_OPAQUE / 7)
             )
            data=self.data
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
            
        
    def updateList(self, dic):
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
    win = BasicListCtrl(**kwargs)
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
