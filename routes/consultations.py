from fastapi import APIRouter, HTTPException, Request, Depends, status
from utils.auth import JWTBearer, AuthHandler
from models.consultations import Consultation
from utils.virtual_coffee_consultation.scheduling_platform import *
from utils.virtual_coffee_consultation.payment_processing import *
from utils.virtual_coffee_consultation.video_conference import *
from utils.virtual_coffee_consultation.users import *
from utils.config import settings
from utils.database_manager import session
from sqlalchemy import text

consultation_router = APIRouter(tags=['Consult'])

@consultation_router.post("/consultations")
async def create_consultation(
    consultation: Consultation,
    request: Request,
    Authorize: JWTBearer = Depends(JWTBearer(roles=["customer", "admin"]))):

    consultee_fullname = Authorize['fullname']
    consultee_id = Authorize['sub']

    try:
        query = text(f"""
                    SELECT * FROM person JOIN recommendation JOIN menu_rec JOIN menu
                    WHERE person.id = recommendation.id_person AND person.id = '{consultee_id}'
                    AND recommendation.id_list = menu_rec.id_list AND menu_rec.id_menu = menu.id
                    ORDER BY rec_time DESC LIMIT 1;
                    """)
        result = session.execute(query)
        if result.rowcount:
            result = result.fetchone()
            preferred_menu = {
                "id": result.id,
                "name": result.name,
                "description": result.description,
                "category": result.category,
                "url_img": result.url_img
            }
            preferred_menu_id = result.id
        else:
            preferred_menu = "Have not been recommended"
            preferred_menu_id = "NULL"
        
        all_vid_conference = get_video_conference()
        id_consult_max = all_vid_conference[0]['consultationID']
        id_advisor_max = all_vid_conference[0]['advisorID']
        for vid_conference in all_vid_conference:
            if vid_conference['consultationID'] > id_consult_max:
                id_consult_max = vid_conference['consultationID']
            if vid_conference['advisorID'] > id_advisor_max:
                id_advisor_max = vid_conference['advisorID']
        id_consult = id_consult_max + 1
        id_advisor = id_advisor_max + 1
        id_participant = get_users()["participantID"]
        id_host = all_vid_conference[0]['hostID']
        meeting_platform = all_vid_conference[0]['meetingPlatform']
        meeting_link = all_vid_conference[0]['meetingLink']
        consultation_date = consultation.consultation_date
        consultation_time = consultation.consultation_time

        payload = {
            "consultationID": id_consult,
            "advisorID": id_advisor,
            "participantID": id_participant,
            "hostID": id_host,
            "meetingPlatform": meeting_platform,
            "meetingLink": meeting_link,
            "consultationDate": consultation_date,
            "consultationTime": consultation_time
        }

        post_video_conference(payload)
        query = text(f"""
                    INSERT INTO consultation (id, id_person, id_advisor, consultation_time, 
                    meeting_platform, meeting_link, preferred_menu)
                    VALUES ({id_consult}, {consultee_id}, {id_advisor}, 
                    '{consultation_date} {consultation_time}',
                    '{meeting_platform}', '{meeting_link}', '{preferred_menu_id}');
                    """)
        session.execute(query)
        session.commit()

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
        "consultation_date": consultation_date,
        "consultation_time": consultation_time,
        "meeting_platform": meeting_platform,
        "meeting_link": meeting_link,
        "preferred_menu": preferred_menu
    }

@consultation_router.get('/consultations')
async def get_consultation_list(
    request: Request, 
    Authorize: JWTBearer = Depends(JWTBearer(roles=["customer", "admin"]))):
    
    try:
        consultee_id = Authorize['sub']
        consultee_fullname = Authorize['fullname']
        query = text(f"""
                     SELECT c.id, c.id_person, c.id_advisor, c.consultation_time, c.meeting_platform, c.meeting_link,
                    menu.id as menu_id, menu.name as name_menu, menu.description as menu_desc, menu.category as menu_cat, menu.url_img
                    FROM consultation as c JOIN menu WHERE id_person = '{consultee_id}' AND menu.id = c.preferred_menu; 
                     """)
        result = session.execute(query)

        if result.rowcount:
            consult_list = []
            for consult in result:
                consult_dict = {
                    "id_consult": consult.id,
                    "id_advisor": consult.id_advisor,
                    "consultee": consultee_fullname,
                    "consultation_time": consult.consultation_time,
                    "meeting_platform": consult.meeting_platform,
                    "meeting_link": consult.meeting_link,
                    "preferred_menu": {
                        "id": consult.menu_id,
                        "name": consult.name_menu,
                        "description": consult.menu_desc,
                        "category": consult.menu_cat,
                        "url_img": consult.url_img
                    }
                }
                consult_list.append(consult_dict)
            
            return consult_list
        else:
            return {
                "message" : "You have not set consultation appointment yet"
            }

    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Something went wrong"
        )
