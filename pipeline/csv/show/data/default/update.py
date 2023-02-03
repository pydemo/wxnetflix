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
from pipeline.generate.utils import get_col_list
import cli_layer.config.app_config as app_config
apc = app_config.apc
#import cli_layer.pipeline.generate.utils as ppl_utils
#from cli_layer.pipeline.utils import get_params
import psycopg2

import cli_layer.config.app_config as app_config
apc = app_config.apc

log = logging.getLogger()


@timer (basename(__file__))
def generate_trigger_update(**kwargs):

	env, cfg = apc.env, apc.cfg
	apc.setParams(**kwargs)
	cp, params=apc.cp, apc.params
	
	config,table_name, out_dir = params
	out_dir = out_dir.strip("'").replace('/', os.sep).replace('\\', os.sep)
	if "{" in out_dir:
		out_loc=eval(f"f'''{out_dir}'''")
	else:
		out_loc=out_dir
	if not isdir(out_loc):
		os.makedirs(out_loc)
	assert config
	assert isfile(config),f'Could not locate config "{config}"'
	assert table_name
	assert table_name.count('.') ==1, 'Provide table_name as SCHEMA.TABLE'
	
	tbl_schema_name, base_table_name = table_name.split('.')
	assert tbl_schema_name
	assert base_table_name
	if 0:
		import yaml

		with open(config, "r") as stream:
			try:
				cfg=yaml.safe_load(stream)
			except yaml.YAMLError as exc:
				print(exc)
				raise
		
		env = os.environ.get('ZZZ_GENERATOR_ENV')
		
		assert env in ['DEV', 'UAT', 'PROD']
		assert env in cfg, f'Generator env "{env}" is not defined in config "{config}"'
	gcfg=cfg[env]
	assert 'audit_table' in gcfg, f' "audit_table"is not set in Generator env "{env}"'
	audit_table = gcfg['audit_table']
	assert audit_table.count('.') ==1, 'Provide "audit_name" in config.yaml as SCHEMA.TABLE'
	
	aud_schema_name, base_audit_table = audit_table.split('.')
	assert aud_schema_name
	assert base_audit_table
	
	#e()
	
	if 1:

		col_list = get_col_list()
		update_if_list=[]
					
		for d in col_list:
			col_name, =d

			update_if_list.append(f'''--{col_name}
		if(OLD.{col_name} <> OLD.{col_name}) then 
			INSERT INTO {audit_table} 			
			SELECT event_id, '{table_name}', _row_id,  '{col_name}', old.{col_name}, new.{col_name}, new.modified_by, now(), 'UPDATE';
		end if;''')
		update_if_list = ''.join(update_if_list)
		#psql(update_if_list)
	if 1:
		
		tmpl_dir = join('pipeline','generate','trigger','_template')
		assert isdir(tmpl_dir),  tmpl_dir
		tmplo = apc.tmpl
		prefix = tmplo.getPrefix()
		tfn = f'{prefix}update_trigger.tmpl'
		tmpl_fn = join(tmpl_dir,tfn)
		assert isfile(tmpl_fn),  tmpl_fn
		with open(tmpl_fn, 'r') as fh:
			tmpl = fh.read()
		#pp(tmpl)
		
		trigger_name = f'ob_audit_update_trigger_{base_table_name}'

		func_name    = f'{tbl_schema_name}.ob_process_audit_{base_table_name}_update'
		sequence_name= f'{tbl_schema_name}.ob_sdl_audit_event_seq'
		tt=eval(f"f'''{tmpl}'''")
		#print(tt)
		out_log_dir = join('out', table_name.upper())
		if not isdir(out_log_dir):
			os.makedirs(out_log_dir)
		if 1:
			ts = datetime.now().strftime("%Y%m%d_%I%M%S_%p")
			#print(ts)
			out_fn = join(out_log_dir, f'{prefix}UPDATE_trigger.{table_name.upper()}.{ts}.sql')
			
			with open(out_fn, 'w') as fh:
				fh.write(tt)
			psql(out_fn, 'Update file name')
			assert isfile(out_fn)
		if 1:			
			
			out_fn = join(out_loc,f'{prefix}UPDATE_trigger.{table_name.upper()}.sql')
			if isfile(out_fn):
				os.remove(out_fn)
			with open(out_fn, 'w') as fh:
				fh.write(tt)
			psql(out_fn, 'Latest Update file name')
			assert isfile(out_fn)		
		with open(out_fn, 'w') as fh:
			fh.write(tt)
	return out_fn
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

	