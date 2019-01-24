#!/usr/bin/python3

from tkinter import *
import requests
import time

# Initialise Window
window = Tk()
window.title("Realtime Adelaide Metro Display")

# Create Labels
Title = Label(window, text="Adelaide Metro Arrivals", font=("Fira Code", 20))

#lineNameVar = StringVar()
#destinationVar = StringVar()
#scheduledVar = StringVar()
#arrivingVar = StringVar()

#lineNameVar.set("Init lineName")
#destinationVar.set("Init Destination")
#scheduledVar.set("Init Scheduled")
#arrivingVar.set("Init Arriving")

#lineNameLabel = Label(window, textvariable = lineNameVar)
#destinationLabel = Label(window, textvariable = destinationVar)
#scheduledLabel = Label(window, textvariable = scheduledVar)
#arrivingLabel = Label(window, textvariable = arrivingVar)

lineNameLabel = Label(window, text = "Init lineName")
destinationLabel = Label(window, text = "Init destination")
scheduledLabel = Label(window, text = "Init scheduled")
arrivingLabel = Label(window, text = "Init arriving")

# Radio Buttons to Select Stop
def changedStopSelection():
    makeRequest(stopSelected.get())
    
stopSelected = IntVar()
rad_ethelton = Radiobutton(window, text = "Ethelton", value=16515, variable=stopSelected, command=changedStopSelection)
rad_adelaide = Radiobutton(window, text = "Adelaide", value=16490, variable=stopSelected, command=changedStopSelection)

# Make Request To Server
def makeRequest(stopNumber):
    print("Making Request")
    url = 'http://realtime.adelaidemetro.com.au/SiriWebServiceSAVM/SiriStopMonitoring.svc/json/SM?MonitoringRef=' + str(stopNumber)
    response = requests.get(url)
    jsonData = response.json()
    print("Response: \n" + str(jsonData))
    stopData = jsonData['StopMonitoringDelivery']
    updateLabels(stopData)

# Train Information Storage Setup
trainInfo = {
    "lineName" : "temp lineName",
    "destination" : "temp destination",
    "scheduled" : "temp scheduled",
    "actual" : "temp actual"
    }

# Update the Train Info Dict
def updateTrainInfo(train):
    print("Updating Train Info")
    trainInfo["lineName"] = str(train['MonitoredVehicleJourney']['LineRef']['Value'])
    trainInfo["destination"] = str(train['MonitoredVehicleJourney']['DestinationName'][0]['Value'])
    trainInfo["scheduled"] = str(time.strftime("%H:%M", time.localtime(int((train['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime'])[6:-7])/1000)))
    trainInfo["actual"] = str(time.strftime("%H:%M", time.localtime(int((train['MonitoredVehicleJourney']['MonitoredCall']['LatestExpectedArrivalTime'])[6:-7]/1000))))

# Update Labels on Screen
def updateTheLabels(stopData)
    print("Updating Labels")
    lastStopData = stopData

    try:
        numberEnroute = len(stopData[0]['MonitoredStopVisit'])
        print("Number enroute: " + str(numberEnroute))
    except:
        print("No Trains")
        numberEnroute = 0

    if numberEnroute != 0:
        for train in stopData[0]['MonitoredStopVisit']:
            updateTrainInfo(train)
            time.sleep(5)
        time.sleep(30)
        makeRequest()
    else:
        time.sleep(120)
        makeRequest()

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