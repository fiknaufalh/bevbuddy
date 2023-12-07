import requests
from utils.config import settings

def get_token(url: str):
    data = {
        'username': settings.vcc_username,
        'password': settings.vcc_password
    }
    response = requests.post(url, data=data)
    return response.json()['access_token']

def get_api_data(url: str, urlToken: str):
    headers = {
        'Authorization': f'Bearer {get_token(urlToken)}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def post_api_data(url, urlToken, payload):
    headers = {
        'Authorization': f'Bearer {get_token(urlToken)}'
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def put_api_data(url, urlToken, payload):
    headers = {
        'Authorization': f'Bearer {get_token(urlToken)}'
    }
    response = requests.put(url, headers=headers, json=payload)
    return response.json()

def delete_api_data(url, urlToken, payload):
    headers = {
        'Authorization': f'Bearer {get_token(urlToken)}'
    }
    response = requests.delete(url, headers=headers, json=payload)
    return response.json()