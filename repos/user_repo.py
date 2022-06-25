from sqlmodel import Session, select

from db.db import engine
from models.user import User


def select_all():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res


def get(username):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()