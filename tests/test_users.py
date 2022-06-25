from fastapi.testclient import TestClient
import pytest
from routers import *
from main import app
from db.db import  session
from repos import user_repo,fintech_repo
from models.user import User


client = TestClient(app)


user = user_repo.get(username="lmessi")
if user != None:
    
    acc = fintech_repo.get_account_by_user(user.username)
    trns = fintech_repo.get_transactions_by_account_id(acc.id)
    for trn in trns:
        session.delete(trn)    
    session.commit()

    session.delete(acc)
    session.delete(user)
    session.commit()

@pytest.fixture
def init_data():
    return User(username= "lmessi",name="Leonel",surname_1= "Messi", surname_2="Lopez",
    email="lmessi@example.com",rol="admin" , status= "A", password="lmessi01")

@pytest.fixture
def token(init_data):
    response = client.post(
        "/login",
        headers={"Content-Type": "application/json"},
        json={"username": init_data.username, "password": init_data.password})    

    return "Bearer " + response.json()["token"]

@pytest.fixture
def account(init_data,token):
    response = client.get(
        "/account/user/" + init_data.username,
        headers={"Content-Type": "application/json","Authorization": token},)    

    return response.json()["id"]

@pytest.mark.users
def test_incorrect_login():
    response = client.post(
        "/login",
        headers={"Content-Type": "application/json"},
        json={"username": "anyuser", "password": "anypass"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username and/or password"}

@pytest.mark.users
def test_correct_userRegistration(init_data):
    response = client.post(
        "/userAccount",
        headers={"Content-Type": "application/json"},

        json={ "username": init_data.username,"name": init_data.name,"surname_1": init_data.surname_1,
  "surname_2": init_data.surname_2,"email": init_data.email,"rol": init_data.rol,"status": init_data.status,"password": init_data.password}
    )
    assert response.status_code == 201
    assert response.json() == {}   

@pytest.mark.users
def test_deplicated_userAccount(init_data):
    response = client.post(
        "/userAccount",
        headers={"Content-Type": "application/json"},
        json={ "username": init_data.username,"name": init_data.name,"surname_1": init_data.surname_1,
  "surname_2": init_data.surname_2,"email": init_data.email,"rol": init_data.rol,"status": init_data.status,"password": init_data.password}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username not available"}  

@pytest.mark.users
def test_correct_login(init_data):
    response = client.post(
        "/login",
        headers={"Content-Type": "application/json"},
        json={"username": init_data.username, "password": init_data.password}
    )

    assert response.status_code == 200
    token = response.json()["token"]
    assert response.json() == {"token": token}

@pytest.mark.users
def test_get_all_users(init_data,token):
    response = client.get(
        "/users",
        headers={"Content-Type": "application/json","Authorization": token},
        json={"username": init_data.username, "password": init_data.password}
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

@pytest.mark.users
def test_get_user(init_data,token):
    response = client.get(
        "/user/" + init_data.username ,
        headers={"Content-Type": "application/json","Authorization": token},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json()["username"] == init_data.username

@pytest.mark.fintech
def test_deposit(token,account):
    response = client.post(
        "/account/deposit",
        headers={"Content-Type": "application/json","Authorization": token},
        json={"amount": 150000, "account_id": account},
    )

    assert response.status_code == 201
    assert response.json() == {"balance": 150000}


@pytest.mark.fintech
def test_withdraw(token,account):
    response = client.post(
        "/account/withdraw",
        headers={"Content-Type": "application/json","Authorization": token},
        json={"amount": 50000, "account_id": account},
    )

    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"balance": 100000}

@pytest.mark.fintech
def test_summary(token,account):
    response = client.get(
        "/account/" + account + "/summary",
        headers={"Content-Type": "application/json","Authorization": token},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

@pytest.mark.fintech
def test_balances(token):
    response = client.get(
        "/account/balances",
        headers={"Content-Type": "application/json","Authorization": token},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"    