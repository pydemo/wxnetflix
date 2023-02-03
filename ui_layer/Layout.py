import os, sys
from ui_layer.utils import  dict2
from ui_layer.common import home, load_config

e=sys.exit





class  Layout(object): 
	def __init__(self, layout_loc):
		global cfg
		self.layout_loc=layout_loc
		self.layout_fn=os.path.basename(layout_loc)
		self.layout_name = os.path.splitext(self.layout_fn)[0]
		self.cfg = cfg = load_config(config_path = layout_loc)
		
	def get(self, key, default = None):
		return cfg.get(key, default)
		
	def items(self, pref=None):
		for key, val in cfg.items():
			print(key)
			yield (key, val)


