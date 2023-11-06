from pydantic import BaseModel

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