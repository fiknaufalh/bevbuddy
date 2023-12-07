from utils.method import *
from utils.config import settings

def get_movies():
    url = f"{settings.mr_api_url}/movies"
    urlToken = f"{settings.mr_api_url}/users/login"
    return get_api_data(url, urlToken)

def get_movie_by_id(id: int):
    url = f"{settings.mr_api_url}/movies/{id}"
    urlToken = f"{settings.mr_api_url}/users/login"
    return get_api_data(url, urlToken)

def get_movie_by_name(name: str):
    url = f"{settings.mr_api_url}/movies/search/?title={name}"
    urlToken = f"{settings.mr_api_url}/users/login"
    return get_api_data(url, urlToken)

def get_movies_similar_by_id(id: int, max_amount: int):
    url = f"{settings.mr_api_url}/movies/similar/?movie_id={id}&max_amount={max_amount}"
    urlToken = f"{settings.mr_api_url}/users/login"
    return get_api_data(url, urlToken)

def create_movies_recommendation(mood: str, max_amount: int):
    url = f"{settings.mr_api_url}/movies/recommendations/?mood={mood}&max_amount={max_amount}"
    urlToken = f"{settings.mr_api_url}/users/login"
    payload={}
    return post_api_data(url, urlToken, payload)
