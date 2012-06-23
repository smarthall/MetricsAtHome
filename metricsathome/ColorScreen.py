import time
import Image
import BaseScreen

class ColorScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._frameno = 0
    self.width = width
    self.height = height
    self.color = self.HTMLColorToPILColor(args.get('color', '#000000'))

  def HTMLColorToPILColor(self, colorstring):
    """ converts #RRGGBB to PIL-compatible integers"""
    colorstring = colorstring.strip()
    while colorstring[0] == '#': colorstring = colorstring[1:]
    # get bytes in reverse order to deal with PIL quirk
    colorstring = colorstring[-2:] + colorstring[2:4] + colorstring[:2]
    # finally, make it numeric
    color = int(colorstring, 16)
    return color

  def getImage(self):
    if self._frameno == 0:
        self._frameno += 1
        return Image.new('RGB', (self.width, self.height), self.color)
    else:
        time.sleep(1)
        return None

