from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from enum import Enum as Enum_

class UserStatus(str, Enum_):
    ACTIVE = "A"
    BLOCKED = "B"

class UserRoles(str, Enum_):
    ADMIN = "admin"
    CLIENT = "client"

class User(SQLModel, table=True):
    username: str = Field(primary_key=True,index=True,nullable=False)
    name: str
    surname_1: Optional[str] = None
    surname_2: Optional[str] = None
    email: EmailStr    
    rol: UserRoles
    status: UserStatus
    password: str = Field(max_length=256, min_length=6)

class UserLogin(SQLModel):
    username: str
    password: str    