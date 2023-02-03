#!/usr/bin/env python


import wx
import os
from os.path import isfile, dirname, join
import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import Base, reciever
from ui_layer.EditMenu import EditMenu
from ui_layer.module.FileCtrl import FileCtrl
from ui_layer.utils import ex
from pathlib import Path

import ui_layer.config.ui_layout as ui_layout 
uilyt = ui_layout.uilyt




#---------------------------------------------------------------------------
class FileCtrlPanel(wx.Panel, Base, EditMenu):
	def __init__(self,  **kwargs):
		#pp(kwargs)
		self.defaultDirectory = kwargs.get('defaultDirectory', '')
		self.wildCard = kwargs.get('wildCard', "Json files (*.json)|*.json") 
		wx.Panel.__init__(self, kwargs['parent'])
		
		self.kwargs=kwargs
		kwargs['parent']=self
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		if 1:
			
			self.new=new = wx.Button(self, -1, "New", size=(40,30))
			
			#sizer.Add(new, 0, wx.ALIGN_TOP)
			
			

			new.Bind(wx.EVT_BUTTON, self.onNew)
			self.new.Show(False)
		
		if 1:
			self.fc=fc = FileCtrl(**kwargs)
			
			fc.BackgroundColour = 'sky blue'
			
			sizer.Add(fc, 1, wx.ALL|wx.EXPAND)
		
		self.SetSizerAndFit(sizer)
		sizer.Layout()
		EditMenu.__init__(self, globals())

		self.Fit()
		
		
	def onExplorer(self, message, arg2=None, **kwargs):
		ctrl = message.GetParent()
		if ctrl == self.fc:

			subprocess.Popen(r'explorer "%s\"' % self.defaultDirectory, shell=True)

	@reciever
	def newFile(self, message, arg2=None, **kwargs):
		ctrl = message.GetParent()
		if ctrl == self.fc:	
			#print(ctrl, self.fc)
			evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.new.GetId())
			wx.PostEvent(self.new, evt)

		
	@reciever
	def Ctrl_D(self, message, arg2=None, **kwargs):
		
		ctrl = message
		#print(ctrl)
		if ctrl == self.fc :
			fns= self.fc.GetPaths()
			strs = "Are you sure you want to delete files:\n" + ('%s\t' % os.linesep).join(fns) + "?"
			dlg = wx.MessageDialog(None, strs, 'Deleting files', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)

			if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
				dlg.Destroy()
				return

			dlg.Destroy()
			
			for fn in fns:
				log.info('Deleting file %s' % fn)
				os.unlink(fn)
			self.fc.SetDirectory(self.defaultDirectory)
	def onNew(self, evt):
		
		defaultFile= '%s.py' % self.defaultDirectory.split(os.sep)[-1]

		dlg = wx.FileDialog(
			self, message="Save file as ...", defaultDir=self.defaultDirectory,
			defaultFile=defaultFile, wildcard=self.wildCard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
			)
		#dlg.SetFilterIndex(0)

		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			self.createFile(path)
			if 1: #__init__.py
				dn = dirname(path)
				initpy =  join(dn, '__init__.py')
				if not isfile(initpy):
					Path(initpy).touch()
				
			

		dlg.Destroy()

	def createFile(self, path):
		#print(path)
		
		if isfile(path): ex('File exists')
		Path(path).touch()
		if 1:		
			self.fc.SetDirectory(self.defaultDirectory)
		if not isfile(path): ex('File was not created')
		if 1:
			self.send('editFile', (path,0))
		self.fc.SetFilename(os.path.basename(path))
		
		
#---------------------------------------------------------------------------
def runTest(**kwargs):
	win = FileCtrlPanel(**kwargs)
	#log.info(kwargs['name']+':runTest')
	return win
	


#---------------------------------------------------------------------------


overview = """\
File picker 

"""


if __name__ == '__main__':
	import sys
	import os
	import run
	run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
