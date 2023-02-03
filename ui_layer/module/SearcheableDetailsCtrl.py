#!/usr/bin/env python


import wx
import boto3
import os, sys, time, json
from os.path import isfile, dirname, join, basename
import subprocess
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

daily='daily'
hourly='hourly'
monthly='monthly'

import cli_layer.aws_pipeline_utils  as APU

from ui_layer.module.Searcheable_Tree import Searcheable_Tree

import ui_layer.config.ui_config as ui_config
uic = ui_config.uic

e=sys.exit

def get_AWS_Pipeline_List():
    pd = APU.list_pipelines()
    #header
    print('source,pipeline_name')
    rows=[]
    for ppl in sorted(pd):
        rows.append(['aws',ppl])
    header = ['source','pipeline_name']
    return header, rows
    
    
#---------------------------------------------------------------------------
class SearcheableDetailsCtrl(wx.Panel, Base, EditMenu):
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
      
        tree_panel = wx.Panel(self, style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)
        self.st = st = Searcheable_Tree(tree_panel)
        self.tree=st.tree
        if 0:
            self.logwin = logwin = wx.LogWindow(parent, 'Log Window', show=False, passToOld=False)
            #v_sizer.Add(self.log_window, 0)
        self.SetSizerAndFit(v_sizer)
        v_sizer.Layout()
        EditMenu.__init__(self, globals())
        self.Fit()
        self.sub('showPipelineDetails')
        
        leftBox = wx.BoxSizer(wx.VERTICAL)
        leftBox.Add(tree_panel, 1, wx.EXPAND)
        leftBox.Fit(self)
        
        
        
        self.SetSizerAndFit(leftBox)
        leftBox.Layout()
        
    def showPipelineDetails(self, message, arg2=None, **kwargs):
    
        ppl=message
        print('gotmessage', ppl)
        uic.ppl=ppl
        pp(ppl)
        """OrderedDict([('source', 'aws'),
             ('pipeline_name', 'core-import-audience-definitions')])"""
        if 1:
            #pd = APU.list_pipelines()
            #pp(pd)
            #e()
            if 0:
                config = botocore.config.Config(
                    read_timeout=900,
                    connect_timeout=900,
                    retries={"max_attempts": 10}
                )

                
                boto3.set_stream_logger('')
                session = boto3.Session()
                dppl = session.client('datapipeline', config=config)
            else:
                dppl = boto3.client('datapipeline')
            #header

            ppl_type=''

            #print('source,ppl_type,pipeline_name,obj_type,obj_id,obj_name,field_id,field_value,git_filename,git_dir')
            if 1:

                        
                self.pdef= pdef = APU.get_pipeline_definition(ppl, client=dppl)
                pp(pdef)
            self.show_data()
                

                

    
    def show_data(self):
 
        treeList=[]
        for k in [k for k in self.pdef if k not in ['ResponseMetadata']]:
            v=[]
            for d in self.pdef[k]:
                #print(d)
                v.append(f"{d['id']} [{d['name']}]")
            treeList.append((k,v))
        uic._treeList=treeList
        self.st.RecreateTree()





#---------------------------------------------------------------------------
def runTest(**kwargs):
    win = SearcheableDetailsCtrl(**kwargs)
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
