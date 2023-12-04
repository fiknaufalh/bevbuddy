from fastapi import APIRouter, HTTPException, Depends, status
from utils.auth import JWTBearer, AuthHandler
from utils.core.scheduling_platform import *
from utils.core.payment_processing import *
from utils.core.video_conference import *

consult_router = APIRouter(tags=['Consult'])

@consult_router.get('/schedule')
async def get_all_scheduling_platform():
    return get_scheduling_platform()

@consult_router.get('/schedule/{id}')
async def get_single_scheduling_platform(id: int):
    return get_scheduling_platform_by_id(id)

@consult_router.get("/payment")
async def get_all_payment_processing():
    return get_payment_processing()

@consult_router.get("/payment/{id}")
async def get_single_payment_processing(id: int):
    return get_payment_processing_by_id(id)

@consult_router.get("/video")
async def get_all_video_conference():
    return get_video_conference()

@consult_router.get("/video/{id}")
async def get_single_video_conference(id: int):
    return get_video_conference_by_id(id)