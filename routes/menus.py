from fastapi import APIRouter, HTTPException, Depends, status
from utils.auth import JWTBearer, AuthHandler
from models.menus import Menu
from utils.database_manager import session
from sqlalchemy import text

menu_router = APIRouter(tags=['Menu'])

@menu_router.get('/menus')
async def get_all_menus():
    query = text("SELECT * FROM menu")
    result = session.execute(query)
    
    menus = []
    for row in result:
        menu_dict = {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "category": row.category,
            "url_img": row.url_img
        }
        menus.append(menu_dict)

    return menus

@menu_router.get('/menus/{id}')
async def get_menu_by_id(id: int):
    query = text(f"SELECT * FROM menu WHERE id = {id}")
    result = session.execute(query)
    
    menus = []
    for row in result:
        menu_dict = {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "category": row.category,
            "url_img": row.url_img
        }
        menus.append(menu_dict)

    if not result.rowcount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Menu with id {id} not found"
        )

    return menus

@menu_router.post('/menus')
async def create_menu(menu: Menu, Authorize: JWTBearer = Depends(JWTBearer(roles=["admin"]))):
    query = text(f"""INSERT INTO menu (id, name, description, category, url_img) 
                 VALUES ({menu.id}, '{menu.name}', '{menu.description}', '{menu.category}', '{menu.url_img}')""")
    session.execute(query)
    session.commit()
    return {"message": "Menu created successfully"}

@menu_router.put('/menus/{id}')
async def update_menu(id: int, menu: Menu, Authorize: JWTBearer = Depends(JWTBearer(roles=["admin"]))):
    query = text(f"""UPDATE menu SET name = '{menu.name}', description = '{menu.description}', 
                 category = '{menu.category}', url_img = '{menu.url_img}' 
                 WHERE id = {id}""")
    result = session.execute(query)
    session.commit()

    if not result.rowcount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Menu with id {id} not found"
    )
    
    return {"message": "Menu updated successfully"}

@menu_router.delete('/menus/{id}')
async def delete_menu(id: int, Authorize: JWTBearer = Depends(JWTBearer(roles=["admin"]))):
    query = text(f"DELETE FROM menu WHERE id = {id}")
    result = session.execute(query)
    session.commit()

    if not result.rowcount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Menu with id {id} not found"
        )

    return {"message": "Menu deleted successfully"}
