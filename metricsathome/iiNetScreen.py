from PIL import Image, ImageFont, FancyDraw
import datetime, time
import Data.iiNet
import BaseScreen
import ImageBuilder



class iiNetScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    # Get config
    username = args['user']
    password = args['pass']
    fontfile = args.get('fontfile', 'font/DejaVuSans.ttf')

    # Design files
    font = ImageFont.truetype(fontfile, 36)
    smallfont = ImageFont.truetype(fontfile, 24)
    textcolor = (0, 0, 0)

    # Get dimensions
    self.width = width
    self.height = height

    # Record frame numbers
    self._frame = 0

    # Connect to iiNet, grab usage data
    data = Data.iiNet.getCurrentMonth(username, password)
    usage = data['usage']
    gb_used = int(data['types']['anytime']['used']) / 1024 / 1024 / 1024
    usedstr = 'Data used: ' + str(int(gb_used)) + ' Gb'

    # Build a Bar Graph
    udata = []
    for k in sorted(usage.keys()):
      udata.append(int(usage[k]['anytime']))

    ib = ImageBuilder.BarGraph(width - (width / 20), height - (height / 5), udata)

    # Make our image
    im = Image.new('RGB', (width, height), (255, 255, 255))
    draw = FancyDraw.FancyDraw(im)

    # Assemble Frame
    draw.cpaste(ib.getImage(), (width / 2, height / 5), center='horizontally')
    draw.ctext((width / 2, 0), 'iiNet Usage', font=font, fill=textcolor, center='horizontally')
    draw.ctext((width / 2, 40), usedstr, font=smallfont, fill=textcolor, center='horizontally')

    # Save the frame
    self._im = im

  def getImage(self):
    if self._frame == 0:
        self._frame = 1

        return self._im
    else:
        time.sleep(1)
        return None

