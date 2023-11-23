import requests
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

API_KEY = "59bbf7c444614eac8bd10ef556c02aa8"
# API_KEY = config['API_KEY']

def get_location(ip_address):
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip_address}"
    response = requests.get(url).json()

    lat = response['latitude']
    long = response['longitude']
    rec_time = response["time_zone"]["current_time"]

    return lat, long, rec_time