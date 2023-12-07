from fastapi import APIRouter, HTTPException, Request, Depends, status
from utils.auth import JWTBearer, AuthHandler
from models.consultations import Consultation
from utils.movie_recommendation.movie_recommendation import *
from utils.database_manager import session
from datetime import datetime
from sqlalchemy import text

movie_router = APIRouter(tags=['Movies Recommendations'])

@movie_router.get("/movies")
async def get_all_movies():
    return get_movies()

@movie_router.get("/movies/{id}")
async def get_single_movie(id: int):
    return get_movie_by_id(id)

@movie_router.get("/movies/search/{name}")
async def search_movies(name: str):
    return get_movie_by_name(name)

@movie_router.get("/movies/similar/")
async def get_similar_movies(id: int, max_amount: int):
    return get_movies_similar_by_id(id, max_amount)

@movie_router.post("/movies/recommendations/")
async def create_movies_recommendations(mood: str, max_amount: int, Authorize: JWTBearer = Depends(JWTBearer(roles=["customer", "admin"]))):
    return create_movies_recommendation(mood, max_amount)