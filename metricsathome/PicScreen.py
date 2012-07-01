import time
import Image
import BaseScreen

class PicScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._frameno = 0
    self.picture = args.get('picture', 'img/sample.jpg')

  def getImage(self):
    if self._frameno == 0:
        self._frameno += 1
        return Image.open(self.picture)
    else:
        time.sleep(1)
        return None

