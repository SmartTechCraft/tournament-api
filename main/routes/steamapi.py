import db.models as models
import db.schemas as schemas
import steamapi.steam_api as steam

from auth.permission import Permission
from auth.auth_bearer import JwtBearer
from auth.auth_handler import sign_jwt, decode_jwt

from db.mysql import sessionLocal, engine
from db import crud
from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

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

@router.get('/get/user/{vanityurl}')
def get_user(request: Request, vanityurl: str, db: Session=(Depends(get_db))):

    if (has_permission_to_view('/get/user/{steamid}', db, crud.get_user_by_username(db=db,username=get_jwt_content(request)['user_name']))):
        steam_data = steam.SteamApi().get_user().by_url_id(vanityurl)
        return {'steamdata': steam_data}
    raise HTTPException(status_code=405, detail="You are not allowed to view this route")

@router.get('/get/basic-info/{steamid}')
def get_basic_info(request: Request, steamid: int, db: Session=Depends(get_db)):

    if (has_permission_to_view('/get/user/{steamid}', db, crud.get_user_by_username(db=db,username=get_jwt_content(request)['user_name']))):
        steam_data = steam.SteamApi().get_user_info().basic_info(steam_id=steamid)
        return {'steamdata': steam_data}
    raise HTTPException(status_code=405, detail="You are not allowed to view this route")

@router.get('/get/recently-played/{steamid}')
def get_recently_played_games(request: Request, steamid: int, db: Session=Depends(get_db)):

    if (has_permission_to_view('/get/user/{steamid}', db, crud.get_user_by_username(db=db,username=get_jwt_content(request)['user_name']))):
        steam_data = steam.SteamApi().get_user_info().recently_played_games(steam_id=steamid)
        return {'steamdata': steam_data}
    raise HTTPException(status_code=405, detail="You are not allowed to view this route")