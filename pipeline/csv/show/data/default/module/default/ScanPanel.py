import wx
from ui_layer.utils import exception, load_pipeline_module
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic

import pipeline.s3.view.module.list_s3_objects_searcheable_2_scan.config.scan_config as scan_config
scan_config.init(**uic.kwargs)
scfg = scan_config.scfg




Controller        = load_pipeline_module(uic, 'Controller/ScanPanel_Controller')


#----------------------------------------------------------------------
class S3Key:
    """"""
    def __init__(self,id, bucket_name,  prefix, profile):
        """"""
        self.id      =id
        self.bucket_name = bucket_name
        self.prefix  = prefix
        self.profile = profile
        
    def getUrl(self):
        return f'{self.profile.upper()}: {self.bucket_name}/{self.prefix}'
        
        
#---------------------------------------------------------------------------
class ScanPanel(wx.Panel, Controller):
    def __init__(self, parent):
        super(ScanPanel, self).__init__(parent)
        h_bucket_name= 'gh-package-pdf'
        bucket_name= 'k9-filestore'
        prefix='k9-feed-doc-lims/'
        self.keys=keys = [
                S3Key(0, bucket_name,   f'{prefix}', "prod"),
                S3Key(1, h_bucket_name, f'{prefix}', "home"),
                S3Key(2, bucket_name, f'{prefix}A', "prod"),
                ]

        sampleList = []

        self.cb = wx.ComboBox(self, size=wx.DefaultSize, choices=sampleList)

        self.widgetMaker(self.cb, keys)
        #self.tc = wx.TextCtrl(self, -1, '', size=(70,-1))

        self.bsc = wx.Button(self, -1, 'Scan S3')
        #print(self.cb.GetSize())
        self.cb.SetValue(self.keys[0].getUrl())
        x,y=self.cb.GetSize()
        self.cb.SetSize((x+150,y))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.cb, 0, wx.ALL, 3)
        #sizer.Add(self.tc, 0, wx.ALL, 3)
        sizer.Add(self.bsc, 0, wx.ALL, 3)

        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.onScan, self.bsc)
        self.changed = False

    def widgetMaker(self, widget, objects):
        """"""
        for obj in objects:
            widget.Append(obj.getUrl(), obj)
        widget.Bind(wx.EVT_COMBOBOX, self.onSelect)
        widget.Bind(wx.EVT_KEY_UP, self.OnKeyUP)

