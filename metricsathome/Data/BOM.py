import urllib2
import Image
from xml.dom.minidom import parse
import dateutil.parser
from datetime import timedelta
from cStringIO import StringIO
import Cache
from ftplib import FTP


class BOM:
  deflayers = ['background', 'topography', 'range',
               'locations', 'copyright', 'legend.0']

  def __init__(self):
    self._xmlurl = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDV10753.xml'
    self._radarbaseurl = 'ftp://ftp2.bom.gov.au/anon/gen/radar/IDR'
    self._ftphost = 'ftp2.bom.gov.au'
    self._transparentcypath = '/anon/gen/radar_transparencies/'
    self._radarpath = '/anon/gen/radar/'
    self._radarimg = None

  def getData(self, aac):
    forecasts = Cache.read('metricsathome.BOM.BOM-data(' + aac + ')');
    if forecasts is not None:
      return forecasts
    
    wdom = parse(urllib2.urlopen(self._xmlurl))
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

    Cache.write('metricsathome.BOM.BOM-data(' + aac + ')', forecasts, 3600)
    return forecasts


  def getRadar(self, code):
    self._radar = Cache.read('metricsathome.BOM.BOM-radar(' + code + ')');
    if self._radar is None:
      img_file = urllib2.urlopen(self._radarbaseurl + code + '.gif' )
      self._radar = img_file.read()
      Cache.write('metricsathome.BOM.BOM-radar(' + code + ')', self._radar, 360)

    return Image.open(StringIO(self._radar))

  def getRadarLoop(self, code):
    cachekey = 'metricsathome.BOM.BOM-radarloop(' + code + ')'
    loopback = self.buildLoopBack(code)

  def buildLoopBack(self, code, layers=deflayers):
    cachekey = 'metricsathome.BOM.BOM-loopback(' + code + ',(' + ','.join(layers) + '))'
    
    background = Cache.read(cachekey);
    if background is not None:
      return Image.open(StringIO(background))

    im = Image.new('RGBA', (524, 564), (255, 255, 255))

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

