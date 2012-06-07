import time
import json

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
  output = json.dumps(_dict)
  with open(filename, 'w') as f:
    f.write(output)

def fromdisk(strfile):
  globals()['filename'] = strfile
  try:
    with open(filename, 'r') as f:
      _dict = json.loads(f.read())
  except IOError:
    pass


