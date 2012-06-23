import Image, ImageFont, ImageDraw
import datetime, time
import Data.YarraTrams
import BaseScreen

class TramScreenV2(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._nextupd = time.time()

    # Data
    self._tramline     = 109
    self._homestopcity = 1749 # Northcote Road to City
    self._homestopbox  = 2749 # Northcote Road to Box Hill
    self._katestop     = 3508 # 101 Collins Street to City
    self._danstop      = 1725 # River Blvd to City
    self._boxstop      = 2757 # Box Hill to Box Hill

    # Design files
    self._font =  ImageFont.truetype('font/DejaVuSans.ttf', 18)
    self._minutefont =  ImageFont.truetype('font/DejaVuSans.ttf', 24)
    self._titlefont =  ImageFont.truetype('font/DejaVuSans.ttf', 48)
    self._timefont =  ImageFont.truetype('font/DejaVuSans.ttf', 44)
    self._bigfont =  ImageFont.truetype('font/DejaVuSans.ttf', 175)
    self._textcolor = (0, 0, 0)

    # Setup API
    api = Data.YarraTrams.YarraTrams()

    # Grab arriving trams
    citynext = api.GetNextPredictedRoutesCollection(self._homestopcity, self._tramline)

    # Get the times and tram numbers
    self._cityarr      = citynext[0]['PredictedArrivalDateTime']
    self._citytram     = citynext[0]['VehicleNo']
    self._cityarrnext  = citynext[1]['PredictedArrivalDateTime']
    self._citytramnext = citynext[1]['VehicleNo']

    #Get the schedules for those trams
    try:
      (citytdetails, citytstops) = api.GetNextPredictedArrivalTimeAtStopsForTramNo(self._citytram)
      (citytdetailsnext, citytstopsnext) = api.GetNextPredictedArrivalTimeAtStopsForTramNo(self._citytramnext)

      # Process into dicts
      citypred = {}
      cityprednext = {}
      try:
        for p in citytstops:
          citypred[int(p['StopNo'])] = p['PredictedArrivalDateTime']
      except KeyError:
        citypred = {}
      try:
        for p in citytstopsnext:
          cityprednext[int(p['StopNo'])] = p['PredictedArrivalDateTime']
      except KeyError:
        cityprednext = {}

      # Get the interesting data
      self._arrkate = citypred.get(self._katestop)
      self._arrdan  = citypred.get(self._danstop)
      self._arrkatenext = cityprednext.get(self._katestop)
      self._arrdannext  = cityprednext.get(self._danstop)
    except ValueError:
      self._arrkate = None
      self._arrdan  = None
      self._arrkatenext = None
      self._arrdannext  = None

    #TODO: Get all next three trams

    # Prepare the basic image
    self._im = Image.new('RGB', (1024, 600), (255, 255, 255))
    draw = ImageDraw.Draw(self._im)
    draw.text((24,  248), 'Minutes', font=self._minutefont, fill=self._textcolor)
    draw.text((536, 248), 'Minutes', font=self._minutefont, fill=self._textcolor)
    draw.text((190,   5), 'Now', font=self._minutefont, fill=self._textcolor)
    draw.text((712,   5), 'Next', font=self._minutefont, fill=self._textcolor)
    draw.text((290,  80), 'Dan\'s Work', font=self._minutefont, fill=self._textcolor)
    draw.text((802,  80), 'Dan\'s Work', font=self._minutefont, fill=self._textcolor)
    draw.text((290, 170), 'Kate\'s Work', font=self._minutefont, fill=self._textcolor)
    draw.text((802, 170), 'Kate\'s Work', font=self._minutefont, fill=self._textcolor)

  def getImage(self):
    if self._nextupd < time.time():
        self._nextupd = time.time() + 1
        
        im = self._im.copy()
        draw = ImageDraw.Draw(im)

        # Get the deltas
        citydelta = self._cityarr - datetime.datetime.now()
        (citywaitm, citywaits) = divmod(citydelta.total_seconds(), 60)
        citydeltanext = self._cityarrnext - datetime.datetime.now()
        (citywaitmnext, citywaitsnext) = divmod(citydeltanext.total_seconds(), 60)

        # Tram times
        draw.text((14, 80), str(int(citywaitm)), font=self._bigfont, fill=self._textcolor)
        draw.text((526, 80), str(int(citywaitmnext)), font=self._bigfont, fill=self._textcolor)

        # Stop arrivals
        if self._arrkate != None:
          draw.text((290, 200), self._arrkate.strftime('%I:%M%p'), font=self._timefont, fill=self._textcolor)
        if self._arrdan != None:
          draw.text((290, 110), self._arrdan.strftime('%I:%M%p'), font=self._timefont, fill=self._textcolor)
        if self._arrkatenext != None:
          draw.text((802, 200), self._arrkatenext.strftime('%I:%M%p'), font=self._timefont, fill=self._textcolor)
        if self._arrdannext != None:
          draw.text((802, 110), self._arrdannext.strftime('%I:%M%p'), font=self._timefont, fill=self._textcolor)

	# Updated time
        draw.text((0, 500), "Updated: %s" % datetime.datetime.now().strftime('%I:%M:%S%p'), font=self._font, fill=self._textcolor)

        return im
    else:
        time.sleep(0.1)
        return None

