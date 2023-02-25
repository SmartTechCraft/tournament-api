from typing import List, Union
from pydantic import BaseModel

class UserBase(BaseModel):

    username: str

class UserLogin(UserBase):

    username: str
    password: str

class UserCreate(UserBase):

    password: str

class User(UserBase):

    id: int
    is_active: bool
    role: str

    class Config:
        
        orm_mode = True