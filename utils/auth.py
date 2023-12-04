import jwt
from fastapi import HTTPException, Security, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv, dotenv_values
from utils.config import settings

load_dotenv()
config = dotenv_values(".env")

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"])
    # secret = "EstrellasDeQuatro"
    # secret = config['SECRET_KEY']
    secret = settings.secret_key
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encode_token(self, user_id, username, fullname, email, role):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=300),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'role': role,
            'username': username,
            'fullname': fullname,
            'email': email
        }
        
        return jwt.encode(
            payload,
            self.secret,
            # algorithm="HS256"
            # algorithm=config['ALGORITHM']
            algorithm=settings.algorithm
        )
        
    def decode_token(self, token):
        try:
            payload = jwt.decode(token,self.secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Invalid token')
        
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)


class JWTBearer(HTTPBearer):
    authHandler = AuthHandler()
    def __init__(self, auto_error:  bool = True, roles: list = None):
        super(JWTBearer,self).__init__(auto_error=auto_error)
        self.roles = roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Scheme Invalid")
            decoded = self.authHandler.decode_token(credentials.credentials)
            if decoded is not None:
                if self.roles and decoded.get("role") not in self.roles:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unauthorized: Invalid role')
                return decoded
        raise HTTPException(status_code=403, detail='Invalid token')
