from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    password: str
    role: str

    class Config:
        schema_extra = {
            "example": {
                "username": "fiknaufalh",
                "fullname": "Fikri Naufal Hamdi",
                "email": "18221096@std.stei.itb.ac.id",
                "password": "weakpassword",
                "role": "customer"
            }
        }

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "fiknaufalh",
                "password": "weakpassword"
            }
        }
