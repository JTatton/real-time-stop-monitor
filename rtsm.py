#!/usr/bin/python3

from __future__ import print_function
import requests
import time

#Console Colours
CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'


stopNumber = '16515'   # ETHELTON 
#stopNumber = '16490'    # ADELAIDE
url = 'http://realtime.adelaidemetro.com.au/SiriWebServiceSAVM/SiriStopMonitoring.svc/json/SM?MonitoringRef=' + stopNumber
response = requests.get(url, timeout=0.5)       # Need timeout to stop it hanging

jsonData = response.json()
stopData = jsonData['StopMonitoringDelivery']

key = ''
mapurl = 'http://open.mapquestapi.com/geocoding/v1/reverse?key='+ key +'&location='

try:
    numberEnroute = len(stopData[0]['MonitoredStopVisit'])
except:
    print('No Trains')
    numberEnroute = 0

print('Number of trains arriving: ' + str(numberEnroute))

if numberEnroute != 0:
    for train in stopData[0]['MonitoredStopVisit']:
        lineName = train['MonitoredVehicleJourney']['LineRef']['Value']
        destination = train['MonitoredVehicleJourney']['DestinationName'][0]['Value']
        expectedArrivalTime = time.strftime("%H:%M", time.localtime(int((train['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime'])[6:-7])/1000))
        latestArrivalTime = time.strftime("%H:%M", time.localtime(int((train['MonitoredVehicleJourney']['MonitoredCall']['LatestExpectedArrivalTime'])[6:-7])/1000))
        currentLocLat = train['MonitoredVehicleJourney']['VehicleLocation']['Items'][0]
        currentLocLong = train['MonitoredVehicleJourney']['VehicleLocation']['Items'][1]
        
        print(CBOLD + str(lineName) + CEND, end='')
        print(' ' + CITALIC + 'to ' + CEND + CRED + CBOLD + str(destination) + CEND)
        print(CITALIC + 'Scheduled for ' + CEND + CBLUE + str(expectedArrivalTime) + CEND)
        if latestArrivalTime > expectedArrivalTime:
            print(CITALIC + 'Arriving at ' + CEND + CSELECTED + CBLINK + CRED + str(latestArrivalTime) + CEND)
        else:
            print(CITALIC + 'Arriving at ' + CEND + CSELECTED + CBLINK + CGREEN + str(latestArrivalTime) + CEND)
        print('Current Location: ' + currentLocLat + ', ' + currentLocLong)

        mapresponse = requests.get(mapurl + currentLocLat + ',' + currentLocLong)
        mapjson = mapresponse.json()
        maplocation = mapjson['results'][0]['locations'][0]['street']
        print('Stop: ' + maplocation)