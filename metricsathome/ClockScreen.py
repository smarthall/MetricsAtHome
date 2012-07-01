import time, datetime
import Image, ImageFont
import BaseScreen
import FancyDraw

class ClockScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._nextframe = 0
    self.width = width
    self.height = height
    self.color = self.HTMLColorToPILColor(args.get('color', '#000000'))
    self.textcolor = self.HTMLColorToPILColor(args.get('textcolor', '#FFFFFF'))
    self.fontfile = args.get('fontfile', 'font/DejaVuSans.ttf')
    self.timefontsize = args.get('timefontsize', 120)
    self.datefontsize = args.get('datefontsize', 36)
    self.timefont = ImageFont.truetype(self.fontfile, self.timefontsize)
    self.datefont = ImageFont.truetype(self.fontfile, self.datefontsize)
    self.timeformat = args.get('timeformat', '%-I:%M%p')
    self.dateformat = args.get('dateformat', '%A %d %B %Y')

  def HTMLColorToPILColor(self, colorstring):
    """ converts #RRGGBB to PIL-compatible integers"""
    colorstring = colorstring.strip()
    while colorstring[0] == '#': colorstring = colorstring[1:]
    # get bytes in reverse order to deal with PIL quirk
    colorstring = colorstring[-2:] + colorstring[2:4] + colorstring[:2]
    # finally, make it numeric
    color = int(colorstring, 16)
    return color

  def getImage(self):
    if time.time() > self._nextframe:
        self._nextframe = time.time() + 1
        timestr = datetime.datetime.now().strftime(self.timeformat)
        datestr = datetime.datetime.now().strftime(self.dateformat)
        im = Image.new('RGB', (self.width, self.height), self.color)
        draw = FancyDraw.FancyDraw(im)
        x = self.width / 2
        timey = self.height / 2
        datey = self.height / 2 + self.height / 8
        draw.ctext((x, timey), timestr, font=self.timefont,
                   fill=self.textcolor, center='both')
        draw.ctext((x, datey), datestr, font=self.datefont,
                   fill=self.textcolor, center='both')
        return im

    else:
        time.sleep(0.5)
        return None

