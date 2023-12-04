from utils.core.method import *
from utils.config import settings

def get_scheduling_platform():
    url = f"{settings.vcc_api_url}/schedulingplatform"
    return get_api_data(url)

def get_scheduling_platform_by_id(id: int):
    url = f"{settings.vcc_api_url}/schedulingplatform/{id}"
    return get_api_data(url)

def post_scheduling_platform():
    url = f"{settings.vcc_api_url}/schedulingplatform"
    return post_api_data(url)

def put_scheduling_platform(id: int):
    url = f"{settings.vcc_api_url}/schedulingplatform/{id}"
    return put_api_data(url)

def delete_scheduling_platform(id: int):
    url = f"{settings.vcc_api_url}/schedulingplatform/{id}"
    return delete_api_data(url)
