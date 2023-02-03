__appname__ = "DataWorm"
import wx 

from six import exec_
import os, sys, six, imp, yaml, string, logging, importlib
from os.path import isdir
from wx.lib import sized_controls

import subprocess

import string
from pprint import pprint as pp

import wx.lib.agw.aui as aui
import ui_layer.images as images

from ui_layer.EditMenu import EditMenu

from ui_layer.StateMan import StateMan
from ui_layer.common import home
from ui_layer.Base import Base, reciever
from ui_layer.utils import  dict2, exception
from ui_layer.common import open_editor

import cli_layer.config.app_config as app_config
apc = app_config.apc

import ui_layer.config.ui_config as ui_config
uic = ui_config.uic

import wx.lib.agw.aui

e=sys.exit

from ui_layer.utils import open_settings

import pathlib


SHOW_ALL = -99
HIDE_ALL = -100
alls = {}




class TB(wx.lib.agw.aui.AuiToolBar, Base):
    def __init__(self, *args, **kwargs):
        global books
        Base.__init__(self)
        wx.lib.agw.aui.AuiToolBar.__init__(self,*args, **kwargs)
        self.SetToolBitmapSize(wx.Size(48, 48))
        books = sbc.getBookList(sbc.pref)
        self.bcnt= {bid:0 for bid in books}
        if 1:		
            self.AddSimpleTool(SHOW_ALL, '%s' % 'Show', wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
            self.AddSeparator()
        
        if 1:
            for bid, bname in books.items():
                btitle, *_ = bname.split(':')
            
                tid=int(bid)
                self.AddSimpleTool(tid, '%s' % (btitle), wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
                self.SetToolDisabledBitmap(tid, wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
                self.EnableTool(tid, False)
                self.AddSeparator()

            self.Bind(wx.EVT_TOOL, self.setPaneFiler)
        if 1:
            self.AddSimpleTool(HIDE_ALL, '%s' % 'Hide', wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
            

        self.Realize()
        self.sub('incrementTBcount')
        self.sub('decrementTBcount')
        self.sub('updateCounts')

    
    @reciever
    def incrementTBcount(self, message, arg2=None, **kwargs):	
        pref=message
        
        self.bcnt[pref.bid] +=1
        self.send('updateCounts', (pref.bid, self.bcnt[pref.bid]) )

    @reciever
    def decrementTBcount(self, message, arg2=None, **kwargs):	
        pref=message
        
        self.bcnt[pref.bid] -=1
        self.send('updateCounts', (pref.bid, self.bcnt[pref.bid]) )
        
        
    @reciever
    def updateCounts(self, message, arg2=None, **kwargs):	
        bid, bcnt = message
        tid=int(bid)
        btitle= books[bid].split(':')[0]
        self.SetToolLabel(tid, '%s (%s)' % (btitle,bcnt ))
        self.EnableTool(tid, True)
        


    def setPaneFiler(self, evt):
        # the following needs to be done to resize/rearrange the toolbar
        obj =evt.GetEventObject() 
        bid=evt.GetId()
        self.send('setPaneFiler', bid)
        

class MGR(wx.lib.agw.aui.AuiManager, Base):
    def __init__(self, parent, *args, **kwargs):
        self.Id = wx.NewIdRef()
        self.parent=parent
        Base.__init__(self)
        wx.lib.agw.aui.AuiManager.__init__(self,*args, **kwargs)
        self.SetManagedWindow(parent)

        if 0:
            tb = TB(parent, -1, wx.DefaultPosition, wx.DefaultSize,
                                 agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_VERT_TEXT)

            if 1:	
                self.AddPane(tb, aui.AuiPaneInfo().\
                    Name("tb").Caption("Sample Vertical Clockwise Rotated Toolbar").\
                    ToolbarPane().Right().GripperTop().TopDockable(False).BottomDockable(False));				
        if 1:
            self.perspective = self.SavePerspective()
            self._perspectives = []
            self._perspectives.append(self.perspective)
            self.Bind(aui.EVT_AUI_PANE_CLOSE, self.onPaneClose)
            self.Update()
        self.sub('setPaneFiler')
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPaneActivated)
        

    def OnPaneActivated(self, evt):
        
        
        obj = evt.GetEventObject()

        page = obj.GetPage(evt.GetSelection())

        if page.__class__.__name__ == 'MainPanel': 
            self.send('reparentPane', page.pref)
        
        
        
    def OnPaneClose(self, evt):

        pn = evt.pane.name
        print(pn)
        if pn not in [root_pane, 'Layout','Script']:
            msg = "Are you sure you want to "
            if evt.GetEventType() == aui.wxEVT_AUI_PANE_MINIMIZE:
                msg += "minimize "
            else:
                msg += "close/hide "

            res = wx.MessageBox(msg + "this pane?", "AUI", wx.YES_NO, self.parent)
            if res != wx.YES:
                evt.Veto()
        else:
            evt.Veto()

                
    @reciever
    def setPaneFiler(self, message, arg2=None, **kwargs):
        self.GetManagedWindow().Freeze()		
        bid=message
        all = [obj for obj in self.GetAllPanes() if obj.window.__class__.__name__ in ['MainPanel'] and obj.name not in['dummy']]
        if bid == SHOW_ALL:
            for pane in all:
                print(bid, pane.name, pane.window.pref)
                self.ShowPane(pane.window, True)

            #self.Update()
        elif bid == HIDE_ALL:
            for pane in all:
                if pane.name not in [root_pane]:
                    print(bid, pane.name, pane.window.pref)
                    self.ShowPane(pane.window, False)
        else:
            for pane in all:
                pref= pane.window.pref
                if int(pref.bid) == int(bid):
                    self.ShowPane(pane.window, True)		
                else:
                    self.ShowPane(pane.window, False)		
        
        
        self.Update()
            
        self.GetManagedWindow().Thaw()

        
    def onPaneClose(self, evt):
        pane = evt.GetPane().window
        self.send('decrementTBcount', pane.pref)
#
# Controller
#		
class Controller(Base):
    def __init__(self):
        Base.__init__(self)
        self.sub('onOpenExplorer')
        self.sub('openFile')
    @reciever
    @exception
    def onOpenExplorer(self, message, arg2=None, **kwargs):
        open_dir = message
        assert isdir(open_dir), open_dir
        subprocess.Popen(r'explorer "%s\"' % open_dir, shell=True)
    @reciever
    @exception
    def openFile(self, message, arg2=None, **kwargs):
        fn, line =message
        if 1:
            open_editor(fn, line, win=self)
        



# -----------------------------------------------------------------------------------
class MyDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(MyDialog, self).__init__(parent, title=title, size=(250, 150),
                                       style=wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_NO_PARENT)
        panel = wx.Panel(self)
        self.btn = wx.Button(panel, wx.ID_OK, label="ok", size=(50, 20), pos=(75, 50))

        style = self.GetWindowStyle()
        
        if style & wx.STAY_ON_TOP:
            print('STAY_ON_TOP = True')
        else:
            print('STAY_ON_TOP = False')


class DataFrame(wx.Frame, StateMan,  EditMenu, Controller): 

    def __init__(self, parent, title):
        global prefs, tb, lctrl
        
        Controller.__init__(self)
        
        wx.Frame.__init__(		
        self, parent, -1, title, size=wx.DefaultSize ,
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Show(False)
        self.Freeze()
        settings_name = uic.aui_path
        
        assert os.path.isfile(settings_name), 'Coannot find app settings file\n%s.' % settings_name
        self.settings = open_settings(settings_name)
        self.pane_captions ={}
        prefs=dict2()
        self.first_pane=True

            

        if 1:
            size=uic.getFrameSize()
            self.SetSize(size)
            
            self.sub('onClose')
            self.sub('setWinTitle')
            pos=uic.getFramePos()
            self.SetPosition (pos)
        if 1:
            self.mgr = mgr = MGR(self)
        
        self.SetIcon(images.Mondrian.GetIcon())	

        EditMenu.__init__(self, globals(), False)


        
        #self.resized = False # the dirty flag
        self.Bind(wx.EVT_SIZE,self.OnSize)
        #self.Bind(wx.EVT_IDLE,self.OnIdle)
        
        self.sub('previewScript')
        
        self.Show(True)
        
        self.sub('changeLayout')
        self.send('changeLayout', (title))
        if 0:
            from ui_layer.ImportButton import ImportButton
            self.b_imp=b_imp=ImportButton(self, -1, "Import 33333", size=(150,100))
            b_imp.Show()
            pp([x for x in dir(b_imp) if 'top' in x.lower()])
        #self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.Bind(wx.EVT_IDLE,self.OnIdle)
        #wx.CallLater(10, self.update)
        #MyDialog(self, "Dialog").Show()
    def OnIdle(self, evt):
        b_imp=self.b_imp
        xb, yb=self.GetSize()
        bx, by= b_imp.GetSize()
        self.b_imp.SetPosition((xb-bx, yb-by))
        b_imp.Refresh()
    def OnSize(self, evt):
        b_imp=self.b_imp
        if 1:
            xb, yb=self.GetSize()
            bx, by= b_imp.GetSize()
            self.b_imp.SetPosition((xb-bx, yb-by))
        #b_imp.Refresh()
        evt.Skip()

    @reciever
    def previewScript(self, message, arg2=None, **kwargs):
        
        script, parent = message
        script_loc, lineno = script
        
        if parent.__class__.__name__ not in ['GenericMessageDialog']:

            from dialog.EditScriptDialog import EditScriptDialog
        
            #if isinstance(parent, EditScriptDialog):
            dlg = EditScriptDialog(parent, script_loc=script_loc, lineno=lineno,  title='Preview "%s"' % script_loc)
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                print('OK')
            elif result == wx.ID_CANCEL:
                print('Cancel')
            else: print(result)		


            
    def OnSize(self,event):
        pass

    def OnIdle(self,event):
        pass
    def getPname(self, pref):
        return '%s%s%s' % (sbc.getBookTitle(pref),sbc.getChapterTitle(pref), sbc.getPageTitle(pref))
    @reciever
    def changeLayout(self, message, arg2=None, **kwargs):
        global root_pane

        from ui_layer.MainPanel import  MainPanel

        if 1:
            pkey=0
            prefs[pkey] = pnl = MainPanel(self)
            pnl.setLayout()
        pname='GH'
        if False: # self.first_pane:
            root_pane=pname
            self.addPane(pnl,pname)
            #self.mgr.AddPane(pnl, aui.AuiPaneInfo().Name(pname).Center().MinimizeButton(False).CloseButton(False).CaptionVisible(False))
            
            if 0:
                log_pname = 1; #self.getPname(log_pref)
                prefs[log_pname] = log_pnl = MainPanel(self)
                log_pnl.setLayout(log_pref)
                self.addPane(log_pnl, log_pname, 'Log')
            else: # add dummy window
                pnl2 = MainPanel(self)
                self.mgr.AddPane(pnl2, aui.AuiPaneInfo().\
                Name("dummy").Center().MinimizeButton(False).CloseButton(False).CaptionVisible(False), target=self.mgr.GetPane(root_pane))
                if 1:
                    pane= self.mgr.GetPane("dummy")
                    pane.Hide()
                    pane.Show(False)
                    self.mgr.ShowPane(pane, False)
                    self.mgr.DetachPane(pane)
                    self.mgr.ClosePane(pane)
                    
            self.first_pane = False
            self.mgr.ShowPane(pnl, True)
            pnl.setFocus()
        else:

        
            
            self.addPane(pnl, pname)
        self.perspective = self.mgr.SavePerspective()
        self.mgr.Update()
        self.Thaw()
    def addPane(self,pane, pname, caption=None):
        global  root_pane
        if not caption:
            caption= pname
            
        #ribbon_info = aui.AuiPaneInfo().Name(pname).CaptionVisible(False).Center().MinimizeButton(False).CloseButton(True).Top().Floatable(False).CloseButton( visible=False).DockFixed()
        #ribbon_info.CaptionVisible(False)

        self.mgr.AddPane(pane, aui.AuiPaneInfo().Name(pname).Center().MinimizeButton(False).CloseButton(False).CaptionVisible(False)) #, target=mgr.GetPane(root_pane))
        #mgr.AddPane(pane, ribbon_info,target=mgr.GetPane(root_pane))
        self.send('incrementTBcount', pane.pref)
        if 1:
            self.SetMenuBar(pane.mb.CreateMenu())		

                
    @reciever
    def setWinTitle(self, message, arg2=None, **kwargs):
        title = '%s' % ( message )
        self.SetTitle(title)
    @reciever
    def onClose(self, message, arg2=None, **kwargs):

        
        if 0:
            dlg = wx.MessageDialog(self, "Are you sure you want to exit?", "Exit", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                #self.Destroy()  # frame
                print ('Kill signal.')
                if 1:
                    if self.settings.ReadBool('GUI/save_default_state_on_exit', True):
                        self.method_save_default_state()
                    if False or self.settings.ReadBool('GUI/save_default_perspective_on_exit', True):
                        self.method_save_default_perspective()
                #self.main_toolbar.Destroy()		
                self.pnl.mgr.UnInit()
                #self._StopThreads()
                self.Close()
            dlg.Destroy()
        self.Close()


