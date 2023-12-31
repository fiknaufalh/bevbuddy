from fastapi import APIRouter, HTTPException, Request, status, Depends, Query
from models.recommendations import RecommendationReq, MenuRes, NutritionRes
from utils.auth import JWTBearer
import utils.tdee_calculator as tdee
from utils.weather_api import get_weather
from utils.location_api import get_location
from utils.database_manager import session
from sqlalchemy import or_, text
from datetime import datetime

recommendation_router = APIRouter(tags=['Beverage Recommendations'])

@recommendation_router.post('/recommendations')
async def create_recommendation(
    req: RecommendationReq, 
    request: Request,
    Authorize: JWTBearer = Depends(JWTBearer(roles=["customer", "admin"]))):

    client_ip = request.client.host if request.client.host != "127.0.0.1" else "182.253.194.14"
    latitude, longitude, rec_time = get_location(client_ip)
    temperature, precipitation, wind_speed = get_weather(latitude, longitude)

    CALORY_PERCENTAGE = 0.5
    PROTEIN_PERCENTAGE = 0.8
    FAT_PERCENTAGE = 0.8
    CARB_PERCENTAGE = 0.8

    calory_upper_bound = CALORY_PERCENTAGE * tdee.calculate_tdee(
        req.gender, req.age, req.weight, req.height, req.activity)
    protein_grams, fat_grams, carb_grams = tdee.calculate_macros(calory_upper_bound)

    protein_grams *= PROTEIN_PERCENTAGE
    fat_grams *= FAT_PERCENTAGE
    carb_grams *= CARB_PERCENTAGE

    mood_keywords = {
        "happy": ["caramel", "special treat", "dusting of cinnamon", "refreshingly sweet", "endless java joy"],
        "loved": ["passion fruit", "strawberry", "ultimate pick-me-up", "tropical", "delicious"],
        "focus": ["espresso shots", "wonderfully rich", "nuance", "dark, rich espresso", "milk-forward"],
        "chill": ["cold brew", "sweetened", "cold foam", "cool lift", "refreshingly chilled"],
        "sad": ["mocha sauce", "bittersweet", "whipped cream", "chocolaty chips", "party in your mouth"],
        "scared": ["spicy", "chai", "cinnamon", "lemon verbena", "caffeine-free"],
        "angry": ["Frappuccino", "blender bash", "party in your mouth", "feel-good energy", "whipped cream"]
    }

    mood = req.mood if req.mood != None else "neutral"
    keywords = mood_keywords.get(mood.lower(), [])
    mood_like_queries = [MenuRes.description.like(f"%{keyword}%") for keyword in keywords]

    weather = req.weather if req.weather != None else "no"
    weather_like_queries = []
    if weather.lower() == "yes":
        if precipitation > 0 or wind_speed > 10 or temperature < 20:
            weather_like_queries.append(MenuRes.category.like(f"%Cold%"))
            weather_like_queries.append(MenuRes.category.like(f"%Iced%"))
        if temperature >= 20:
            weather_like_queries.append(MenuRes.category.like(f"%Hot%"))

    try:
        mood_subquery = session.query(MenuRes.id).filter(or_(*mood_like_queries)).subquery()
        weather_subquery = session.query(MenuRes.id).filter(or_(*weather_like_queries)).subquery()

        filter_queries = [
            NutritionRes.calories <= calory_upper_bound,
            NutritionRes.protein <= protein_grams,
            NutritionRes.fats <= fat_grams,
            NutritionRes.carbs <= carb_grams
        ]

        if weather.lower() == "yes":
            result = filter_queries.append(MenuRes.id.not_in(weather_subquery))
        if mood.lower() != "neutral":
            result = filter_queries.append(MenuRes.id.in_(mood_subquery))

        max_rec = req.max_rec if req.max_rec > 0 else 0
        result = session.query(MenuRes, NutritionRes).join(MenuRes).filter(*filter_queries).limit(max_rec)

        if not result.count():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Menu with given criteria not found"
            )

        query = text(f"SELECT MAX(id_list) FROM recommendation")
        result_recommendation_id_list = session.execute(query)
        id_list = result_recommendation_id_list.fetchone()[0]
        id_list = 1 if id_list == None else id_list + 1

        query = text(f"""INSERT INTO weather (latitude, longitude, temperature, precipitation, wind_speed) 
                    VALUES ({latitude}, {longitude}, {temperature}, {precipitation}, {wind_speed})""")
        session.execute(query)
        session.commit()

        id_weather = session.execute(text("SELECT MAX(id) from weather")).fetchone()
        id_weather = id_weather[0] if id_weather[0] != None else 1

        rec_time = datetime.strptime(rec_time[:19], "%Y-%m-%d %H:%M:%S")

        recommendation_data = {
            "id_person": Authorize['sub'], 
            "id_list": id_list,
            "id_weather": id_weather,  
            "rec_time": rec_time,
            "mood": req.mood
        }

        query = text(f"""INSERT INTO recommendation (id_person, id_list, id_weather, rec_time, mood)
                        VALUES ({recommendation_data['id_person']}, 
                        {recommendation_data['id_list']}, 
                        {recommendation_data['id_weather']}, 
                        '{recommendation_data['rec_time']}', 
                        '{recommendation_data['mood']}')""")
        session.execute(query)
        session.commit()

        for menu_res, nutrition_res in result:
            query = text(f"INSERT INTO menu_rec (id_list, id_menu) VALUES ({id_list}, {menu_res.id})")
            session.execute(query)
            session.commit()
    except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Menu with given criteria not found"
            )

    rec = []
    for menu_res, nutrition_res in result:
        rec_dict = {
            "id": menu_res.id,
            "name": menu_res.name,
            "description": menu_res.description,
            "category": menu_res.category,
            "url_img": menu_res.url_img,
            "calories": nutrition_res.calories,
            "protein": nutrition_res.protein,
            "fats": nutrition_res.fats,
            "carbs": nutrition_res.carbs,
            "sugar": nutrition_res.sugar
        }
        rec.append(rec_dict)

    return rec

