import wx
from ui_layer.utils import exception, load_pipeline_module
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic
if 0:
	#import pipeline.s3.view.module.list_s3_objects_searcheable_2_scan.config.scan_config as scan_config
	scan_config        = load_pipeline_module(uic, 'config/scan_config')

	scan_config.init(**uic.kwargs)
	scfg = scan_config.scfg




Controller        = load_pipeline_module(uic, 'Controller/SearchTablePanel_Controller')


#----------------------------------------------------------------------
class TableFilter:
	""""""
	def __init__(self,id, schema, table,  dbenv):
		""""""
		self.id      =id
		self.schema = schema
		self.table  = table
		self.dbenv = dbenv
		
	def getUrl(self):
		return f'{self.dbenv.upper()}: {self.schema}.{self.table}'
		
		
#---------------------------------------------------------------------------
class SearchTablePanel(wx.Panel, Controller):
	def __init__(self, parent):
		super(SearchTablePanel, self).__init__(parent)

		self.keys=keys = [
				TableFilter(0, '*', '*',   		 'DEV'),
				TableFilter(1, 'site_intelligence','ob_sdl_audit', 'DEV'),
				TableFilter(2, 'site_intelligence', 'ob_sdl_audit*','DEV'),
				]

		sampleList = []

		self.cb = wx.ComboBox(self, size=wx.DefaultSize, choices=sampleList)

		self.widgetMaker(self.cb, keys)
		#self.tc = wx.TextCtrl(self, -1, '', size=(70,-1))

		self.bsc = wx.Button(self, -1, 'Refresh')
		#print(self.cb.GetSize())
		self.cb.SetValue(self.keys[0].getUrl())
		x,y=self.cb.GetSize()
		self.cb.SetSize((x+150,y))
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.cb, 0, wx.ALL, 3)
		#sizer.Add(self.tc, 0, wx.ALL, 3)
		sizer.Add(self.bsc, 0, wx.ALL, 3)

		self.SetSizer(sizer)
		self.Bind(wx.EVT_BUTTON, self.onScan, self.bsc)
		self.changed = False

	def widgetMaker(self, widget, objects):
		""""""
		for obj in objects:
			widget.Append(obj.getUrl(), obj)
		widget.Bind(wx.EVT_COMBOBOX, self.onSelect)
		widget.Bind(wx.EVT_KEY_UP, self.OnKeyUP)

