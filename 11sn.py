'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

fake = pd.DataFrame({'cat': ['red', 'green', 'blue'], 'val': [1, 2, 3]})
ax = sns.barplot(x = 'val', y = 'cat', 
              data = fake, 
              color = 'black')
ax.set(xlabel='common xlabel', ylabel='common ylabel')
plt.show()
'''
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
        if 0:
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
            self.SetSizer(self.sizer)
            self.Fit()
        #self.nf = pd.read_csv('netflix_titles_2021.csv')
        #sns.heatmap(self.nf.isnull())
        #self.tips = sns.load_dataset("tips")
        self.tips = pd.read_csv('tips.csv')
        #print(self.tips)
        self.button = wx.Button(self, label="Plot data", pos=(100,15))
        self.button.Bind(wx.EVT_BUTTON, self.OnButtonClick)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.button, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.pid=0
        
    def OnButtonClick(self,event):
        #sns.set()
        self.figure.set_canvas(self.canvas)
        self.axes.cla()
        print(123)
        if 0:
            t = arange(0.0, 3.0, 0.01)
            s = sin(2 * pi * t)
            self.axes.plot(t, s)
            
        if 0:
            
            #sns.heatmap(self.nf.isnull(), ax=self.axes)
            g = sns.FacetGrid(self.tips, col="day", height=4, aspect=.5)
            g.map(sns.barplot, "sex", "total_bill", order=["Male", "Female"], ax=self.axes)
            self.axes.plot()
        if 0:
            pal = dict(Lunch="seagreen", Dinner=".7")
            g = sns.FacetGrid(self.tips, hue="time", palette=pal, height=5)
            #g.add_legend()
            sns.scatterplot(x=self.tips["total_bill"],y=self.tips[ "tip"], alpha=.5, ax=self.axes).set(title='My sustom title')
            #g.map(sns.scatterplot, "total_bill", "tip", s=100, alpha=.5, ax=[self.axes])
            g.add_legend()
            sns.set_title('My sustom title')
            self.canvas.draw()
        if 1:
            g = sns.FacetGrid(self.tips, hue="time")
            sns.scatterplot(
                data=self.tips, x="total_bill", y="tip", hue="size", ax=self.axes
            ).set(title='My sustom title')
            g.add_legend()
            self.canvas.draw()


if __name__ == "__main__":
    app = wx.PySimpleApp()
    fr = wx.Frame(None, title='test')
    panel = CanvasPanel(fr)
    #panel.draw()
    fr.Show()
    app.MainLoop()