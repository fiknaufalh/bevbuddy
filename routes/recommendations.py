from fastapi import APIRouter, HTTPException, Request, Depends, status
from models.recommendations import RecommendationReq, MenuRes, NutritionRes
from utils.auth import JWTBearer
import utils.tdee_calculator as tdee
from utils.weather_api import get_weather
from utils.location_api import get_location
from utils.database_manager import session
from sqlalchemy import or_, text
from datetime import datetime

recommendation_router = APIRouter(tags=['Recommendation'])

@recommendation_router.post('/recommendations')
async def create_recommendation(
    req: RecommendationReq, 
    request: Request,
    Authorize: JWTBearer = Depends(JWTBearer(roles=["customer", "admin"]))):

    client_ip = request.client.host if request.client.host != "127.0.0.1" else "182.253.194.14"
    latitude, longitude, rec_time = get_location(client_ip)
    temperature, precipitation, wind_speed = get_weather(latitude, longitude)

    CALORY_PERCENTAGE = 0.4
    PROTEIN_PERCENTAGE = 0.7
    FAT_PERCENTAGE = 0.7
    CARB_PERCENTAGE = 0.7

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
        if precipitation > 0 or wind_speed > 10 or temperature < 5:
            weather_like_queries.append(MenuRes.category.like(f"%Cold%"))
            weather_like_queries.append(MenuRes.category.like(f"%Iced%"))
        if temperature > 25:
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

        query = text(f"SELECT MAX(id_list) FROM menu_rec")
        result_menu_rec = session.execute(query)
        id_list = result_menu_rec.fetchone()[0]
        id_list = 1 if id_list == None else id_list + 1

        for menu_res, nutrition_res in result:
            query = text(f"INSERT INTO menu_rec (id_list, id_menu) VALUES ({id_list}, {menu_res.id})")
            session.execute(query)
            session.commit()


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
