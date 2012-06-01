import time, sys

# Screens
import metricsathome.Screens.WhiteScreen
import metricsathome.Screens.BlackScreen
import metricsathome.Screens.HelloWorldScreen

# Display Drivers
import metricsathome.Drivers.SamsungFrameDriver
import metricsathome.Drivers.X11Driver

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
    #return metricsathome.Drivers.X11Driver.X11Driver()
    return metricsathome.Drivers.SamsungFrameDriver.SamsungFrameDriver()

  def getScreens(self):
    return [
      metricsathome.Screens.HelloWorldScreen.HelloWorldScreen,
      metricsathome.Screens.BlackScreen.BlackScreen,
      metricsathome.Screens.WhiteScreen.WhiteScreen,
      ]





def run():
  sc = ScreenController();
  sc.go()




