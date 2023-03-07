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

def get_role_by_id(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_all_roles(db: Session):
    return db.query(models.Role).all()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(name=role.name, level=role.level, can_ban=role.can_ban, can_support=role.can_support, can_manage=role.can_manage, can_view_routes=role.can_view_routes)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role