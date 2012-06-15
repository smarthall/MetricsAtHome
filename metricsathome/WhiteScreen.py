import time
import Image

class WhiteScreen:
  def __init__(self, width, height, args):
    self._frameno = 0
    self.width = width
    self.height = height

  def getImage(self):
    if self._frameno == 0:
        self._frameno += 1
        return Image.new('RGB', (self.width, self.height), (255, 255, 255))
    else:
        time.sleep(1)
        return None

