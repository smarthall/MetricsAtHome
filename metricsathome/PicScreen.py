import time
import Image

class PicScreen:
  def __init__(self, width, height, args):
    self._frameno = 0

  def getImage(self):
    if self._frameno == 0:
        self._frameno += 1
        return Image.open('img/sample.jpg')
    else:
        time.sleep(1)
        return None

