import Image, ImageDraw

class BarGraph():
  def __init__(self, width, height, data):
    self.size = (width, height)
    self.data = data
    self.color = (0, 200, 30)
    self.needsredraw = True

  def setSize(self, width, height):
    self.size = (width, height)
    self.needsredraw = True

  def setData(self, data):
    self.data = data
    self.needsredraw = True

  def setColor(self, red, green, blue):
    self.color = (red, green, blue)
    self.needsredraw = True

  def _redraw(self):
    # Make image
    im = Image.new('RGBA', self.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)

    # Gather data
    height = self.size[1]
    width = self.size[0]

    # Pre calculations
    yscaling = float(height) / max(self.data)
    barwidth = width / len(self.data)

    # Draw
    i = 0
    for d in self.data:
      # Get the height of the bar
      barheight = d * yscaling

      # Get the rectangle coords
      lx = i * barwidth
      rx = (i + 1) * barwidth
      ty = height - barheight
      by = height

      # Draw the rectangle
      draw.rectangle([lx, ty, rx, by], fill=self.color)

      # Move across one bar
      i += 1

    #Save image
    self.im = im
    needsredraw = False

  def getImage(self):
    if self.needsredraw:
      self._redraw()

    return self.im




