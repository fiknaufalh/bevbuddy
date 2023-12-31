from fastapi import APIRouter, HTTPException, Depends, status
from utils.auth import JWTBearer, AuthHandler
from models.nutritions import Nutrition
from utils.database_manager import session
from sqlalchemy import text

nutrition_router = APIRouter(tags=['Nutrition'])

@nutrition_router.get('/nutritions')
async def get_all_nutritions():
    query = text("SELECT * FROM nutrition")
    result = session.execute(query)
    
    nutritions = []
    for row in result:
        nutrition_dict = {
            "id_menu": row.id_menu,
            "calories": row.calories,
            "protein": row.protein,
            "fats": row.fats,
            "carbs": row.carbs,
            "sugar": row.sugar
        }
        nutritions.append(nutrition_dict)
    
    return nutritions


@nutrition_router.get('/nutritions/{id}')
async def get_nutrition_by_id(id: int):
    query = text(f"SELECT * FROM nutrition WHERE id_menu = {id}")
    result = session.execute(query)

    if not result.rowcount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Nutrition with id {id} not found"
        )

    nutritions = []
    for row in result:
        nutrition_dict = {
            "id_menu": row.id_menu,
            "calories": row.calories,
            "protein": row.protein,
            "fats": row.fats,
            "carbs": row.carbs,
            "sugar": row.sugar
        }
        nutritions.append(nutrition_dict)
    
    return nutritions

@nutrition_router.post('/nutritions')
async def create_nutrition(nutrition: Nutrition, Authorize: JWTBearer = Depends(JWTBearer(roles=['admin']))):
    
    if not session.execute(text(f"SELECT * FROM menu WHERE id = {nutrition.id_menu}")).rowcount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Menu with id {nutrition.id_menu} not found"
        )
    
    try:
        query = text(f"""INSERT INTO nutrition (id_menu, calories, protein, fats, carbs, sugar) 
                    VALUES ({nutrition.id_menu}, {nutrition.calories}, {nutrition.protein}, 
                    {nutrition.fats}, {nutrition.carbs}, {nutrition.sugar})""")
        session.execute(query)
        session.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail=f"Nutrition with id {nutrition.id_menu} already exists"
        )

    return {"message": "Nutrition created successfully"}

@nutrition_router.put('/nutritions/{id}')
async def update_nutrition(id: int, nutrition: Nutrition, Authorize: JWTBearer = Depends(JWTBearer(roles=['admin']))):
    query = text(f"""UPDATE nutrition 
                 SET id_menu = {nutrition.id_menu}, calories = {nutrition.calories}, 
                 protein = {nutrition.protein}, fats = {nutrition.fats}, 
                 carbs = {nutrition.carbs}, sugar = {nutrition.sugar} 
                 WHERE id_menu = {id}""")
    result = session.execute(query)
    session.commit()

    if not result.rowcount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Nutrition with id {id} not found"
        )
    
    return {"message": "Nutrition updated successfully"}

@nutrition_router.delete('/nutritions/{id}')
async def delete_nutrition(id: int, Authorize: JWTBearer = Depends(JWTBearer(roles=['admin']))):
    query = text(f"DELETE FROM nutrition WHERE id_menu = {id}")
    result = session.execute(query)
    session.commit()

    if not result.rowcount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Nutrition with id {id} not found"
        )

    return {"message": "Nutrition deleted successfully"}

