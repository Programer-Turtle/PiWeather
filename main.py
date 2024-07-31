import NWS
import os
import time
from time import sleep, strftime
from datetime import datetime, timedelta
from LCD1602 import CharLCD1602
lcd1602 = CharLCD1602()

NWS.InitiateAPI("PiWeatherSation", "email here")

#Put your latitude and longitude
latitude = "38.89355704224317"
longitude = "-77.033268223003"
lastRecordedTime = ""
lastRecordedAlertTime = ""
WeatherMinuteInterval = 1

def GetWeatherData():
    global lastRecordedTime 
    lastRecordedTime = datetime.now()
    print("GotWeather")
    return NWS.GetCurrentForecast(latitude, longitude)

def GetAlertData():
    global lastRecordedAlertTime
    lastRecordedAlertTime = datetime.now()
    print("GotAlerts")
    alertData = NWS.GetWeatherAlerts(latitude, longitude)
    alerts = []
    for alert in alertData:
        alerts.append({
            'event':alertData['properties']['event'],
            'headline':alertData['properties']['headline'],
            'description':alertData['properties']['description'],
            'severity':alertData['properties']['severity'],
            'instruction':alertData['properties']['instruction'],
            'urgency':alertData['properties']['urgency']
                })
    return alerts


def CheckIfTimePassed():
    return datetime.now().hour != lastRecordedAlertTime.hour

def CheckIfAlertTimePassed():
    return (datetime.now() - lastRecordedTime)>=timedelta(minutes=2)

def Main():
    WeatherData = GetWeatherData()
    Alerts = GetAlertData()


    while True:
        TopweatherString = f"NWS   {WeatherData['temperature']}{WeatherData['temperatureUnit']}"
        AlertString = ""
        if(Alerts != None):
            ListOfStrings = []
            for alert in Alerts:
                CurrentAddedAlertString = f"{alert['event']} {alert['description']} Severity is {alert['severity']}"
                if(alert['instruction'] != 'None'):
                    CurrentAddedAlertString+= f" {alert['instruction']}"
                ListOfStrings.append(f"{alert['event']} ")
            AlertString = "   ".join(ListOfStrings)

        BottomWeatherString = f"                {WeatherData['shortForecast']} {AlertString}"
        lcd1602.init_lcd()
        for i in range(0, len(BottomWeatherString)):
            lcd1602.clear()
            lcd1602.write(0, 0, TopweatherString)
            lcd1602.write(0, 1, BottomWeatherString[i:16+i])
            time.sleep(0.5)
        if(CheckIfTimePassed() == True):
            WeatherData = GetWeatherData()
        if(CheckIfAlertTimePassed() == True):
            Alerts = GetAlertData() 