@recommendation_router.get('/recommendations')
async def get_recommendation_history(
    request: Request,
    Authorize: JWTBearer = Depends(JWTBearer(roles=["customer", "admin"])),
    mood: str = Query("all", enum=["happy", "loved", "focus", "chill", "sad", "scared", "angry", "neutral", "all"]),
    start_date: datetime = None,
    end_date: datetime = None):

    if start_date == None:
        start_date = datetime(2023, 1, 1)
    if end_date == None:
        end_date = datetime.now()

    try:
        user_id = Authorize['sub']
        query = text(f"""
                    SELECT menu.id, menu.name, menu.description, menu.category, menu.url_img, 
                    recommendation.mood, recommendation.rec_time 
                    FROM person JOIN recommendation JOIN menu_rec JOIN menu
                    WHERE person.id = recommendation.id_person AND person.id = '{user_id}'
                    AND recommendation.id_list = menu_rec.id_list AND menu_rec.id_menu = menu.id
                    ORDER BY rec_time DESC;
                    """)
        result = session.execute(query)

        if result.rowcount:
            rec_list = []
            for rec in result:
                if mood != "all" and mood.lower() != rec.mood.lower():
                    continue
                if rec.rec_time < start_date or rec.rec_time > end_date:
                    continue
                rec_dict = {
                    "id_menu": rec.id,
                    "name": rec.name,
                    "description": rec.description,
                    "category": rec.category,
                    "url_img": rec.url_img,
                    "mood": rec.mood,
                    "rec_time": rec.rec_time
                }
                rec_list.append(rec_dict)
            
            return rec_list
        else:
            return {
                "message": "You have not received any recommendation yet"
            }
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Something went wrong"
        )
    
@recommendation_router.delete('/recommendations')
async def delete_recommendation_history(
    request: Request,
    Authorize: JWTBearer = Depends(JWTBearer(roles=["customer", "admin"])),
    mood: str = Query("all", enum=["happy", "loved", "focus", "chill", "sad", "scared", "angry", "neutral", "all"]),
    start_date: datetime = None,
    end_date: datetime = None):

    if start_date == None:
        start_date = datetime(2023, 1, 1)
    if end_date == None:
        end_date = datetime.now()

    try:
        user_id = Authorize['sub']
        query = text(f"""
                    SELECT recommendation.id_rec, recommendation.id_list,
                    recommendation.mood, recommendation.rec_time 
                    FROM person JOIN recommendation JOIN menu_rec
                    WHERE person.id = recommendation.id_person AND person.id = '{user_id}'
                    AND recommendation.id_list = menu_rec.id_list ORDER BY rec_time DESC;
                    """)
        result = session.execute(query)

        if result.rowcount:
            rec_list = []
            for rec in result:
                if mood != "all" and mood.lower() != rec.mood.lower():
                    continue
                if rec.rec_time < start_date or rec.rec_time > end_date:
                    continue
                rec_dict = {
                    "id_rec": rec.id_rec,
                    "id_list": rec.id_list,
                    "mood": rec.mood,
                    "rec_time": rec.rec_time
                }
                rec_list.append(rec_dict)
            
            for rec in rec_list:
                query = text(f"DELETE FROM menu_rec WHERE id_list = {rec['id_rec']}")
                session.execute(query)
                session.commit()

                query = text(f"DELETE FROM recommendation WHERE id_rec = {rec['id_rec']}")
                session.execute(query)
                session.commit()

            return {
                "message": "Recommendation history deleted"
            }
        else:
            return {
                "message": "You have not received any recommendation yet"
            }
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Something went wrong"
        )