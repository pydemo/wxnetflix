import wx
import os, re, sys, copy, string
from os.path import join
import json, shutil, glob

from datetime import datetime 
from copy import deepcopy
from pprint import pprint as pp
from ui_layer.log_init import  info, debug
from ui_layer.utils import  dict2, exception
from cli_layer.common import CFG_LAYER_DIR
from ui_layer.common import *

e=sys.exit

import ui_layer.config.ui_config as ui_config 
uic = ui_config.uic

from ui_layer.Config import Config
from ui_layer.Layout import Layout

import cli_layer.config.app_config as app_config
apc = app_config.apc



class UiLayout(Config): 
    def __init__(self, pipeline):
        Config.__init__(self)
        self.cfg = None
        self.pref=None
        self.ppl=pipeline
        self.layout_dir=self.getLayoutDir()
        #self.build_loc = join(UI_TMP_DIR, BUILD_DIR, BUILD_FN )
        self.build_tmpl_loc = join(uic.root, CFG_LAYER_DIR,  BUILD_DIR, BUILD_TMPL_FN )
    @exception
    def loadLayout(self):
        global  cfg
        
        self.layout_fn = self.getLayoutFile()
        self.layout_name = self.getLayoutFileName()
        self.layout_loc= join(uic.root, self.layout_fn)
        assert os.path.isfile(self.layout_loc), 'UI layout does not exists\n%s\n%s' % (self.layout_loc,self.layout_fn)
        cfg=load_config(config_path = self.layout_loc)
        return cfg

    def getLayoutDir(self):
        out = join (PIPELINE_DIR, self.ppl, 'ui')
        assert out
        return out
        
    def getLayoutFile(self):
        out = join (os.getcwd(),PIPELINE_DIR, self.ppl, 'ui_layout', self.getLayoutFileName())
        assert out
        return out

    def getLayoutFileName(self):
        assert apc.kwargs
        pp(apc.kwargs)
        return '%s.json' % apc.kwargs.get('ui_layout1','default')
        
    def getNode_LayoutRoot1(self, nref, ntype):
        api = getattr(sbc, 'get%sRoot' % ntype)
        return os.path.join(api(nref),self.LAYOUT_DIR)
        
        
    def getAllLayouts(self, pref):
    

        out={}
        for k, ntype in self.ntypes.items():
            if k in pref: 
                out.update(self.getNode_LayoutList(pref, ntype))
        
        return out

    def getNode_LayoutList(self, pref, ntype):
        api = getattr(self,'get%sCopyRef' % ntype)
        nref =  api(pref)
        layout_root = self.getNode_LayoutRoot(nref, ntype)
        return {os.path.relpath(file,self.root):nref for file in glob.glob(os.path.join(layout_root, JSON_EXT))}



        
        
    def assertExists(self):
        assert os.path.isdir(self.cfg_root), 'Config root does not exists for app "%s"' % self.app_name
        assert os.path.isdir(self.layout_root), 'Layout root does not exists for app "%s"\n%s' % (self.app_name,self.layout_root)
        return self
 
        
    def getLayoutList(self):
        return [os.path.basename(file) for file in glob.glob(os.path.join(self.layout_root, JSON_EXT))]



        
    def get(self, key, default = None):	
        global cfg
        if not 'cfg' in globals():
            self.cfg=cfg=self.loadLayout()

            return self.cfg.get(key, default)
        
    def items(self):
        
        global cfg
        if not 'cfg' in globals():
            self.cfg=cfg=self.loadLayout()
            return [(k,v) for k, v in cfg.items() if not k.startswith('_')]

    def keys(self):
        
        global cfg
        if 'cfg' in globals():
            return cfg.keys()
        else:
            
            cfg=self.loadLayout()
            return cfg.keys()
