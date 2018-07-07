import requests
import time

#stopNumber = '16515'#ETHELTON 
stopNumber = '16490'
url = 'http://realtime.adelaidemetro.com.au/SiriWebServiceSAVM/SiriStopMonitoring.svc/json/SM?MonitoringRef=' + stopNumber

print('URL : ' + url)

response = requests.get(url)

jsonData = response.json()

stopData = jsonData['StopMonitoringDelivery']

numberEnroute = len(stopData[0]['MonitoredStopVisit'])

print('Number of trains: ' + str(numberEnroute))

for train in stopData[0]['MonitoredStopVisit']:
    lineName = train['MonitoredVehicleJourney']['LineRef']['Value']
    print('Line: ' + str(lineName))
    destination = train['MonitoredVehicleJourney']['DestinationName'][0]['Value']
    print('Destination: ' + str(destination))
    expectedArrivalTimeRAW = train['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime']
    expectedArrivalTime = expectedArrivalTimeRAW[6:-7]
    expectedArrivalTimeNice = time.strftime("%H:%M", time.localtime(int(expectedArrivalTime)/1000))
    print('Scheduled Arrival: ' + str(expectedArrivalTimeNice))

    latestArrivalTimeRAW = train['MonitoredVehicleJourney']['MonitoredCall']['LatestExpectedArrivalTime']
    latestArrivalTime = latestArrivalTimeRAW[6:-7]
    latestArrivalTimeNice = time.strftime("%H:%M", time.localtime(int(latestArrivalTime)/1000))
    print('Real-Time Arrival: ' + str(latestArrivalTimeNice) + '\n')