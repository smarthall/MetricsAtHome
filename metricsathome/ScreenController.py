import time, sys

# Screens
import metricsathome.WhiteScreen
import metricsathome.BlackScreen
import metricsathome.HelloWorldScreen

# Display Drivers
#import metricsathome.SamsungUSBDriver
import metricsathome.X11Driver

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
    return metricsathome.X11Driver.X11Driver()

  def getScreens(self):
    return [
      metricsathome.HelloWorldScreen.HelloWorldScreen,
      metricsathome.BlackScreen.BlackScreen,
      metricsathome.WhiteScreen.WhiteScreen,
      ]





def run():
  sc = ScreenController();
  sc.go()




