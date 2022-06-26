from fastapi import APIRouter,  Depends ,HTTPException,status
from sqlmodel import SQLModel
from db.db import engine, session
from repos import user_repo
from models.user import User,UserLogin
from models.fintech import Account
from auth.auth import AuthHandler

user_router = APIRouter()
auth_handler = AuthHandler()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    
@user_router.get('/users',tags=['User Account'],description='List users')
def get_users(_user=Depends(auth_handler.get_current_user)):
    users = user_repo.select_all()

    return users

@user_router.get('/user/{username}',tags=['User Account'],description='Get user information')
def user(username: str,_user=Depends(auth_handler.get_current_user)):
    user = user_repo.get(username=username)
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Username not exist')

    return user


@user_router.post('/userAccount', status_code=status.HTTP_201_CREATED, tags=['User Account'],description='Register new user')
def register(user: User):
    item = user_repo.get(username=user.username)
    if item != None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username not available')

    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, name=user.name, surname_1= user.surname_1,
    surname_2=user.surname_2,email =user.email,rol=user.rol,
    status=user.status,password=hashed_pwd)

    session.add(u)
    session.commit()

    a = Account(user_id=user.username)

    session.add(a)
    session.commit()

    return u

@user_router.post('/login', tags=['User Account'])
def login(user: UserLogin):
    
    user_found = user_repo.get(user.username)
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

    token = auth_handler.encode_token(user_found.username)
    return {'token': token}    