import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class MainFrame(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, wx.NewId(), "Main") 
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.figure = Figure(figsize=(1,2))
        self.axe = self.figure.add_subplot(111)
        self.figurecanvas = FigureCanvas(self, -1, self.figure)
        self.valueCtrl = wx.TextCtrl(self, -1, "")
        self.buttonPlot = wx.Button(self, wx.NewId(), "Plot")
        self.sizer.Add(self.figurecanvas, proportion=1, border=5,
                       flag=wx.ALL | wx.EXPAND)
        self.sizer.Add(self.buttonPlot, proportion=0, border=2, flag=wx.ALL)
        self.sizer.Add(self.valueCtrl, proportion=0, border=2, flag=wx.ALL)
        self.SetSizer(self.sizer)
        self.buttonPlot.Bind(wx.EVT_BUTTON, self.on_button_plot)

    def on_button_plot(self, evt):
        self.figure.set_canvas(self.figurecanvas)
        self.axe.clear()
        self.axe.plot(range(int(self.valueCtrl.GetValue())), color='green')
        self.figurecanvas.draw()

class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop() 