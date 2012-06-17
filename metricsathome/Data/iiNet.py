import urllib2
from xml.dom.minidom import parseString
import Cache
import datetime

iiNetCM = 'https://toolbox.iinet.net.au/cgi-bin/new/volume_usage_xml.cgi?action=login'

def getCurrentMonth(username, password):
  url = iiNetCM + '&username=' + username + '&password=' + password
  cachekey = 'metricsathome.Data.iiNet-(' + iiNetCM + ',' + username + ')'
  xmlstring = Cache.read(cachekey)
  if xmlstring is None:
    xmlstring = urllib2.urlopen(url).read()
    Cache.write(cachekey, xmlstring, 60 * 30)
  xmlDoc = parseString(xmlstring)
  result = {}
  processQuotaReset(xmlDoc.getElementsByTagName('quota_reset')[0], result)
  processExpectedTraffic(xmlDoc.getElementsByTagName('expected_traffic_types')[0], result)
  processDailyUsage(xmlDoc.getElementsByTagName('day_hour'), result)

  return result

def processQuotaReset(xmlNode, results):
  data = filter(lambda a: a.attributes != None, xmlNode.childNodes)
  for n in data:
    results[n.nodeName] = n.firstChild.nodeValue

def processExpectedTraffic(xmlNode, results):
  data = filter(lambda a: a.attributes != None, xmlNode.childNodes)
  types = {}
  for n in data:
    dtype = n.attributes['classification'].nodeValue
    types[dtype] = {}
    types[dtype]['used'] = n.attributes['used'].nodeValue
    children = filter(lambda a: a.attributes != None, n.childNodes)
    for c in children:
      types[dtype][c.nodeName] = c.firstChild.nodeValue
  results['types'] = types

def processDailyUsage(xmlNodes, results):
  data = filter(lambda a: a.attributes != None, xmlNodes)
  usage = {}
  for d in data:
    date = datetime.datetime.strptime(d.attributes['period'].nodeValue, '%Y-%m-%d')
    usage[date] = {}
    children = filter(lambda a: a.attributes != None, d.childNodes)
    for c in children:
      usage[date][c.attributes['type'].nodeValue] = c.firstChild.nodeValue
  results['usage'] = usage

