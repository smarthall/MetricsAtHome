
import Image

class BlackScreen:
  def __init__(self):
    self._frameno = 0

  def getInfo(self):
    return {
      'duration':     5,
      'name':         'Black Screen',
      'framesleep':   1000,
    }

  def getImage(self, width, height):
    if self._frameno == 0:
        return Image.new('RGB', (width, height), (0, 0, 0))
        self._frameno += 1
    else:
        return None

