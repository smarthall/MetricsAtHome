import Image, ImageFont, ImageDraw
import datetime
import Data.YarraTrams

class TramScreen:
  def __init__(self):
    self._frameno = 0

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

    # Get the deltas
    boxdelta = self._boxarr - datetime.datetime.now()
    citydelta = self._cityarr - datetime.datetime.now()

    # Then in seconds/minutes
    self._citywaitm, self._citywaits = divmod(citydelta.total_seconds(), 60)
    self._boxwaitm,  self._boxwaits  = divmod(boxdelta.total_seconds(),  60)

    #TODO: Get the schedules for those trams
    #TODO: Get all next three trams

  def getInfo(self):
    return {
      'duration':     60,
      'name':         'Yarra Trams screen',
    }

  def getImage(self, width, height):
    if self._frameno == 0:
        self._frameno += 1

        im = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(im)

        draw.text((0, 0), "Tram Times", font=self._font, fill=self._textcolor)
        draw.text((0, 80), "To City: %s minutes" % int(self._citywaitm), font=self._font, fill=self._textcolor)
        draw.text((0, 160), "To Box Hill: %s minutes" % int(self._boxwaitm), font=self._font, fill=self._textcolor)

        return im
    else:
        return None

