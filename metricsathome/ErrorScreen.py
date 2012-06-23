import Image, ImageFont, ImageDraw
import traceback, time

class ErrorScreen:
  def __init__(self, width, height, args):
    self.width = width
    self.height = height

    textcolor = (0, 0, 0)
    bigfont   =  ImageFont.truetype('font/DejaVuSans.ttf', 48)
    smallfont =  ImageFont.truetype('font/DejaVuSans.ttf', 12)

    self._img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
    imgDraw = ImageDraw.Draw(self._img)
    imgDraw.text((0, 0), 'Error', font=bigfont, fill=textcolor)
    msgy = 60
    for line in traceback.format_exc().split("\n"):
      imgDraw.text((0, msgy), line, font=smallfont, fill=textcolor)
      (x, y) = imgDraw.textsize(line, font=smallfont)
      msgy += y

  def getImage(self):
    time.sleep(1)
    return self._img

