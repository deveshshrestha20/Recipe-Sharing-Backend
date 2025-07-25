from typing import Optional, List

from pydantic import BaseModel
from pydantic.config import ConfigDict

from app.schemas.comment import CommentResponse


# For RecipeCreate — no extra config is needed. It works with dictionaries.
class RecipeCreate(BaseModel):
    title: str
    ingredients: str
    description: str
    image_url: Optional[str] = None

#
# For this , the RecipeOut and the RecipeUpdate provides a SQLAlchemy object, not a dictionary.
#
# Pydantic doesn’t understand it unless you tell it:
#
# “Hey, this is an object. Read it using .title, not ["title"].”

# That’s why you add:
# model_config = ConfigDict(from_attributes=True)
class RecipeOut(BaseModel):
    id: int
    title: str
    ingredients: str
    description: str
    image_url: str
    chef_id: int

    model_config = ConfigDict(from_attributes=True)

class RecipeWithCounts(BaseModel):
    id: int
    title: str
    ingredients: str
    description: str
    image_url: str
    chef_id: int
    likes_count: int
    comments_count: int

    model_config = ConfigDict(from_attributes=True)

class RecipeDetailResponse(BaseModel):
    recipe: RecipeWithCounts
    comments: List[CommentResponse]

    model_config = ConfigDict(from_attributes=True)

class RecipeUpdate(BaseModel):
    title: Optional[str]
    ingredients: Optional[str]
    description: Optional[str]
    image_url: Optional[str]

    model_config = ConfigDict(from_attributes=True)