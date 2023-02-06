from pprint import pprint as pp
from ui_layer.Base import Base, reciever

class TemplateTypePanel_Controller(Base):
	#----------------------------------------------------------------------
	def __init__(self):
		Base.__init__(self)
	def onRadioBox(self,e): 
		
		self.status=self.rbox.GetStringSelection()
		print (f' "{self.status}" is clicked from Radio Box' )
		self.send('changeTemplate', self.keys[self.status])
		
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
	#@reciever
