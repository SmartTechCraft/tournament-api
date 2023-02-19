from fastapi import FastAPI
from routes.user import router as user_router

app = FastAPI()

@app.get("/")
def index():
    return {"backend": "backend is running"}

app.include_router(user_router, tags=['user'], prefix='/user')