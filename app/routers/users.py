from fastapi import APIRouter,  HTTPException, status
from sqlmodel import SQLModel
from db.db import engine, session
from repos import user_repo
from models.user import User
from models.fintech import Account

user_router = APIRouter()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@user_router.get('/users',tags=['User Account'],description='List users')
def get_users():
    users = user_repo.select_all()

    return users

@user_router.get('/user/{username}',tags=['User Account'],description='Get user information')
def user(username: str):
    user = user_repo.get(username=username)
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Username not exist')

    return user


@user_router.post('/userAccount', status_code=status.HTTP_201_CREATED, tags=['User Account'],description='Register new user')
def register(user: User):
    item = user_repo.get(username=user.username)
    if item != None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username not available')

    u = User(username=user.username, name=user.name, surname_1= user.surname_1,
    surname_2=user.surname_2,email =user.email,rol=user.rol,
    status=user.status,password=user.password)

    session.add(u)
    session.commit()

    a = Account(user_id=user.username)

    session.add(a)
    session.commit()

    return u