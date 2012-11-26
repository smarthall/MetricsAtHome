import Image, ImageFont
import FancyDraw
import time
import StringIO
from Data.BOM import BOM
import BaseScreen

class FridgeScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._dimensions = (width, height)
    self._nextupd = time.time()
    self._tempfont = ImageFont.truetype('font/DejaVuSans.ttf', 48)
    self._textcolor =     (0,  0,    0  )
    self._freezercolor =  (24, 184,  219)
    self._fridgecolor =   (5,  80,   242)

  def getImage(self):
    if self._nextupd >= time.time():
      time.sleep(1 / 10)
      return None
    self._nextupd = time.time() + 1

    im = Image.new('RGBA', self._dimensions, (255, 255, 255))
    draw = FancyDraw.FancyDraw(im)

    draw.text((179, 81), u'-20\u00b0C', font=self._tempfont, fill=self._freezercolor)
    draw.text((179, 181), u'2\u00b0C', font=self._tempfont, fill=self._fridgecolor)


    return im

