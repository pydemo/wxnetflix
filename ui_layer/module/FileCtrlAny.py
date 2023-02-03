#!/usr/bin/env python


import wx
import os
from os.path import isfile, dirname, join
import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import Base, reciever
from ui_layer.EditMenu import EditMenu
from ui_layer.module.FileCtrl import FileCtrl
from ui_layer.utils import ex
from pathlib import Path

import ui_layer.config.ui_layout as ui_layout 
uilyt = ui_layout.uilyt




#---------------------------------------------------------------------------
class FileCtrlPanel(wx.Panel, Base, EditMenu):
    def __init__(self,  **kwargs):
        #pp(kwargs)
        self.defaultDirectory = kwargs.get('defaultDirectory', '')
        self.wildCard = kwargs.get('wildCard', "Any files (*.*)|*.*") 
        
        wx.Panel.__init__(self, kwargs['parent'])
        
        self.kwargs=kwargs
        kwargs['parent']=self
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        if 1:
            
            self.new=new = wx.Button(self, -1, "New", size=(40,30))
            
            #sizer.Add(new, 0, wx.ALIGN_TOP)
            
            

            new.Bind(wx.EVT_BUTTON, self.onNew)
            self.new.Show(False)
        
        if 1:
            #kwargs['parent']=self
            self.fc=fc = FileCtrl(**kwargs)
            
            fc.BackgroundColour = 'sky blue'
            
            sizer.Add(fc, 1, wx.ALL|wx.EXPAND)
        
        self.SetSizerAndFit(sizer)
        sizer.Layout()
        EditMenu.__init__(self, globals())

        self.Fit()
        

    def onNew(self, evt):
        
        defaultFile= '%s.py' % self.defaultDirectory.split(os.sep)[-1]

        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=self.defaultDirectory,
            defaultFile=defaultFile, wildcard=self.wildCard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )
        #dlg.SetFilterIndex(0)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.createFile(path)
            if 1: #__init__.py
                dn = dirname(path)
                initpy =  join(dn, '__init__.py')
                if not isfile(initpy):
                    Path(initpy).touch()
        
#---------------------------------------------------------------------------
def runTest(**kwargs):
    win = FileCtrlPanel(**kwargs)
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
