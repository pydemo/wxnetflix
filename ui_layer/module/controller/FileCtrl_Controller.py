import wx
import os
from os.path import isfile, dirname, join
import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import reciever


from ui_layer.utils import exception
from pathlib import Path

from ui_layer.common import open_editor

def open_in_excel(fn):
    os.startfile(fn)

#---------------------------------------------------------------------------
class Controller(object):
    def __init__(self):
        self.sub('editFile')
        self.sub('Ctrl_D')
        self.sub('newFile')
        self.sub('onExplorer')
        self.sub('editFileInExcel')
        

    @reciever
    def editFileInExcel(self, message, arg2=None, **kwargs):
        sender, fn, line =message
        if sender == self.Id:
            open_in_excel(fn)

    
    @reciever
    @exception
    def editFile(self, message, arg2=None, **kwargs):
        sender, fn, line =message
        if sender == self.Id:
            open_editor(fn, line, win=self)
        if 0:
            subprocess.Popen(r'explorer "%s\"' % self.defaultDirectory, shell=True)

    @reciever
    def newFile(self, message, arg2=None, **kwargs):
        ctrl = message.GetParent()
        if ctrl == self.fc:	
            #print(ctrl, self.fc)
            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.new.GetId())
            wx.PostEvent(self.new, evt)

    @exception
    @reciever
    def Ctrl_D(self, message, arg2=None, **kwargs):
        
        ctrl = message
        
        if 1:
            if hasattr(self,'fc') and ctrl == self.fc :
                fns= self.fc.GetPaths()
                strs = "Are you sure you want to delete files:\n" + ('%s\t' % os.linesep).join(fns) + "?"
                dlg = wx.MessageDialog(None, strs, 'Deleting files', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)

                if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                    dlg.Destroy()
                    return

                dlg.Destroy()
                
                for fn in fns:
                    log.info('Deleting file %s' % fn)
                    os.unlink(fn)
                self.fc.SetDirectory(self.defaultDirectory)



        
    @reciever
    def onExplorer(self, message, arg2=None, **kwargs):
        ctrl = message.GetParent()
        if ctrl == self.fc:

            subprocess.Popen(r'explorer "%s\"' % self.defaultDirectory, shell=True)

    @reciever
    def newFile(self, message, arg2=None, **kwargs):
        ctrl = message.GetParent()
        if ctrl == self.fc:	
            #print(ctrl, self.fc)
            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.new.GetId())
            wx.PostEvent(self.new, evt)

        
    @reciever
    def Ctrl_D(self, message, arg2=None, **kwargs):
        
        ctrl = message
        #print(ctrl)
        if ctrl == self.fc :
            fns= self.fc.GetPaths()
            strs = "Are you sure you want to delete files:\n" + ('%s\t' % os.linesep).join(fns) + "?"
            dlg = wx.MessageDialog(None, strs, 'Deleting files', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)

            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                dlg.Destroy()
                return

            dlg.Destroy()
            
            for fn in fns:
                log.info('Deleting file %s' % fn)
                os.unlink(fn)
            self.fc.SetDirectory(self.defaultDirectory)
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
                
            

        dlg.Destroy()

    def createFile(self, path):
        #print(path)
        
        if isfile(path): ex('File exists')
        Path(path).touch()
        if 1:		
            self.fc.SetDirectory(self.defaultDirectory)
        if not isfile(path): ex('File was not created')
        if 1:
            self.send('editFile', (path,0))
        self.fc.SetFilename(os.path.basename(path))
        