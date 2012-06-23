import Image, ImageFont, ImageDraw
import datetime, time
import Data.iiNet
import BaseScreen



class iiNetScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._frame = 0

    self.width = width
    self.height = height
    
    data = Data.iiNet.getCurrentMonth(args['user'], args['pass'])
    usage = data['usage']

    im = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    amax = max(map(lambda a: int(a['anytime']), usage.values()))
    
    i = 0
    barwidth = width / len(usage.keys())
    for k in sorted(usage.keys()):
      bh = float(usage[k]['anytime']) / amax * height
      lx = i * barwidth
      rx = lx + barwidth
      ty = height - bh
      by = height
      draw.rectangle([lx, ty, rx, by], fill=(0, 200, 30))
      i += 1
      
    self._im = im

  def getImage(self):
    if self._frame == 0:
        self._frame = 1

        return self._im
    else:
        time.sleep(1)
        return None

