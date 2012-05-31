import time, sys

# Screens
import metricsathome.WhiteScreen
import metricsathome.BlackScreen
import metricsathome.HelloWorldScreen

# Display Drivers
#import metricsathome.SamsungUSBDriver
import metricsathome.X11Driver

def run():
  d = metricsathome.X11Driver.X11Driver()
  
  screens = [
    metricsathome.HelloWorldScreen.HelloWorldScreen,
    metricsathome.BlackScreen.BlackScreen,
    metricsathome.WhiteScreen.WhiteScreen,
    ]

  di = d.getInfo()

  for s in screens:
    cur = s()
    si = cur.getInfo()
    print 'Screen: %s' % si['name']
    quitntime = int(time.time() + si['duration'])
    while (quitntime > time.time()) and (d.devicePresent()):
      frame = cur.getImage(di['width'], di['height'])
      if not frame == None:
        d.showFrame(frame)
      if not d.devicePresent():
        sys.exit(0)




