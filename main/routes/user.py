import db.models as models
import db.schemas as schemas

from auth.auth_bearer import JwtBearer
from auth.auth_handler import sign_jwt, decode_jwt

from db.mysql import sessionLocal, engine
from db import crud
from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
router = APIRouter()
roles = ['player', 'developer', 'admin', 'supervisor']

def get_jwt_content(token: str):
    return decode_jwt(token=token)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/create', dependencies=[Depends(JwtBearer())], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)

    if (db_user):
        raise HTTPException(status_code=400, detail="There is already a user with that username registered")
    return crud.create_user(db=db, user=user)

@router.post('/login')
async def user_login(user: schemas.UserLogin, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    
    if (db_user and crud.validate_user_password(db=db, username=user.username, password=user.password)):
        return sign_jwt(user.username, db_user.role)
    raise HTTPException(status_code=401, detail="wrong username or password")

@router.get('/get/{username}', dependencies=[Depends(JwtBearer())])
def get_user(request: Request, username: str, db: Session=Depends(get_db)):
    jwt = get_jwt_content(request.headers.get('authorization').split('Bearer ', 1)[1])
    db_user = crud.get_user_by_username(db=db, username=username)

    if (jwt):
        if (jwt['user_name'] == username and username == db_user.username): #NOTE: we need to add roles
            return db_user
        raise HTTPException(status_code=401, detail="you have no permission to do this")
    return {}