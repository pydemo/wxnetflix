import boto3
import codecs, json
import os, sys, csv, time, zipfile, logging
from os.path import join, basename, isfile, isdir, dirname


import importlib

e=sys.exit
from os.path import isfile, split, join, basename, isdir
import   subprocess
from collections import OrderedDict
from pprint import pprint as pp
from pathlib import Path
from cli_layer.fmt import pfmtd
from cli_layer.common import *
from collections import defaultdict, UserDict
import cli_layer.config.app_config as app_config 

log=logging.getLogger()
import getpass

import traceback
try:
    import cStringIO
except ImportError:
    import io as cStringIO


    
    
def get_params(**kwargs):
    params = kwargs['params']
    assert params, params
    cp=dict()
    if type(params) in [tuple]:
    
        cp = {pid:p for pid,p in enumerate(params)}
    else:
        assert type(params) in [str]
        cp[0]=params

    return cp, params
    
def upload_file(infile, outkey, bucket_name):
    #ACCESS_KEY, SECRET_KEY = keys 
    #assert ACCESS_KEY
    #assert SECRET_KEY
    s3 = boto3.client('s3') #, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    
    assert isfile(infile)
    with open(infile, "rb") as fh:
        s3.upload_fileobj(fh,bucket_name,outkey)
    return 0
        
        
