#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os, sys
from pprint import pprint as pp
e=sys.exit
from os.path import join, split, dirname, abspath
try:
    dirName = dirname(abspath(__file__))
except:
    dirName = dirname(abspath(sys.argv[0]))


import platform
import tempfile

import wx
import wx.lib.mixins.listctrl as listmix
import datetime
import sys
import boto3
import os, sys, time, json
from os.path import isfile, dirname, join, isdir
import subprocess
from tempfile import gettempdir
from ui_layer.log_init import log, info, debug
from ui_layer.Base import reciever, Base

from collections import OrderedDict

from ui_layer.utils import exception
from pathlib import Path

from ui_layer.common import open_editor

import cli_layer.aws_pipeline_utils  as APU

import ui_layer.config.ui_config as ui_config
uic = ui_config.uic

import cli_layer.config.app_config as app_config
apc = app_config.apc

from wxasync import AsyncBind, WxAsyncApp, StartCoroutine



import sqlite3
from subprocess import Popen, PIPE

from pathlib import Path

from cli_layer.common import  SLITE_LOC


import sqlite3
DB_NAME     = "s3_files.db"
MAXINT = 99999999
PAGE_SIZE = 30 

BUCKET_NAME= 'itx-bhq-program-fire'
PREFIX='dev/thrombosis/sdl-update'

e=sys.exit

AsyncDownload, EVT_ASYNC_DOWNLOAD = wx.lib.newevent.NewEvent()

from ui_layer.utils import exception, load_pipeline_module

Controller        = load_pipeline_module(uic, 'Controller/ListCtrl_Controller')

