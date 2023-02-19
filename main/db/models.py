from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .mysql import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(String(45))
    is_active = Column(Boolean, default=True)

    #items = relationship("Item", back_populates="owner")