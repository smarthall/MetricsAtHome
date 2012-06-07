import Image, ImageFont, ImageDraw
import datetime, time
import Data.YarraTrams

class TramScreen:
  def __init__(self):
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
    self._textcolor = (0, 0, 0)

    # Setup API
    api = Data.YarraTrams.YarraTrams('2125f4e4-5026-4660-84ad-76740dee460b')

    # Grab arriving trams
    citynext = api.GetNextPredictedRoutesCollection(self._homestopcity, 109)
    boxnext = api.GetNextPredictedRoutesCollection(self._homestopbox, 109)

    # Get the times and tram numbers
    self._cityarr  = citynext[0]['PredictedArrivalDateTime']
    self._citytram = citynext[0]['VehicleNo']
    self._boxarr   = boxnext[0]['PredictedArrivalDateTime']
    self._boxtram  = boxnext[0]['VehicleNo']

    #Get the schedules for those trams
    try:
      (citytdetails, citytstops) = api.GetNextPredictedArrivalTimeAtStopsForTramNo(self._citytram)
      (boxtdetails, boxtstops) = api.GetNextPredictedArrivalTimeAtStopsForTramNo(self._boxtram)

      # Process into dicts
      citypred = {}
      boxpred = {}
      try:
        for p in citytstops:
          citypred[int(p['StopNo'])] = p['PredictedArrivalDateTime']
      except KeyError:
        citypred = {}

      try:
        for p in boxtstops:
          boxpred[int(p['StopNo'])] = p['PredictedArrivalDateTime']
      except KeyError:
        boxpred = {}

      # Get the interesting data
      self._arrkate = citypred.get(self._katestop)
      self._arrdan  = citypred.get(self._danstop)
      self._arrbox  = boxpred.get(self._boxstop)
    except ValueError:
      self._arrkate = None
      self._arrdan  = None
      self._arrbox  = None

    #TODO: Get all next three trams

  def getInfo(self):
    return {
      'duration':     60,
      'name':         'Yarra Trams screen',
    }

  def getImage(self, width, height):
    if self._nextupd < time.time():
        self._nextupd = time.time() + 1

        im = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(im)

        # Get the deltas
        boxdelta = self._boxarr - datetime.datetime.now()
        citydelta = self._cityarr - datetime.datetime.now()

        # Then in seconds/minutes
        (citywaitm, citywaits) = divmod(citydelta.total_seconds(), 60)
        (boxwaitm,  boxwaits)  = divmod(boxdelta.total_seconds(),  60)

        # Tram times
        draw.text((0, 0), "Tram Times", font=self._font, fill=self._textcolor)
        draw.text((0, 20), "To City: %s minutes" % int(citywaitm), font=self._font, fill=self._textcolor)
        draw.text((0, 300), "To Box Hill: %s minutes" % int(boxwaitm), font=self._font, fill=self._textcolor)

        # Stop arrivals
        if self._arrkate != None:
          draw.text((0, 40), "Arrives Kate's work: %s" % self._arrkate.strftime('%I:%M%p'), font=self._font, fill=self._textcolor)
        if self._arrdan != None:
          draw.text((0, 80), "Arrives Dan's work: %s" % self._arrdan.strftime('%I:%M%p'), font=self._font, fill=self._textcolor)
        if self._arrbox != None:
          draw.text((0, 340), "Arrives Box Hill: %s" % self._arrbox.strftime('%I:%M%p'), font=self._font, fill=self._textcolor)

	# Updated time
        draw.text((0, 500), "Updated: %s" % datetime.datetime.now().strftime('%I:%M:%S%p'), font=self._font, fill=self._textcolor)

        return im
    else:
        return None

