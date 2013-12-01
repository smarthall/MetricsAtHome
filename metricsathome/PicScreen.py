import time
try:
  import Image
except ImportError:
  from PIL import Image

import BaseScreen
import FancyDraw

class PicScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._frameno = 0
    self.picture = args.get('picture', 'img/sample.jpg')
    self.width = width
    self.height = height
    self.im = Image.new('RGBA', (width, height), (0, 0, 0))

    srcim = Image.open(self.picture).convert('RGBA')
    ratio = min(float(width) / srcim.size[0], float(height) / srcim.size[1])
    if ratio < 1:
      method = Image.ANTIALIAS
    else:
      method = Image.NEAREST
    srcim = srcim.resize((int(srcim.size[0] * ratio),
                          int(srcim.size[1] * ratio)), method)
    draw = FancyDraw.FancyDraw(self.im)
    draw.cpaste(srcim, (width / 2, height / 2), center='both')

  def getImage(self):
    if self._frameno == 0:
        self._frameno += 1
        return self.im
    else:
        time.sleep(1)
        return None

