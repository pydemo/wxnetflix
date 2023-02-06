import os, sys, json, codecs, shutil
from datetime import datetime

from os.path import join, isdir
from os.path import isfile, isdir, join, basename
from pprint import pprint as pp


from cli_layer.common import TMP_DIR, PIPELINE_DIR

e=sys.exit

env= os.environ.get('ZZZ_NETFLIX_PLOTTER_ENV')
assert env in ['DEV','QA','PROD'], 'Undefined env: "set ZZZ_NETFLIX_PLOTTER_ENV=DEV"'


def qprint(*args, **kwargs):
	global quiet
	if not quiet: print(*args, file=sys.stderr, **kwargs)
class Config(object): 

	def __init__(self, **kwargs):
		global env
		self.setCfg(**kwargs)
		self.cfg_root = cfg_root= self.getCfgRoot()		
		if not isdir(cfg_root): os.makedirs(cfg_root)

		self.root= self.getRoot()
		self.env=env
		self.pipeline     = pipeline = kwargs['pipeline'].strip()
		if '\\' in pipeline:
			self.dotted_pipeline=pipeline.replace('\\','.')
		else:
			self.dotted_pipeline=pipeline.replace('/','.')
		
		
		self.pipeline_dir = join(PIPELINE_DIR, self.dotted_pipeline.replace('.', os.sep))
		self.home=None
		self.lame_duck=0 # import limit        
	def getConfigName(self):
		return self.config_name
	def getRoot(self):
		return os.getcwd()
	def getBuildRoot(self):
		return join(os.getcwd(), '_build')
	def getTemplateRoot(self):
		return join(self.getBuildRoot(), '_template')		
	def getCfgRoot(self):
		return join(TMP_DIR,'cli_config')
		
	def setCfg(self,**kwargs):
		if kwargs.get('quiet'):
			self.quietOn() 
		else:
			self.quietOff()

		
	def getToolsRoot(self):
		return join(self.getRoot(), 'tools')
		
	def LoadConfig(self, config_path, quiet=False):
		out =None
		if config_path.endswith('.json'):
			out = self.jLoadConfig(config_path=config_path, quiet=quiet)
		elif self.apc_path.endswith('.yml'):
			out = self.yLoadConfig(config_path=config_path, quiet=quiet)
		else:
			raise Exception(f'Uknown config exception: "{config_path}"')
		assert out
		return out
	def jLoadConfig(self, config_path, quiet=False):
		if not quiet:
			print('-'*80)
			print('Loading json config: %s' % config_path)
		
		with codecs.open(config_path, encoding="utf-8") as stream:
			data=stream.read()
			cfg = json.loads(data)
		from cli_layer.utils import d2d2
		out =d2d2(cfg)
		if not quiet:
			print('-'*80)
		return out
		
	def yLoadConfig(self, config_path, quiet=False):
		if not quiet:
			print('-'*80)
			print('Loading yaml config: %s' % config_path)
		
		
		import yaml

		with open(config_path, "r") as stream:
			try:
				cfg=yaml.safe_load(stream)
			except yaml.YAMLError as exc:
				print(exc)
				raise
		from cli_layer.utils import d2d2
		out =d2d2(cfg)
		if not quiet:
			print('-'*80)
		return out
		
	def quietOn(self):
		global quiet
		self.quiet=quiet=True
	def quietOff(self):
		global quiet
		self.quiet=quiet=False
		
	def getHome(self):
		home=self.home
		assert home
		assert isdir(home)
		return home
		
		  

	def saveConfig(self):
		
		#assert hasattr(self, 'cfg')
		assert isfile(self.apc_path)
		
		with open(self.apc_path, 'w') as fp:
			dump = json.dumps(self.cfg, indent='\t', separators=(',', ': '))
		   
			new_data= re.sub('"\n[\t]+},', '"},', dump)

			fp.write(dump)
	def initCfgFile(self,path):
		
		ts='{:%Y%b%d_%H%M%S_%f}'.format(datetime.now())
		if not isfile(path):
			if 0:
				print(111, path)
				base_cfg_loc=join('config_layer', f'app_config.{self.env}.json')
				assert isfile(base_cfg_loc),base_cfg_loc

				shutil.copyfile(base_cfg_loc,path)
				
			with open(path,'w') as fh:
				fh.write('{"ts":"%s"}' % ts)
	def load(self, quiet=False):

		if not quiet: 
			print(self.apc_path)

		self.cfg = self.LoadConfig(config_path=self.apc_path, quiet=quiet)

		assert self.cfg is not None, self.cfg
		
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
		assert isfile(self.apc_path), 'App config JSON file does not exists for app "%s"\n%s' % (self.app_name,self.apc_path)
		
		return self

	
	def createConfigRoot(self):
		if not os.path.isdir(self.cfg_root):
			os.makedirs(self.cfg_root, exist_ok=True)
		return self



	def validate(self):
		if not  os.path.isdir(self.cfg_root):
			raise Exception('Cfg root does not exists at " %s "' % ( self.cfg_root))
		if not isfile(self.apc_path):
			print('ERROR: App config does not exists at \n%s' % self.apc_path)
			
		return self


	def getAppName(self, layout_loc=None):
		if not layout_loc: return self.app_name
		else:
			return os.path.splitext(os.path.basename(layout_loc))[0]

			
		
		

		