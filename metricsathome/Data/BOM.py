import urllib2
import Image
from xml.dom.minidom import parse
import dateutil.parser
from datetime import timedelta
from cStringIO import StringIO
import Cache

class BOM:
  def __init__(self):
    self._xmlurl = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDV10753.xml'
    self._radarbaseurl = 'ftp://ftp2.bom.gov.au/anon/gen/radar/IDR'
    self._fcasts = None
    self._radarimg = None

  def getData(self, aac):
    self._fcasts = Cache.read('metricsathome.BOM.BOM-data(' + aac + ')');
    if self._fcasts is not None:
      return self._fcasts
    
    self._wdom = parse(urllib2.urlopen(self._xmlurl))
    areas = self._wdom.getElementsByTagName('area')
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

    imdata = StringIO(self._radar)
    return Image.open(imdata)

