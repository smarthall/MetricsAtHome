
import Image

class WhiteScreen:
  def __init__(self):
    self._frameno = 0

  def getInfo(self):
    return {
      'duration':     5,
      'name':         'White Screen',
    }

  def getImage(self, width, height):
    if self._frameno == 0:
        self._frameno += 1
        return Image.new('RGB', (width, height), (255, 255, 255))
    else:
        return None

