from sqlalchemy import Column, Integer, ForeignKey

from app.database.base import Base

class Likes(Base):
    __tablename__ = 'likes'
    recipe_id = Column(Integer, ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True,nullable=False)
