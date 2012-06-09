import urllib2
import Image
from xml.dom.minidom import parse
import dateutil.parser
from datetime import timedelta
from cStringIO import StringIO

class BOM:
  def __init__(self):
    self._xmlurl = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDV10753.xml'
    self._radarbaseurl = 'ftp://ftp2.bom.gov.au/anon/gen/radar/IDR'

  def getData(self, aac):
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
    return forecasts


  def getRadar(self, code):
    img_file = urllib2.urlopen(self._radarbaseurl + code + '.gif' )
    imdata = StringIO(img_file.read())
    return Image.open(imdata)

