import wx
import sys
import threading
import time

try:
    import Image
except ImportError:
    from PIL import Image

class X11Frame(wx.Frame):
  def __init__(self, width, height):
    wx.Frame.__init__(self, None, wx.ID_ANY,
    "Metrics At Home X11", size=(width, height))
    self._swidth = width
    self._sheight = height
    self._newFrame = False
    wx.EVT_CHAR(self,self._callback)
    self._curframe = None
    self._framelock = threading.Lock()
    self.Bind(wx.EVT_IDLE, self.updFrame)

  def updFrame(self, evt):
    self._framelock.acquire()
    if self._curframe != None and self._newFrame:
      wximage = wx.EmptyImage(self._swidth, self._sheight)
      wximage.SetData(self._curframe.convert('RGB').tostring())
      bitmap = wximage.ConvertToBitmap()
      window_list = self.GetChildren()
      for w in window_list:
        w.Destroy()
      wx.StaticBitmap(self,-1,bitmap, (0, 0))
    self._framelock.release()

  def showFrame(self, wximage):
    self._framelock.acquire()
    self._curframe = wximage
    self._newFrame = True
    self._framelock.release()

  def _callback(self,evt,a,f):
    # Closes the window upon any keypress
    self._timer.Stop()
    self.Destroy()




class UIThread(threading.Thread):
  def __init__(self, width, height):
    self._swidth = width
    self._sheight = height
    self._x11 = None
    threading.Thread.__init__(self)

  def run(self):
    self._app = wx.PySimpleApp()
    self._x11 = X11Frame(self._swidth, self._sheight)
    self._x11.Show()
    self._app.MainLoop()

  def showFrame(self, wximage):
    if self._x11 != None:
      self._x11.showFrame(wximage)
      self._app.WakeUpIdle()





class X11Driver:
  # Emulate Samsung SPF-87H
  #swidth  = 800
  #sheight = 480

  # Emulate Samsung SPF-107H
  swidth  = 1024
  sheight = 600

  def __init__(self):
    self._thread = UIThread(X11Driver.swidth, X11Driver.sheight)
    self._thread.start()

  def getInfo(self):
    return {
      'name':    'X11 Driver (wxWidgets)',
      'width':   X11Driver.swidth,
      'height':  X11Driver.sheight,
    }

  def showFrame(self, frame):
    if frame.size != (X11Driver.swidth, X11Driver.sheight):
      raise Exception('X11 driver currently only supports one resolution')
    self._thread.showFrame(frame)

  def devicePresent(self):
    try:
      return self._thread.isAlive()
    except wx.PyDeadObjectError:
      return False

