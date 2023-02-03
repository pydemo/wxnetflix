import wx
import os, sys, six, shutil
from os.path import isfile, join, isdir, splitext
from pprint import pprint as pp
from ui_layer.utils import  fstring, fstring2, exception
import wx.lib.agw.aui as aui
#from include.log_tools import ex

from ui_layer.utils import evt_stacktrace

import ui_layer.config.ui_config as ui_config 
uic = ui_config.uic

import ui_layer.config.ui_layout as ui_layout 
uilyt = ui_layout.uilyt

e=sys.exit

DEFAULT_IU_FLOC = join('ui_layer', 'config', 'template', 'default_ui.json')
PPL_DEFAULT_UI_DIR = join(uic.root, 'ui_layer', 'pipeline', uic.pipeline)
PPL_DEFAULT_UI_FN = 'default.json'


DEFAULT_PERSPECTIVE = "Default Perspective"

class PageBuilder(object):
    @exception
    def __init__(self, layout_fn):
        global code
        code=[]
        
        if not  isfile(layout_fn):
            e(f'Layout file does not exists:\n{layout_fn}')
        if 0:
            if not  isfile(layout_fn):
                assert isfile(DEFAULT_IU_FLOC), DEFAULT_IU_FLOC
                if not isdir(PPL_DEFAULT_UI_DIR):
                    os.makedirs(PPL_DEFAULT_UI_DIR)
                floc=join(PPL_DEFAULT_UI_DIR, PPL_DEFAULT_UI_FN)
                shutil.copyfile(DEFAULT_IU_FLOC,floc)

        self.layout_fn = layout_fn
        if not isdir(uic.getBuildRoot()): os.makedirs(uic.getBuildRoot())
    def file_from_name(self, layout):
        return '%s.json' % layout
        
    def getWinName (self, cref):
        layer, winname = cref.split(':')
        return winname
        
    def getWinKey(self, ccfg):
        mpath  	= ccfg.get("modulePath", None)
        cname  	= ccfg.get("className", None)
        return '%s.%s' % (mpath, cname)

    def get_params(self,**kwargs):
        out=[]
        for key,val in kwargs.items():
            out.append(f', {key}=r"{val}"')
        return ''.join(out)
    def get_pref(self,ccfg):
        out=[]
        pref = ccfg['pref']

        for key in  [key for key in pref if key in apc.ntypes]:
            out.append(f"{key} = '{pref[key]}'")
        return ','.join(out)


        
    @exception
    def buildPageLayout(self):

        global uilyt, uic
        #print(self.layout_fn)
        #e()
        layout_fn = self.layout_fn

        for sect, scfg in uilyt.items():

            for cref  in [x for x in scfg if not ':_' in x]:
                ccfg = scfg[cref]

                assert 'modulePath' in ccfg
                ccfg['modulePath'] = str(fstring2(ccfg['modulePath'],uic.root))
                mpath 	=   ccfg['modulePath']
                #pp(mpath)
                #e()
                bsize 	= ccfg.get("bestSize", None)
                cvis  	= False #ccfg.get("captionVisible", None)
                closeb  = ccfg.get("closeButton", None)
                cname  	= ccfg.get("className", None)
                oapi  	= ccfg.get("objectAPI", 'runTest')
                children  = ccfg.get("childFrame", None)
                assert oapi
                assert cname
                assert mpath
                #mpath = str(fstring2(mpath,apc.getRoot()))
                
                
                layer, _ = cref.split(':')

                
                
                ccfg['layout_fn'] = layout_fn
                    
                if 1:
                    winname = self.getWinName(cref)
                    winkey= self.getWinKey(ccfg)
                    apiParams = ccfg.get('apiParams', {})
                    #pp(apiParams)
                    #e()
                    for k in apiParams:
                        apiParams[k] = str(fstring2(apiParams[k],uic.root))

                    rmod=splitext(mpath.replace('\\','.').replace('/','.'))[0] #.rstrip('.py')
                    code.append(f"""
        #
        #{winname} | {winkey}	
        #{mpath}
        # {rmod}
        from {rmod} import {oapi}
            """ )

                    apparams =self.get_params(**apiParams)
                    code.append(f"        winname   = '%s'" % winname)
                    code.append(f"        winkey    = r'%s'" % winkey)
                    code.append(f"        win = parent={oapi}(parent=self.parent, name=winname, lineno=0, layout_fn = r'{layout_fn}' {apparams})")
                    if 'send' in ccfg:
                        code.append(f"        win.sender='%s'" % ccfg['send'])
                    if 'sub' in ccfg:
                        for sb in ccfg['sub']:
                            code.append(f"        win.sub('%s')" % sb)
                    code.append(f"        self.attachWin(win, winkey,winname)")

                if 1:

                    bestsize="""
        BestSize(wx.Size(%s,%s)).MinSize(wx.Size(%s,%s)).""" % tuple(bsize+bsize) if bsize else ''
                    captionvisible= 'True' if cvis else 'False' 
                    closebutton= False #'True' if closeb else 'False' 
                    cmd=f"""
        self.mgr.AddPane(win,aui.AuiPaneInfo().{sect}().Layer({layer}).{bestsize}Caption("{winname}").
        CloseButton({closebutton}).Name("{winname}").CaptionVisible({captionvisible}))"""
                    #pp(cmd)
                    #e()
                    code.append(cmd)

                
                if children:
                    
                    for c_cref in [x for x in children if not ':_' in x]:
                        c_ccfg= children[c_cref]
                        assert 'modulePath' in c_ccfg
                        c_ccfg['modulePath'] = str(fstring2(c_ccfg['modulePath'],uic.getRoot()))
                
                        c_mpath     = c_ccfg.get("modulePath", None)
                        c_bsize     = c_ccfg.get("bestSize", None)
                        c_cvis      = c_ccfg.get("captionVisible", None)
                        c_closeb    = c_ccfg.get("closeButton", None)
                        c_cname     = c_ccfg.get("className", None)
                        c_oapi      = c_ccfg.get("objectAPI", 'runTest')
                        
                        c_layer, c_winname = c_cref.split(':')
                        
                        c_ccfg['layout_fn'] = layout_fn
                        
                        
                        if 1:
                            c_winname = self.getWinName(c_cref)
                            c_winkey= self.getWinKey(c_ccfg)
                            code.append(f'        if 1: #Child111 | {c_winname} | {c_winkey}')
                            apiParams = c_ccfg.get('apiParams', {})
                            for k in apiParams:
                                apiParams[k] = str(fstring2(apiParams[k],uic.getRoot()))

                            c_rmod=splitext(c_mpath.replace('\\','.').replace('/','.'))[0]
                            code.append(f"""
            from {c_rmod} import {c_oapi}
                    """ )

                            apparams =self.get_params(**apiParams)
                            code.append(f"            winname   = '%s'" % c_winname)
                            code.append(f"            winkey    = r'%s'" % c_winkey)
                            code.append(f"            win = {oapi}(parent=self.parent, name=winname,  lineno=0, layout_fn =r'{layout_fn}'  {apparams})")
                            if 'send' in c_ccfg:
                                code.append(f"            win.sender='%s'" % c_ccfg['send'])
                            if 'sub' in c_ccfg:
                                for sb in c_ccfg['sub']:
                                    code.append(f"            win.sub('%s')" % sb)
                            
                            code.append(f"            self.attachWin(win, winkey,winname)")

                        c_captionvisible= 'True' if cvis else 'False' 
                        c_closebutton= False # 'True' if closeb else 'False' 
                        
                        c_cmd=f"""
            self.mgr.AddPane(win, aui.AuiPaneInfo().CaptionVisible({c_captionvisible}).Caption("{c_winname}").CloseButton({c_closebutton}).
            Name("{c_winname}"), target=self.mgr.GetPane("{winname}"))"""
                        code.append(c_cmd)
                    code.append('        self.mgr.ShowPane(parent, True)')

        self.createPage()
    def createPage(self):
        build_loc= uilyt.build_tmpl_loc
        assert isfile(build_loc), build_loc
        with open(build_loc, 'r') as fh:
            tmpl = fh.read()
        
        page_load = '\n'.join(code)
        out = tmpl.replace('{page_load}', page_load)
        
        self.saveCode(out)
    def getBuildName(self):
        bn=self.layout_fn.replace('\\','-').replace('/','-')
        assert bn.endswith('.json')
        sp= bn.split('.json')
        assert len(sp) ==2
        fn = '%s.py' % sp[0] 
        return fn
    def getBuildLoc(self):
        return join(uic.getBuildRoot(), self.getBuildName())
        
    def saveCode(self, out):
        if 1:
            bfn=self.getBuildLoc()
            with open(bfn, 'w') as ph:
                ph.write(out)
        if 0:
            build_dir = join('ui_layer', 'build')
            assert isdir(build_dir), build_dir
            bfn=join(build_dir,'Layout.py')
            with open(bfn, 'w') as ph:
                ph.write(out)
        

        
        

