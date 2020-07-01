from fastapi import FastAPI

app = FastAPI()

@app.get('/login')
async def login():
    return {"message":"hello"}

@app.get('/user/(:id)')
async def userID(id):
    return {"user":{
        "id":"123",
        "name":"Wesley"
    }}