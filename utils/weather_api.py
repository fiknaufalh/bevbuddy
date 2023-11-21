import requests
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

API_KEY = config['API_KEY']

def get_weather(ip_address): 
    # default ip address is for handling local testing
    if ip_address == "127.0.0.1":
        ip_address = "8.8.8.8"

    url_location = f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip_address}"
    response_location = requests.get(url_location).json()

    lat = response_location['latitude']
    long = response_location['longitude']

    url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,precipitation,wind_speed_10m"
    response_weather = requests.get(url_weather).json()

    rec_time = response_location["time_zone"]["current_time"]
    temperature = response_weather['current']['temperature_2m']
    precipitation = response_weather['current']['precipitation']
    wind_speed = response_weather['current']['wind_speed_10m']

    return rec_time, temperature, precipitation, wind_speed
