from fastapi import FastAPI
from fastapi.responses import FileResponse
from routes.menus import menu_router
from routes.nutritions import nutrition_router
from routes.recommendations import recommendation_router
import uvicorn

app = FastAPI()

app.include_router(menu_router)
app.include_router(nutrition_router)
app.include_router(recommendation_router)

@app.get("/")
def root():
    return {"message": f"Welcome to BevBuddy! (Created by: Fikri Naufal Hamdi)"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)