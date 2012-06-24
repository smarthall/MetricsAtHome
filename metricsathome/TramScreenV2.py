import Image, ImageFont, ImageDraw
import datetime, time
import Data.YarraTrams
import BaseScreen

class TramScreenV2(BaseScreen.BaseScreen):
  def __init__(self, width, height, args):
    self._nextupd = time.time()

    # Data
    self._tramline     = args['routeno']
    self._stop         = args['stopno']
    self._firststop    = args['firststopnum']
    self._firststopstr = args['firststopname']
    self._secondstop   = args['secondstopnum']
    self._secondstopstr= args['secondstopname']

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
    tnext = api.GetNextPredictedRoutesCollection(self._stop, self._tramline)

    # Get the times and tram numbers
    self._arr        = tnext[0]['PredictedArrivalDateTime']
    self._tramno     = tnext[0]['VehicleNo']
    self._arrnext    = tnext[1]['PredictedArrivalDateTime']
    self._tramnonext = tnext[1]['VehicleNo']

    #Get the schedules for those trams
    try:
      (tdetails, tstops) = api.GetNextPredictedArrivalTimeAtStopsForTramNo(self._tramno)
      (tdetailsnext, tstopsnext) = api.GetNextPredictedArrivalTimeAtStopsForTramNo(self._tramnonext)

      # Process into dicts
      pred = {}
      prednext = {}
      try:
        for p in tstops:
          pred[int(p['StopNo'])] = p['PredictedArrivalDateTime']
      except KeyError:
        pred = {}
      try:
        for p in tstopsnext:
          prednext[int(p['StopNo'])] = p['PredictedArrivalDateTime']
      except KeyError:
        prednext = {}

      # Get the interesting data
      self._arrfirst       = pred.get(self._firststop)
      self._arrsecond      = pred.get(self._secondstop)
      self._arrfirstnext   = prednext.get(self._firststop)
      self._arrsecondnext  = prednext.get(self._secondstop)
    except ValueError:
      self._arrfirst      = None
      self._arrsecond     = None
      self._arrfirstnext  = None
      self._arrsecondnext = None

    #TODO: Get all next three trams

    # Prepare the basic image
    self._im = Image.open('img/TramScreenBack.png')
    draw = ImageDraw.Draw(self._im)
    draw.text((24,  248), 'Minutes', font=self._minutefont, fill=self._textcolor)
    draw.text((536, 248), 'Minutes', font=self._minutefont, fill=self._textcolor)
    draw.text((190,   5), 'Now', font=self._minutefont, fill=self._textcolor)
    draw.text((712,   5), 'Next', font=self._minutefont, fill=self._textcolor)
    draw.text((290,  80), self._firststopstr, font=self._minutefont, fill=self._textcolor)
    draw.text((802,  80), self._firststopstr, font=self._minutefont, fill=self._textcolor)
    draw.text((290, 170), self._secondstopstr, font=self._minutefont, fill=self._textcolor)
    draw.text((802, 170), self._secondstopstr, font=self._minutefont, fill=self._textcolor)

  def getImage(self):
    if self._nextupd < time.time():
        self._nextupd = time.time() + 1
        
        im = self._im.copy()
        draw = ImageDraw.Draw(im)

        # Get the deltas
        delta = self._arr - datetime.datetime.now()
        (waitm, waits) = divmod(delta.total_seconds(), 60)
        deltanext = self._arrnext - datetime.datetime.now()
        (waitmnext, waitsnext) = divmod(deltanext.total_seconds(), 60)

        # Tram times
        draw.text((14, 80), str(int(waitm)), font=self._bigfont, fill=self._textcolor)
        draw.text((526, 80), str(int(waitmnext)), font=self._bigfont, fill=self._textcolor)

        # Stop arrivals
        if self._arrfirst != None:
          draw.text((290, 110), self._arrfirst.strftime('%I:%M%p'), font=self._timefont, fill=self._textcolor)
        if self._arrsecond != None:
          draw.text((290, 200), self._arrsecond.strftime('%I:%M%p'), font=self._timefont, fill=self._textcolor)
        if self._arrfirstnext != None:
          draw.text((802, 110), self._arrfirstnext.strftime('%I:%M%p'), font=self._timefont, fill=self._textcolor)
        if self._arrsecondnext != None:
          draw.text((802, 200), self._arrsecondnext.strftime('%I:%M%p'), font=self._timefont, fill=self._textcolor)

	# Updated time
        draw.text((0, 500), "Updated: %s" % datetime.datetime.now().strftime('%I:%M:%S%p'), font=self._font, fill=self._textcolor)

        return im
    else:
        time.sleep(0.1)
        return None

