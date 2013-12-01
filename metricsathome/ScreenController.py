import time, sys, os
import datetime
import logging
import yaml
import threading

# utils
import Data.Cache as Cache
import BaseScreen

# Display Drivers
from Drivers.SamsungFrameDriver import SamsungFrameDriver, FrameNotFoundException

class ScreenLoader(threading.Thread):
  def __init__(self, screen, width, height, args):
    threading.Thread.__init__(self)
    self._screeninit = screen
    self._width = width
    self._height = height
    self._args = args

  def run():
    self.result = self._screeninit(self._width, self._height, self._args)

class ScreenController:
  def __init__(self):
    self._scrnum = -1
    self._dev = self.getDevice()

    # Process the config
    if os.path.exists('/etc/metricsathome.yaml'):
      config = yaml.safe_load(open('/etc/metricsathome.yaml','r'))
    else:
      config = yaml.safe_load(open('conf/default.yaml','r'))
    # Get global config
    self._cachelocation = config.get('cachelocation', '/tmp/metricsathome-cache')
    # get screen configs
    self._screenconfig = config['screenconfig']
    for conf in self._screenconfig.keys():
      if self._screenconfig[conf]['args'] is None:
        self._screenconfig[conf]['args'] = {}
    # Build schedule
    schedule = [config['defaultscreens']] * 24
    if config['screenschedule'] is not None:
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
      try:
        self.showScreen(scn, dur)
      except:
        import ErrorScreen
        screen = ErrorScreen.ErrorScreen(di['width'], di['height'], scn.__class__.__name__, {})
        self.showScreen(screen, 15)


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
    duration = conf['duration']
    # Make the screen
    screen = self.makeScreen(width, height, conf)

    return (screen, duration)

  def makeScreen(self, width, height, conf):
    try:
      parts = conf['class'].split('.')
      module = ".".join(parts[:-1])
      m = __import__( module )
      for comp in parts[1:]:
        m = getattr(m, comp)
      # Create the screen, passing it the arguments it needs
      screen = m(width, height, conf['args'])
      if not isinstance(screen, BaseScreen.BaseScreen):
        raise Exception('The selected class is not a screen')
    except:
      import ErrorScreen
      screen = ErrorScreen.ErrorScreen(width, height, conf['class'], conf['args'])
      duration = 15

    return screen

  def getDevice(self):
    try:
      return SamsungFrameDriver()
    except FrameNotFoundException:
      print 'Can\'t find a screen, loading X11Driver'
      import Drivers.X11Driver
      return Drivers.X11Driver.X11Driver()





def run():
  sc = ScreenController();
  sc.go()




