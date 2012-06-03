import urllib2
from xml.dom.minidom import parse

class BOM:
  def __init__(self):
    self._url = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDV10753.xml'
    self.refreshData()

  def refreshData(self):
    self._wdom = parse(urllib2.urlopen(self._url))

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
