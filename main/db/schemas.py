from typing import List, Union
from pydantic import BaseModel

class UserBase(BaseModel):

    username: str

class UserLogin(UserBase):

    username: str
    password: str

class UserCreate(UserBase):

    password: str
    email: str
    steamid: int

class User(UserBase):

    id: str
    is_active: bool
    role: str

    class Config:
        
        orm_mode = True

################ ROLES ################
class RoleBase(BaseModel):

    name: str
    level: int
    can_ban: bool
    can_support: bool
    can_manage: bool

class RoleCreate(RoleBase):

    can_view_routes: dict

class Role(RoleBase):

    id: int
    level: int
    can_ban: bool
    can_support: bool
    can_manage: bool

    class Config:

        orm_mode = True