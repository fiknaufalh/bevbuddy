from utils.core.method import *
from utils.config import settings

def get_payment_processing():
    url = f"{settings.vcc_api_url}/paymentprocessing"
    return get_api_data(url)

def get_payment_processing_by_id(id: int):
    url = f"{settings.vcc_api_url}/paymentprocessing/{id}"
    return get_api_data(url)

def post_payment_processing():
    url = f"{settings.vcc_api_url}/paymentprocessing"
    return post_api_data(url)

def put_payment_processing(id: int):
    url = f"{settings.vcc_api_url}/paymentprocessing/{id}"
    return put_api_data(url)

def delete_payment_processing(id: int):
    url = f"{settings.vcc_api_url}/paymentprocessing/{id}"
    return delete_api_data(url)
