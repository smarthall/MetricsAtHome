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
    self._num = 0

  def go(self):
    dev = self.getDevice()
    screens = self.getScreens()

    while dev.devicePresent():
      cur = self.getNextScreen(screens)
      si = cur.getInfo()
      self.showScreen(cur, dev)

  def showScreen(self, screen, dev):
    di = dev.getInfo()
    si = screen.getInfo()
    quitntime = int(time.time() + si['duration'])
    while (quitntime > time.time()) and (dev.devicePresent()):
      frame = screen.getImage(di['width'], di['height'])
      if not frame == None:
        dev.showFrame(frame)

  def getNextScreen(self, screens):
    self._num = (self._num + 1) % len(screens)
    return screens[self._num]()

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




