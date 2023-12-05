from fastapi import APIRouter, HTTPException, Request, Depends, status
from utils.auth import JWTBearer, AuthHandler
from models.consultations import Consultation
from utils.core.scheduling_platform import *
from utils.core.payment_processing import *
from utils.core.video_conference import *
from utils.core.users import *
from utils.database_manager import session
from sqlalchemy import or_, text

consultation_router = APIRouter(tags=['Consult'])

@consultation_router.post("/consultations")
async def create_consultation(
    consultation: Consultation,
    request: Request,
    Authorize: JWTBearer = Depends(JWTBearer(roles=["customer", "admin"]))):

    consultee_fullname = Authorize['fullname']
    consultee_username = Authorize['username']

    try:
        query = text(f"""
                    SELECT * FROM person JOIN recommendation JOIN menu_rec JOIN menu
                    WHERE person.id = recommendation.id_person AND person.username = '{consultee_username}'
                    AND recommendation.id_list = menu_rec.id_list AND menu_rec.id_menu = menu.id
                    ORDER BY rec_time DESC LIMIT 1;
                    """)
        result = session.execute(query)
        if result.rowcount:
            result = result.fetchone()
            preferred_menu = {
                "name": result.name,
                "description": result.description,
                "category": result.category,
                "url_img": result.url_img
            }
        else:
            preferred_menu = "Have not been recommended"
        
        id_consult = 123456789
        video_conference = get_video_conference_by_id(id_consult)
        id_advisor = video_conference['advisorID']
        meeting_platform = video_conference['meetingPlatform']
        meeting_link = video_conference['meetingLink']

    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=f"Please fill in the consultation form first"
        )
    
    return {
        "id_consult": id_consult,
        "id_advisor": id_advisor,
        "consultee": consultee_fullname,
        "consultation_date": consultation.consultation_date,
        "consultation_time": consultation.consultation_time,
        "meeting_platform": meeting_platform,
        "meeting_link": meeting_link,
        "preferred_menu": preferred_menu
    }

@consultation_router.get('/schedule')
async def get_all_scheduling_platform():
    return get_scheduling_platform()

@consultation_router.get('/schedule/{id}')
async def get_single_scheduling_platform(id: int):
    return get_scheduling_platform_by_id(id)

@consultation_router.get("/payment")
async def get_all_payment_processing():
    return get_payment_processing()

@consultation_router.get("/payment/{id}")
async def get_single_payment_processing(id: int):
    return get_payment_processing_by_id(id)

@consultation_router.get("/video")
async def get_all_video_conference():
    return get_video_conference()

@consultation_router.get("/video/{id}")
async def get_single_video_conference(id: int):
    return get_video_conference_by_id(id)