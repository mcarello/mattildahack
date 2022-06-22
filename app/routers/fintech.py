from fastapi import APIRouter,  HTTPException, status
from sqlmodel import SQLModel
from db.db import engine, session
from repos import fintech_repo
from models.fintech import Account,Transaction,Deposit,Withdraw,TransactionType
from models.user import User
import uuid as uuid_pkg

fintech_router = APIRouter()

@fintech_router.get('/account/user/{username}',tags=['Fintech'],description='Get account data by username')
def account_by_user(username: str):
    account = fintech_repo.get_account_by_user(username=username)
    if account == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Account not exist')

    return account

@fintech_router.get('/account/balances',tags=['Fintech'],description='Get all accounts and balances')
def account_balances():
    accounts = fintech_repo.account_select_all()
    
    return accounts

@fintech_router.get('/transaction/{id}',tags=['Fintech'],description='Get transaction data by id')
def transaction_by_id(id: uuid_pkg.UUID):
    transaction = fintech_repo.get_transaction_by_id(id=id)
    if transaction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Transaction not exist')

    return transaction

@fintech_router.get('/account/{id}',tags=['Fintech'],description='Get account data by id')
def account_by_id(id: uuid_pkg.UUID):
    account = fintech_repo.get_account_by_id(id=id)
    if account == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Account not exist')

    return account

@fintech_router.get('/account/{id}/summary',tags=['Fintech'],description='Summary Checking Accounts')
def summary_account(id: uuid_pkg.UUID):
    account = fintech_repo.get_account_by_id(id=id)
    if account == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Account not exist')

    trns = fintech_repo.get_transactions_by_account_id(id=id)
    
    return {"id":account.id,"user_id":account.user_id,"status":account.status,"balance":account.balance,"transactions":trns}



@fintech_router.post('/account/deposit', status_code=status.HTTP_201_CREATED, tags=['Fintech'],description='Deposit funds in account')
def deposit_founds(deposit: Deposit):
    account = fintech_repo.get_account_by_id(id=deposit.account_id)
    if account == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Account not exist')

    trn = Transaction(type=TransactionType.DEPOSIT,amount=deposit.amount,account_id=deposit.account_id)


    account.balance = account.balance + deposit.amount

    session.add(account)
    session.add(trn)
    session.commit()
    return {"balance":account.balance}    

@fintech_router.post('/account/withdraw', status_code=status.HTTP_201_CREATED, tags=['Fintech'],description='Withdraw funds in account')
def withdraw_founds(withdraw: Withdraw):
    account = fintech_repo.get_account_by_id(id=withdraw.account_id)
    if account == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Account not exist')

    trn = Transaction(type=TransactionType.WITHDRAW,amount=withdraw.amount,account_id=withdraw.account_id)

    balance = account.balance - withdraw.amount
    if balance <0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Insufficient funds')

    account.balance = balance

    session.add(account)
    session.add(trn)
    session.commit()
    return {"balance":balance}    