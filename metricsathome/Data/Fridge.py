import urllib2
import Cache

fridgeURL = 'http://admin01.int.tildaslash.com/fridge/data/'
modcachekey = 'metricsathome.Data.Fridge'
cachetime = 10

def weight():
  return _updateData()['weight']

def tempA():
  return _updateData()['tempA']

def tempB():
  return _updateData()['tempB']

def _updateData():
  items = ['weight', 'tempA', 'tempB']
  result = {}
  for i in items:
    val = Cache.read(modcachekey + '-' + i)
    if val == None:
      val = float(urllib2.urlopen(fridgeURL + i).read())
      Cache.write(modcachekey + '-' + i, val, cachetime)
    result[i] = val

  return result

