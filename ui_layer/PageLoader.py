import wx
import os, sys, six
from pprint import pprint as pp

import wx.lib.agw.aui as aui
from ui_layer.PageBuilder import PageBuilder

from ui_layer.utils import evt_stacktrace, import_module_3, exception


import ui_layer.config.ui_config as ui_config 
uic = ui_config.uic




e=sys.exit

import ui_layer.config.ui_layout as ui_layout 
uilyt = ui_layout.uilyt



DEFAULT_PERSPECTIVE = "Default Perspective"


    
class PageLoader(object):

        
    def __init__(self):
        global code
        code=[]
        self.refs={}
    def setLayout(self ):

        layout_fn = uilyt.getLayoutFile()
        print(111,layout_fn)

        if not self.layout_fn == layout_fn:

            for winkey in self.refs:
                for winname, pref in self.refs[winkey].items():
                    self.detachWin(winkey, winname)
            print('%s:Loading layout: "%s"' % (self.cn,layout_fn))
            print('-'*60)
            #e()
            self.loadPageLayout(layout_fn=layout_fn)
            
            self.send('setWinTitle', layout_fn)

    @exception
    def loadPageLayout(self, layout_fn):
        pb = PageBuilder (layout_fn)
        print(layout_fn)
        if 0:
            pb.buildPageLayout()
            mod_path = pb.getBuildLoc()
        
            if 0:
                mod= import_module_3(r'_build\Page.py')
            else:
                print(mod_path)
                mod= import_module_3(mod_path)
            p=mod.Page(self,self.mgr, self.refs)
            p.load_page()
        else:
            from  ui_layer.build.Layout import Page 
            p=Page(self,self.mgr, self.refs)
            p.load_page()
        

        if self.mgr.GetNotebooks():
            self.nb =self.mgr.GetNotebooks()[0]
            self.nb.SetSelection(0)
            
            
            self.nb.Update()

        self.auiConfigurations[DEFAULT_PERSPECTIVE] = self.mgr.SavePerspective()
        self.mgr.Update()
        self.mgr.SetAGWFlags(self.mgr.GetAGWFlags() ^ aui.AUI_MGR_TRANSPARENT_DRAG)