import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
from asyncio.events import get_event_loop
import sys, time
import wx.lib.newevent
SomeNewEvent, EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
SomeNewEventAsync, EVT_SOME_NEW_EVENT_ASYNC = wx.lib.newevent.NewEvent()
from pprint import pprint as pp
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic

from ui_layer.Base import reciever, Base


from ui_layer.utils import exception, load_pipeline_module
from pathlib import Path
import cli_layer.aws_pipeline_utils  as APU
import cli_layer.s3_utils  as S3U
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic
#Main_Searcheable_ListPanel= load_pipeline_module(uic, 'Main_Searcheable_ListPanel')

e=sys.exit
class dict2(dict):                                                              

    def __init__(self, **kwargs):                                               
        super(dict2, self).__init__(kwargs)                                     

    def __setattr__(self, key, value):                                          
        self[key] = value                                                       

    def __dir__(self):                                                          
        return self.keys()                                                      

    def __getattr__(self, key):                                                 
        try:                                                                    
            return self[key]                                                    
        except KeyError:                                                        
            raise AttributeError(key)                                           

    def __setstate__(self, state):                                              
        pass 

class NavigationPanel(wx.Panel, Base):
    def __init__(self, parent=None):
        super(NavigationPanel, self).__init__(parent)
        self.ref= dict2(page=0, chunk=0, size=10)
        
        self.b_first = b_first=wx.Button(self, wx.ID_OK, label="First", size=(50, 25))
        b_first.Bind(wx.EVT_BUTTON, self.onFirstPage)
        self.b_prev = b_prev=wx.Button(self, wx.ID_OK, label="Prev", size=(50, 25))
        b_prev.Bind(wx.EVT_BUTTON, self.onPrevPage)
        self.b_next = b_next=wx.Button(self, wx.ID_OK, label="Next", size=(50, 25))
        b_next.Bind(wx.EVT_BUTTON, self.onNextPage)
        self.b_last = b_last=wx.Button(self, wx.ID_OK, label="Last", size=(50, 25))
        b_last.Bind(wx.EVT_BUTTON, self.onLastPage)
        if 0:
            self.b_order = b_order=wx.Button(self, wx.ID_OK, label="Order", size=(50, 30))
            b_order.Bind(wx.EVT_BUTTON, self.onOrder)
            self.b_download = b_download=wx.Button(self, wx.ID_OK, label="Download", size=(50, 30))
            b_download.Bind(wx.EVT_BUTTON, self.onDownload)
            
        button1 =  wx.Button(self, label="Async")
  
        
        #self.list_ctrl = Main_Searcheable_ListPanel(parent=self)


        sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(self.b_first, 0,0,3)
        h_sizer.Add(self.b_prev, 0,0,3)
        h_sizer.Add(self.b_next, 0,0,3)
        h_sizer.Add(self.b_last, 0,0,3)
        if 0:
            h_sizer.Add((25,5), 0,0,3)
            h_sizer.Add(self.b_order, 0,0,3)
            h_sizer.Add((25,5), 0,0,3)
            h_sizer.Add(self.b_download, 0,0,3)        
            h_sizer.Add((5,5), 1, wx.ALL|wx.EXPAND,1)
        h_sizer.Add(button1, 0,0,3)        
        h_sizer.Add((5,5), 1, wx.ALL|wx.EXPAND,1)        
        sizer.Add(h_sizer, 0,0,1)
        #sizer.Add(self.list_ctrl, 1, wx.ALL|wx.EXPAND, 1)
        self.SetSizer(sizer)
        AsyncBind(wx.EVT_BUTTON, self.async_download, button1)
        self.b_last.Enable(False)
    def onDownload(self,event):
        self.slog('NavigationPanel: onDownload')
        self.send('downloadChunk',())        
    def onFirstPage(self,event):
        self.slog('NavigationPanel: First')
        self.send('firstPage',())
    def onOrder(self,event):
        self.slog('NavigationPanel: Order')
        self.send('onOrder',())
        
    def onPrevPage(self,event):
        self.slog('NavigationPanel: Prev')
        self.send('prevPage',())
    def onNextPage(self,event):
        self.slog('NavigationPanel: Next')
        self.send('nextPage',())
        
    def onLastPage(self,event):
        self.slog('NavigationPanel: Last')
        r = wx.MessageDialog(
            None,
            'Fetch full file list?' ,
            'Confirm last page retrieval',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        ).ShowModal()

        if r != wx.ID_YES:
            return
            
        self.send('lastPage',())  
    async def async_download(self, event):
        self.slog ('NavigationPanel: async_download')
        await asyncio.sleep(1)
        self.slog ('NavigationPanel: async_download')
        await asyncio.sleep(1)
        self.slog ('NavigationPanel: async_download')
        await asyncio.sleep(1)
        self.slog ('NavigationPanel: async_download')

