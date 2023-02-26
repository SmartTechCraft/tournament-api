from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from .mysql import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(String(45)) #NOTE: need to hash
    is_active = Column(Boolean, default=True)
    role = Column(String(30), default="player")

    #items = relationship("Item", back_populates="owner")

class Role(Base):

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    level = Column(Integer, default=1)
    can_ban = Column(Boolean, default=False)
    can_support = Column(Boolean, default=False)
    can_manage = Column(Boolean, default=False)
    can_view_routes = Column(JSON)