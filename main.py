from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.menus import menu_router
from routes.nutritions import nutrition_router
from routes.beverage_recommendations import recommendation_router
from routes.coffee_consultations import consultation_router
from routes.movies_recommendations import movie_router
from routes.users import user_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menu_router)
app.include_router(nutrition_router)
app.include_router(recommendation_router)
app.include_router(consultation_router)
app.include_router(movie_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": f"Welcome to BevBuddy!", "author": "Fikri Naufal Hamdi"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)