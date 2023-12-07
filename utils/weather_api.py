import requests

def get_weather(lat, long): 
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,precipitation,wind_speed_10m"
        response = requests.get(url).json()

        temperature = response['current']['temperature_2m']
        precipitation = response['current']['precipitation']
        wind_speed = response['current']['wind_speed_10m']

    except:
        temperature = 28.9
        precipitation = 0.0
        wind_speed = 5.8
        print("Use default weather")

    print(f"Temperature: {temperature}")
    print(f"Precipitation: {precipitation}")
    print(f"Wind Speed: {wind_speed}")

    return temperature, precipitation, wind_speed
