from datetime import datetime
import requests

print("Warning not all data is realtime and may be just a prediction.")
Appheaders = None

def InitiateAPI(AppName, ContactEmail):
    if(not AppName or not ContactEmail):
        raise Exception("You either forgot AppNamr or ContactEmail")
    global Appheaders
    Appheaders = {'User-Agent': f'{AppName}, {ContactEmail}'}

def BypassInitiate():
    print("Bypassing Initiation is not recommended and can increase your chances of the API blocking your request.")
    global Appheaders 
    Appheaders = {'User-Agent': f'User bypassed headers.'}

def GetHourlyForecast(latitude, longitude):
    #Gets Weather data from location
    if (not Appheaders):
        raise Exception("You did not initiate API. Try calling the InitiateAPI with your app's name and your contact email.")
    response =  requests.get(f"https://api.weather.gov/points/{latitude},{longitude}", headers=Appheaders)
    response = response.json()

    #Seperates Data
    APIForecastResponse = requests.get(response['properties']["forecastHourly"], headers=Appheaders)
    CurrentHourlyForecastData = (APIForecastResponse.json())["properties"]["periods"]

    Data = {}
    for hour in CurrentHourlyForecastData:
        originalTimeData = hour["startTime"]
        PartialyformatedDate = datetime.fromisoformat(originalTimeData)
        FormatedDate = f"{PartialyformatedDate.date()}/{PartialyformatedDate.hour}:00"
        Data[FormatedDate] = hour
    return Data


def GetCurrentForecast(latitude, longitude):
    CurrentDate = datetime.now()
    FormatedDate = f"{CurrentDate.date()}/{CurrentDate.hour}:00"
    CurrentForecast = GetHourlyForecast(latitude, longitude)[FormatedDate]
    return CurrentForecast

def GetCurrentConditions(latitude, longitude):
    CurrentWeather = GetCurrentForecast(latitude, longitude)
    return {
        "ShortForecast": CurrentWeather['shortForecast'],
        "DeatiledForecast": CurrentWeather['detailedForecast']
    }

def GetCurrentTemperature(latitude, longitude):
    CurrentWeather = GetCurrentForecast(latitude, longitude)
    return f"{CurrentWeather['temperature']}{CurrentWeather['temperatureUnit']}"

def GetCurrentWindData(latitude, longitude):
    CurrentWeather = GetCurrentForecast(latitude, longitude)
    return {
        "WindSpeed": CurrentWeather['windSpeed'],
        "WindDirection": CurrentWeather['windDirection']
    }

def GetWeatherAlerts(latitude, longitude):
    if (not Appheaders):
        raise Exception("You did not initiate API. Try calling the InitiateAPI with your app's name and your contact email.")
    #Gets Alerts
    AlertsData = (requests.get(f"https://api.weather.gov/alerts/active?point={latitude},{longitude}", headers=Appheaders).json())
    if (not 'features' in AlertsData.keys()):
        AlertsData = GetWeatherAlerts(latitude, longitude)
    AlertsData = AlertsData['features']
    Data = {}

    if AlertsData:
        for alert in AlertsData:
            Data[alert['properties']['headline']] = alert
    else:
        Data = None

    return Data