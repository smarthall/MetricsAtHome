import sys, os, time, struct
import usb.core
from usb.util import *
import Image
import StringIO

class SamsungFrameDriver:
  vendId = 0x04e8
  prodMassStore = 0x2035
  prodMiniDisp  = 0x2036

  def __init__(self):
    # Look for the frame in storage mode
    dev = usb.core.find(idVendor=SamsungFrameDriver.vendId, idProduct=SamsungFrameDriver.prodMassStore)
    if dev:
      try:
        dev.ctrl_transfer(CTRL_TYPE_STANDARD | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x06, 0xfe, 0xfe, 254)
      except usb.core.USBError as e:
        errorStr = str(e)
      time.sleep(3)

    # Look for a frame in display mode
    dev = usb.core.find(idVendor=SamsungFrameDriver.vendId, idProduct=SamsungFrameDriver.prodMiniDisp)
    if dev:
      dev.set_configuration()
      result = dev.ctrl_transfer(CTRL_TYPE_VENDOR | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x04, 0x00, 0x00, 1)
    else:
      raise Exception("Device not found")

    self._dev = dev


  def getInfo(self):
    return {
      'name':    'X11 Driver (wxWidgets)',
      'width':   1024,
      'height':  600,
    }

  def showFrame(self, frame):
    if frame.size != (1024, 600):
      raise Exception('Samsung frames only support one resolution')
    # Get the frame as a string
    out = StringIO.StringIO()
    frame.save(out, 'JPEG', quality=95)
    pic = out.getvalue()
    out.close()

    rawdata = b"\xa5\x5a\x18\x04" + struct.pack('<I', len(pic)) + b"\x48\x00\x00\x00" + pic
    pad = 16384 - (len(rawdata) % 16384)
    tdata = rawdata + pad * b'\x00'
    tdata = tdata + b'\x00'
    endpoint = 0x02
    self._dev.write(endpoint, tdata )

  def devicePresent(self):
    #TODO
    #STUB
    return True

