import time, sys
import datetime
import logging
import yaml

# utils
import Data.Cache as Cache

# Screens
import WhiteScreen
import BlackScreen
import HelloWorldScreen
import PicScreen
import TramScreen
import TramScreenV2
import WeatherScreen

# Display Drivers
from Drivers.SamsungFrameDriver import SamsungFrameDriver, FrameNotFoundException

class ScreenController:
  def __init__(self):
    self._scrnum = -1
    self._dev = self.getDevice()
    self._screens = self.getScreens()

    # Process the config
    config = yaml.safe_load(open('conf/default.yaml','r'))
    # Get global config
    self._cachelocation = config.get('cachelocation', '/tmp/metricsathome-cache')
    # get screen configs
    self._screenconfig = config['screenconfig']
    # Build schedule
    schedule = [config['defaultscreens']] * 24
    for sched in config['screenschedule']:
      for h in sched['hours']:
        schedule[h] = sched['screens']
    self._schedule = schedule

    # Application setup
    logging.basicConfig(level=logging.INFO)
    Cache.fromdisk(self._cachelocation)

  def go(self):
    while self._dev.devicePresent():
      di = self._dev.getInfo()
      (scn, dur) = self.getNextScreen(di['width'], di['height'])
      self.showScreen(scn, dur)

  def showScreen(self, screen, duration):
    quitntime = int(time.time() + duration)
    while (quitntime > time.time()) and (self._dev.devicePresent()):
      frame = screen.getImage()
      if frame is not None:
        self._dev.showFrame(frame)
      else:
        time.sleep(0.001)

  def getNextScreen(self, width, height):
    # Find the schedule, and screen we want
    sched = self._schedule[datetime.datetime.now().hour]
    self._scrnum = (self._scrnum + 1) % len(sched)
    # Get the screen config
    conf = self._screenconfig[sched[self._scrnum]]
    # Import the screen
    parts = conf['class'].split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
      m = getattr(m, comp)            
    # Create the screen, passing it the arguments it needs
    screen = m(width, height, conf['args'])

    return (screen, conf['duration'])

  def getDevice(self):
    try:
      return SamsungFrameDriver()
    except FrameNotFoundException:
      print 'Can\'t find a screen, loading X11Driver'
      import Drivers.X11Driver
      return Drivers.X11Driver.X11Driver()

  def getScreens(self):
    return [
      BlackScreen.BlackScreen,
      WeatherScreen.WeatherScreen,
      TramScreenV2.TramScreenV2,
      #TramScreen.TramScreen,
      #PicScreen.PicScreen,
      #HelloWorldScreen.HelloWorldScreen,
      #WhiteScreen.WhiteScreen,
      ]





def run():
  sc = ScreenController();
  sc.go()




