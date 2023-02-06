import wx
import os, sys, logging
from os.path import join, isdir, split, basename
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
from asyncio.events import get_event_loop
import time
import wx.lib.agw.aui as aui
from pprint import pprint as pp
from cli_layer.utils import timer, get_module_loc, import_module, get_err, init_logging


#log=init_logging()
import cli_layer.config.app_config as app_config 

import click
click.disable_unicode_literals_warning = True
home=os.path.dirname(sys.argv[0])
if not home :
    home=os.path.dirname(os.path.abspath(__file__))
e=sys.exit

bnf=basename(__file__)

nop_opt=sys.argv[1]

if nop_opt.strip() in ['-nop']: #'Arguments must start with "Total pipeline params count [-nop]"'
    nop=str(sys.argv[2])
    assert nop.isdigit(), '-nop must be count of procedure params (got "%s").' % nop
else:
    nop=None


import cli_layer.config.app_config as app_config  

        
        


class MainFrame(wx.Frame):
    def __init__(self, title, parent=None):
        super(MainFrame, self).__init__(parent, title=title, size=(600,800), pos=(400,200))
        vbox = wx.BoxSizer(wx.VERTICAL)
        from ui_layer.LoaderPanel import LoaderPanel
        panel=LoaderPanel(self)
        if 1:
            self.mgr = aui.AuiManager()
            self.mgr.SetManagedWindow(self)
            self.allowAuiFloating = False
            #self.refs=defaultdict(dict)
            
            self.mgr.AddPane(panel,aui.AuiPaneInfo().Center().Layer(1).
            BestSize(wx.Size(200,150)).MinSize(wx.Size(200,150)).
            CloseButton(False).Name("MainPanel").CaptionVisible(False))


from cli_layer.utils import  cli_exception
#@timer (bnf)
def main_ui(**kwargs):
    global log, apc
    if 1:
        app_config.init(**kwargs)
        apc = app_config.apc
        apc.validate().load() 
    if 1:
        from ui_layer.app import main_ui
        from ui_layer.common import UI_TMP_DIR, UI_CFG_FN

        import ui_layer.config.ui_config as ui_config 
        ui_config.init(**kwargs)
        import ui_layer.config.ui_layout as ui_layout 
        ui_layout.init(**kwargs)

@click.command()
@click.option('-l',  '--lame_duck', default = 0,	help = 'Limit', type=int, 	required=False )
@click.option('-nop','--num_of_params', default = None,	help="ParmsConfig", type=int, required=False)
@click.option('-r',  '--runtime',	default = 'DEV',help = 'Runtime.') # DEV/UAT/PROD
@click.option('-p',  '--pipeline',  default = None,	help = 'ETL pipeline name',	required=True )
@click.option('-pa', '--params', 	nargs=int(nop) if nop else 0, help="Pipeline params", type=str, required=False)
@click.option('-ld', '--lame_duck',	default = 0,  help="Import limit", type=int, required=False)
@click.option('-la', '--ui_layout',	default='default', type=str, required=False, help="Open manual test ui.")
@click.option('-d' , '--debug',     is_flag=True, help="Print debug output.")
@click.option('-q' , '--quiet',     is_flag=True, help="Quet mode.")
@click.option('-h' , '--help',      is_flag=True, help="Show usage.")
@click.option('-o' , '--open',      is_flag=True, help="Open pipeline file and exit.")
@cli_exception
def main(**kwargs):
    global log
    if 1:
        app_config.init(**kwargs)
        apc = app_config.apc
        apc.validate().load() 
    if 1:
        from ui_layer.app import main_ui
        from ui_layer.common import UI_TMP_DIR, UI_CFG_FN

        import ui_layer.config.ui_config as ui_config 
        ui_config.init(**kwargs)
        import ui_layer.config.ui_layout as ui_layout 
        ui_layout.init(**kwargs)
    
    app = WxAsyncApp()
    
    if not apc.title:
        apc.title=apc.cfg['title']
    frame = MainFrame(title=apc.title)
    frame.Show()
    app.SetTopWindow(frame)
    loop = get_event_loop()
    loop.run_until_complete(app.MainLoop())
if __name__=="__main__":
    main()
    