import urllib2
import Cache
import datetime

fridgeURL = 'http://admin01.int.tildaslash.com/fridge/data/'

def _updateData(self):
  items = ['weight', 'tempA', 'tempB']
  weighttxt = urllib2.urlopen(fridgeURL + 'weight').read()
  tempAtxt = urllib2.urlopen(fridgeURL + 'tempA').read()
  tempBtxt = urllib2.urlopen(fridgeURL + 'tempB').read()



