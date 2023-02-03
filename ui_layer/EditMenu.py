import wx
import os, sys, ast
from os.path import join
import copy, inspect

from pydispatch import dispatcher
#from include.utils import ex
from pprint import pprint as pp

from ui_layer.Base import Base

e=sys.exit



def reciever(f):
    def wrapper(*args, **kwargs):
        #debug('SIGNAL: %s->%s: [%s] [%s]' % (kwargs['sender'].cn, args[0].cn, kwargs['signal'], kwargs['message']))
        return f(*args, **kwargs)
    return wrapper
    
    
class EditMenu(object):
    def __init__(self, gs, bind =True):
        global evtid
        #Base.__init__(self)
        self.gs = gs
        if bind:
            #print(self.__class__.__name__)
            self.gen_bind(wx.EVT_CONTEXT_MENU, self, self.OnEditMenu, () )
        self.ep  = self.getEditPath(gs)
        self.ecp = self.getEditConfigPath(gs)
        evtid={}
        self.emenu=None
    
        
    def gen_bind(self, type, instance, handler, *args, **kwargs):
        self.Bind(type, lambda event: handler(event, *args, **kwargs), instance)			
    def OnEditMenu(self, event, params):		
        sender = event.GetEventObject()
        
        if not self.emenu:

            emenu=self.emenu = wx.Menu()
            if 0:
                for m in self.getMenuItem_2(emenu, self.gs):
                    emenu.Append(m)
                #menu.Append(self.getMenuItem(menu, self.gs))
                #menu.Append(self.parent.getMenuItem(self.parent, self.gs))
            else:
                self.setMenuItem_2(emenu, self.gs)
        self.PopupMenu(self.emenu)
        #menu.Destroy()
    def getMenuItem(self, menu, gs):
        if not hasattr(self, "gs"):
            self.gs = gs

        if not hasattr(self, "id_ed"):
            self.id_ed = wx.NewIdRef()
            
            self.Bind(wx.EVT_MENU, self.onEditObjFile, id=self.id_ed)	
        item = wx.MenuItem(menu, self.id_ed,'Edit 11 "%s"' % self.getEditPath(gs))
        return item

    def getMenuItem_2000(self, menu, gs):
        if not hasattr(self, "gs"):
            self.gs = gs
        out =[]
        for id, obj in enumerate([self, self.GetParent(), \
            self.GetParent().GetParent(), self.GetParent().GetParent().GetParent(),\
            self.GetParent().GetParent().GetParent().GetParent() if self.GetParent().GetParent().GetParent() else None]):
            #print(123,obj.__class__.__name__)
            if hasattr(obj, 'onPreviewScript'):
                if not hasattr(obj, "id_ed"):
                    obj.id_ed = wx.NewIdRef()

                    obj.Bind(wx.EVT_MENU, obj.onPreviewScript, id=obj.id_ed)
                
                #pp(dir(self))
                item = wx.MenuItem(menu, obj.id_ed,'Preview "%s"' % obj.ep)
                out.append(item)

        return out
    
    def setMenuItem_2(self, menu, gs):
        global evtid
        if not hasattr(self, "gs"):
            self.gs = gs
        #out =[]
        #self.evtid=evtid={}
        #evtid= self.evtid
        #if evtid: return 


        
        for id, obj in enumerate(self.getParents()):
            #print(123,obj.__class__.__name__)
            if hasattr(obj, 'onEditObjFile'):
                obj.mro=mro={}
                if not hasattr(obj, "id_eof"):
                    obj.id_eof = wx.NewIdRef()
                    if 1 :
                        #print(obj)
                        #pp(dir(obj))
                        obj.mro=mro={}
                        for mobj in obj.__class__.__mro__:
                            id_eof = wx.NewIdRef()
                            obj.Bind(wx.EVT_MENU, obj.onEditMroFile, id=id_eof)
                            mro[str(mobj)]=[mobj,id_eof]
                            
                    obj.Bind(wx.EVT_MENU, obj.onEditObjFile, id=obj.id_eof)
                
                #pp(dir(self))
                item = wx.MenuItem(menu, obj.id_eof,'Edit "%s"' % obj.ep)
                font = item.GetFont()
                font.SetWeight(wx.BOLD)
                item.SetFont(font)

                menu.Append(item)
                modules = set()
                if 1:
                    def visit_Import(node):
                        for name in node.names:
                            modules.add(name.name.split(".")[0])

                    def visit_ImportFrom(node):
                        # if node.module is missing it's a "from . import ..." statement
                        # if level > 0 it's a "from .submodule import ..." statement
                        if node.module is not None and node.level == 0:
                            if node.module.startswith('ui.'):
                                path=join(*(node.module.split(".")))+'.py'
                                modules.add(join(os.getcwd(),path))
                                

                    node_iter = ast.NodeVisitor()
                    #node_iter.visit_Import = visit_Import
                    node_iter.visit_ImportFrom = visit_ImportFrom
                    with open(obj.ep) as f:
                        node_iter.visit(ast.parse(f.read()))
                    
                    for path in sorted(modules):
                        id_eof = wx.NewIdRef()
                        evtid[id_eof]=path
                        self.Bind(wx.EVT_MENU, self.onEditMroFile, id=id_eof)
                        if 1:
                            item = wx.MenuItem(menu, id_eof,'       Edit "%s"' % path)
                           
                            menu.Append(item)

                            
                if 0:
                    for mstr, v in [(mstr, v) for mstr,v in mro.items() if v[0].__class__.__name__ in ['type']]:
                        mobj, id_eof = v
                        cn=mobj.__class__.__name__

                        try:
                            path = inspect.getfile(mobj)
                            if path not in modules:
                                item = wx.MenuItem(menu, id_eof,'   Edit "%s"' % path)
                                
                                menu.Append(item)
                                evtid[id_eof]=path
                                
                        
                        except TypeError:
                            pass
                    
                    

                mro={}
        if hasattr(self, 'onEditMroFile'):
            menu.AppendSeparator() 
            if 1:
                
                import ui_layer.config.ui_config as ui_config 
                pp(dir(ui_config))
                
                for i in inspect.getmembers(ui_config, inspect.isclass):
                    name, tp= i
                    print(name, tp.__class__, tp.__class__.__name__, inspect.getfile(tp))
                import ui_layer.config.ui_layout as ui_layout 
        
            for id, obj in enumerate([ui_config, ui_layout]):
                path=obj.__file__
                id_eof = wx.NewIdRef()
                
                evtid[id_eof]=path
                self.Bind(wx.EVT_MENU, self.onEditMroFile, id=id_eof)
                if 1:
                    item = wx.MenuItem(menu, id_eof,'Edit "%s"' % path)
                    font = item.GetFont()
                    font.SetWeight(wx.BOLD)
                    item.SetFont(font)
                    menu.Append(item)
                if 1:
                    for i in inspect.getmembers(obj, inspect.isclass):
                        name, tp= i
                        path=inspect.getfile(tp)
                        id_eof = wx.NewIdRef()
                        evtid[id_eof]=path
                        self.Bind(wx.EVT_MENU, self.onEditMroFile, id=id_eof)
                        if 1:
                            item = wx.MenuItem(menu, id_eof,'   Edit "%s"' % path)
                            #out.append(item)
                            menu.Append(item)
                                
        
        
        if 0:
            menu.AppendSeparator() 
            for id, obj in enumerate(self.getParents()):
                #print(123,obj.__class__.__name__)
                if hasattr(obj, 'onPreviewScript'):
                    if not hasattr(obj, "id_ps"):
                        obj.id_ps = wx.NewIdRef()

                        obj.Bind(wx.EVT_MENU, obj.onPreviewScript, id=obj.id_ps)
                    
                    #pp(dir(self))
                    item = wx.MenuItem(menu, obj.id_ps,'Preview "%s"' % obj.ep)
                    #out.append(item)
                    menu.Append(item)


        return 
    def onEditMroFile(self, event):
        global evtid
        if event.Id in evtid:
            fn = evtid[event.Id]
            assert fn
            self.send('openFile', (fn,0))
        else:
            pp(self.evtid)
    def getMenuItems(self, menu, gs):
        if not hasattr(self, "gs"):
            self.gs = gs
        out =[]
        for id, obj in enumerate([self, self.GetParent(), self.GetParent().GetParent(), self.GetParent().GetParent().GetParent()]):
            if not hasattr(obj, "id_ed"):
                obj.id_ed = wx.NewIdRef()
                
                obj.Bind(wx.EVT_MENU, obj.onEditObjFile, id=obj.id_ed)
            item = wx.MenuItem(menu, obj.id_ed,'Edit 33 "%s"' % obj.ep)
            out.append(item)
        return out

    def getPyConfigMenuItems(self, menu, gs):
        if not hasattr(self, "gs"):
            self.gs = gs
        out =[]
        for id, obj in enumerate([ self.GetParent(), self.GetParent().GetParent()]):
            if not hasattr(obj, "id_edc"):
                obj.id_edc = wx.NewIdRef()

                obj.Bind(wx.EVT_MENU, obj.onEditObjFileConfig, id=obj.id_edc)
            
            item = wx.MenuItem(menu, obj.id_edc,'Edit "%s"' % obj.ecp)
            out.append(item)
        return out


        
    def getJsonConfigMenuItems(self, menu):
        out =[]
        for cpath in [ apc.apc_path, sbc.sbc_path]:
            
            id= wx.NewIdRef()
            item = wx.MenuItem(menu, id,'Edit "%s"' % cpath)
            self.gen_bind(wx.EVT_MENU, item, self.onEditFile, cpath)			
            
            
            out.append(item)
        return out

    def load_cfg(self):
        global sbc, apc
        
        if not globals().get('sbc', None):
            import include.sb_settings as sb_settings 
            sbc = sb_settings.sbc
        if not globals().get('apc', None):
            import include.app_config as app_config 
            apc = app_config.apc
    
    def getJsonPyConfigMenuItems(self, menu):
        #self.load_cfg()
            
        out =[]
        for cpath in [ apc.apc_path, sbc.sbc_path]:
            
            id= wx.NewIdRef()
            bn = os.path.basename(cpath)
            fn, ext = os.path.splitext(bn)
            newfn = os.path.join(sbc.getRoot(),'include', '%s.py' % fn)
            item = wx.MenuItem(menu, id,'Edit "%s"' % newfn)
            self.gen_bind(wx.EVT_MENU, item, self.onEditFile, newfn)			
            
            
            out.append(item)
        return out
        
    def getLayoutConfigMenuItems(self, menu):
        self.load_cfg()

        out =[]

        for fn in [r'include\AppLayout.py',os.path.join(sbc.getAppsRoot(),sbc.getLayoutFile(sbc.pref))]:
            id= wx.NewIdRef()
            newfn = os.path.join(sbc.getRoot(), fn)
            item = wx.MenuItem(menu, id,'Edit "%s"' % newfn)
            self.gen_bind(wx.EVT_MENU, item, self.onEditFile, newfn)			
            
            
            out.append(item)
        return out
        
        
    def onEditFile(self, event, params):
    

        fn = params
        assert fn
        if fn:

            self.send('editFile', (fn,0))	
        else:
            error('onEditJsonFile: File name is empty')
    
    
    def onPreviewScript(self, event):
    
        
        fn = self.getEditPath(self.gs)
        assert fn
        if fn:
            self.send('previewScript', ((fn, 0), self))
        else:
            error('onEditObjFile: File name is empty')
            
    def onEditObjFile(self, event):
    
        obj = event.GetEventObject()
        fn = self.getEditPath(self.gs)
        assert(fn)
        
        if fn:
            
            self.send('openFile', (fn,0))	
        else:
            error('onEditObjFile: File name is empty')

        
    def onEditObjFileConfig(self, event):
    
        
        fn = self.getEditConfigPath(self.gs)

        if fn:
            self.send('editFile', (fn,0))	
        else:
            error('onEditObjFileConfig: File name is empty')		


