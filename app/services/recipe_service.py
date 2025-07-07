from fastapi import HTTPException
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user
from starlette import status

from app.models import Recipe, User
from app.models.recipe import Recipe

from app.schemas import RecipeCreate
from app.models.recipe import Recipe

def create_new_recipe(recipe_data: RecipeCreate, user_id: int,db: Session ):
    # Convert Pydantic -> SQLAlchemy model
    new_recipe = Recipe(**recipe_data.model_dump(), chef_id=user_id)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

def get_all_recipes(db: Session) -> list[type[Recipe]]:
    return db.query(Recipe).all()

def delete_specific_recipe(recipe_id: int,user_id:int, db: Session):
    # Fetching the recipe
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Recipe not found")

    # Comparing the ids to make sure that only the chef who created the recipe can delete it
    if recipe.chef_id != user_id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this recipe")

    db.delete(recipe)
    db.commit()
    db.refresh(recipe)






    recipe.commit()
