import urllib2
try:
  import Image
except ImportError:
  from PIL import Image

from xml.dom.minidom import parse
import dateutil.parser
from datetime import timedelta
from cStringIO import StringIO
import Cache
from ftplib import FTP


class BOM:
  deflayers = ['background', 'topography', 'range',
               'locations', 'copyright', 'legend.0']
  backlayers = ['background', 'topography']
  forelayers = ['range', 'locations', 'copyright', 'legend.0']
  modcachekey = 'metricsathome.Data.BOM'

  def __init__(self):
    self._xmlbase = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/'
    self._radarbaseurl = 'ftp://ftp2.bom.gov.au/anon/gen/radar/IDR'
    self._ftphost = 'ftp2.bom.gov.au'
    self._transparentcypath = '/anon/gen/radar_transparencies/'
    self._radarpath = '/anon/gen/radar/'
    self._radarimg = None

  def getData(self, aac, xml):
    "Get XML codes here: http://www.bom.gov.au/info/precis_forecasts.shtml"
    forecasts = Cache.read(BOM.modcachekey + '-data(' + aac + ',' + xml + ')')
    if forecasts is not None:
      return forecasts

    wdom = parse(urllib2.urlopen(self._xmlbase + xml))
    areas = wdom.getElementsByTagName('area')
    area = filter(lambda a: a.attributes['aac'].value == aac, areas)[0]
    fcasts = filter(lambda a: a.attributes != None, area.childNodes)
    forecasts = []
    for f in fcasts:
      values = {}
      values['date'] = dateutil.parser.parse(f.attributes['end-time-local'].value) - timedelta(days=1)
      for e in f.getElementsByTagName('element'):
        values[e.attributes['type'].value] = e.firstChild.nodeValue
      for e in f.getElementsByTagName('text'):
        values[e.attributes['type'].value] = e.firstChild.nodeValue
      forecasts.append(values)
    forecasts = sorted(forecasts, key=lambda f: f['date'])

    Cache.write(BOM.modcachekey + '-data(' + aac + ')', forecasts, 3600)
    return forecasts


  def getRadar(self, code):
    self._radar = Cache.read(BOM.modcachekey + '-radar(' + code + ')')
    if self._radar is None:
      img_file = urllib2.urlopen(self._radarbaseurl + code + '.gif' )
      self._radar = img_file.read()
      Cache.write(BOM.modcachekey + '-radar(' + code + ')', self._radar, 360)

    return Image.open(StringIO(self._radar))

  def getRadarLoop(self, code):
    rdrimgs = []
    cachekey = BOM.modcachekey + '-radarloop(' + code + ')'
    rdrloopstr = Cache.read(cachekey)
    if rdrloopstr is not None:
      for s in rdrloopstr:
        rdrimgs.append(Image.open(StringIO(s)).convert('RGBA'))
      return rdrimgs

    background = self.buildOverlay(code, BOM.backlayers)
    foreground = self.buildOverlay(code, BOM.forelayers)

    ftp = FTP(self._ftphost)
    ftp.login()
    ftp.cwd(self._radarpath)
    files = ftp.nlst('IDR' + code + '.T.*.png')

    for f in files:
      ftpcachekey = BOM.modcachekey + '-ftp://' + self._ftphost + self._radarpath + f
      imgstr = Cache.read(ftpcachekey)
      imageio = None
      if imgstr is not None:
        imageio = StringIO(imgstr)
      else:
        imgget = StringIO()
        ftp.retrbinary('RETR ' + f, imgget.write)
        Cache.write(ftpcachekey, imgget.getvalue(), 10800)
        imageio = StringIO(imgget.getvalue())
        imgget.close()
      try:
        rdrtrans = Image.open(imageio).convert('RGBA')
        im = Image.new('RGBA', (512, 564), (255, 255, 255, 0))
        im.paste(background, (0, 0), background)
        im.paste(rdrtrans, (0, 0), rdrtrans)
        im.paste(foreground, (0, 0), foreground)
        rdrimgs.append(im)
      except IOError:
        print 'WARNING: BOM is including bad images again';

    rdrloopstr = []
    for i in rdrimgs:
      imgout = StringIO()
      i.save(imgout, format='PNG')
      rdrloopstr.append(imgout.getvalue())

    Cache.write(cachekey, rdrloopstr, 360)

    return rdrimgs

  def buildOverlay(self, code, layers=deflayers):
    cachekey = BOM.modcachekey + '-overlay(' + code + ',(' + ','.join(layers) + '))'

    background = Cache.read(cachekey)
    if background is not None:
      return Image.open(StringIO(background))

    im = Image.new('RGBA', (512, 564), (255, 255, 255, 0))

    ftp = FTP(self._ftphost)
    ftp.login()
    ftp.cwd(self._transparentcypath)
    files = ftp.nlst('IDR' + code + '.*.png')
    files += ftp.nlst('IDR.*.png')

    alllayers = {}
    for f in files:
       b = f.find('.') + 1
       e = f.rfind('.')
       alllayers[f[b:e]] = f

    for l in layers:
      imgout = StringIO()
      ftp.retrbinary('RETR ' + alllayers[l], imgout.write)
      imgin = StringIO(imgout.getvalue())
      img = Image.open(imgin).convert('RGBA')
      im.paste(img, (0,0), img)
      imgout.close()
      imgin.close()

    imgout = StringIO()
    im.save(imgout, format='PNG')
    Cache.write(cachekey, imgout.getvalue(), 604800) # cache for a week
    imgout.close()

    return im

