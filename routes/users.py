from fastapi import APIRouter, HTTPException, status
from models.users import UserRegister, UserLogin
from utils.auth import AuthHandler
from utils.database_manager import session
from sqlalchemy import text
from utils.config import settings

user_router = APIRouter(tags=["User"])

@user_router.post('/register', status_code=status.HTTP_201_CREATED)
def register(inputUser: UserRegister):

    if (len(inputUser.username) < 4):
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
                            detail="The username must have a minimum of 4 characters")
    
    if (len(inputUser.password) < 6):
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
                            detail="The password must have a minimum of 6 characters")
    
    admin_token = settings.admin_token
    if (inputUser.role == 'admin' and inputUser.token != admin_token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please enter admin token correctly!")
    
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
        return {"message": "Account registered successfully!"}
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail="Username has been taken, please choose another username!")


@user_router.post('/login')
def login(inputUser: UserLogin):
    users = session.execute(text("""SELECT id, username, fullname, email, password, role 
                                 FROM person WHERE username=:uname"""), {"uname":inputUser.username})
    
    for user in users:
        if not AuthHandler().verify_password(plain_password=inputUser.password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password!')

        fullName = user.fullname
        firstName = fullName.split()[0]

        token = AuthHandler().encode_token(
            user_id=user.id, 
            username=user.username, 
            fullname=user.fullname, 
            email=user.email, 
            role=user.role
        )

        return {'message': f'Login successful. Welcome, {firstName}!','token': token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Username not registered!')
