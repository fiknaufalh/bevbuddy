from utils.core.method import *
from utils.config import settings

def get_video_conference():
    url = f"{settings.vcc_api_url}/videoconference"
    return get_api_data(url)

def get_video_conference_by_id(id: int):
    url = f"{settings.vcc_api_url}/videoconference/{id}"
    return get_api_data(url)

def post_video_conference():
    url = f"{settings.vcc_api_url}/videoconference"
    return post_api_data(url)

def put_video_conference(id: int):
    url = f"{settings.vcc_api_url}/videoconference/{id}"
    return put_api_data(url)

def delete_video_conference(id: int):
    url = f"{settings.vcc_api_url}/videoconference/{id}"
    return delete_api_data(url)
