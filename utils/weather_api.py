import requests

def get_weather(lat, long): 
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,precipitation,wind_speed_10m"
    response = requests.get(url).json()

    temperature = response['current']['temperature_2m']
    precipitation = response['current']['precipitation']
    wind_speed = response['current']['wind_speed_10m']

    return temperature, precipitation, wind_speed
