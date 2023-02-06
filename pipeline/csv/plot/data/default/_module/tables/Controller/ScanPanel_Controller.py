from pprint import pprint as pp
from ui_layer.Base import Base, reciever

class ScanPanel_Controller(Base):
    #----------------------------------------------------------------------
    def onSelect(self, event):
        """"""
        if 0:
            print ("You selected: " + self.cb.GetStringSelection())
            obj = self.cb.GetClientData(self.cb.GetSelection())
            val=self.cb.GetValue()
            obj.prefix = val
            self.send('scanS3', obj)
            
        self.changed=False
        self.sendScan()
        self.sub('scanS3_done')
    @reciever
    def scanS3_done(self,message, arg2=None, **kwargs):
        obj, changed = message
        print('scanS3_done')
        self.slog('reciever<-scanS3_done' )
        if changed:
            self.saveScanStr(obj)
        else:
            self.slog('scanS3_done<-not changed' )
    def saveScanStr(self, obj):
        text = f"""--------------------
        saveScanStr :
        {obj.id}, {obj.bucket_name}, {obj.prefix}, {obj.profile}

        --------------------------"""
                
        print(text)
    def sendScan(self):
        obj = self.keys[self.cb.GetSelection()]
        val=self.cb.GetValue() 
        assert val
        obj.prefix = val
        if 1:
            self.slog(f'send->{obj.prefix}/{self.changed}' )
        self.send('scanS3', (obj, self.changed))

            #self.slog(f'  {self.__class__.__name__}->' )
            #self.slog(f'    {obj.prefix}' )
    def onScan(self, event):
        """"""

        self.sendScan()

    def OnKeyUP(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == 13:
            self.sendScan()
        else:
             self.changed = True
        event.Skip() 