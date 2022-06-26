from sys import prefix
from fastapi import FastAPI
import uvicorn
from routers.users import user_router
from routers.fintech import fintech_router

app = FastAPI()


app.include_router(user_router,prefix="/api.mcarello.io/v1")
app.include_router(fintech_router,prefix="/api.mcarello.io/v1")



@app.get('/', status_code=200,description='status')
def get_status():
    return {'status': "ok"} 


if __name__== '__main__':
    uvicorn.run('main:app',host="localhost",port=8000,reload=True)
    ###create_db_and_tables()