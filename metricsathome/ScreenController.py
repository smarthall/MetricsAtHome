import time

# Screens
import metricsathome.WhiteScreen
import metricsathome.BlackScreen
import metricsathome.HelloWorldScreen

# Display Drivers
#import metricsathome.SamsungUSBDriver
import metricsathome.X11Driver

def run():
  s = metricsathome.HelloWorldScreen.HelloWorldScreen()
  display = metricsathome.X11Driver.X11Driver()
  disinfo = display.getInfo()
  
  while display.devicePresent():
    display.process()
    frame = s.getImage(disinfo['width'], disinfo['height'])
    if not frame == None:
      display.showFrame(frame)


