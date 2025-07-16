from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True,nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    ingredients = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable = True)

    chef_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    chef = relationship("User", back_populates="recipes")
    comments = relationship("Comments", back_populates="recipe",cascade="all, delete-orphan")