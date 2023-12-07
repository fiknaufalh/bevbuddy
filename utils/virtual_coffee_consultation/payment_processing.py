from utils.method import *
from utils.config import settings

def get_payment_processing():
    url = f"{settings.vcc_api_url}/paymentprocessing"
    urlToken = f"{settings.vcc_api_url}/token"
    return get_api_data(url, urlToken)

def get_payment_processing_by_id(id: int):
    url = f"{settings.vcc_api_url}/paymentprocessing/{id}"
    urlToken = f"{settings.vcc_api_url}/token"
    return get_api_data(url, urlToken)

def post_payment_processing():
    url = f"{settings.vcc_api_url}/paymentprocessing"
    urlToken = f"{settings.vcc_api_url}/token"
    return post_api_data(url, urlToken)

def put_payment_processing(id: int):
    url = f"{settings.vcc_api_url}/paymentprocessing/{id}"
    urlToken = f"{settings.vcc_api_url}/token"
    return put_api_data(url, urlToken)

def delete_payment_processing(id: int):
    url = f"{settings.vcc_api_url}/paymentprocessing/{id}"
    urlToken = f"{settings.vcc_api_url}/token"
    return delete_api_data(url, urlToken)
