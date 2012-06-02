import time, sys

# Screens
import Screens.WhiteScreen
import Screens.BlackScreen
import Screens.HelloWorldScreen
import Screens.PicScreen
import Screens.TramScreen

# Display Drivers
import Drivers.SamsungFrameDriver
import Drivers.X11Driver

class ScreenController:
  def __init__(self):
    self._scrnum = -1
    self._dev = self.getDevice()
    self._screens = self.getScreens()

  def go(self):
    while self._dev.devicePresent():
      cur = self.getNextScreen()
      si = cur.getInfo()
      self.showScreen(cur)

  def showScreen(self, screen):
    di = self._dev.getInfo()
    si = screen.getInfo()
    quitntime = int(time.time() + si['duration'])
    while (quitntime > time.time()) and (self._dev.devicePresent()):
      frame = screen.getImage(di['width'], di['height'])
      if not frame == None:
        self._dev.showFrame(frame)

  def getNextScreen(self):
    self._scrnum = (self._scrnum + 1) % len(self._screens)
    return self._screens[self._scrnum]()

  def getDevice(self):
    try:
      return Drivers.SamsungFrameDriver.SamsungFrameDriver()
    except Drivers.SamsungFrameDriver.FrameNotFoundException:
      return Drivers.X11Driver.X11Driver()

  def getScreens(self):
    return [
      Screens.BlackScreen.BlackScreen,
      Screens.TramScreen.TramScreen,
      Screens.PicScreen.PicScreen,
      Screens.HelloWorldScreen.HelloWorldScreen,
      Screens.WhiteScreen.WhiteScreen,
      ]





def run():
  sc = ScreenController();
  sc.go()




