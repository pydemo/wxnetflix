import wx
import sys
from os.path import isfile
import ui_layer.images as images
import random
from pprint import pprint as pp
try:
    from agw import genericmessagedialog as GMD
except ImportError: # if it's not there locally, try

    import wx.lib.agw.genericmessagedialog as GMD	
from wx.lib.embeddedimage import PyEmbeddedImage

from ui_layer.common import open_editor
from ui_layer.Base import Base, reciever
from ui_layer.Base import Base, reciever
from ui_layer.EditMenu import EditMenu

e=sys.exit

ART_ICONS = []
for d in dir(wx):
    if d.startswith('ART_'):
        if not eval('wx.%s'%d).endswith(b'_C'):
            ART_ICONS.append(eval('wx.%s'%d))
import logging
log=logging.getLogger('ui')
#----------------------------------------------------------------------
_error = PyEmbeddedImage(
    "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")
_ok = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAjdJ"
    "REFUOI2tksFLk3Ecxp+97975vmuve1dWuiUTNIy1JlsLpkZG0aXLbv0B0aVDUMfVQTp0jJpF"
    "EHl5LxUZgZcuQjAID4KUyWwyEU3d9m7O5d733dze97dfB1siJSn1nJ/P5+ELX+Afwx6YuAMB"
    "AVgwjcaBBdIovP2eyKMLPYNdM+7kNKZA9i3gR+ENCeF4Hx+8VigVBgrKWrXKGp/2JeCfwhsW"
    "Q/HTQiCaVTOYUiZtDuoMQqefrc1S9+uOEGNSRzqd+4j72/c1l4OOQNwn+aOFWg5TdBJEIKbH"
    "dI9zHLMt6H3lHrjScfU5x3DSmOXNrVUUxwFQ6S3vDdh9cZ/zTHSz8R0pMguGMKaRMuX5peQ9"
    "ZULPW8+PnB286L78zH/M76/DwCYtjSTefaAOQZjpEDofn5J8UR0qViqLoCpLql+IXFzS72IC"
    "eQCwssR2NFfOtNXsFZx09SLkDnfSlsYTluUy7a3Hz6mWMrLGKswiJaV0WS6Uyr9gAGC7It0L"
    "WrWYm99K9VdcqugSD8Pd6nG6RNeJCq9ZstwqNL1CMl/z8npdiRkPd2AAYJcTy41FcSVZt+lK"
    "na9FaLspCg4ehDew3qJgs6qStUxerhItlr+h74KB5iPNgVZuGkm6QpQWmy3i8AoiY7dA1XTy"
    "LZuVGYHGZi8t/gbvCABgDFS7vpVEgSgS29bv5CR7XtmQjxxyxt77En+Edwt+Svpua3MbRT5T"
    "a9QXPGL7gxc9L/eE98wwHWaG6JD1783/kB9qTvueLt8LjwAAAABJRU5ErkJggg==")

import wx.html as html
import os, sys,traceback, subprocess
def format_stacktrace():
    parts = ["Traceback (most recent call last):\n"]
    parts.extend(traceback.format_stack(limit=50)[:-2])
    parts.extend(traceback.format_exception(*sys.exc_info())[1:])
    return "".join(parts)



