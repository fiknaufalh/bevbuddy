import requests
from utils.config import settings

def get_token():
    url = f"{settings.vcc_api_url}/token"
    data = {
        'username': settings.vcc_username,
        'password': settings.vcc_password
    }
    response = requests.post(url, data=data)
    return response.json()['access_token']

def get_api_data(url: str):
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def post_api_data(url):
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.post(url, headers=headers)
    return response.json()

def put_api_data(url):
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.put(url, headers=headers)
    return response.json()

def delete_api_data(url):
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.delete(url, headers=headers)
    return response.json()