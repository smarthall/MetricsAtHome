import wx
import sys
import Image
import threading

class X11Frame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, wx.ID_ANY,
    "Metrics At Home X11", size=(320,240))
    
    wx.EVT_CHAR(self,self._callback)
    self._curframe = None
    #self._timer = wx.Timer(self)
    #self.Bind(wx.EVT_TIMER, self.updFrame)
    #self._timer.Start(1000.0)
    self._framelock = threading.Lock()
    self.Bind(wx.EVT_IDLE, self.updFrame)

  def updFrame(self, evt):
    self._framelock.acquire()
    if self._curframe != None:
      wximage = wx.EmptyImage(320, 240)
      wximage.SetData(self._curframe.convert('RGB').tostring())
      bitmap = wximage.ConvertToBitmap()
      wx.StaticBitmap(self,-1,bitmap, (0, 0))
    self._framelock.release()
    evt.RequestMore()

  def showFrame(self, wximage):
    self._framelock.acquire()
    self._curframe = wximage
    self._framelock.release()

  def _callback(self,evt,a,f):
    # Closes the window upon any keypress
    self._timer.Stop()
    self.Destroy()




class UIThread(threading.Thread):
  def __init__(self):
    self._x11 = None
    threading.Thread.__init__(self)

  def run(self):
    self._app = wx.PySimpleApp()
    self._x11 = X11Frame()
    self._x11.Show()
    self._app.MainLoop()

  def showFrame(self, wximage):
    if self._x11 != None:
      self._x11.showFrame(wximage)






class X11Driver:
  def __init__(self):
    self._thread = UIThread()
    self._thread.start()

  def getInfo(self):
    return {
      'name':    'X11 Driver (wxWidgets)',
      'width':   320,
      'height':  240,
    }

  def showFrame(self, frame):
    if frame.size != (320, 240):
      raise Exception('X11 driver currently only supports 320x240')
    self._thread.showFrame(frame)

  def devicePresent(self):
    try:
      return self._thread.isAlive()
    except wx.PyDeadObjectError:
      return False

