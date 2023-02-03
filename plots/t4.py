import wx
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg 


def update(event):
    n=n_slider.GetValue()
    ax.clear()
    ax.plot(theta, 5*np.cos(n*theta))
    fig.canvas.draw()
def close(event):
    window.Close()

app = wx.App(redirect=False)
window = wx.Frame(None, -1, "Embedding with wxPython")
fig = Figure(figsize=(6, 5), dpi=100)
canvas = FigureCanvas(window, -1, fig)
toolbar = NavigationToolbar2WxAgg(canvas)
ax = fig.add_subplot(111,projection='polar')
theta = np.arange(0., 2., 1./180.)*np.pi
ax.plot(theta, 5*np.cos(3*theta))

n_slider = wx.Slider(window, wx.ID_ANY, 3, 3, 10, size=(250,20),
                     style=(wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | 
                            wx.SL_LABELS)) 
n_slider.Bind(wx.EVT_SCROLL, update)
myfont = wx.Font(12, wx.ROMAN, wx.ITALIC, wx.BOLD)
n_slider.SetFont(myfont)
button.SetFont(myfont)

window.SetInitialSize(wx.Size(int(fig.bbox.width), 
                      int(fig.bbox.height)))
                      
sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Insert(0, canvas, 1, wx.EXPAND | wx.ALL)
sizer.Insert(1, button, 0, wx.EXPAND)
sizer.Insert(2, n_slider, 0, wx.ALIGN_RIGHT)
sizer.Insert(3, toolbar, 0, wx.ALIGN_LEFT)


window.SetSizer(sizer)
window.Fit()
window.Show()



frame.Show()
app.MainLoop()


