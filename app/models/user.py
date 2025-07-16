import enum

from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database.base import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_chef = Column(Boolean, nullable=False, default=False)
    recipes = relationship("Recipe", back_populates="chef",cascade="all, delete-orphan")
    comments = relationship("Comments", back_populates="user",cascade="all, delete-orphan")
    # FOR RBAC ( Role Based Access Control )
    role = Column(Enum(RoleEnum),default=RoleEnum.user)



