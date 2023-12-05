from utils.core.method import *
from utils.config import settings

def get_users():
    url = f"{settings.vcc_api_url}/users/me"
    return get_api_data(url)