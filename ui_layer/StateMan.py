import wx
class StateMan(object): 
	def method_save_default_perspective(self):
		self.method_set_default_pane_captions()
		current_perspective = self.pnl.mgr.SavePerspective()
		self.method_set_translation_pane_captions()
		if self.settings.Read('GUI/perspective', '') != current_perspective:
			self.settings.Write('GUI/perspective', current_perspective)
			self.settings.Flush()
	def method_set_default_pane_captions(self):
		for name, caption in self.pane_captions.items():
			self.pnl.mgr.GetPane(name).Caption(caption[0])

	def method_set_translation_pane_captions(self):
		for name, caption in self.pane_captions.items():
			self.pnl.mgr.GetPane(name).Caption(caption[1])			
	def method_save_default_state(self):
		flag_flush = False
		position = self.GetPosition()
		if position != eval(self.settings.Read('GUI/position', '()')):
			self.settings.Write('GUI/position', repr(position))
			flag_flush = True
		size = self.GetSize()
		if size != eval(self.settings.Read('GUI/size', '()')):
			self.settings.Write('GUI/size', repr(size))
			flag_flush = True
		font = self.GetFont().GetNativeFontInfo().ToString()
		if font != self.settings.Read('GUI/font', ''):
			self.settings.Write('GUI/font', font)
			flag_flush = True
		is_maximized = self.IsMaximized()
		if is_maximized != self.settings.ReadBool('GUI/maximized', False):
			self.settings.WriteBool('GUI/maximized', is_maximized)
			flag_flush = True
		is_iconized = self.IsIconized()
		if is_iconized != self.settings.ReadBool('GUI/iconized', False):
			self.settings.WriteBool('GUI/iconized', is_iconized)
			flag_flush = True
		is_fullscreen = self.IsFullScreen()
		if is_fullscreen != self.settings.ReadBool('GUI/fullscreen', False):
			self.settings.WriteBool('GUI/fullscreen', is_fullscreen)
			flag_flush = True
		if flag_flush:
			self.settings.Flush()
	def method_load_default_state(self):
		#frame_font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
		#frame_font.SetNativeFontInfoFromString(self.settings.Read('GUI/font', ''))
		#self.SetFont(frame_font)
		self.SetSize(eval(self.settings.Read('GUI/size', '(100,100)')))
		self.SetPosition(eval(self.settings.Read('GUI/position', '(100,100)')))
		centre_on_screen = eval(self.settings.Read('GUI/centre_on_screen', repr((False, wx.BOTH))))
		if centre_on_screen[0]:
			self.CentreOnScreen(centre_on_screen[1])
		self.Maximize(self.settings.ReadBool('GUI/maximized', False))
		self.Iconize(self.settings.ReadBool('GUI/iconized', False))
		self.ShowFullScreen(self.settings.ReadBool('GUI/fullscreen', False), self.settings.ReadInt('GUI/fullscreen_style', default_fullscreen_style))

