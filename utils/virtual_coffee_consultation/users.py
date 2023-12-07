from utils.method import *
from utils.config import settings

def get_users():
    url = f"{settings.vcc_api_url}/users/me"
    urlToken = f"{settings.vcc_api_url}/token"
    return get_api_data(url, urlToken)