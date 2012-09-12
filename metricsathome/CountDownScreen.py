import time, datetime
import dateutil.parser
from dateutil.tz import *
import Image, ImageFont
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
        ttlsec = int(timedelta.total_seconds())
        secs = ttlsec % 60
        ttlsec -= secs
        mins = ttlsec % 3600 / 60
        ttlsec -= mins
        hours = ttlsec % 86400 / 3600
        ttlsec -= hours
        days = ttlsec / 86400

        # Days
        draw.ctext((xsector * 1, 300), str(days), font=self.timefont,
                   fill=self.textcolor, center='horizontal')
        draw.ctext((xsector * 1, 370), "days", font=self.timelabelfont,
                   fill=self.textcolor, center='horizontal')

        # Hours
        draw.ctext((xsector * 3, 300), str(hours), font=self.timefont,
                   fill=self.textcolor, center='horizontal')
        draw.ctext((xsector * 3, 370), "hours", font=self.timelabelfont,
                   fill=self.textcolor, center='horizontal')

        # Minutes
        draw.ctext((xsector * 5, 300), str(mins), font=self.timefont,
                   fill=self.textcolor, center='horizontal')
        draw.ctext((xsector * 5, 370), "minutes", font=self.timelabelfont,
                   fill=self.textcolor, center='horizontal')

        # Seconds
        draw.ctext((xsector * 7, 300), str(secs), font=self.timefont,
                   fill=self.textcolor, center='horizontal')
        draw.ctext((xsector * 7, 370), "seconds", font=self.timelabelfont,
                   fill=self.textcolor, center='horizontal')

        return im

    else:
        time.sleep(0.5)
        return None

