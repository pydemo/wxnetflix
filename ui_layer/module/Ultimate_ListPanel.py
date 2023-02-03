import wx
import wx.lib.mixins.listctrl as listmix
from wx.lib.agw import ultimatelistctrl as ULC

import wx
import os, sys, time, json
from os.path import isfile, dirname, join, isdir
#import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import reciever


from ui_layer.utils import exception
from pathlib import Path

from ui_layer.common import open_editor
#from ui_layer.module.controller.Searcheable_ListCtrl_Controller import Controller
#from ui_layer.module.Sortable_Searcheable_ListCtrl import Sortable_Searcheable_ListCtrl

import cli_layer.aws_pipeline_utils  as APU
import cli_layer.s3_utils  as S3U
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic


APPNAME='Sortable Ultimate List Ctrl'
APPVERSION='1.0'
MAIN_WIDTH=300
MAIN_HEIGHT=300

def get_S3_File_List():
    bucket_name= 'gh-package-pdf'
    pd = S3U.list_s3_files(bucket_name)
    #header
    #print('source,pipeline_name')
    rows=[]
    for ppl in sorted(pd):
        #pp(pd[ppl])
        #e()
        rows.append(( bucket_name,str(pd[ppl]['Size']),pd[ppl]['Key']))
    header = ['Bucket','Key', 'Size']
    return header, rows
    
    
class Ultimate_ListPanel(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS, size=(MAIN_WIDTH,MAIN_HEIGHT))

        self.list_ctrl = ULC.UltimateListCtrl(self, -1, agwStyle=ULC.ULC_REPORT|ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        header, rows=get_S3_File_List()
        maxint=9999999
        for cid, col in enumerate(header):
            self.list_ctrl.InsertColumn(maxint, col, format=wx.LIST_FORMAT_CENTER)

        if 0:
            for rowIndex, data in enumerate(rows):
                for colIndex, coldata in enumerate(data):
                    pp(coldata)
                    if colIndex == 0:
                        self.list_ctrl.InsertStringItem(rowIndex, coldata)
                    else:
                        self.list_ctrl.SetStringItem(rowIndex, colIndex, coldata)
                self.list_ctrl.SetItemData(rowIndex, data)

            self.itemDataMap = {data : data for data in rows} 
        
        if 0:
            self.itemDataMap={}
            for item in rows:
                index = self.list_ctrl.InsertStringItem(sys.maxsize, item[0])
                for col, text in enumerate(item[1:]):
                    self.list_ctrl.SetStringItem(index, col+1, text)
                self.list_ctrl.SetItemData(index, index)
                self.itemDataMap[index] = item
                #img = index
                #print ( index)
                #self.list_ctrl.SetItemImage(index, img, img)
        if 1:
            self.itemDataMap={}
            for key, row in enumerate(rows):
                char_value, number_value, date_value = row
                index = self.list_ctrl.InsertStringItem(maxint, char_value)
                self.list_ctrl.SetItemData(index, key) #muss sein
                self.list_ctrl.SetStringItem(index, 1, str(number_value))
                #self.SetStringItem(index, 2, date_value.strftime("%d.%m.%Y"))
                self.list_ctrl.SetStringItem(index, 2, date_value)
                self.list_ctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE)
                self.itemDataMap[index] = row
            
        listmix.ColumnSorterMixin.__init__(self, 3)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list_ctrl)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
    def sortColumn(item1, item2):
        try: 
            i1 = int(item1)
            i2 = int(item2)
        except ValueError:
            return cmp(item1, item2)
        else:
            return cmp(i1, i2)
    def GetListCtrl(self):
        return self.list_ctrl

    def OnColClick(self, event):
        pass