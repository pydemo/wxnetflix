import wx
import os, re, sys, copy, string
from os.path import isfile, isdir, join, basename
import json
import itertools
from datetime import datetime 
from copy import deepcopy
from pprint import pprint as pp

from cli_layer.Config import *

from cli_layer.common import LAYER_DIR, IN_DIR, CONFIG_DIR, OUT_DIR, PPL_DIR, CFG_LAYER_DIR

from ui_layer.common import *
from ui_layer.utils import dict2, exception

import shutil
import logging

log=logging.getLogger('ui')
error=log.error

e=sys.exit

def qprint(*args, **kwargs):
    global quiet
    if not quiet: print(*args, file=sys.stderr, **kwargs)



    
class Service:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, sname, mapping):
        """Constructor"""
        self.id = id
        
        self.sname = sname
        self.mapping = mapping
    def getVendorFilter(self):
        fls= self.mapping.getVendorFilter(service=self)
        return fls[self.id]

class Filter:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, fval, filter, mapping):
        """Constructor"""
        self.id = id
        self.fval = fval
        self.name = filter.name
        self.column= filter.column
        self.mapping = mapping

        
class Mapping:
    """"""
    VFILTER = dict2(name='Vendor filter', column='vendor')
    CASE = dict2(key_col='Merged Columns',  val_col='CASE')
    #----------------------------------------------------------------------
    def __init__(self, id, fn, dn, pipeline):
        """Constructor"""
        self.id = id
        self.fn = fn
        self.dn = dn
        self.pipeline = pipeline
        self.floc=self.getFloc()
        self.csv=load_csv(self.floc)
        self.header = [x.strip() for x in self.csv.pop(0)]
        self.services=[]
        self.filters=[]
        
    def getFloc(self):
        return join(self.dn, self.fn)

    def getServices(self):
        services = self.services
        header=self.header
        if not services:
            for sid, sn in enumerate(header[1:-2]):
                services.append(Service(sid, sn, self))
        
        return services
    def getFilters(self, filter):

        frow=self.getFilterRow(filter.name)
        
        filters=self.filters
        if not filters:
            for fid, fval in enumerate(frow[1:-2]):
                filters.append(Filter(fid, fval, filter, self))
        
        return filters
        
    def getHeader(self):
        return self.header
    
    def getFilterRow(self, filter_name):
        for row in self.csv:
            first_col, *_ = row
            if filter_name.strip().lower() == first_col.strip().lower():
                return row
            
        assert 1==2, 'Cannot find filter row "%s"' % filter_name
        
    def getVendorFilter(self, service):
        services = self.services
        assert service in services, '%s not in %s' % (services, self.services)
        #print(self.VFILTER)
        fls= self.getFilters(self.VFILTER)
        #pp(fls)
        return fls
    def getColId(self, cname):
        return self.getHeader().index(cname)
    def getMappedColRows(self):
        for row in self.csv:
            if row[0]:
                yield row
    
    def getCaseDict(self):
        key_cid=self.getColId(self.CASE.key_col)
        val_cid=self.getColId(self.CASE.val_col)
        out={}
        for row in self.getMappedColRows():
            key, val = row[key_cid], row[val_cid]
            if val.strip():
                out[key.strip()] = val.strip()
        return out
        
class CsvFile:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, fn, dn, pipeline):
        """Constructor"""
        self.id = id
        self.fn = fn
        self.dn = dn
        self.pipeline = pipeline
        self.floc=self.getFloc()
        #self.load()
    def getFloc(self):
        return join(self.dn, self.fn)
    @exception
    def load(self):
        self.csv=load_csv(self.floc)
        self.header = self.csv.pop(0)
        self.numRows=len(self.csv)
        self.numCols=len(self.header)
    def getColId(self, colname):
        return self.header.index(colname)
    def GetCellValue(self, row, col):
        return self.csv[row][col]

