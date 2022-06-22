from typing import Optional,List
from datetime import datetime
from sqlmodel import  SQLModel,Relationship,Field
from enum import Enum as Enum_, IntEnum
import uuid as uuid_pkg

class TransactionType(str, Enum_):
    DEPOSIT = "D"
    WITHDRAW = "W"
    BALANCE = "B"

class AccountStatus(IntEnum):
    ACTIVE = 1
    BLOCKED = 2
    CANCELED = 3  

class Account(SQLModel, table=True):
    id: uuid_pkg.UUID  = Field(default_factory=uuid_pkg.uuid4,primary_key=True,index=True,nullable=False)
    balance: float  = Field(default=0.0)
    status: Optional[AccountStatus] = Field(default=AccountStatus.ACTIVE)
    user_id: str = Field(default=None, foreign_key="user.username")

    transactions: List["Transaction"] = Relationship(back_populates="account")


class Transaction(SQLModel, table=True):
    id: uuid_pkg.UUID  = Field(default_factory=uuid_pkg.uuid4,primary_key=True,index=True,nullable=False)
    type: TransactionType

    timestamp: datetime = Field(index=False, default_factory=datetime.utcnow)
    amount: float

    account_id: uuid_pkg.UUID = Field(default=None, foreign_key="account.id")
    account: Optional[Account] = Relationship(back_populates="transactions")

class Deposit(SQLModel):    
    amount: float 
    account_id: uuid_pkg.UUID = Field(default=None, foreign_key="account.id")

class Withdraw(SQLModel):    
    amount: float 
    account_id: uuid_pkg.UUID = Field(default=None, foreign_key="account.id")