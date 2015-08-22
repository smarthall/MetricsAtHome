import time, datetime
import dateutil.parser
from dateutil.tz import *
from PIL import Image, ImageFont
import BaseScreen
import FancyDraw

class CountDownScreen(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    # init
    self._nextframe = 0

    # screen data
    self.width = width
    self.height = height

    # Config
    self.eventtitle = args.get('event', 'Something!')
    self.strdatetime = args.get('datetime', 'Mon Dec 24 00:00:00 EST 2012')

    # Colors
    self.color = self.HTMLColorToPILColor(args.get('color', '#000000'))
    self.textcolor = self.HTMLColorToPILColor(args.get('textcolor', '#FFFFFF'))

    # Standard fonts
    self.fontfile = args.get('fontfile', 'font/DejaVuSans.ttf')
    self.fontsize = args.get('fontsize', 48)
    self.timefontsize = args.get('timefontsize', 80)
    self.timelabelfontsize = args.get('timelabelfontsize', 48)

    # Title font
    self.titlefontfile = args.get('titlefontfile', 'font/DejaVuSans.ttf')
    self.titlefontsize = args.get('titlefontsize', 100)

    # Process options
    self.datetime = dateutil.parser.parse(self.strdatetime)
    self.font = ImageFont.truetype(self.fontfile, self.fontsize)
    self.timefont = ImageFont.truetype(self.fontfile, self.timefontsize)
    self.timelabelfont = ImageFont.truetype(self.fontfile, self.timelabelfontsize)
    self.titlefont = ImageFont.truetype(self.titlefontfile, self.titlefontsize)

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
        timedelta = self.datetime - datetime.datetime.now(tzutc())
        im = Image.new('RGB', (self.width, self.height), self.color)
        draw = FancyDraw.FancyDraw(im)
        titlex = self.width / 2
        draw.ctext((titlex, 0), "Countdown to", font=self.font,
                   fill=self.textcolor, center='horizontal')
        draw.ctext((titlex, self.fontsize + 10), self.eventtitle, font=self.titlefont,
                   fill=self.textcolor, center='horizontal')

        xsector = self.width / 8
        numbery = self.height / 2
        texty = self.height / 2 + self.height / 8

        ttlsec = int(timedelta.total_seconds())
        days = ttlsec / 86400
        ttlsec %= 86400
        hours = ttlsec / 3600
        ttlsec %= 3600
        mins = ttlsec / 60
        ttlsec %= 60
        secs = ttlsec

        # Days
        draw.ctext((xsector * 1, numbery), str(days), font=self.timefont,
                   fill=self.textcolor, center='both')
        draw.ctext((xsector * 1, texty), "days", font=self.timelabelfont,
                   fill=self.textcolor, center='both')

        # Hours
        draw.ctext((xsector * 3, numbery), str(hours), font=self.timefont,
                   fill=self.textcolor, center='both')
        draw.ctext((xsector * 3, texty), "hours", font=self.timelabelfont,
                   fill=self.textcolor, center='both')

        # Minutes
        draw.ctext((xsector * 5, numbery), str(mins), font=self.timefont,
                   fill=self.textcolor, center='both')
        draw.ctext((xsector * 5, texty), "minutes", font=self.timelabelfont,
                   fill=self.textcolor, center='both')

        # Seconds
        draw.ctext((xsector * 7, numbery), str(secs), font=self.timefont,
                   fill=self.textcolor, center='both')
        draw.ctext((xsector * 7, texty), "seconds", font=self.timelabelfont,
                   fill=self.textcolor, center='both')

        return im

    else:
        time.sleep(0.5)
        return None

