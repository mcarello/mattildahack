from sqlmodel import Session, select

from db.db import engine
from models.fintech import Transaction,Account


def account_select_all():
    with Session(engine) as session:
        statement = select(Account)
        res = session.exec(statement).all()
        return res

def get_account_by_user(username):
    with Session(engine) as session:
        statement = select(Account).where(Account.user_id == username)
        return session.exec(statement).first()

def get_account_by_id(id):
    with Session(engine) as session:
        statement = select(Account).where(Account.id == id)
        return session.exec(statement).first()        

def get_transactions_by_account_id(id):
    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.account_id == id)
        ac = session.exec(statement).all()

        return ac 

def get_transaction_by_account(account_id):
    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.account_id == account_id)
        return session.exec(statement).first()

def get_transaction_by_id(id):
    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.id == id)
        return session.exec(statement).first()