class ListCtrl(wx.ListCtrl, listmix.ColumnSorterMixin, Controller):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style = wx.LC_REPORT)
        Controller.__init__(self)
        self.bucket_name = BUCKET_NAME
        self.prefix      = PREFIX
        self.file_prefix=''
        self.initList()
        
        listmix.ColumnSorterMixin.__init__(self, numColumns = self.GetColumnCount())
        
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClick)
        
        self.sub('nextPage')
        self.sub('lastPage')
        self.sub('prevPage')
        self.sub('firstPage')
        self.sub('onOrder')
        self.sub('downloadChunk')
        
        
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

    @reciever
    def __downloadChunk(self, message, arg2=None, **kwargs):
        for self.header, fname in dump_S3ChunkToFile():
            if 1: #Insert into SqLite
                tname='s3_table'
                print('Loading file', fname)
                load_table(tname, fname)
            time.sleep(1)
    @reciever
    def downloadChunk(self, message, arg2=None, **kwargs):
        print('Started dc')
        if 0:
            StartCoroutine(self.async_download, self)
        if 1:
            #AsyncDownload, EVT_ASYNC_DOWNLOAD
            evt = AsyncDownload()
            wx.PostEvent(self, evt)
    async def update_clock(self):
        print('test update_clock')

    async def async_download(self, event):
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')


    @reciever
    def _downloadChunk(self, message, arg2=None, **kwargs):
        self.header, fname = next(dump_S3ChunkToFile())
        print(fname)
        if 0:
            pstart=CHUNK_SIZE*self.pid
            rcnt=len(rows)
            self.itemDataMap = {x:self.data[x] for x in range(pstart, pstart+rcnt)}
            self.Refresh()
        if 1: #Insert into SqLite
            tname='s3_table'
            print('Loading file', fname)
            load_table(tname, fname)

    def setSqliteData(self):
        self.header, rows = next(self.row_gen)
        #self.data.update(rows)
        pstart=CHUNK_SIZE*self.pid
        rcnt=len(rows)        
        self.itemDataMap = {x:self.data[x] for x in range(pstart, pstart+rcnt)}
        
        #return header, rows

    @reciever
    def onOrder(self, message, arg2=None, **kwargs):

        self.slog('ListCtrl: onOrder')
        #pp(self.data)
        if 1:
            lst=sorted(self.data.items(), key=lambda kv: kv[1][3])
            print('*'*80)
            #pp(lst)
            self.data={i:x[1] for i,x in enumerate(sorted(self.data.items(), key=lambda kv: kv[1][3]))}
            self.setPage()
            #self.itemDataMap = self.data
            print('-'*80)
            #pp(self.data)
            self.Refresh()

    def getAllData(self):
        for header, rows in self.row_gen:
            self.data.update(rows)
            assert rows
            self.pid +=1
            print('getAllData:', self.pid,'data:', len(self.data),len(rows), len(header))
            
        print(CHUNK_SIZE*self.pid, CHUNK_SIZE*(self.pid+1))

    def OnKeyUp(self, evt=None):

        self.ctrl_down = evt.controlDown
    def OnColClick(self, event):
        #pp(dir(event))
        cid= event.Column
        self.slog('Colid: %s' % cid)
        print(self.ctrl_down)
        
        if self.ctrl_down:
            self.ctrl_down=False
            r = wx.MessageDialog(
                None,
                'Fetch full file list?' ,
                'Confirm global sort',
                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
            ).ShowModal()
            
            if r != wx.ID_YES:
                
                return
        else:
            if 0:
                self.pid -=1
                self.setData()
                self.Refresh()
            event.Skip()

    def onKeyPress(self, evt):

        self.ctrl_down = evt.controlDown

        evt.Skip()
            
    def GetListCtrl(self):
        return self.slist        

    def Refresh(self):
        self.Freeze()
        self.DeleteAllItems()
        data=self.itemDataMap
        if 1:
            # Daten in ListCtrl schreiben
            for key in list(data.keys()):
                #pp(data[key])
                #pp(self.header)
                if 1:
                    pid = data[key][0]
                    index = self.InsertStringItem(MAXINT, str(pid))
                    self.SetItemData(index, key) #muss sein
                    for vid in range(1,len(data[key])):
                        self.SetStringItem(index, vid, data[key][vid])
                    #self.SetColumnWidth(2, 100)
                    #break
                    
                if 0:
                    pid, char_value, char_value_2, char_value_3, char_value, char_value_2, char_value_3, char_value, char_value_2, char_value_3, char_value, char_value_2, char_value_3 = data[key]
                    index = self.InsertStringItem(MAXINT, str(pid))
                    self.SetItemData(index, key) #muss sein
                    self.SetStringItem(index, 1, char_value)
                    self.SetStringItem(index, 2, char_value_2)
                    self.SetStringItem(index, 3, char_value_3)
                    #self.SetColumnWidth(2, 100)
                    break

        self.Thaw()
        if 1:
            self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.SetColumnWidth(2, 130)
            self.SetColumnWidth(3, wx.LIST_AUTOSIZE)
        if 0:
            for cid,k in enumerate(self.header):
                self.SetColumnWidth(cid, wx.LIST_AUTOSIZE_USEHEADER)
                    
        

    def GetListCtrl(self):
        return self


        
    def open_pdf(self, local_fn):
        assert isfile(local_fn)
        status=os.startfile(local_fn)
        print(status)
    def linux(self):
        from webbrowser import BackgroundBrowser
        browser = BackgroundBrowser('/usr/bin/okular')
        browser.args.extend(
            ['--icon', 'okular', '-caption', 'Okular']
        )
        browser.open("/path/to/file.pdf")  
        
    def view_pdf(self, local_fn):
        import wx.lib.mixins.inspection as WIT
        


        pdfV = PDFViewer(None, size=(800, 600))
        pdfV.viewer.UsePrintDirect = False
        pdfV.viewer.LoadFile(local_fn)
        pdfV.Show()

class MyFrame(wx.Frame):
    
    def __init__(
        self, parent = None, title = "Example", size = wx.Size(550, 420)
    ):
        wx.Frame.__init__(self, parent, -1, title, size = size)
        
        panel = wx.Panel(self)
        
        vbox_main = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox_main)
        
        my_list = SortedListCtrl(panel)
        vbox_main.Add(my_list, 1, wx.EXPAND | wx.ALL, 10)

def main():
    """Testing"""
    app = wx.PySimpleApp()
    f = MyFrame()
    f.Center()
    f.Show()
    app.MainLoop()

if __name__ == "__main__":

    main()