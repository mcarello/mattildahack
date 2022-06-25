import os

from sqlmodel import create_engine
from sqlmodel import Session

url = "postgresql://" + os.environ['POSTGRES_USER'] + ":" + os.environ['POSTGRES_PASSWORD'] + "@" + os.environ['POSTGRES_SERVER'] + ":" + os.environ['POSTGRES_PORT'] + "/" + os.environ['POSTGRES_DB']
#sqlite_url = 'postgresql+psycopg2://postgres:postgres@db:5432'
engine = create_engine(url, echo=True)
session = Session(bind=engine)



