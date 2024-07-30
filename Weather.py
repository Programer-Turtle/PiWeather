import requests
headers = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}


def GetWeather(latitude, longitude):
    #Gets Weather data from location
    response =  requests.get(f"https://api.weather.gov/points/{latitude},{longitude}", headers=headers).json()

    #Seperates Data
    CurrentHourlyForcastData = (requests.get(response['properties']["forecastHourly"], headers=headers).json())["properties"]["periods"][0]
    TemperatureData = f"{CurrentHourlyForcastData['temperature']}{CurrentHourlyForcastData['temperatureUnit']}"
    ConditionData = f"{CurrentHourlyForcastData['shortForecast']}"

    #Combines data into dictionary
    WeatherData = {
        "Temperature":TemperatureData,
        "Condition":ConditionData
    }

    return WeatherData

def GetWeatherAlerts(latitude, longitude):
    #Gets Alerts
    AlertsData = (requests.get(f"https://api.weather.gov/alerts/active?point={latitude},{longitude}", headers=headers).json())['features']
    AlertsList = []

    if AlertsData:
        for alert in AlertsData:
            AlertsList.append(alert['properties']['headline'])
    else:
        AlertsList = "None"

    return AlertsList