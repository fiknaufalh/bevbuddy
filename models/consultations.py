from pydantic import BaseModel
from typing import Literal

class Consultation(BaseModel):
    consultation_date: str
    consultation_time: str

    class Config:
        json_schema_extra = {
            "example": {
                "consultation_date": "2023-12-31",
                "consultation_time": "10:00"
            }
        }
