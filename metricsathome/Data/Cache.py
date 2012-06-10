import time
import cPickle as pickle
import datetime

_dict = {}
filename = None

def write(key, value, expiry):
  _dict[key] = (time.time() + expiry, value)
  if filename is not None:
    todisk()

def read(key):
  try:
    (expiry, value) = _dict[key]
  except KeyError:
    gc()
    return None
  if time.time() < expiry:
    return value
  else:
    return None

def ttl(key):
  try:
    (expiry, value) = _dict[key]
  except KeyError:
    gc()
    return 0
  ttl = expiry - time.time()
  if ttl > 0:
    return ttl
  else:
    return 0

def gc():
  for k in _dict.keys():
    (expiry, value) = _dict[k]
    if expiry < time.time():
      del _dict[k]

def todisk():
  gc()
  pickle.dump(_dict, open(filename, 'w'), pickle.HIGHEST_PROTOCOL)

def fromdisk(strfile):
  globals()['filename'] = strfile
  try:
    globals()['_dict'] = pickle.load(open(filename, 'r'))
  except IOError:
    pass


