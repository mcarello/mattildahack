from fastapi import FastAPI
import uvicorn
from routers.users import user_router
from routers.fintech import fintech_router

app = FastAPI()

app.include_router(user_router)
app.include_router(fintech_router)

if __name__== '__main__':
    uvicorn.run('main:app',host="localhost",port=8000,reload=True)
    #create_db_and_tables()