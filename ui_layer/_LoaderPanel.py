import wx
import os, sys, six, imp, string, traceback

import wx.lib.agw.aui as aui
from copy import deepcopy

from collections import defaultdict
from pprint import pprint as pp


from pydispatch import dispatcher 
from ui_layer.utils import  GetConfig, MakeDocDirs, GetDocFile
from ui_layer.Base import Base, reciever
from ui_layer.PaneMenu import PaneMenu



import traceback
try:
    import cStringIO
except ImportError:
    import io as cStringIO
    
from traceback import print_exc	


e=sys.exit
    

from ui_layer.EditMenu import EditMenu	



import ui_layer.config.ui_config as ui_config 
uic = ui_config.uic



from ui_layer.PageLoader import PageLoader


class LoaderPanel(wx.Panel, Base, EditMenu, PageLoader):

        
    def __init__(self, parent):
        global frame
        Base.__init__(self)
        PageLoader.__init__(self)
        wx.Panel.__init__(self, parent)
        frame=parent
        
        self.refs=defaultdict(dict)
        

        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(self)
        self.allowAuiFloating = False
        self.ReadConfigurationFile()
        self.pref=None
        self.module = None
        self.reparent=[]
        self.layout_fn=None
        self.SetMinSize((1040,800))
        
        self.mb = PaneMenu(frame)
        if 1:
            self.sub("onSave")
            self.sub("onEdit")
            
            self.sub("reparentPane")

        EditMenu.__init__(self, globals())
        if 0:
            
            from ui_layer.ImportButton import ImportButton
            self.b_imp=b_imp=ImportButton(self, -1, "Import 33333", size=(156,65))
            pp([x for x in dir(b_imp) if 'top' in x.lower()])
        #self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.Bind(wx.EVT_IDLE,self.OnIdle)
    def OnIdle(self, evt):
        b_imp=self.b_imp
        xb, yb=self.GetSize()
        bx, by= b_imp.GetSize()
        self.b_imp.SetPosition((xb-bx, yb-by+8))
        b_imp.Refresh()
    def OnSize(self, evt):
        b_imp=self.b_imp
        if 1:
            xb, yb=self.GetSize()
            bx, by= b_imp.GetSize()
            self.b_imp.SetPosition((xb-bx+8, yb-by))
        b_imp.Refresh()
        evt.Skip()
    def setFocus(self):
        #pp(self.pref)
        if 0:
            uilyt.page_title = 'Title123'
    def CreateMenu(self):
        return self.mb.CreateMenu()






        
    @reciever
    def reparentPane(self, message, arg2=None, **kwargs):
        #global lctrl
        #print('reparentPane',self.reparent, self.pref.get('pid') if self.pref else None)
        if message==self.pref:
            
            for win in self.reparent:
                if 0:
                    win.Reparent(self)
            self.mgr.Update()
    
    def CreateTextCtrl(self, ctrl_text=""):

        if ctrl_text.strip():
            text = ctrl_text
        else:
            text = "This is text box %d"%self._textCount
            self._textCount += 1

        return wx.TextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)
                           

    @reciever
    def onSave(self, message, arg2=None, **kwargs):
        if 1:
            
            sender = kwargs.get('sender')
            
            
    @reciever
    def onEdit(self, message, arg2=None, **kwargs):
        if 1:
            
            sender = kwargs.get('sender')
    def loadWorm0(mpath):
        scope = {}
        try:
            code = compile(open(mpath).read(), 'test', "exec")
            
            exec_(code, self.module)
            
            self.window = locals()['DataPanel3'](parent=self, value='test4')
        except:

            log.error('*'*60)
            log.error(sys.exc_info())
            log.error('*'*60)
            raise
    def load_module_20(self, full_name):
        orig = full_name.split('.')[-1]


        mod = sys.modules.setdefault(full_name, imp.new_module(full_name))
        mod.__file__ 	= ''
        mod.__name__ 	= full_name
        mod.__path__ 	= ''
        mod.__loader__ 	= self
        mod.__package__ = '.'.join(full_name.split('.')[:-1])
        _code= string.Template(open(full_name).read())
        code = _code.substitute({'mod_name': orig})
        six.exec_(code, mod.__dict__)

        return mod				
    def load_module0(self, mpath):
            
            #self.module=DataPanel
            
            self.module=import_module_3( mpath)
            
            
            win = self.module.runTest(self, 'Test')
            
            if win:
                # so set the frame to a good size for showing stuff
                #self.SetSize((640, 480))
                win.SetFocus()
                self.window = win
                
                #frect = self.GetRect()	
    
            else:
                # It was probably a dialog or something that is already
                # gone, so we're done.
                self.Destroy()

                
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

        MakeDocDirs()
        pickledFile = GetDocFile()

        if not os.path.isfile(pickledFile):
            self.pickledData = {}
            return

        fid = open(pickledFile, "rb")
        try:
            self.pickledData = cPickle.load(fid)
        except:
            self.pickledData = {}

        fid.close()

        
    #---------------------------------------------
    def OnActivate(self, evt):
        wx.LogMessage("OnActivate: %s" % evt.GetActive())
        evt.Skip()

    #---------------------------------------------
    def OnAppActivate(self, evt):
        wx.LogMessage("OnAppActivate: %s" % evt.GetActive())
        evt.Skip()
        
    def get_win(self, mpath):
        try:
            module=import_module_2( mpath)
            win = module.runTest(self, 'Test3')		
        except Exception as ex:
            #wx.MessageBox(str(ex))
            #win2.Destroy()

            del module
            #self.Thaw()
            raise
        else:
            return win

            
    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Freeze()

    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Thaw()
        