import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
from asyncio.events import get_event_loop
import time
import wx.lib.newevent
SomeNewEvent, EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
SomeNewEventAsync, EVT_SOME_NEW_EVENT_ASYNC = wx.lib.newevent.NewEvent()

import ui_layer.config.ui_config as ui_config
uic = ui_config.uic

from ui_layer.Base import reciever, Base

#from  ui_layer.TestSubPanel_3 import TestSubPanel
from ui_layer.utils import exception, load_pipeline_module
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic
MainPanel= load_pipeline_module(uic, 'MainPanel')

from ui_layer.module.controller.LoaderPanel_Controller import LoaderPanel_Controller as Controller

class LoaderPanel(wx.Panel, Controller):
	def __init__(self, parent=None):
		super(LoaderPanel, self).__init__(parent)

		if 1:
			vbox = wx.BoxSizer(wx.VERTICAL)
			
			panel = MainPanel(parent=self)
			
		if 1:
			self.flog = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, (-1,130),
									  wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE)
			self.flog.Hide()
		if 1:
			self.nlog = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, (-1,130),
									  wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE)
			self.nlog.Hide()
		vbox.Add(panel, 1, wx.EXPAND|wx.ALL)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.flog, 1, wx.EXPAND)
		hbox.Add(self.nlog, 1, wx.EXPAND)
		vbox.Add(hbox, 0, wx.EXPAND)
		self.SetSizer(vbox)
		self.Layout()
		self.sub('navlog')
		self.sub('filterlog')


