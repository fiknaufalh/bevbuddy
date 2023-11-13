from pydantic import BaseModel, EmailStr

class UserRegisterModel(BaseModel):
    fullname: str
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Fikri Naufal Hamdi",
                "username": "fiknaufalh",
                "password": "weakpassword"
            }
        }

class UserLoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "fiknaufalh",
                "password": "weakpassword"
            }
        }
        
users = []