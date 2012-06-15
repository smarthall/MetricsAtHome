import Image, ImageFont, ImageDraw

class HelloWorldScreen:
  def __init__(self, width, height, args):
    self.width = width
    self.height = height
    self._xpos = 0
    self._ypos = 0
    self._xdir = 4
    self._ydir = 4
    self._text = "Hello world!"
    self._textcolor = (0, 0, 0)
    self._font =  ImageFont.truetype('font/DejaVuSans.ttf', 96)
    (self._textw, self._texth) = self._font.getsize(self._text)

  def getImage(self):
    img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
    imgDraw = ImageDraw.Draw(img)
    

    self._xpos = (self._xpos + self._xdir)
    if self._xpos >= (width - self._textw):
      self._xpos = (width - self._textw) - 1
      self._xdir *= -1
    elif self._xpos <= 0:
      self._xpos = 0
      self._xdir *= -1

    self._ypos = (self._ypos + self._ydir)# % (height - texth)
    if self._ypos >= (height - self._texth):
      self._ypos = (height - self._texth) - 1
      self._ydir *= -1
    elif self._ypos <= 0:
      self._ypos = 0
      self._ydir *= -1
    
    imgDraw.text((self._xpos, self._ypos), self._text, font=self._font, fill=self._textcolor)
    return img

