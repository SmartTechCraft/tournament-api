from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import router as user_router
from routes.role import router as role_router
from routes.steamapi import router as steam_api_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"backend": "backend is running"}

app.include_router(user_router, tags=['user'], prefix='/user')
app.include_router(role_router, tags=['role'], prefix='/role')
app.include_router(steam_api_router, tags=["steamapi"], prefix='/steamapi')