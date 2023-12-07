from utils.method import *
from utils.config import settings

def get_scheduling_platform():
    url = f"{settings.vcc_api_url}/schedulingplatform"
    urlToken = f"{settings.vcc_api_url}/token"
    return get_api_data(url, urlToken)

def get_scheduling_platform_by_id(id: int):
    url = f"{settings.vcc_api_url}/schedulingplatform/{id}"
    urlToken = f"{settings.vcc_api_url}/token"
    return get_api_data(url, urlToken)

def post_scheduling_platform(payload: dict):
    url = f"{settings.vcc_api_url}/schedulingplatform"
    urlToken = f"{settings.vcc_api_url}/token"
    return post_api_data(url, urlToken, payload)

def put_scheduling_platform(id: int, payload: dict):
    url = f"{settings.vcc_api_url}/schedulingplatform/{id}"
    urlToken = f"{settings.vcc_api_url}/token"
    return put_api_data(url, urlToken, payload)

def delete_scheduling_platform(id: int):
    url = f"{settings.vcc_api_url}/schedulingplatform/{id}"
    urlToken = f"{settings.vcc_api_url}/token"
    return delete_api_data(url, urlToken)
