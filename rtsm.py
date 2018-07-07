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

response = requests.get(url)

jsonData = response.json()

stopData = jsonData['StopMonitoringDelivery']

try:
    numberEnroute = len(stopData[0]['MonitoredStopVisit'])
except:
    print('No Trains')
    numberEnroute = 0

print('Number of trains arriving: ' + str(numberEnroute))

for train in stopData[0]['MonitoredStopVisit']:
    lineName = train['MonitoredVehicleJourney']['LineRef']['Value']
    print(CBOLD + str(lineName) + CEND)
    destination = train['MonitoredVehicleJourney']['DestinationName'][0]['Value']
    print('to ' + CRED + str(destination) + CEND)
    expectedArrivalTimeRAW = train['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime']
    expectedArrivalTime = expectedArrivalTimeRAW[6:-7]
    expectedArrivalTimeNice = time.strftime("%H:%M", time.localtime(int(expectedArrivalTime)/1000))
    print('Scheduled for ' + CBLUE + str(expectedArrivalTimeNice) + CEND)

    latestArrivalTimeRAW = train['MonitoredVehicleJourney']['MonitoredCall']['LatestExpectedArrivalTime']
    latestArrivalTime = latestArrivalTimeRAW[6:-7]
    latestArrivalTimeNice = time.strftime("%H:%M", time.localtime(int(latestArrivalTime)/1000))

    if latestArrivalTime > expectedArrivalTime:
        print('Arriving at ' + CSELECTED + CBLINK + CRED + str(latestArrivalTimeNice) + CEND + '\n')
    elif latestArrivalTime == expectedArrivalTime:
        print('Arriving at ' + CSELECTED + CBLINK + CYELLOW + str(latestArrivalTimeNice) + CEND + '\n')
    else:
        print('Arriving at ' + CSELECTED + CBLINK + CGREEN + str(latestArrivalTimeNice) + CEND + '\n')






