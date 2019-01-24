#!/usr/bin/python3

from tkinter import *
import requests
import time

# Initialise Window
window = Tk()
window.title("Realtime Adelaide Metro Display")

# Create Labels
Title = Label(window, text="Adelaide Metro Arrivals", font=("Fira Code", 20))

lineNameVar = StringVar()
destinationVar = StringVar()
scheduledVar = StringVar()
arrivingVar = StringVar()

lineNameLabel = Label(window, textvariable = lineNameVar)
destinationLabel = Label(window, textvariable = destinationVar)
scheduledLabel = Label(window, textvariable = scheduledVar)
arrivingLabel = Label(window, textvariable = arrivingVar)

# Radio Buttons to Select Stop
def changedStopSelection():
    makeRequest(stopSelected.get())

stopSelected = IntVar()

rad_ethelton = Radiobutton(window, text = "Ethelton", value=16515, variable=stopSelected, command=changedStopSelection)
rad_adelaide = Radiobutton(window, text = "Adelaide", value=16490, variable=stopSelected, command=changedStopSelection)

def makeRequest(stopNumber):
    url = 'http://realtime.adelaidemetro.com.au/SiriWebServiceSAVM/SiriStopMonitoring.svc/json/SM?MonitoringRef=' + str(stopNumber)
    response = requests.get(url)
    jsonData = response.json()
    stopData = jsonData['StopMonitoringDelivery']
    updateLabels(stopData)

def updateLabels(stopData):
    try:
        numberEnroute = len(stopData[0]['MonitoredStopVisit'])
    except:
        print("No Trains")
        numberEnroute = 0
    
    if numberEnroute != 0:
        #countdown = 20
        #while(countdown >= 0):
        #    print('Countdown = ' + str(countdown))
            for train in stopData[0]['MonitoredStopVisit']:
                lineName = train['MonitoredVehicleJourney']['LineRef']['Value']
                destination = train['MonitoredVehicleJourney']['DestinationName'][0]['Value']
                expectedArrivalTimeRAW = train['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime']
                expectedArrivalTime = expectedArrivalTimeRAW[6:-7]
                expectedArrivalTimeNice = time.strftime("%H:%M", time.localtime(int(expectedArrivalTime)/1000))

                latestArrivalTimeRAW = train['MonitoredVehicleJourney']['MonitoredCall']['LatestExpectedArrivalTime']
                latestArrivalTime = latestArrivalTimeRAW[6:-7]
                latestArrivalTimeNice = time.strftime("%H:%M", time.localtime(int(latestArrivalTime)/1000))

                lineNameVar = str(lineName)
                destinationVar = str(destination)
                scheduledVar = str(expectedArrivalTimeNice)
                arrivingVar = str(latestArrivalTimeNice)
                time.sleep(3)
        #    countdown -= 1
        #makeRequest()
    else:
        time.sleep(60)
        #makeRequest()


#Layout
Title.grid(column=1, row=0)
rad_ethelton.grid(column=0, row=1)
rad_adelaide.grid(column = 1, row=1)

lineNameLabel.grid(column=1,row=2)
destinationLabel.grid(column=1,row=3)
scheduledLabel.grid(column=1,row=4)
arrivingLabel.grid(column=1,row=5)

# Start Window
window.mainloop()