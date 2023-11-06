from pydantic import BaseModel
from typing import Literal

class Recommendation(BaseModel):
    id_rec: int
    id_menu: int
    id_weather: int
    mood: str

    class Config:
        json_schema_extra = {
            "example": {
                "id_rec": 1,
                "id_menu": 1,
                "id_weather": 1,
                "mood": "Happy"
            }
        }

class RecommendationReq(BaseModel):
    gender: Literal ["Male", "Female"]
    age: int
    weight: float
    height: float
    activity: Literal ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"]

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "Male",
                "age": 20,
                "weight": 63.0,
                "height": 171.0,
                "activity": "lightly_active"
            }
        }