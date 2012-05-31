
import Image, ImageFont, ImageDraw
import time

class HelloWorldScreen:
  def __init__(self):
    self._xpos = 999

  def getInfo(self):
    return {
      'duration':     5,
      'name':         'Hello World Screen',
    }

  def getImage(self, width, height):
    xpos = int(time.time() % 10) * 10
    if self._xpos != xpos:
      img = Image.new('RGB', (width, height), (255, 255, 255))
      black = (0, 0, 0)
      imgDraw = ImageDraw.Draw(img)
      fntNorm =  ImageFont.truetype('font/DejaVuSans.ttf', 24)
      imgDraw.text((xpos, 20), "Hello World", font=fntNorm, fill=black)
      self._xpos = xpos
      return img
    else:
      return None

