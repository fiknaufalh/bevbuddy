from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi import FastAPI, Body
from models.users import UserRegisterModel, UserLoginSchema, users
from utils.auth import AuthHandler
from utils.database_manager import session
from sqlalchemy import text

user_router = APIRouter(tags=["User"])

@user_router.post('/register', status_code=201)
def register(inputUser: UserRegisterModel):
    if (len(inputUser.username) <= 3):
        raise HTTPException(status_code=405, detail="Username harus memiliki minilmal 4 karakter")
        return
    
    if (len(inputUser.password) <= 5):
        raise HTTPException(status_code=405, detail="Password harus memiliki minimal 6 karakter")
        return
    
    hashed_password = AuthHandler().get_password_hash(passsword=inputUser.password)

    newUser = {"fullname": inputUser.fullname, "username": inputUser.username, "passkey": hashed_password}

    query = text("INSERT INTO person (fullname, username, passkey) VALUES (:fullname, :username, :passkey)")
    try:
        session.execute(query, newUser)
        session.commit()
        return {"message": "Akun Berhasil Didaftarkan!"}
    except:
        raise HTTPException(status_code=406, detail="Username sudah diambil, silakah pilih username lain!")


@user_router.post('/login')
def login(inputUser: UserLoginSchema):
    users = session.execute(text("SELECT username, passkey, fullname FROM person WHERE username=:uname"), {"uname":inputUser.username})
    hashed_password = AuthHandler().get_password_hash(passsword=inputUser.password)
    for user in users:
        if not AuthHandler().verify_password(plain_password=inputUser.password, hashed_password=user[1]):
            raise HTTPException(status_code=401, detail='Username atau password salah!')
            return
        fullName = user[2]
        firstName = fullName.split()[0]
        token = AuthHandler().encode_token(user.username)
        return {'message': f'login berhasil! Selamat datang, {firstName}!',
                'token': token}
    raise HTTPException(status_code=401, detail='Username tidak terdaftar!')

@user_router.get('/users')
async def get_all_users():
    query = text("SELECT * FROM person")
    result = session.execute(query)
    
    users = []
    for row in result:
        user_dict = {
            "fullname": row.fullname,
            "username": row.username,
            "passkey": row.passkey
        }
        users.append(user_dict)
    
    return users