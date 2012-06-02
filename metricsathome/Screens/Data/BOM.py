import urllib2
from xml.dom.minidom import parse

class BOM:
  def __init__(self):
    self._url = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDV10753.xml'

  def getData(self, aac):
    forecasts = []
    wdom = parse(urllib2.urlopen(self._url))
    areas = wdom.getElementsByTagName('area')
    area = filter(lambda a: a.attributes['aac'].value == aac, areas)[0]
    

