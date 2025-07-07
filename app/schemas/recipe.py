from typing import Optional

from pydantic import BaseModel
from pydantic.config import ConfigDict


class RecipeCreate(BaseModel):
    title: str
    ingredients: str
    description: str
    image_url: Optional[str] = None

class RecipeOut(BaseModel):
    id: int
    title: str
    ingredients: str
    description: str
    image_url: str
    chef_id: int

    model_config = ConfigDict(from_attributes=True)