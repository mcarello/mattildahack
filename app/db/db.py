import os

from sqlmodel import create_engine
from sqlmodel import Session


sqlite_url = 'postgresql+psycopg2://postgres:postgres@db:5432'
engine = create_engine(sqlite_url, echo=True)
session = Session(bind=engine)