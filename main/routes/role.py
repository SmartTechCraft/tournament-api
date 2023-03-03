import db.models as models
import db.schemas as schemas

from auth.permission import Permission
from auth.auth_bearer import JwtBearer
from auth.auth_handler import decode_jwt

from db.mysql import sessionLocal, engine
from db import crud
from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
router = APIRouter()

GET_ROLE_BY_ID_ROUTE = '/get/{id}'

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


@router.get(GET_ROLE_BY_ID_ROUTE)
def get_role_by_id(request: Request, id: int, db: Session=Depends(get_db)):
    db_role = crud.get_role_by_id(db=db, role_id=id)

    if (db_role):
        if (has_permission_to_view(GET_ROLE_BY_ID_ROUTE, db, crud.get_user_by_username(db=db,username=get_jwt_content(request)['user_name']))):
                return db_role
        raise HTTPException(status_code=405, detail="You are not allowed to view this route")
    raise HTTPException(status_code=404, detail="role not found")