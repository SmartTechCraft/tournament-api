import db.models as models
import db.schemas as schemas

from auth.permission import Permission
from auth.auth_bearer import JwtBearer
from auth.auth_handler import sign_jwt, decode_jwt

from db.mysql import sessionLocal, engine
from db import crud
from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

CREATE_USER_ROUTE = '/create'
GET_USER_ROUTE = '/get/{username}'

models.Base.metadata.create_all(bind=engine)
router = APIRouter()

def get_jwt_content(request: Request):
    header = request.headers.get('authorization')
    if (header):
        token = header.split('Bearer ', 1)[1]
        return decode_jwt(token=token)
    raise HTTPException(status_code=405, detail="no authorization header found")

def has_permission_to_view(route: str, db, db_user) -> bool:
    if (Permission(db=db, db_user=db_user, crud=crud).can_view(route=route)):
        return True
    return False

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(CREATE_USER_ROUTE, dependencies=[Depends(JwtBearer())], response_model=schemas.User)
def create_user(request: Request, user: schemas.UserCreate, db: Session=Depends(get_db)):
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

@router.get(GET_USER_ROUTE, dependencies=[Depends(JwtBearer())])
def get_user(request: Request, username: str, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=username)

    if (has_permission_to_view(GET_USER_ROUTE, db, crud.get_user_by_username(db=db,username=get_jwt_content(request)['user_name']))):
        if (db_user):
            return {"username": db_user.username}
        raise HTTPException(status_code=404, detail="user not found")
    raise HTTPException(status_code=405, detail="You are not allowed to view this route")