import Image

class PicScreen:
  def __init__(self):
    self._frameno = 0

  def getInfo(self):
    return {
      'duration':     15,
      'name':         'Picture Screen',
    }

  def getImage(self, width, height):
    if self._frameno == 0:
        return Image.open('img/sample.jpg')
        self._frameno += 1
    else:
        return None

