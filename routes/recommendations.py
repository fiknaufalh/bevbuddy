from fastapi import APIRouter, HTTPException, status
from models.recommendations import RecommendationReq
import utils.tdee_calculator as tdee
from utils.database_manager import session
from sqlalchemy import text

recommendation_router = APIRouter(tags=['Recommendation'])

@recommendation_router.post('/recommendations')
async def create_recommendation(req: RecommendationReq):

    calory_upper_bound = tdee.calculate_tdee(req.gender, req.age, req.weight, req.height, req.activity)
    protein_grams, fat_grams, carb_grams = tdee.calculate_macros(calory_upper_bound)

    query = text(f"""SELECT * FROM menu JOIN nutrition ON menu.id = nutrition.id_menu
                 WHERE calories <= {calory_upper_bound} AND protein <= {protein_grams} 
                 AND fats <= {fat_grams} AND carbs <= {carb_grams} 
                 ORDER BY calories DESC LIMIT 3""")

    result = session.execute(query)
    session.commit()

    if not result.rowcount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Menu with given criteria not found"
        )

    rec = []
    for row in result:
        rec_dict = {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "category": row.category,
            "url_img": row.url_img,
            "calories": row.calories,
            "protein": row.protein,
            "fats": row.fats,
            "carbs": row.carbs,
            "sugar": row.sugar
        }
        rec.append(rec_dict)

    return rec
