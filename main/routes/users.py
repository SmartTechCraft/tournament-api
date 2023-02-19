import db.models as models
import db.schemas as schemas

from db.mysql import sessionLocal, engine
from db import crud
from fastapi import Depends, APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if (db_user):
        raise HTTPException(status_code=400, detail="There is already user with that username registered")
    return crud.create_user(db=db, user=user)

#@router.get('/users/', response_description="lists all the users", response_model=List[schemas.User.])
#def read_users(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    #users = crud.get_users(db)
    #return users