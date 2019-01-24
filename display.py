#!/usr/bin/python
from __future__ import print_function
import requests
import time
import RPi.GPIO as GPIO

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
LED_ON = 15
 
# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def lcd_init():
    # Initialise display
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
    
    GPIO.output(LCD_RS, mode) # RS
    
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)
    
    # Toggle 'Enable' pin
    lcd_toggle_enable()
    
    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)
    
    # Toggle 'Enable' pin
    lcd_toggle_enable()
 
def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)
 
def lcd_string(message,line,style):
    # Send string to display
    # style=1 Left justified
    # style=2 Centred
    # style=3 Right justified
    
    if style==1:
        message = message.ljust(LCD_WIDTH," ")
    elif style==2:
        message = message.center(LCD_WIDTH," ")
    elif style==3:
        message = message.rjust(LCD_WIDTH," ")
    
    lcd_byte(line, LCD_CMD)
    
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)
 
def lcd_backlight(flag):
    # Toggle backlight on-off-on
    GPIO.output(LED_ON, flag)

def main():
    print('Inside Main\n')
    # Main program block
 
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable
    
    # Initialise display
    lcd_init()

    ## TRAIN STUFF
    stopNumber = '16515'   # ETHELTON 
    #stopNumber = '16490'    # ADELAIDE

    url = 'http://realtime.adelaidemetro.com.au/SiriWebServiceSAVM/SiriStopMonitoring.svc/json/SM?MonitoringRef=' + stopNumber
    response = requests.get(url)
    jsonData = response.json()
    stopData = jsonData['StopMonitoringDelivery']
    print(stopData)

    try:
        numberEnroute = len(stopData[0]['MonitoredStopVisit'])
    except:
        lcd_string("No Trains", LCD_LINE_2,2)
        numberEnroute = 0

    if numberEnroute != 0:
        countdown = 20
        while(countdown >= 0):
            print('Countdown = ' + str(countdown))
            for train in stopData[0]['MonitoredStopVisit']:
                lineName = train['MonitoredVehicleJourney']['LineRef']['Value']
                destination = train['MonitoredVehicleJourney']['DestinationName'][0]['Value']
                expectedArrivalTimeRAW = train['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime']
                expectedArrivalTime = expectedArrivalTimeRAW[6:-7]
                expectedArrivalTimeNice = time.strftime("%H:%M", time.localtime(int(expectedArrivalTime)/1000))

                latestArrivalTimeRAW = train['MonitoredVehicleJourney']['MonitoredCall']['LatestExpectedArrivalTime']
                latestArrivalTime = latestArrivalTimeRAW[6:-7]
                latestArrivalTimeNice = time.strftime("%H:%M", time.localtime(int(latestArrivalTime)/1000))

                lcd_string(str(lineName), LCD_LINE_1, 2)
                lcd_string("To: " + str(destination),LCD_LINE_2,1)
                lcd_string("Scheduled:     " + str(expectedArrivalTimeNice), LCD_LINE_3,1)
                lcd_string("Arriving:      " + str(latestArrivalTimeNice), LCD_LINE_4, 1)
                time.sleep(3)
            countdown -= 1
        main()
    else:
        time.sleep(60)
        main()

if __name__ == '__main__':
     
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
