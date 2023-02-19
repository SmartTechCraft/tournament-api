from fastapi import FastAPI
from routes.users import router as users_router

app = FastAPI()

@app.get("/")
def index():
    return {"backend": "backend is running"}


app.include_router(users_router, tags=['users'])