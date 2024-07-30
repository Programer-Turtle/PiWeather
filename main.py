import Weather
import os
import smbus
import time
from time import sleep, strftime
from datetime import datetime, timedelta
from LCD1602 import CharLCD1602
lcd1602 = CharLCD1602()

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
    return Weather.GetWeather(latitude, longitude)

def GetAlertData():
    global lastRecordedAlertTime
    lastRecordedAlertTime = datetime.now()
    print("GotAlerts")
    return Weather.GetWeatherAlerts(latitude, longitude)


def CheckIfTimePassed():
    return datetime.now().hour != lastRecordedAlertTime.hour

def CheckIfAlertTimePassed():
    return (datetime.now() - lastRecordedTime)>=timedelta(minutes=2)

def Main():
    WeatherData = GetWeatherData()
    Alerts = GetAlertData()


    while True:
        TopweatherString = WeatherData["Temperature"]
        AlertString = ""
        if(Alerts != "None"):
            AlertString = " ".join(Alerts)
        BottomWeatherString = f"{WeatherData['Condition']} {AlertString}                "
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