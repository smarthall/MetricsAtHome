import Image, ImageFont, FancyDraw
import datetime, time
import Data.iiNet
import BaseScreen
import ImageBuilder



class iiNetScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    # Get config
    username = args['user']
    password = args['pass']

    # Design files
    font =  ImageFont.truetype('font/DejaVuSans.ttf', 17)
    textcolor = (0, 0, 0)

    # Get dimensions
    self.width = width
    self.height = height

    # Record frame numbers
    self._frame = 0

    # Connect to iiNet, grab usage data
    data = Data.iiNet.getCurrentMonth(username, password)
    usage = data['usage']

    # Build a Bar Graph
    data = []
    for k in sorted(usage.keys()):
      data.append(int(usage[k]['anytime']))

    ib = ImageBuilder.BarGraph(width - (width / 20), height - (height / 10), data)

    # Make our image
    im = Image.new('RGB', (width, height), (255, 255, 255))
    draw = FancyDraw.FancyDraw(im)

    # Paste the chart onto the frame
    draw.cpaste(ib.getImage(), (width / 2, height / 10), center='horizontally')

    # Save the frame
    self._im = im

  def getImage(self):
    if self._frame == 0:
        self._frame = 1

        return self._im
    else:
        time.sleep(1)
        return None

