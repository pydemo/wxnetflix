import wx
import wx.lib.newevent

from ui_layer.log_init import log
from ui_layer.Base import Base
from pprint import pprint as pp

APP_EXIT = 1

	
#---------------------------------------------------------------------------
class DataMenu( Base):
	def __init__(self, parent):
		global frame
		frame=parent
		Base.__init__(self)
		
	def CreateMenu(self):
		global mb
		mb = wx.MenuBar()
		
		if 1:
			menu = wx.Menu()
		
			if 1:
				item = wx.MenuItem(menu, APP_EXIT, '&Quit\tCtrl+Q')
				menu.Append(item)
				frame.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)

			if 1:			
				id=wx.NewIdRef()
				item = wx.MenuItem(menu, id, '&Save\tCtrl+S')
				menu.Append(item)
				frame.Bind(wx.EVT_MENU, self.OnSave, id=id)
			if 1:			
				id=wx.NewIdRef()
				item = wx.MenuItem(menu, id, '&Delete\tCtrl+D')
				menu.Append(item)
				frame.Bind(wx.EVT_MENU, self.OnDelete, id=id)
			if 1:			
				id=wx.NewIdRef()
				item = wx.MenuItem(menu, id, '&New\tCtrl+N')
				menu.Append(item)
				frame.Bind(wx.EVT_MENU, self.OnNew, id=id)
			if 1:			
				id=wx.NewIdRef()
				item = wx.MenuItem(menu, id, '&Open in Explorer\tCtrl+X')
				menu.Append(item)
				frame.Bind(wx.EVT_MENU, self.OnExplorer, id=id)
				
				
			mb.Append(menu, '&File')
			
		if 1:
			menu = wx.Menu()
		
			if 1:			
				id=wx.NewIdRef()

				item = wx.MenuItem(menu, id, '&Edit\tCtrl+E')
				menu.Append(item)
				frame.Bind(wx.EVT_MENU, self.OnEdit, id=id)

			mb.Append(menu, '&Edit')
			
		if 1:
			menu = wx.Menu()
			if 1:
				item = menu.Append(-1, "&Widget Inspector\tF6", "Show the wxPython Widget Inspection Tool")
				frame.Bind(wx.EVT_MENU, self.OnWidgetInspector, item)
			mb.Append(menu, '&Tools')
			

			
		
		return mb
	def OnQuit(self, e):
		frame.Close()
	
	def OnSave(self, e):
		log.info('OnSave')
		self.send("onSave", 'test')
	def OnDelete(self, e):
		log.info('OnDelete')		
		fc=wx.Window.FindFocus().GetParent()
		self.send('Ctrl_D',fc)
		
		#e.Skip()
		
	def OnEdit(self, e):
		log.info('OnEdit')
		fc=wx.Window.FindFocus().GetParent()
		for fn in fc.GetPaths():
			self.send('editFile', (fn, 0))
	def OnExplorer(self, e):
		log.info('OnExplorer')
		self.send('onExplorer', wx.Window.FindFocus())
		
			
	def OnNew(self, e):
		log.info('OnNew')
		#fc=wx.Window.FindFocus().GetParent()
		self.send('newFile', wx.Window.FindFocus())


	def OnExitApp(self, evt):
		frame.Close(True)

	def OnWidgetInspector(self, evt):
		wx.lib.inspection.InspectionTool().Show()
		#---------------------------------------------------------------------------