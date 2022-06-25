from fastapi import HTTPException, Security,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
import datetime
from repos.user_repo import get

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    secret = 'HiUYuyCAmCdRLLK68uXQwiT1gu8eOdF2l2Y8DRjpGzc'

    def get_password_hash(self,password):
        return self.pwd_context.hash(password)


    def verify_password(self,pwd,hashed_pwd):
        return self.pwd_context.verify(pwd,hashed_pwd)

    def encode_token(self,user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }

        return jwt.encode(payload,self.secret,algorithm='HS256')

    def decode_token(self,token):
        try:
            payload = jwt.decode(token,self.secret,algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401,detail='Expired signature')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401,detail='Ivalid token')


    def auth_wrapper(self,auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )
        username = self.decode_token(auth.credentials)
        if username is None:
            raise credentials_exception
        user = get(username)
        if user is None:
            raise credentials_exception
        return user        