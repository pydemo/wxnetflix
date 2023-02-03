import wx
import os, sys, csv, subprocess
from os.path import join, basename, isfile, isdir, dirname
import inspect, traceback
import logging
import importlib
import ui_layer.dialog.ErrDlg as ED
from cli_layer.fmt import pfmtd
from ui_layer.common import  getEditor


from locale import getdefaultlocale, setlocale, LC_ALL
default_fullscreen_style = wx.FULLSCREEN_NOSTATUSBAR | wx.FULLSCREEN_NOBORDER | wx.FULLSCREEN_NOCAPTION

e=sys.exit


log=logging.getLogger('ui')
error=log.error
def format_stacktrace():
    parts = ["Traceback (most recent call last):\n"]
    parts.extend(traceback.format_stack(limit=25))
    parts.extend(traceback.format_exception(*sys.exc_info())[1:])
    return "".join(parts)
def import_module(file_path):
    #if not apc.quiet: print(file_path)
    bn=basename(file_path)
    
    mod_name,file_ext = os.path.splitext(os.path.split(file_path)[-1])
    spec = importlib.util.spec_from_file_location(mod_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if 1:
        sys.modules[mod_name] = module
    
    return module
    
def load_pipeline_module(uic, mod_name):
    assert isdir(uic.pipeline_dir)
    dn = dirname(mod_name)
    fn = basename(mod_name)
    #assert not dn, dn
    mod_loc= join(uic.pipeline_dir,'module',uic.ui_layout, dn, f'{fn}.py')
    assert isfile(mod_loc), mod_loc
    return getattr(import_module(mod_loc),  fn)


def exceptionLogger(func,  mname=''):
    def logger_func(*args, **kw):
        
        try:
            if not kw:
                return func(*args)
            return func(*args, **kw)
        except Exception:
            fname=func.__name__			
            stacktrace = format_stacktrace().replace('"<string>"', '"%s"' % mname)
            error(stacktrace)

            if 1:
                #import dialog.StacktraceDlg as ED
                #import dialog.ErrDlg as ED
                ED.show(stacktrace)
            if 0:
                dlg = wx.MessageDialog(win, stacktrace,
                    'Cannot open file',
                    wx.OK | wx.ICON_INFORMATION
                    #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                    )
                dlg.ShowModal()
                dlg.Destroy()
        
    logger_func.__name__ = func.__name__
    logger_func.__doc__ = func.__doc__
    if hasattr(func, '__dict__'):
        logger_func.__dict__.update(func.__dict__)
    return logger_func 
    
def evt_stacktrace(mname):
    """
    A decorator that will catch and log any exceptions that may occur
    to the named logger.
    """
    import functools
    return functools.partial(exceptionLogger, mname=mname) 

def import_module_3(file_path):
    bn=basename(file_path)
    mod_name,file_ext = os.path.splitext(os.path.split(file_path)[-1])
    spec = importlib.util.spec_from_file_location(mod_name, file_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as err:
        ex(str(err))
    if 1:
        sys.modules[mod_name] = module
    return module
    
class fstring:
    def __init__(self, payload):
        self.payload = payload		
    def __str__(self):
        
        vars = inspect.currentframe().f_back.f_globals.copy()
        vars.update(inspect.currentframe().f_back.f_locals)
        #pp(list(vars.keys()))
        #pp(self.payload)
        #pp(vars.get('page_load'))
        return self.payload.format(**vars)

            
class fstring2:
    def __init__(self, payload, relpath=None):
        self.payload = payload
        self.relpath=relpath
    def __str__(self):
        
        vars = inspect.currentframe().f_back.f_globals.copy()
        vars.update(inspect.currentframe().f_back.f_locals)
        if not self.payload.format(**vars):
            return self.payload
        if self.relpath:
            
            return os.path.relpath(self.payload.format(**vars), self.relpath) 
        else:
            return self.payload.format(**vars)
        

def exception(func):
    def wrapper(*args, **kwargs):
        
        try:
            original_return_val = func(*args, **kwargs)
        except:
            ex()
        
        return original_return_val
    return wrapper

    
def ex(win=None,_exit=False):

    stacktrace = format_stacktrace()
    error(stacktrace)
    if 1:
        ED.show(stacktrace)
    if _exit:
        raise
    else:
        return False
class dict2(dict):                                                              

    def __init__(self, **kwargs):                                               
        super(dict2, self).__init__(kwargs)                                     

    def __setattr__(self, key, value):                                          
        self[key] = value                                                       

    def __dir__(self):                                                          
        return self.keys()                                                      

    def __getattr__(self, key):                                                 
        try:                                                                    
            return self[key]                                                    
        except KeyError:                                                        
            raise AttributeError(key)                                           

    def __setstate__(self, state):                                              
        pass 
        
def load_csv_dict(fname):
    out=dict2()
    with open(fname, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for rid, row in enumerate(spamreader):
            out[rid]=dict2(row=row)
    return out
    
    
def open_settings(filename):
    #filename=r'c:\Python35-64\apps\BatchStatusBrowser\cfg\batch_status.cfg'
    conf = wx.FileConfig(localFilename = filename)
    #print(conf)
    
    def create_entry(entry_name, entry_value):
        if not conf.HasEntry(entry_name):
            if isinstance(entry_value, (str, bytes)):
                conf.Write(entry_name, entry_value)
            elif isinstance(entry_value, int):
                conf.WriteInt(entry_name, entry_value)
            elif isinstance(entry_value, bool):
                conf.WriteBool(entry_name, entry_value)
            else:
                conf.Write(entry_name, repr(entry_value))
            return True
        else:
            return False
    flag_flush = False
    #print(getdefaultlocale())
    if create_entry('Language/Catalog', getdefaultlocale()[0]):
        flag_flush = True
    if create_entry('GUI/load_default_perspective_on_start', True):
        flag_flush = True
    if create_entry('GUI/save_default_perspective_on_exit', True):
        flag_flush = True
    if create_entry('GUI/perspective', ''):
        flag_flush = True
    if create_entry('GUI/load_default_state_on_start', True):
        flag_flush = True
    if create_entry('GUI/save_default_state_on_exit', True):
        flag_flush = True
    if create_entry('GUI/fullscreen_style', default_fullscreen_style):
        flag_flush = True
    if create_entry('GUI/centre_on_screen', repr((False, wx.BOTH))):
        flag_flush = True
    if create_entry('GUI/default_open_path', '.'):
        flag_flush = True
    if flag_flush:
        conf.Flush()
    
    return conf


DEFAULT_PERSPECTIVE = "Default Perspective"
_platformNames = ["wxMSW", "wxGTK", "wxMac"]

    
def GetDocFile():

    docFile = os.path.join(GetDataDir(), "docs", "TrunkDocs.pkl")

    return docFile
    
def MakeDocDirs():

    docDir = os.path.join(GetDataDir(), "docs")
    if not os.path.exists(docDir):
        os.makedirs(docDir)

    for plat in _platformNames:
        imageDir = os.path.join(docDir, "images", plat)
        if not os.path.exists(imageDir):
            os.makedirs(imageDir)	
def GetDocImagesDir():

    MakeDocDirs()
    return os.path.join(GetDataDir(), "docs", "images")

def GetDataDir():
    """
    Return the standard location on this platform for application data
    """
    sp = wx.StandardPaths.Get()
    return sp.GetUserDataDir()
    
def GetConfig():
    if not os.path.exists(GetDataDir()):
        os.makedirs(GetDataDir())

    config = wx.FileConfig(
        localFilename=os.path.join(GetDataDir(), "options"))
    return config
    
    
def edit_file( fn):
    EDITOR=getEditor()
    assert isfile(fn), fn
    if 1:
        subprocess.call([EDITOR, fn])