import wx
import sys
import Image


class X11Frame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, wx.ID_ANY,
    "Metrics At Home X11", size=(320,240))
    
    wx.EVT_CHAR(self,self._callback)
    self._curframe = None
    self._timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.updFrame)
    self._timer.Start(100.0)

  def updFrame(self, evt):
    if self._curframe != None:
      wx.StaticBitmap(self,-1,self._curframe.ConvertToBitmap(), (0, 0))

  def _callback(self,evt,a,f):
    # Closes the window upon any keypress
    self._timer.Stop()
    self.Hide()





class X11Driver(wx.Frame):
  def __init__(self):
    self._app = wx.PySimpleApp()
    self._x11 = X11Frame()
    self._x11.Show()

  def getInfo(self):
    return {
      'name':    'X11 Driver (wxWidgets)',
      'width':   320,
      'height':  240,
    }

  def showFrame(self, frame):
    if frame.size != (320, 240):
      raise Exception('X11 driver currently only supports 320x240')
    wximage = wx.EmptyImage(320, 240)
    wximage.SetData(frame.convert('RGB').tostring())
    self._x11._curframe = wximage

  def process(self):
    self._app.Yield()

  def devicePresent(self):
    try:
      return self._x11.IsShown()
    except wx.PyDeadObjectError:
      return False

