import wx
from pprint import pprint as pp
from ui_layer.utils import exception, load_pipeline_module
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic
if 0:
	#import pipeline.s3.view.module.list_s3_objects_searcheable_2_scan.config.scan_config as scan_config
	scan_config        = load_pipeline_module(uic, 'config/scan_config')

	scan_config.init(**uic.kwargs)
	scfg = scan_config.scfg




Controller        = load_pipeline_module(uic, 'Controller/TemplateTypePanel_Controller')


#----------------------------------------------------------------------
class TemplateType:
	""""""
	def __init__(self,id, type, prefix):
		""""""
		self.id      =id
		self.type = type
		self.prefix=prefix
	def getPrefix(self):
		return self.prefix
	def __str__(self):
		return self.type
		
		
#---------------------------------------------------------------------------
class TemplateTypePanel(wx.Panel, Controller):
	def __init__(self, parent):
		super(TemplateTypePanel, self).__init__(parent)

		self.keys=keys = {
				'Static' : TemplateType(0, 'Static','s_'),
				'Dynamic': TemplateType(1, 'Dynamic','d_')
				}

		tmpl = list(keys.keys())
		
		self.rbox = wx.RadioBox(self, label = '', choices = tmpl, majorDimension = 1, style =wx.NO_BORDER|wx.RA_SPECIFY_ROWS) #size=(150, 40), 
		#self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox) 
		self.widgetMaker(self.rbox)
		#self.tc = wx.TextCtrl(self, -1, '', size=(70,-1))

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.rbox, 1, wx.ALL, 3)


		self.SetSizer(sizer)

	def widgetMaker(self, widget):
		""""""
		widget.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
		self.send('changeTemplate', self.keys['Static'])