def compressDir(indir, outfn):
    

    assert isdir(indir), indir
    path = join(indir,'python')


    zipf = zipfile.ZipFile(outfn, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
                
    zipf.close()
    print(f'COMPRESS dir "{indir}" succeded ({0})')
   
    return 0
        
def compressFiles(dir, outfn):
    
    

    assert isdir(dir), dir
    
    path = join(dir,'**','*.*')  

    files = [f for f in glob.glob(path , recursive=True)]
    pp(files)
    e()

    with zipfile.ZipFile(outfn , 'w') as ziph:
        for floc in files:
            ext = splitext(basename(floc))[1]
            fto = join('python', floc)
            ziph.write(floc,fto)
    code=SUCCESS
    print(f'COMPRESS layer "{dir}" succeded ({code})')
    return SUCCESS
        
class Val2Key(UserDict):                                                              
    def __init__(self, **kwargs):                                               
        super().__init__(kwargs)
        self.val_to_keys = defaultdict(list)
    def __setitem__(self, key, value):                                          
        super().__setitem__(key, value)
        self.val_to_keys[value].append(key)
    def __dir__(self):                                                          
        return self.keys()                                                      

    def __setstate__(self, state):                                              
        pass

    def get_key_for_val(self, value):
        out= self.val_to_keys[value]
        assert len(out) ==1, f'Value "{value}" does not exists'
        return out[0]

class duald(dict):                                                              
    def __init__(self, **kwargs):                                               
        super(duald, self).__init__(kwargs)
        
    #def __setitem__(self, key, value):                                          
    #    super().__setitem__(key, value)
    def __dir__(self):                                                          
        return self.keys()                                                      

    def __setstate__(self, state):                                              
        pass
    def __setattr__(self, key, value):                                          
        self[key] = value
    def __getattr__(self, key):
        idk='id'
        namek='id'
        try:
            if key in [idk,namek]:
                if key == idk:
                    id=self.get_id()
                    return id  
                else:
                    name=self.get_name()
                    return names
            else:
                return self[key]
        except KeyError:                                                        
            
            raise AttributeError(key)
            
    def get_id(self):
        global tmpl
        if self.get('id'):
            return self['id']
        else:
            name = self['name']
            
            assert name in tmpl.frefs.values(), f' "{name}" not in "{tmpl.frefs.values()}"'
            key = tmpl.frefs.get_key_for_val(name)
            return key
    def get_name(self):
        global tmpl
        
        if self.get('name'):
            return self.name
        else:
            id = self['id']
            
            assert id in tmpl.frefs, f' "{id}" not in "{tmpl.frefs}"'
            vals = tmpl.frefs[id]
            return vals
            

def load_csv(fname):
    out=[]
    with open(fname, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            out.append(row)
    return out



if is_nt:


    def cli_exception(func):
        def wrapper(*args, **kwargs):
         if 1:
            #manual test only

            from ui_layer.app import headless_ui, format_stacktrace
            from ui_layer.common import UI_TMP_DIR, UI_CFG_FN
            from ui_layer.utils import error
            import ui_layer.dialog.ErrDlg as ED
            import ui_layer.config.ui_config as ui_config 
            import cli_layer.config.app_config as app_config 
            

            app=headless_ui()
            try:

                original_return_val = func(*args, **kwargs)
            except:

                kwargs['quiet']=False
                if not kwargs.get('ui_layout') :
                    kwargs['ui_layout'] = 'default'
                import ui_layer.config.ui_config as ui_config
                ui_config.init(**kwargs)
                uic = ui_config.uic
                #ui_config.init(**kwargs)
                #apc = app_config.apc
                print()
                if 0: #apc.dl:
                    pfmtd(apc.dl,'DELETE Status')
                    print()
                if 0: #apc.cr:
                    pfmtd(apc.cr,'CREATE Status')
                    print()
                
                stacktrace = format_stacktrace()
                error(stacktrace)
                if 1:
                    ED.show(stacktrace)
                app.MainLoop()
                original_return_val=1
            return original_return_val
        return wrapper

else:


    def cli_exception(func):
        def wrapper(*args, **kwargs):
         if 1:
            original_return_val = func(*args, **kwargs)
            return original_return_val
        return wrapper
    
    

def get_err():
    err_log = cStringIO.StringIO()
    traceback.print_exc(file=err_log)
    return err_log.getvalue()
    
def format_stacktrace():
    parts = ["Traceback (most recent call last):\n"]
    parts.extend(traceback.format_stack(limit=25))
    parts.extend(traceback.format_exception(*sys.exc_info())[1:])
    return "".join(parts)

def d2d2(d):
    out=dict2()
    for k, v in d.items():
        if type(v) in [dict]:
            out[k]= d2d2(v)
        else:
            out[k]=v
    return out


def init_logging(d=0):
    global info, debug
    LOGGING_CONFIG = { 
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': { 
            'standard': { 
                '_format': '%(asctime)s|%(levelname)s|%(process)d|%(module)s.py|%(funcName)s|%(lineno)d| %(message)s',
                'format': '%(asctime)s|%(levelname)s/%(process)d/%(name)s|%(module)s.py|%(funcName)s|%(lineno)d| %(message)s',
                'datefmt':'%I:%M:%S'
            },
                'verbose': {
                    'format': '%(asctime)s|%(levelname)s|%(process)d|%(module)s.py|%(funcName)s()|%(lineno)d|%(message)s',
                    'datefmt':'%I:%M:%S'
                }
        },
        'handlers': { 
            'default': { 
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
                'console': {
                    'level': 'DEBUG' if d else 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
        },
        'loggers': { 
            '': { 
                'handlers': ['console'],
                'level':  'DEBUG' if d else 'INFO',
                'propagate': False
            },

        } 
    }
    logging.config.dictConfig(LOGGING_CONFIG)

    log=logging.getLogger()

    if 1:
        logging.getLogger('boto3').setLevel(logging.WARNING)
        logging.getLogger('boto3.resources').setLevel(logging.WARNING)
        #logging.getLogger('boto').setLevel(logging.WARNING)
        logging.getLogger('botocore').setLevel(logging.WARNING)
        
        logging.getLogger('s3transfer').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        
        logging.getLogger('socks').setLevel(logging.WARNING)
        logging.getLogger('asyncio').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)

        


    if 0:
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
        pp(loggers)
        e()


    return log


    

def _timer(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            start = time.time()
            
            result = function(*args, **kwargs)
            end = time.time()
            if 1: #not apc.quiet:
                log.info("Elapsed %s:%s:---> [ %0.3f ] sec." % (argument, function.__name__, (end - start)))
            return result
        return wrapper
    return decorator

def timer(*arguments):
    def decorator(function):
        def wrapper(*args, **kwargs):
            log = logging.getLogger()
            start = time.time()
            
            result = function(*args, **kwargs)
            end = time.time()
            if 1: #not apc.quiet:
                file, =arguments
                log.info("%s->%s->Elapsed: %0.3f sec." % (file, f'{function.__name__}()', (end - start)))
                #print("ELAPSED |%s | %s |---> [ %0.3f ] sec." % (file, function.__name__, (end - start)))
            return result
        return wrapper
    return decorator
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

def import_module_3(file_path):
    bn=basename(file_path)
    mod_name,file_ext = os.path.splitext(os.path.split(file_path)[-1])
    spec = importlib.util.spec_from_file_location(mod_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    if 1:
        sys.modules[mod_name] = module
    return module
    

    
    return module
def convert_path(path):
    if not is_nt:
        return path.replace('\\','/')
    else:
        return path
def os_path(path):
    if is_nt:
        return path.replace('/',os.sep)
    else:
        return path.replace('\\',os.sep)
        
def get_module_loc(**kwargs):
    pp(kwargs)
    cli_layout = kwargs.get('cli_layout' )
    assert cli_layout, 'Please, define cli_layout'
    
    pipeline	= os_path(kwargs['pipeline'])
    #if not apc.quiet: print(pipeline)
    _, ppl_name = split(pipeline)
    mod_fn = '%s.py' % ppl_name
    mod_dir = join(PPL_DIR,pipeline)
    assert isdir(mod_dir), mod_dir
    mod_loc = join (mod_dir, cli_layout, mod_fn)
    assert isfile(mod_loc), mod_loc
    mod_file = Path(mod_loc).resolve()
    
    print(str(mod_file))

    return str(mod_file)


    