class StHtmlWindow(html.HtmlWindow, Base):
    def __init__(self, parent, id, err):
        Base.__init__(self)
        html.HtmlWindow.__init__(self, parent, id, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.parent=parent
        if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
            self.SetStandardFonts()
        if 1:
            import re
            urls = re.findall('(\"((?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)\", line (\d+))+', err)
            #pp(urls)
            for url in urls:
                match, file, line = url
                new = match.replace('line %d' % int(line), \
                r'<a href="%s|%d" >line %d</a>' % (file, int(line), int(line)))
                #pp(os.getcwd())
                err= err.replace(match,new)
            if 1: 
                files = re.findall('\((C\:.*py)\)', err)
                #pp(files)
                #e()
                for fn in files:
                    assert isfile(fn)
                    url = r'<a href="%s|%d" >%s</a>' % (fn, 0, fn)
                    err= err.replace('(%s)' % fn,url)
        if 1:
            herr=[]
            for line in err.split('\n'):
                if line.strip().startswith('asrt'):
                    line = '<b>%s</b>' % line
                herr.append('%s<br>' % line)
            msg=''.join(herr)
            ht = """<html>
         <head>
            <style type="text/css">
            div#container{background-color:#F0F8FF;width:700px}
            div#content {height:200px;width:400px;float:left;word-break: break-all;}
            div#predict{width:700px;}
            .box {height:200px;width:300px;overflow:hidden;background-repeat: no-repeat;background-position:center center;float:left;}
             img{margin-top: -50px;}
             a:link{ text-decoration:none;}
            </style>
         </head>
         <body>
           <div>
            <p>%s
            </p>
          </div>
          </body></html>
          """ % (msg)

            #dialog = MyBrowser(self, -1, title='Error') 
            self.SetPage(ht) 
            if 1:
                x, y = self.GetPosition()
                xs, ys=self.GetSize()
                myx, myy= self.GetSize()
                self.SetPosition((x+xs/2-myx/2,y+ys/2-myy/2))
                #print(self.GetScreenPosition())
        #EditMenu.__init__(self, globals(), True)

        

    def OnLinkClicked(self, linkinfo):
        fn, line=linkinfo.GetHref().split('|')
        
        if wx.GetKeyState(wx.WXK_CONTROL):
            print ("Control key is down")
            
            self.send('previewScript', ((fn,line), wx.GetTopLevelParent(self)))
            #self.parent.Destroy()
        else:
            open_editor(fn, int(line), win=self.parent)
        
        

    def OnSetTitle(self, title):
        print('OnSetTitle: %s\n' % title)
        super(StHtmlWindow, self).OnSetTitle(title)

    def OnCellMouseHover0(self, cell, x, y):
        print('OnCellMouseHover: %s, (%d %d)\n' % (cell, x, y))
        super(StHtmlWindow, self).OnCellMouseHover(cell, x, y)

    def OnCellClicked(self, cell, x, y, evt):
        #print('OnCellClicked: %s, (%d %d)\n' % (cell, x, y))
        if isinstance(cell, html.HtmlWordCell):
            sel = html.HtmlSelection()
            #print('     %s\n' % cell.ConvertToText(sel))
        return super(StHtmlWindow, self).OnCellClicked(cell, x, y, evt)

    # def OnHTMLOpeningURL(self, urlType, url):
    #     print('OnHTMLOpeningURL: %s %s' % (urlType, url))
    #     if urlType == wx.html.HTML_URL_IMAGE and 'canada' not in url:
    #         return (wx.html.HTML_REDIRECT, "bitmaps/canada.gif")
    #     return (wx.html.HTML_OPEN, "")
    


class GenericMessageDialog(wx.Dialog, Base, EditMenu):
    def __init__(self, parent, message, caption, agwStyle,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.DEFAULT_DIALOG_STYLE|wx.WANTS_CHARS|wx.RESIZE_BORDER,
                     wrap=-1):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, caption, pos, size, style)
        Base.__init__(self)
        self._created=False
        self.msg=message
        self._agwStyle = agwStyle
        self.win =parent
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_IDLE,self.OnIdle)
        self.resized=False
        self.sub('previewScript')
        EditMenu.__init__(self, globals())

        
    

    @reciever
    def previewScript(self, message, arg2=None, **kwargs):
        
        script, parent = message
        script_loc, lineno = script
        
        
        if parent ==self:
            try:
                
                from dialog.EditScriptDialog import EditScriptDialog
                dlg = EditScriptDialog(self, script_loc=script_loc, lineno=lineno, title='Preview "%s"' % script_loc)
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    print('OK')
                elif result == wx.ID_CANCEL:
                    print('Cancel')
                else: print(result)
            except:
                stacktrace = format_stacktrace()
                if 1:
        
                    import dialog.ErrDlg as ED
                    ED.show(stacktrace)
                
            
    def OnResize(self, event):
        
        self.resized = True
        event.Skip() 
    def OnIdle(self,event):
        if self.resized: 
            import ui_layer.config.ui_config as ui_config 
            if hasattr(ui_config, 'apc'):
                uic = ui_config.uic
                    
                # take action if the dirty flag is set
                print ("New size:", self.GetSize())
                self.resized = False # reset the flag
                uic.setErrDlgSize(self.GetSize())
                uic.setErrDlgPos(self.GetPosition())
        event.Skip()
        
    def OnKeyUP(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.Close()
        event.Skip() 
        
    def ShowModal(self):
        """
        Shows the dialog, returning one of ``wx.ID_OK``, ``wx.ID_CANCEL``, ``wx.ID_YES``,
        ``wx.ID_NO`` or ``wx.ID_HELP``.
        :note: Notice that this method returns the identifier of the button which was
         clicked unlike the :class:`MessageBox` () function.
        :note: Reimplemented from :class:`Dialog`.
        """

        if not self._created:

            self._created = True
            self.CreateMessageDialog()
            

        return wx.Dialog.ShowModal(self)
    def CreateMessageDialog(self):
        """ Actually creates the :class:`GenericMessageDialog`, just before showing it on screen. """

        message = self.msg
        sizer = wx.BoxSizer(wx.VERTICAL) 
        self.browser = StHtmlWindow(self, -1, message)
        #pp(dir(self.browser))
        #self.browser.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.onNav)
        #self.browser.Bind(wx.html2.EVT_WEBVIEW_NEWWINDOW, self.onNewWindow)
        bitmap = _error
        icon = wx.StaticBitmap(self, -1, bitmap.GetBitmap())
        sizer.Add(icon, 0, wx.ALIGN_LEFT, 10) 
        sizer.Add(self.browser, 1, wx.EXPAND, 10) 
        #b_ok = wx.Button(self, wx.ID_OK, label='Ok')
        #b_ok.Bind(wx.EVT_BUTTON, self.onSelect)
        import wx.lib.buttons as buttons
        klass = buttons.ThemedGenBitmapTextButton
        ok = klass(self, wx.ID_OK, _ok.GetBitmap(), "OK")
        #sizerBtn.Add(ok, 1)
        sizer.Add(ok, 0, wx.ALIGN_RIGHT, 10) 

        self.Fit()

        self.SetSizerAndFit(sizer) 
        
        win   = self.win
        
        if win.__class__.__name__==self.__class__.__name__:
            x, y=win.GetPosition()
            w,h	=win.GetSize()
            self.SetPosition((x+100, y+100))
            self.SetSize((w,h))
        elif not hasattr(win, 'frame'):

            uic=None
            try:
                import ui_layer.config.ui_config as ui_config 
                uic = ui_config.uic
            except:
                raise
            if uic:
                size= uic.getErrDlgSize()

                pos = uic.getErrDlgSPos()
                if size and pos:
                    self.SetSize(size)
                    self.SetPosition(pos)
                else:
        
                    x, y=uic.getFramePos()
                    w, h=uic.getFrameSize()
                    myx, myy = w/2, h/2
                    print(1, x, y,w,h)
                    self.SetPosition((x+w/2-myx/2-50,y+h/2-myy/2-100))
                    self.SetSize((myx+50, myy+200))
            else: #no DataWorm yet, just StartFrame
                x, y=win.GetPosition()
                w, h=win.GetSize()
                myx, myy = w/2, h/2
                print(1, x, y,w,h)
                self.SetPosition((x+w/2-myx/2-50,y+h/2-myy/2-100))
                self.SetSize((myx+50, myy+200))
        else:

            import ui_layer.config.ui_config as ui_config 
            uic = ui_config.uic

            if uic:
                size= uic.getErrDlgSize()
                pos = uic.getErrDlgSPos()
                if size and pos:
                    self.SetSize(size)
                    self.SetPosition(pos)
                else:
                    x, y=win.frame.GetPosition()
                    w,h=win.frame.GetSize()
                    myx, myy = w/2, h/2
                    print(2,x, y,w,h)
                    self.SetPosition((x+w/2-myx/2,y+h/2-myy/2))
                    self.SetSize((myx, myy))
        r = self.browser.GetScrollRange(wx.VERTICAL)
        self.browser.Scroll(0, r)
        self.Show() 
    

        
        #self.SwitchFocus()
    def SwitchFocus(self):
        """ Switch focus between buttons. """

        current = wx.Window.FindFocus()
        font = self.GetFont()
        boldFont = wx.Font(font.GetPointSize(), font.GetFamily(), font.GetStyle(), wx.FONTWEIGHT_BOLD,
                           font.GetUnderlined(), font.GetFaceName())

        for child in self.GetChildren():
            if isinstance(child, wx.lib.buttons.ThemedGenBitmapTextButton) or \
               isinstance(child, AB.AquaButton) or isinstance(child, GB.GradientButton):
                if child == current:
                    # Set a bold font for the current focused button
                    child.SetFont(boldFont)
                else:
                    # Restore the other buttons...
                    child.SetFont(font)
                child.Refresh()
def show(msg, win=None):
    if not win:
        try:
            win   = wx.GetApp().GetTopWindow()
            print(win)
        except:
            log.warn('SHOW: Cannot find top window.')
            raise
    if win:
        wname = win.__class__.__name__
        
        dlg = GenericMessageDialog(win, msg,
                                "%s error" % wname,
                                wx.CANCEL|wx.ICON_ERROR)

        #dlg.SetPosition((400,400))
        #dlg.SetExtendedMessage(msg)
        dlg.SetIcon(images.Mondrian.GetIcon())
        
        dlg.ShowModal()

        #dlg.SetPosition((400,400))
        if 0:
            dlg.Destroy()
            print('desroyed')
    else:
        log.warn('SHOW: Cannot create dialog window.')
        