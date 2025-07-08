from fastapi import HTTPException
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user
from starlette import status
from starlette.responses import Response

from app.models import Recipe, User
from app.models.recipe import Recipe

from app.schemas import RecipeCreate
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeUpdate


def create_new_recipe(recipe_data: RecipeCreate, user_id: int,db: Session ):
    # Convert Pydantic -> SQLAlchemy model
    new_recipe = Recipe(**recipe_data.model_dump(), chef_id=user_id)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

def get_all_recipes(db: Session) -> list[type[Recipe]]:
    return db.query(Recipe).all()

def get_specific_recipe(recipe_id: int,user_id:int, db: Session):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


def update_recipe(recipe_id: int,recipe_data: RecipeUpdate, user_id: int,db: Session):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if user_id != recipe.chef_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to make changes to this recipe")

    # To update the SQLAlchemy model (recipe), you need to loop through the fields and values the user provided.
    # But you can’t loop directly through a Pydantic model.
    # So that's why we convert it to a dict first which is how we can loop through the values and fields.

    # Exclude_unset property makes it so that only those new attribute values that has been given by the user are updated and the other values are kept same.
    # If exclude_unset property is not set, the title when only changed when edited , the other attributes are set to None , which differs from the behavior
    #    that we actually need.
    for key,value in recipe_data.model_dump(exclude_unset=True).items():
        setattr(recipe,key,value)

    db.commit()
    db.refresh(recipe)
    return recipe


def delete_specific_recipe(recipe_id: int,user_id:int, db: Session):
    # Fetching the recipe
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    # Comparing the ids to make sure that only the chef who created the recipe can delete it
    if recipe.chef_id != user_id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this recipe")

    db.delete(recipe)
    db.commit()
    return Response(status.HTTP_204_NO_CONTENT)


