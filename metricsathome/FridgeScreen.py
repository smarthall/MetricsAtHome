import Image, ImageFont
import FancyDraw
import time
import StringIO
from Data import Fridge
import BaseScreen

class FridgeScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._dimensions = (width, height)
    self._nextupd = time.time()
    self._tempfont = ImageFont.truetype('font/DejaVuSans.ttf', 48)
    self._textcolor =     (0,  0,    0  )
    self._freezercolor =  (24, 184,  219)
    self._fridgecolor =   (5,  80,   242)

    self._fridge = Image.open('img/fridge.png').convert('RGBA')

  def getImage(self):
    if self._nextupd >= time.time():
      time.sleep(1 / 10)
      return None
    self._nextupd = time.time() + 1

    im = Image.new('RGBA', self._dimensions, (255, 255, 255))
    draw = FancyDraw.FancyDraw(im)

    im.paste(self._fridge, (20, 20), self._fridge)
    draw.ctext((152, 98),  u'%.1f' % Fridge.tempA() + u'\u00b0C',
               font=self._tempfont, fill=self._freezercolor, center='both')
    draw.ctext((152, 345), u'%.1f' % Fridge.tempB() + u'\u00b0C',
               font=self._tempfont, fill=self._fridgecolor, center='both')

    return im

