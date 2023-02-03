import wx
import os, sys
import csv, codecs, json

import os, sys, traceback, subprocess
from os.path import isfile, join, isdir

from pprint import pprint as pp

e=sys.exit
home=os.path.dirname(sys.argv[0])
if not home :
    home=os.path.dirname(os.path.abspath(__file__))
APP_NAME='gh_cli'
if os.name == "nt":
    UI_TMP_DIR=join('C:\\','tmp',APP_NAME)
else:
    UI_TMP_DIR=join('/tmp',APP_NAME)


START_SIZE  = (550, 550)
START_POS	= (350,150)

UI_DIR      = 'ui_layer'
AUI_FN      = 'aui.cfg'
JSON_EXT    = "*.json"
TOOLS_DIR   = 'tools'
UI_CFG_FN   = 'GH_ui.json'
#INCLUDE_DIR = 'include'
MODULE_DIR  = 'module'
PIPELINE_DIR= 'pipeline'
BUILD_DIR   = 'ui_build'
CONFIG_DIR  = 'config'
TEMPLATE_DIR= 'template'
UI_TMPL_CFG_FN = 'uic_config.json'
BUILD_TMPL_FN  = 'PageTemplate.py'
UI_TMPL_DIR = join('ui_layer','template')


import collections

PageType = collections.namedtuple('PageType', ['host', 'app'])
PAGE_TYPE = PageType(0, 1)

AUI_TMPL="""[Language]
Catalog=en_US
[GUI]
load_default_perspective_on_start=1
save_default_perspective_on_exit=1
perspective=layout2|name=LogWindow;caption=;state=67373052;dir=3;layer=1;row=0;pos=0;prop=100000;bestw=-1;besth=150;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=Editor;caption=;state=263164;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=240;besth=-1;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=DemoTree;caption=;state=263164;dir=4;layer=2;row=0;pos=0;prop=100000;bestw=240;besth=-1;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=DemoTree1;caption=;state=263164;dir=4;layer=2;row=0;pos=1;prop=100000;bestw=240;besth=-1;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|dock_size(3,1,0)=171|dock_size(5,0,0)=242|dock_size(4,2,0)=242|
load_default_state_on_start=1
save_default_state_on_exit=1
fullscreen_style=28
centre_on_screen=(False, 12)
default_open_path=.
position=wx.Point(100, 100)
size=wx.Size(1370, 1120)
font=0;-12;0;0;0;400;0;0;0;1;0;0;0;0;Segoe UI
"""
if 1:
    ui_cfg_tmpl_dir= join(UI_DIR, CONFIG_DIR, TEMPLATE_DIR)
    assert isdir(ui_cfg_tmpl_dir), 'UI config template dir does not exists: "%s"' % ui_cfg_tmpl_dir
    ui_cfg_tmpl_fn= join(ui_cfg_tmpl_dir,UI_TMPL_CFG_FN)
    assert isfile(ui_cfg_tmpl_fn), 'UI config template file does not exists: "%s"' % ui_cfg_tmpl_fn
    UI_CFG_TMPL=open(ui_cfg_tmpl_fn, 'r').read()
def load_config(config_path,  verify_version=True):

    with codecs.open(config_path, encoding="utf-8") as stream:
        config = json.load(stream)

    return config



    
def format_stacktrace():
    parts = ["Traceback (most recent call last):\n"]
    parts.extend(traceback.format_stack(limit=50)[:-2])
    parts.extend(traceback.format_exception(*sys.exc_info())[1:])
    return "".join(parts)

def getEditor(apc=None):
    if not apc:
        APP_ROOT=os.getcwd()
    else:
        APP_ROOT=apc.home
    floc=join('..\\','..\\','Notepad++', 'notepad++.exe')
    assert isfile(floc), floc
    return floc

def open_editor(fn, ln=0, win=None, cdir=None):
    
    EDITOR= getEditor()
    #print(EDITOR)
    try:
        if cdir: os.chdir(cdir)
        assert os.path.isfile(fn), 'Cannot open file "%s" [%s]' % (fn, os.getcwd())

        
        #info('Editing 1 "%s"' % fn)
        if ln:
            subprocess.call([EDITOR, fn, '-n%d' % ln])
        else:
            subprocess.call([EDITOR, fn])
    except:
        raise
        if 0:
            import inspect
            #pp (traceback.format_stack(limit=500))
            frm = inspect.trace()
            #pp(frm)
            mod = inspect.getmodule(frm[0])
            modname = mod.__name__ if mod else frm[1]
            #print ('Thrown from', modname)
        
        if 1:
            print(format_stacktrace())
        if 0:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print ("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=50, file=sys.stdout)
            print ("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=50, file=sys.stdout)
        if 0:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print ("*** print_exc:")
            traceback.print_exc()
            print ("*** format_exc, first and last line:")
            formatted_lines = traceback.format_exc().splitlines()
            print (formatted_lines[0])
            print (formatted_lines[-1])
            print ("*** format_exception:")
            print (repr(traceback.format_exception(exc_type, exc_value,
                                                  exc_traceback)))
            print ("*** extract_tb:")
            print (repr(traceback.extract_tb(exc_traceback)))
            print ("*** format_tb:")
            print (repr(traceback.format_tb(exc_traceback)))
            print ("*** tb_lineno:", exc_traceback.tb_lineno)
    
        if 0:
            stacktrace = format_stacktrace()
            error(stacktrace)

            if 1:
                import dialog.ErrDlg as ED
                ED.show(stacktrace, win)
            if 0:
                dlg = wx.MessageDialog(win, stacktrace,
                    'Cannot open file',
                    wx.OK | wx.ICON_INFORMATION
                    #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                    )
                dlg.ShowModal()
                dlg.Destroy()
                