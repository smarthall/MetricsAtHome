import Image, ImageDraw, ImageFont
import time
import StringIO
from Data.BOM import BOM
import BaseScreen

class WeatherScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._nextupd = time.time()
    self.width = width
    self.height = height
    self._framespeed = 0.5
    self._dayfont = ImageFont.truetype('font/DejaVuSans.ttf',     22)
    self._mainfont = ImageFont.truetype('font/DejaVuSans.ttf',    24)
    self._daytempfont = ImageFont.truetype('font/DejaVuSans.ttf', 36)
    self._tempfont = ImageFont.truetype('font/DejaVuSans.ttf',    72)
    self._textcolor = (0,   0,   0)
    self._maxcolor  = (255, 0,   0)
    self._mincolor  = (50,   50,   255)
    self._bomxml = args.get('xmlfile', 'IDV10753.xml')
    self._bomarea = args.get('weatherdistrict', 'VIC_PT042')
    self._bomradarcode = args.get('radarcode', '023')

    self._wicon = []
    for i in range(1, 17):
      im = Image.open('img/icons/' + str(i) + '.png').convert('RGBA')
      im = im.resize((83, 83), Image.BICUBIC)
      self._wicon.append(im)

    bomapi = BOM()
    self._wdata = bomapi.getData(self._bomarea, self._bomxml)
    self._radarloop = bomapi.getRadarLoop(self._bomradarcode)
    self._rimg = 0

  def getImage(self):
    if self._nextupd >= time.time():
      time.sleep(self._framespeed / 10)
      return None
    self._nextupd = time.time() + self._framespeed

    im = Image.open('img/WeatherBack.png')
    draw = ImageDraw.Draw(im)

    # Todays data
    today = self._wdata[0]
    maxtext = today.get('air_temperature_maximum', '')
    mintext = today.get('air_temperature_minimum', '')
    im.paste(self._wicon[int(today['forecast_icon_code']) - 1], (42, 81), self._wicon[int(today['forecast_icon_code']) - 1])
    draw.text((87, 42), today['date'].strftime('%A %d %B %Y'), font=self._mainfont, fill=self._textcolor)
    draw.text((179, 81), maxtext, font=self._tempfont, fill=self._maxcolor)
    draw.text((315, 81), mintext, font=self._tempfont, fill=self._mincolor)
    draw.text((42, 183), today['precis'], font=self._mainfont, fill=self._textcolor)

    # The next few days
    xoffsets = [20, 156, 292]
    yoffsets = [230, 400]
    for i in range(1, 7):
      pred = self._wdata[i]
      xoff = xoffsets[(i - 1) % 3]
      yoff = yoffsets[int((i - 1) / 3)]
      
      im.paste(self._wicon[int(pred['forecast_icon_code']) - 1], (xoff + 22, yoff + 20), self._wicon[int(pred['forecast_icon_code']) - 1])
      draw.text((xoff + 22, yoff + 8), pred['date'].strftime('%a'), font=self._dayfont, fill=self._textcolor)
      draw.text((xoff + 22, yoff + 113), pred['air_temperature_maximum'], font=self._daytempfont, fill=self._maxcolor)
      draw.text((xoff + 67, yoff + 113), pred['air_temperature_minimum'], font=self._daytempfont, fill=self._mincolor)

    # Put the radar in
    self._rimg = (self._rimg + 1) % len(self._radarloop)
    im.paste(self._radarloop[self._rimg], (470, 30), self._radarloop[self._rimg])

    return im

