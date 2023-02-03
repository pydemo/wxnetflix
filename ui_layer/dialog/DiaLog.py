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
            _ht = """
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
          
          """ % (msg)
            ht = """
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
            if 0:
                x, y = self.GetPosition()
                xs, ys=self.GetSize()
                myx, myy= self.GetSize()
                self.SetPosition((x+xs/2-myx/2,y+ys/2-myy/2))
                #print(self.GetScreenPosition())
        #EditMenu.__init__(self, globals(), True)
        self.sub('dia_Log')
    def dia_Log(self, message, arg2=None, **kwargs):
        msg=message
        print(555, dia_Log)
        

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
        #bitmap = _error
        #icon = wx.StaticBitmap(self, -1, bitmap.GetBitmap())
        #sizer.Add(icon, 0, wx.ALIGN_LEFT, 10) 
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
        if 1:

            import ui_layer.config.ui_config as ui_config 
            uic = ui_config.uic

            if 0 and uic:
                size= uic.getErrDlgSize()
                pos = uic.getErrDlgSPos()
                if size and pos:
                    self.SetSize(size)
                    self.SetPosition(pos)
                else: pass
        if 1:
            x, y=win.frame.GetPosition()
            w,h=win.frame.GetSize()
            myx, myy = w/2, h/2
            print(2,x, y,w,h)
            self.SetPosition((x+w/2-myx/2, y+h/2-myy/2))
            print('Dialog size', (myx-100, myy-200))
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
        except:
            log.warn('SHOW: Cannot find top window.')
    if win:
        wname = win.__class__.__name__
        
        dlg = GenericMessageDialog(win, msg,
                                "Import Log [%s]" % wname,
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