import urllib2
import Image
from xml.dom.minidom import parse
from cStringIO import StringIO

class BOM:
  def __init__(self):
    self._xmlurl = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDV10753.xml'
    self._radarbaseurl = 'ftp://ftp2.bom.gov.au/anon/gen/radar/IDR'
    self.refreshData()

  def refreshData(self):
    self._wdom = parse(urllib2.urlopen(self._xmlurl))

  def getData(self, aac):
    areas = self._wdom.getElementsByTagName('area')
    area = filter(lambda a: a.attributes['aac'].value == aac, areas)[0]
    fcasts = filter(lambda a: a.attributes != None, area.childNodes)
    forecasts = []
    for f in fcasts:
      values = {}
      for e in f.getElementsByTagName('element'):
        values[e.attributes['type'].value] = e.firstChild.nodeValue
      for e in f.getElementsByTagName('text'):
        values[e.attributes['type'].value] = e.firstChild.nodeValue
      forecasts.append(values)
    return forecasts


  def getRadar(self, code):
    img_file = urllib2.urlopen(self._radarbaseurl + code + '.gif' )
    imdata = StringIO(img_file.read())
    return Image.open(imdata)

