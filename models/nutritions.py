from pydantic import BaseModel

class Nutrition(BaseModel):
    id_menu: int
    calories: float
    protein: float
    fats: float
    carbs: float
    sugar: float

    class Config:
        json_schema_extra = {
            "example": {
                "id_menu": 2123736,
                "calories": 250,
                "protein": 2,
                "fats": 12,
                "carbs": 33,
                "sugar": 32
            }
        }

