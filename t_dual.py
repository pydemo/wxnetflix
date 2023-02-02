if 0 :
    from PyQt4 import QtGui, QtCore
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure

import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


import sys
import seaborn as sns

tips = sns.load_dataset("tips")

class MainWindow(wx.Frame):


    def __init__(self):
        wx.Frame.__init__(self, None, wx.NewId(), "Main") 
        self.sizer =sizer= wx.BoxSizer(wx.VERTICAL)

        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122, sharex=self.ax1, sharey=self.ax1)
        self.axes=[self.ax1, self.ax2]
        self.canvas = FigureCanvas(self, -1,self.fig)
        if 0:
            self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding, 
                                      QtGui.QSizePolicy.Expanding)
            self.canvas.updateGeometry()
        self.myb = wx.StaticBox(self,-1,label="Employee Detail:-",pos=(1,1),size=(380,98))
        self.dropdown1 = wx.ComboBox(self.myb)
        self.dropdown1.Append(["sex", "time", "smoker"])
        self.myb2 = wx.StaticBox(self,-1,label="Employee Detail:-",pos=(1,1),size=(380,98))
        self.dropdown2 = wx.ComboBox(self.myb2)
        self.dropdown2.Append(["sex", "time", "smoker", "day"])
        #self.dropdown2.setCurrentIndex(2)

        #self.dropdown1.currentIndexChanged.connect(self.update)
        #self.dropdown2.currentIndexChanged.connect(self.update)
        #self.label = wx.Label("A plot:")

        sizer.Add(wx.StaticText(self, -1,"Select category for subplots"))
        sizer.Add(self.dropdown1)
        sizer.Add(wx.StaticText(self, -1,"Select category for markers"))
        sizer.Add(self.dropdown2)

        sizer.Add(self.canvas)

        self.Layout()


    def update(self):

        colors=["b", "r", "g", "y", "k", "c"]
        self.ax1.clear()
        self.ax2.clear()
        cat1 = self.dropdown1.currentText()
        cat2 = self.dropdown2.currentText()
        print (cat1, cat2)

        for i, value in enumerate(tips[cat1].unique().get_values()):
            #print "value ", value
            df = tips.loc[tips[cat1] == value]
            self.axes[i].set_title(cat1 + ": " + value)
            for j, value2 in enumerate(df[cat2].unique().get_values()):
                #print "value2 ", value2
                df.loc[ tips[cat2] == value2 ].plot(kind="scatter", x="total_bill", y="tip", 
                                                ax=self.axes[i], c=colors[j], label=value2)
        self.axes[i].legend()   
        self.fig.canvas.draw_idle()


class MyApp(wx.App):
    def OnInit(self):
        frame = MainWindow()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop() 