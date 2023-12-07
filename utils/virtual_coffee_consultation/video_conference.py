from utils.method import *
from utils.config import settings

def get_video_conference():
    url = f"{settings.vcc_api_url}/videoconference"
    urlToken = f"{settings.vcc_api_url}/token"
    return get_api_data(url, urlToken)

def get_video_conference_by_id(id: int):
    url = f"{settings.vcc_api_url}/videoconference/{id}"
    urlToken = f"{settings.vcc_api_url}/token"
    return get_api_data(url, urlToken)

def post_video_conference(payload: dict):
    url = f"{settings.vcc_api_url}/videoconference"
    urlToken = f"{settings.vcc_api_url}/token"
    return post_api_data(url, urlToken, payload)

def put_video_conference(id: int, payload: dict):
    url = f"{settings.vcc_api_url}/videoconference/{id}"
    urlToken = f"{settings.vcc_api_url}/token"
    return put_api_data(url, urlToken, payload)

def delete_video_conference(id: int):
    url = f"{settings.vcc_api_url}/videoconference/{id}"
    urlToken = f"{settings.vcc_api_url}/token"
    return delete_api_data(url, urlToken)
