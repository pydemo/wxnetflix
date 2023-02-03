from numpy import arange, sin, pi
import matplotlib
from pprint import pprint as pp
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import wx
import seaborn as sns
import numpy as np
import pandas as pd
#sns.set()




class SamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure =fig= Figure()

        self.axx=[]
        if 1:
            self.ff = fig.subfigures(1, 2, wspace=0.07)
            
            for ff in self.ff:
                self.axx.append(ff.add_subplot(111))
        #self.ax = self.figure.add_subplot(111)
        if 0:
            self.x = np.array(list('XYZV'))
            self.y = np.array([200,400,300,20])
        self.tips = pd.read_csv('tips.csv')
        #self.axx[0].set_ylabel("Sample numbers")
        

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.button = wx.Button(self, label="Plot data", pos=(100,15))
        self.button.Bind(wx.EVT_BUTTON, self.OnButtonClick)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.button, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.pid=0
    def plot_heatmap(self, data, color):
        #sns.heatmap(data[["Home", "Away"]])  
        #print(data)        
        #sns.barplot(data[["sex", "total_bill"]],  ax=self.axx[self.pid], order=["sex"])
        order_list = ["Male", "Female"]
        sns.barplot(x=data['sex'], y=data['tip'],  order=order_list, ax=self.axx[self.pid]).set(title=data['day'][data.index[0]])
        #print(data['day'][data.index[0]])
        #self.axx[self.pid].set(xlabel="Sex", ylabel='Tips')
        #ax.set_ylabel(df.columns[i])
        #print(self.pid)
        self.pid +=1
        
        #data.index = pd.to_datetime(data["day"])
        #data[["sex", "total_bill"]].plot(kind="area", ax=self.ax)
    def hist_plot(self, data, color):
        
                

        sns.histplot(data["tip"], ax=self.axx[self.pid]).set(title=data['time'][data.index[0]])
        self.pid +=1
            
            
        
        #data.index = pd.to_datetime(data["day"])
        #data[["sex", "total_bill"]].plot(kind="area", ax=self.ax)
    def OnButtonClick(self,event):
        #sns.set()
        self.figure.set_canvas(self.canvas)
        if 0:
            sns.barplot(self.tips, palette="BuGn_d", ax=self.ax)
        if 0:
            g = sns.FacetGrid(self.tips, col="day", height=2, aspect=.5)
            g.map_dataframe(self.plot_heatmap)
            g.set_axis_labels("Total bill (US Dollars)", "Tip")

        if 1:
            g = sns.FacetGrid(self.tips, col="time", height=2, aspect=.5)
            g.map_dataframe(self.hist_plot)

        if 0:
            g = sns.FacetGrid(self.tips, col="day", height=4, aspect=.5)
            g.map(sns.barplot, "sex", "total_bill", order=["Male", "Female"], ax=self.axx)
            g.set_axis_labels("Total bill (US Dollars)", "Tip")
            #self.canvas.draw()
        if 0:
            with sns.axes_style("white"):
                g = sns.FacetGrid(self.tips, row="sex", col="smoker", margin_titles=True, height=2.5)
            g.map(sns.scatterplot, "total_bill", "tip", color="#334488",ax=self.ax)
            g.set_axis_labels("Total bill (US Dollars)", "Tip")
            g.set(xticks=[10, 30, 50], yticks=[2, 6, 10])
            g.figure.subplots_adjust(wspace=.02, hspace=.02)
            for ax in g.axes_dict.values():
                ax.plot()
        if 0:
             

            tips = sns.load_dataset('tips')
            ordered_days = sorted(tips['day'].unique())
            g = sns.FacetGrid(tips,col='day',col_order=ordered_days,col_wrap=2)
            #                                               change this to 4 ^
            g.map(sns.boxplot,'sex','total_bill',order=["Male", "Female"],palette='muted', ax=self.ax)
            for ax in g.axes.flatten(): 
                ax.tick_params(labelbottom=True)
            #plt.tight_layout()
            #plt.show()
        
        self.canvas.draw()
        #pp(g.axes_dict)

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = wx.Frame(None, title='Sample bar plot')
    panel = SamplePanel(frame)
    frame.Show()
    
    app.MainLoop()