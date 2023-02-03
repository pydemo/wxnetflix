# -*- coding: utf-8 -*- 
from __future__ import print_function
__author__ = "Olek B"
__copyright__ = "Copyright 2021"
__credits__ = []
__appname__='Redshift cli'
__license__ = ""
__title__ = "Redshift cli"
__version__ = "0.10000"
__maintainer__ = "Olek B"
__email__ = ""
__github__=	""
__status__ = "Development" 
import logging
import logging.config
logging.captureWarnings(True)
import decimal, datetime
import os,sys, time, csv
from os.path import join, isdir, split, basename

from cli_layer.utils import  cli_exception
from cli_layer.common import TMP_DIR

from pprint import pprint as pp

import cli_layer.config.app_config as app_config 
   
    
from cli_layer.utils import timer, get_module_loc, import_module, get_err, init_logging


log=init_logging()

import click
click.disable_unicode_literals_warning = True
e = sys.exit

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
@cli_exception
def main_cli(**kwargs):

    #pp(kwargs)
    
    mod_file = get_module_loc(**kwargs)
    #print(7777777777, mod_file)
    #e()
    if not apc.quiet:
        print('#'*80)
        log.info('Importing module: %s' % mod_file)
        print('#'*80)

    api = import_module(mod_file)
    #pp(kwargs)
    mname=kwargs['pipeline'].replace('\\','_').replace('/','_')
    method= getattr(api, mname)
    method(**kwargs)



@click.command()
@click.option('-l',  '--lame_duck', default = 0,	help = 'Limit', type=int, 	required=False )
@click.option('-nop','--num_of_params', default = None,	help="ParmsConfig", type=int, required=False)
@click.option('-r',  '--runtime',	default = 'DEV',help = 'Runtime.') # DEV/UAT/PROD
@click.option('-p',  '--pipeline',  default = None,	help = 'ETL pipeline name',	required=True )
@click.option('-pa', '--params', 	nargs=int(nop) if nop else 0, help="Pipeline params", type=str, required=False)
@click.option('-ld', '--lame_duck',	default = 0,  help="Import limit", type=int, required=False)
@click.option('-la', '--cli_layout', default='default',	 type=str, required=False, help="CLI layout.")
@click.option('-d' , '--debug',     is_flag=True, help="Print debug output.")
@click.option('-h' , '--help',      is_flag=True, help="Show usage.")
@click.option('-y' , '--yes',       is_flag=True, help="Force overwrite.")
@click.option('-q' , '--quiet',     is_flag=True, help="Quet mode.")
@click.option('-o' , '--open',      is_flag=True, help="Open pipeline file and exit.")


@timer (bnf)
def main(**kwargs):
    global log, apc
    #e()
    if 1:
        app_config.init(**kwargs)
        apc = app_config.apc
        apc.validate().load()
    if kwargs['open']:
        from ui_layer.common import open_editor
        from cli_layer.utils import get_module_loc
        ppl = kwargs['pipeline']
        mfn= get_module_loc(**kwargs)
        
        open_editor(mfn)
    else:
        #headless
        main_cli(**kwargs)

if __name__ == "__main__":
    main()