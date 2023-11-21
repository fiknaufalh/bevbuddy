from fastapi import APIRouter, HTTPException, status
from models.users import UserRegister, UserLogin
from utils.auth import AuthHandler
from utils.database_manager import session
from sqlalchemy import text

user_router = APIRouter(tags=["User"])

@user_router.post('/register', status_code=status.HTTP_201_CREATED)
def register(inputUser: UserRegister):
    if (len(inputUser.username) < 4):
        raise HTTPException(status_code=405, detail="Username harus memiliki minilmal 4 karakter")
    
    if (len(inputUser.password) < 6):
        raise HTTPException(status_code=405, detail="Password harus memiliki minimal 6 karakter")
    
    hashed_password = AuthHandler().get_password_hash(password=inputUser.password)

    newUser = {
        "username": inputUser.username, 
        "fullname": inputUser.fullname,
        "email": inputUser.email, 
        "password": hashed_password,
        "role": inputUser.role
    }

    query = text("""INSERT INTO person (username, fullname, email, password, role) 
                 VALUES (:username, :fullname, :email, :password, :role)""")
    try:
        session.execute(query, newUser)
        session.commit()
        return {"message": "Akun Berhasil Didaftarkan!"}
    except:
        raise HTTPException(status_code=406, detail="Username sudah diambil, silakah pilih username lain!")


@user_router.post('/login')
def login(inputUser: UserLogin):
    users = session.execute(text("""SELECT id, username, fullname, email, password, role 
                                 FROM person WHERE username=:uname"""), {"uname":inputUser.username})
    
    for user in users:
        if not AuthHandler().verify_password(plain_password=inputUser.password, hashed_password=user.password):
            raise HTTPException(status_code=401, detail='Username atau password salah!')

        fullName = user.fullname
        firstName = fullName.split()[0]

        token = AuthHandler().encode_token(
            user_id=user.id, 
            username=user.username, 
            fullname=user.fullname, 
            email=user.email, 
            role=user.role
        )

        return {'message': f'login berhasil! Selamat datang, {firstName}!','token': token}
    raise HTTPException(status_code=401, detail='Username tidak terdaftar!')
