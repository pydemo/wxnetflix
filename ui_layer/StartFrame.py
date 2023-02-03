import wx
from ui_layer.common import * 
from ui_layer.utils import exception


from ui_layer.utils import ex
class StartFrame(wx.Frame):#, Base):
    @exception
    def __init__(self, parent, headless):
        wx.Frame.__init__(self, parent, size = START_SIZE, pos = START_POS)
        self.Show(False)
        
        #self.Freeze()
        
        if not headless:
            from ui_layer.DataFrame import DataFrame
            self.frame = frame= DataFrame(self, 'GH UI')

        #self.Thaw()

