import Image, ImageDraw

class BarGraph():
  def __init__(self, width, height, data):
    self.size = (width, height)
    self.data = data
    self.needsredraw = True

  def setSize(width, height):
    self.size = (width, height)
    self.needsredraw = True

  def setData(data):
    self.data = data
    self.needsredraw = True

  def _redraw():
    # Make image
    im = Image.new('RGBA', self.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)

    # Pre calculations
    xscaling = max(data) / height
    barwidth = width / len(data)

    # Draw
    i = 0
    for d in data:
      bh = 

    #Save image
    self.im = im
    needsredraw = False

  def getImage():
    if needsredraw:
      self._redraw()

    return self.im




