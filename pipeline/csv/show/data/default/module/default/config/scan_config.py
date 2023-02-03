import sys
from pprint import pprint as pp
if 0:
    import ui_layer.config.ui_config as ui_config
    uic = ui_config.uic
e=sys.exit
#Controller        = load_pipeline_module(uic, 'config/ScanPanel_Controller')

#from ui_layer.ScanConfig import ScanConfig
from ui_layer.UiConfig import UiConfig

def init(**kwargs):
    global scfg
    kwargs['config_prefix'] = 'SCAN_URLS'
    scfg = UiConfig(**kwargs)