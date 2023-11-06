from pydantic import BaseModel
from datetime import datetime

class Weather(BaseModel):
    id: int
    time: datetime
    latitude: float
    longitude: float
    temperature: float
    wind_speed: float
    precipitation: float

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "time": "2023-11-06T20:00",
                "latitude": 40.730610,
                "longitude": -73.935242,
                "temperature": 24.4,
                "wind_speed": 4.7,
                "precipitation": 0.10
            }
        }