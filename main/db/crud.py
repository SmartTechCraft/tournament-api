from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def validate_user_password(db: Session, username: str, password: str):
    return db.query(models.User).filter(models.User.username == username, models.User.password == password).first()

########## ROLES ##########
def get_role_by_name(db: Session, role_name: str):
    return db.query(models.Role).filter(models.Role.name == role_name).first()