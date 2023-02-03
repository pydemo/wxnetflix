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
from ui_layer.module.Ultimate_ListPanel import Ultimate_ListPanel


list_cache=join('ui_cache','GH', 'list_objects', 'List_Objects_Center_1.json')




#---------------------------------------------------------------------------
class UltimateFrame(wx.Panel, Base, EditMenu, DoubleClick):
    
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
      
        
        self.slp = slp = Ultimate_ListPanel(parent=self)


            
        if 0:
            self.logwin = logwin = wx.LogWindow(parent, 'Log Window', show=False, passToOld=False)
            #v_sizer.Add(self.log_window, 0)
        v_sizer.Add(slp, 1, wx.EXPAND|wx.ALL)
        
        leftBox = wx.BoxSizer(wx.VERTICAL)
        leftBox.Add(v_sizer, 1, wx.EXPAND|wx.ALL)
        self.SetSizerAndFit(leftBox)
        #self.Fit()
        #v_sizer.leftBox()        
        #leftBox.Fit(self)
        
        
        
        #self.SetSizerAndFit(leftBox)
        #leftBox.Layout()
        #DoubleClick.__init__(self,self.showPipeline)


#---------------------------------------------------------------------------
def runTest(**kwargs):
    win = UltimateFrame(**kwargs)
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
