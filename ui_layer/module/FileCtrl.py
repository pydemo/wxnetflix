import wx
import os
from os.path import isdir
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import Base, reciever
from ui_layer.EditMenu import EditMenu
from ui_layer.module.controller.FileCtrl_Controller import Controller
    
from ui_layer.utils import evt_stacktrace, exception

class FileCtrl(wx.FileCtrl, Base, EditMenu,Controller ):
    @exception
    def __init__(self, **kwargs):
        if 1:
            self.defaultDirectory=defaultDirectory = kwargs.get('defaultDirectory', '')	
            defaultFilename  = kwargs.get('defaultFilename', '')
            wildCard = kwargs.get('wildCard', "Python files (*.py)|*.py") 
            self.parent=parent 	 = kwargs.get('parent')
            
            style	 = kwargs.get('style', wx.FC_DEFAULT_STYLE|wx.FC_MULTIPLE)
            pos 	 = kwargs.get('pos', wx.DefaultPosition)
            size	 = kwargs.get('size', wx.DefaultSize)
            self.id = id =	wx.NewIdRef()
            name	 = kwargs.get('name', "filectrl")
        if 0:
            print('8'*50)
            print(defaultDirectory)
            print('8'*50)
        if not isdir(defaultDirectory):
            os.makedirs(defaultDirectory)
        wx.FileCtrl.__init__(self, parent, id, defaultDirectory, defaultFilename,
                             wildCard, style, pos, size, name)
        Base.__init__(self)
        self.Bind(wx.EVT_FILECTRL_FILEACTIVATED, self.OnFileActivated)
        #self.Bind(wx.EVT_FILECTRL_FOLDERACTIVATED, self.OnFolderActivated)
        self.Bind(wx.EVT_FILECTRL_SELECTIONCHANGED, self.OnSelectionChanged)
        self.Bind(wx.EVT_FILECTRL_FOLDERCHANGED, self.OnFolderChanged)
        self.Bind(wx.EVT_FILECTRL_FILTERCHANGED, self.OnFilterChanged)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouse)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        EditMenu.__init__(self, globals(), True)
        Controller.__init__(self)
        #self.Bind(wx.EVT_CHAR, self.KeyDown)
        self.parent= kwargs.get('parent')

        
    def OnFileActivated0(self, event):
        import os
        fns=self.GetFilenames()
        dn=self.Directory
        for fn in fns: 
            info('File Activated: %s\n' % fn)
            self.send('editFile', (os.path.join(dn, fn),0))

    @evt_stacktrace(__name__)
    def OnFileActivated(self, event):
        pp(self.Id)
        print('OnFileActivated')
        fns=self.GetFilenames()
        dn=self.Directory
        script_loc = os.path.join(dn, fns[0])
        lineno=0
        if wx.GetKeyState(wx.WXK_CONTROL):
            print ("Control key is down")
            self.send('editFileInExcel', (self.Id, script_loc,0))
        else: 
            lineno = 0
            
            self.send('editFile', (self.Id, script_loc,0))

                
    def GetSelection(self):
        fns=self.GetFilenames()
        dn=self.Directory
        script_loc =None
        if fns:
            script_loc = os.path.join(dn, fns[0])
        return script_loc
    def KeyDown(self, event=None):
        print("OnKeyDown event %s" % (event))
        
        
    
    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        #print (keycode)
        if keycode == wx.WXK_SPACE:
            print ("you pressed the spacebar!")
        event.Skip()		
        
    def OnMouse(self, evt):
        self.last_was_mouse = True
        print('OnMouse')
        evt.Skip()



    def OnSelectionChanged(self, event):
        for path in self.GetPaths():
            info('Selection Changed: %s\n' % path)
        #print(3333, self.parent)
        #self.send(self.parent.sender, (self,self.GetPaths()[0]))
        #ms = wx.MouseState()
        #self.send('onFileSelection', (self, self.GetPaths()[0]))
        print(self.GetPaths()[0])
        

    def OnFolderChanged(self, event):
        info('Directory Changed: %s\n' % self.GetDirectory())
        self.defaultDirectory=self.GetDirectory()

    def OnFilterChanged(self, event):
        info('Filter Changed: %s\n' % self.GetFilterIndex())

    def on_open_folder(self, event):
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_mp3_listing(dlg.GetPath())
        dlg.Destroy()