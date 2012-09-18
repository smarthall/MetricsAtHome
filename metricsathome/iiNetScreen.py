import Image, ImageFont, ImageDraw
import datetime, time
import Data.iiNet
import BaseScreen
import ImageBuilder



class iiNetScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._frame = 0

    self.width = width
    self.height = height

    data = Data.iiNet.getCurrentMonth(args['user'], args['pass'])
    usage = data['usage']

    im = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    data = []
    for k in sorted(usage.keys()):
      data.append(int(usage[k]['anytime']))

    ib = ImageBuilder.BarGraph(width, height, data)

    self._im = ib.getImage()

  def getImage(self):
    if self._frame == 0:
        self._frame = 1

        return self._im
    else:
        time.sleep(1)
        return None

