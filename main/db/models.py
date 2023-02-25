from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .mysql import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(String(45)) #NOTE: need to hash
    is_active = Column(Boolean, default=True)
    role = Column(String(30), default="user")

    #items = relationship("Item", back_populates="owner")