class UiConfig(Config): 
    def __init__(self, **kwargs):
        Config.__init__(self, **kwargs)
        if 1:
            cfg_root= UI_TMP_DIR
            cfgfn   = UI_CFG_FN
            cfg_loc = join(cfg_root, cfgfn)
            
        self.ui_path=cfg_loc

        print(7777,cfg_loc)
        self.aui_dir = self.getCfgRoot()
        if not isdir(self.aui_dir): os.makedirs(self.aui_dir)
        self.aui_path = aui_path= join(self.getCfgRoot(), AUI_FN)
        
        if not isfile(aui_path): 
            with open(aui_path, 'w') as fh:
                fh.write(AUI_TMPL)
        self.validate().load()
        self.root=os.getcwd()
        pp(kwargs)
        self.pipeline     = pipeline = kwargs['pipeline'].strip()
        pp(kwargs)
        self.params=params=kwargs['params']

        self.ui_layout=kwargs['ui_layout']

        self.module_root=join (self.root,UI_DIR,MODULE_DIR) 
        self.csv_root=join (IN_DIR,pipeline) 
        self.in_root=join (IN_DIR,pipeline) 
        self.out_root=join (OUT_DIR,pipeline) 
        self.ppl_root=join (PPL_DIR,pipeline) 
        self.ppl_utils_root=join (PPL_DIR,pipeline,'include') 
        self.map_root=join (LAYER_DIR,CONFIG_DIR,'subconfig') 
        self.ppl_cfg_root=join (CFG_LAYER_DIR,pipeline) 
        if '\\' in pipeline:
            self.dotted_pipeline=pipeline.replace('\\','.')
        else:
            self.dotted_pipeline=pipeline.replace('/','.')
        self.pipeline_dir = join(PIPELINE_DIR, self.dotted_pipeline.replace('.', os.sep))
    def getCsvFiles(self):
        out=[]
        for fid, fn in enumerate(os.listdir(self.csv_root)):
            out.append(CsvFile(fid, fn, self.csv_root, self.pipeline))
        return out
    def getMappings(self):
        out=[]
        if 0:
            for fid, fn in enumerate(os.listdir(self.map_root)):
                out.append(Mapping(fid, fn, self.map_root, self.pipeline))
        return out
    def getFrameSize(self):
        fs= self.cfg.get('frameSize',None)
        assert fs, fs
        return [int(x) for x in fs]
    def getFramePos(self):
        fs= self.cfg.get('framePosition',None)
        assert fs, fs
        return [int(x) for x in fs]	

    def setCfg(self,**kwargs):
        if kwargs['quiet']:
            self.quietOn() 
        else:
            self.quietOff()

    def saveConfig(self):
        
        #assert hasattr(self, 'cfg')
        assert isfile(self.ui_path)
        
        with open(self.ui_path, 'w') as fp:
            dump = json.dumps(self.cfg, indent='\t', separators=(',', ': '))
            if 0:
                new_data= re.sub('{\n[\t]+"page"','{"page"', dump)
                new_data= re.sub(',\n[\t]+"layout"',', "layout"', new_data)
            
            new_data= re.sub('"\n[\t]+},', '"},', dump)

            fp.write(dump)
    def initCfgFile(self,path):
        if not isfile(path):
            with open(path, 'w') as fh: fh.write(UI_CFG_TMPL)
    def load(self):
        self.initCfgFile(path=self.ui_path)
        self.cfg = self.LoadConfig(config_path=self.ui_path)
        return self
        
        
            
    def getPythonHome(self):
        cfg=self.cfg
        assert 'Python' in cfg
        assert 'home' in cfg['Python']
        return cfg['Python']['home']

    def getApcPath(self):
        return join(self.getCfgRoot(), self.APC_FILE_NAME )
    def getApcExecPath(self):
        return join(self.getCfgRoot(), self.EXEC_APC_FILE_NAME )
    def assertExists(self):
        assert isdir(self.cfg_root), 'Config root does not exists for app "%s"\n%s' % (self.app_name, self.cfg_root)
        assert isfile(self.ui_path), 'App config JSON file does not exists for app "%s"\n%s' % (self.app_name,self.ui_path)
        
        return self

    
    def createConfigRoot(self):
        if not os.path.isdir(self.cfg_root):
            os.makedirs(self.cfg_root, exist_ok=True)
        return self



    def validate(self):
        if not  os.path.isdir(self.cfg_root):
            raise Exception('Cfg root does not exists at " %s "' % ( self.cfg_root))
        if not isfile(self.ui_path):
            error('App config does not exists at \n%s' % self.ui_path)
            
        return self


    def getAppName(self, layout_loc=None):
        if not layout_loc: return self.app_name
        else:
            return os.path.splitext(os.path.basename(layout_loc))[0]
    def quietOn(self):
        global quiet
        self.quiet=quiet=True
    def quietOff(self):
        global quiet
        self.quiet=quiet=False
    def getErrDlgSize(self):
        cfg=self.cfg
        assert 'ErrDlg' in cfg
        assert 'size' in cfg['ErrDlg']
        return cfg['ErrDlg']['size']
    def getErrDlgSPos(self):
        cfg=self.cfg
        assert 'ErrDlg' in cfg
        assert 'pos' in cfg['ErrDlg']
        return cfg['ErrDlg']['pos']
    def setErrDlgSize(self, size):
        cfg=self.cfg
        assert 'ErrDlg' in cfg
        assert 'size' in cfg['ErrDlg']
        cfg['ErrDlg']['size'] = tuple(size)
        self.saveConfig()
    def setErrDlgPos(self, pos):
        cfg=self.cfg
        assert 'ErrDlg' in cfg
        assert 'pos' in cfg['ErrDlg']
        cfg['ErrDlg']['pos']= tuple(pos)
        self.saveConfig()