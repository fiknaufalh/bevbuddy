from pydantic import BaseModel
from typing import Literal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey
from datetime import datetime

class Recommendation(BaseModel):
    id_rec: int
    id_person: int
    id_menu: int
    id_weather: int
    rec_date: datetime
    mood: str

    class Config:
        json_schema_extra = {
            "example": {
                "id_rec": 1,
                "id_person": 1,
                "id_menu": 1,
                "id_weather": 1,
                "rec_date": "2021-01-01",
            }
        }

class RecommendationReq(BaseModel):
    gender: Literal ["Male", "Female"]
    age: int
    weight: float
    height: float
    activity: Literal ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"]
    mood: Literal ["happy", "loved", "focus", "chill", "sad", "scared", "angry", "neutral"] | None = None
    weather: Literal ["yes", "no"] | None = None,
    max_rec: int = 5

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "Male",
                "age": 20,
                "weight": 63.0,
                "height": 171.0,
                "activity": ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"],
                "mood": ["happy", "loved", "focus", "chill", "sad", "scared", "angry", "neutral"],
                "weather": "['yes', 'no'] - Are you concerned about the weather?",
                "max_rec": 5
            }
        }

Base = declarative_base()

class MenuRes(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    category = Column(String(255))
    url_img = Column(String(255))

class NutritionRes(Base):
    __tablename__ = 'nutrition'

    calories = Column(Float)
    protein = Column(Float)
    fats = Column(Float)
    carbs = Column(Float)
    sugar = Column(Float)
    id_menu = Column(Integer, ForeignKey('menu.id'), primary_key=True)