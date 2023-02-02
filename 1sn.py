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
class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        #self.nf = pd.read_csv('netflix_titles_2021.csv')
        #sns.heatmap(self.nf.isnull())
        #self.tips = sns.load_dataset("tips")
        self.tips = pd.read_csv('tips.csv')
        print(self.tips)

    def draw(self):
        if 0:
            t = arange(0.0, 3.0, 0.01)
            s = sin(2 * pi * t)
            self.axes.plot(t, s)
            
        if 1:
            self.axes.cla()
            #sns.heatmap(self.nf.isnull(), ax=self.axes)
            g = sns.FacetGrid(self.tips, col="day", height=4, aspect=.5)
            g.map(sns.barplot, "sex", "total_bill", order=["Male", "Female"], ax=self.axes)
            self.axes.plot()
            self.canvas.draw()



if __name__ == "__main__":
    app = wx.PySimpleApp()
    fr = wx.Frame(None, title='test')
    panel = CanvasPanel(fr)
    panel.draw()
    fr.Show()
    app.MainLoop()