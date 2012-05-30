
import Image, ImageFont, ImageDraw

class HelloWorldScreen:
  def __init__(self):
    self._sent = False

  def getInfo(self):
    return {
      'duration':     5,
      'name':         'Hello World Screen',
      'framesleep':   1000,
    }

  def getImage(self, width, height):
    if not self._sent:
      img = Image.new('RGB', (width, height), (255, 255, 255))
      black = (0, 0, 0)
      imgDraw = ImageDraw.Draw(img)
      fntNorm =  ImageFont.truetype('font/DejaVuSans.ttf', 24)
      imgDraw.text((20, 20), "Hello World", font=fntNorm, fill=black)
      self._sent = True
      return img
    else:
      return None

