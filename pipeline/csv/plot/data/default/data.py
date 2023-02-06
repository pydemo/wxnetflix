#generate.trigger.bat
import os, sys, csv, time, logging
import datetime as dt
from  datetime import datetime
import decimal
from os.path import split, join, isdir, basename, isfile
from pprint import pprint as pp
from cli_layer.utils import timer, get_err, load_pipeline_module
from pathlib import Path
from cli_layer.common import *
from cli_layer.fmt import  pfmt, pfmtv, pfmtd, psql
e=sys.exit

import cli_layer.config.app_config as app_config
apc = app_config.apc


import cli_layer.config.app_config as app_config
apc = app_config.apc

log = logging.getLogger()


@timer (basename(__file__))
def csv_show_data(**kwargs):

	env, cfg = apc.env, apc.cfg
	apc.setParams(**kwargs)
	cp, params=apc.cp, apc.params
	
	config,file_name = params
	assert config
	assert isfile(config),f'Could not locate config "{config}"'
	assert file_name

	return 0
if __name__=="__main__":
	kwargs={'cli_layout': 'default',
	 'debug': False,
	 'help': False,
	 'lame_duck': 0,
	 'num_of_params': 2,
	 'open': False,
	 'params': ('config.yaml', 'site_intelligence.ob_ct_sdl_union_1'),
	 'pipeline': 'generate\\trigger\\update',
	 'quiet': False,
	 'runtime': 'DEV',
	 'yes': False}
	generate_trigger_update(**kwargs)

	