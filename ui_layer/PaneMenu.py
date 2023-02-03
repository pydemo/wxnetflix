import wx
import wx.lib.newevent

from ui_layer.utils import exception
from ui_layer.DataMenu import DataMenu
from ui_layer.log_init import log
from copy import deepcopy

import ui_layer.config.ui_config as ui_config 
uic = ui_config.uic



APP_EXIT = 1

    
#---------------------------------------------------------------------------
class PaneMenu( DataMenu):
    def __init__(self, parent):
        global frame
        self.Id = wx.NewIdRef()
        frame=parent
        DataMenu.__init__(self, parent)
        
    def CreateMenu(self):

        smb = super(PaneMenu, self).CreateMenu()



        
        if 1:
            menu = wx.Menu()
            if 1:			
                id=wx.NewIdRef()

                item = wx.MenuItem(menu, id, '&Layout\tCtrl+L')
                menu.Append(item)
                frame.Bind(wx.EVT_MENU, self.onCtrl_L, id=id)
                #frame.Bind(wx.EVT_MENU, self.OnShowLayoutDialog, id=id)
            smb.Append(menu, '&Window')
            
            return smb
    @exception
    def onCtrl_L(self, evt):
        log.info('Ctrl_L')
        fc=wx.Window.FindFocus()
        self.send('Ctrl_L',fc)
        
    def OnPreviewLayout(self, e):
        log.info('OnPreviewLayout')
        
        self.send("previewLayout", ())
        
    def OnPage(self, evt, pref):
        print(pref)
        sbc.setPref(pref)
        self.send('changeLayout', pref)
        self.send('activatePageButton', pref)
    def cref(self, evt, cref):
        self.send('showChapter', cref)	
        self.send('activateChapterButton', cref)

        