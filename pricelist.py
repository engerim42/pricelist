#!/usr/bin/python
import xmlrpclib
import pprint
import time
import sys
import datetime

from time import sleep

def handle_error( error_code):
   print 'invalid parameters or internal error. Details: ' + str(error_code)
   sys.exit()
   return

domain = sys.argv[1]

api = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')

action = 'create'
currency = 'EUR'
grid = 'A'
phase = 'open'

if (len(sys.argv)>2):
  currency = sys.argv[2]

if (len(sys.argv)>3):
  grid = sys.argv[3]

if (len(sys.argv)>4):
  action = sys.argv[4]

if (len(sys.argv)>5):
  phase = sys.argv[5]

apikey = 'your-key'

found=0

try:
  r = api.domain.price.list(apikey, {'tlds': [domain], 'currency': currency, 'grid': grid, 'action':[action]})
except (xmlrpclib.Fault, \
  xmlrpclib.ProtocolError, xmlrpclib.ResponseError), error_code:
  handle_error(error_code)
if len(r) == 0:
  print "Invalid request"
  sys.exit(0)

while (r[0]['available'] ==  'pending'):
  try:
    sleep(1)
    r = api.domain.price.list(apikey, {'tlds': [domain], 'currency': currency, 'grid': grid, 'action':[action]})
    #pprint.pprint(r)
  except (xmlrpclib.Fault, \
    xmlrpclib.ProtocolError, xmlrpclib.ResponseError), error_code:
    handle_error(error_code)

for itemn in r[0]['prices']:
  r_phase = r[0]['current_phase'] + " (current phase, price is for golive)"
  if (action == 'create'):
    r_phase = str(itemn['action']['param']['tld_phase'])
  for item2 in itemn['unit_price']:
    print domain + " Action: " + action + " Available: " + r[0]['available'] + " Phase: " + r_phase + " Duration: " + str(item2['min_duration']) \
    + "-" + str(item2['max_duration']) + "(" + str(item2['duration_unit']) + ") " \
    + str(item2['price']) + " (" + item2['currency'] + "/" + item2['grid'] + ")" + " Price type: " + str(item2['price_type'])
for phases in r[0]['phases']:
  myphases = str(phases['phase']) + " ";
  myphases += "Start: " + str(phases['date_start']) + " "
  myphases += "Start Gandi: " + str(phases['date_start_gandi']) + " ";
  myphases += "End: " + str(phases['date_end']);
  print myphases
