import ImageDraw

class FancyDraw(ImageDraw.ImageDraw):
  def __init__(self, image):
    self._im = image
    ImageDraw.ImageDraw.__init__(self, image)

  def _getcentering(self, axis):
    if axis == 'both':
      return (True, True)
    elif axis.startswith('horiz'):
      return (True, False)
    elif axis.startswith('vert'):
      return (False, True)

  def ctext(self, pos, text, **kwargs):
    (x, y) = pos
    (ch, cv) = self._getcentering(kwargs.pop('center', 'none'))

    if ch:
      x -= self.textsize(text, font=kwargs.get('font'))[0] / 2
    if cv:
      y -= self.textsize(text, font=kwargs.get('font'))[1] / 2

    return self.text((x, y), text, **kwargs)

  def cpaste(self, image, pos, **kwargs):
    (x, y) = pos
    mask = kwargs.get('mask', image)
    (ch, cv) = self._getcentering(kwargs.pop('center', 'none'))

    if ch:
      x -= image.size[0] / 2
    if cv:
      y -= image.size[1] / 2

    self._im.paste(image, (x, y), mask)

