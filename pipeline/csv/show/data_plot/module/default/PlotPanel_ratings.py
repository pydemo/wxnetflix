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
from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import wx
import seaborn as sns
import pandas as pd 
sns.set()

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
def cnt_col(df, col, new_col):
        df[new_col] = df[col].count()
        return df
def sum_col(df, col, new_col):
        df[new_col] = df[col].sum()
        return df        
class PlotPanel_ratings(wx.Panel, Base):
    def __init__(self, parent=None):
        super(PlotPanel_ratings, self).__init__(parent)
        self.ref= dict2(page=0, chunk=0, size=10)
        
        self.b_plot = b_plot=wx.Button(self, wx.ID_OK, label="Plot", size=(50, 25))
        b_plot.Bind(wx.EVT_BUTTON, self.onPlot)

            
        #button1 =  wx.Button(self, label="Async")

        sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(self.b_plot, 0,0,3)

        #h_sizer.Add(button1, 0,0,3)        
        h_sizer.Add((5,5), 1, wx.ALL|wx.EXPAND,1)        
        sizer.Add(h_sizer, 0,0,1)
        #sizer.Add(self.list_ctrl, 1, wx.ALL|wx.EXPAND, 1)
        #self.SetSizer(sizer)
        #AsyncBind(wx.EVT_BUTTON, self.async_download, button1)
        if 1:
            self.figure = Figure()
            self.axes = self.figure.add_subplot(111)
            self.canvas = FigureCanvas(self, -1, self.figure)
            if 0:
                self.tips = pd.read_csv('tips.csv')
                self.tips=self.tips.groupby("sex").apply(cnt_col, 'sex', 'sex_count')
                self.tips=self.tips.groupby("sex").apply(sum_col, 'tip', 'total_tips')
                pp(self.tips)
            if 1:
                self.data = pd.read_csv('in/netflix_titles_2021.csv')
                self.data=self.data.groupby("rating").apply(cnt_col, 'rating', 'rating_count')
                
            
            sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
            
            self.SetSizer(sizer)
            self.Fit()
            self.pid=0
        if 0:
        
            self.figure =fig= Figure()

            self.axx=[]
            if 1:
                self.ff = fig.subfigures(1, 2, wspace=0.07)
                
                for ff in self.ff:
                    self.axx.append(ff.add_subplot(111))
            if 0:
                self.data = pd.read_csv('tips.csv')
            else:
                self.data = pd.read_csv('in/netflix_titles_2021.csv')
                self.data=self.data.groupby("rating").apply(cnt_col, 'rating', 'rating_count')
            
            self.canvas = FigureCanvas(self, -1, self.figure)

            #self.tips=self.tips.groupby("sex").apply(cnt_col, 'sex', 'sex_count')
            #self.tips=self.tips.groupby("sex").apply(sum_col, 'tip', 'total_tips')
            #pp(self.tips)
            
            sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
            
            self.SetSizer(sizer)
            self.Fit()
            self.pid=0
            
    def hist_plot(self, data, color):
        
                

        sns.histplot(x=data["rating"], y=data["rating_count"], ax=self.axx[self.pid]).set(title=data['type'][data.index[0]])
        self.pid +=1
    def Plot (self):
        self.figure.set_canvas(self.canvas)
        

        if 0:
            for ax in self.axx:
                ax.cla()        
            g = sns.FacetGrid(self.data, col="type", height=2, aspect=.5)
            g.map_dataframe(self.hist_plot)
            
        if 1:
            self.axes.cla()
            g = sns.FacetGrid(self.data, hue="type")
            sns.scatterplot(
                data=self.data, x="rating_count", y="rating", hue="type", ax=self.axes
            ).set(title='Netflix')
            if 0:
                sns.scatterplot(
                    data=self.data, x="rating", y="rating_count", hue="type", ax=self.axes
                ).set(title='Netflix <2021')
            g.add_legend()
        self.canvas.draw()
        self.pid=0
    def onPlot(self,event):
        print('PlotPanel: Plot')
        if 0:
            self.send('Plot',())
        else:
            self.Plot()
        
 
    async def async_download(self, event):
        print('NavigationPanel: async_download') # self.slog 
        await asyncio.sleep(1)
        print('NavigationPanel: async_download')
        await asyncio.sleep(1)
        print('NavigationPanel: async_download')
        await asyncio.sleep(1)
        print('NavigationPanel: async_download')

