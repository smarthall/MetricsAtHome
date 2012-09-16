import urllib2
from xml.dom.minidom import parseString
import Cache
import datetime

iiNetCM = 'https://toolbox.iinet.net.au/cgi-bin/new/volume_usage_xml.cgi?action=login'

def getCurrentMonth(username, password):
  # Try to return from cache
  cachekey = 'metricsathome.Data.iiNet-(' + iiNetCM + ',' + username + ')'
  iinetusage = Cache.read(cachekey)
  if iinetusage is not None:
    return iinetusage

  # Fall back to the net
  url = iiNetCM + '&username=' + username + '&password=' + password
  xmlstring = urllib2.urlopen(url).read()
  xmlDoc = parseString(xmlstring)
  if len(xmlDoc.getElementsByTagName('error')):
    raise Exception('iiNet API Error: ' + xmlDoc.getElementsByTagName('error')[0].firstChild.nodeValue)
  result = {}
  processQuotaReset(xmlDoc.getElementsByTagName('quota_reset')[0], result)
  processExpectedTraffic(xmlDoc.getElementsByTagName('expected_traffic_types')[0], result)
  processDailyUsage(xmlDoc.getElementsByTagName('day_hour'), result)

  # Save in cache
  Cache.write(cachekey, result, 7200)

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

