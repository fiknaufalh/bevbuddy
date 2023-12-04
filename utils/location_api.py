import requests
from dotenv import load_dotenv, dotenv_values
from utils.config import settings

load_dotenv()
config = dotenv_values(".env")

# API_KEY = "59bbf7c444614eac8bd10ef556c02aa8"
# API_KEY = config['API_KEY']
API_KEY = settings.api_key

def get_location(ip_address):
    try:
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip_address}"
        response = requests.get(url).json()

        lat = response['latitude']
        long = response['longitude']
        rec_time = response["time_zone"]["current_time"]
    except:
        lat = -6.1753924
        long = 106.8271528
        rec_time = "2023-11-25 15:37:00"
        print("Use default location")

    return lat, long, rec_time