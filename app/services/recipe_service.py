from fastapi import HTTPException
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from starlette import status
from starlette.responses import Response
from app.models import Recipe, User, Likes
from app.schemas import RecipeCreate
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeUpdate, RecipeWithLikes



def create_new_recipe(recipe_data: RecipeCreate, user_id: int,db: Session ):
    # Convert Pydantic -> SQLAlchemy model
    new_recipe = Recipe(**recipe_data.model_dump(), chef_id=user_id)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

def get_all_recipes(db: Session):

    # recipes = db.query(Recipe).all()
    recipes = db.query(Recipe, func.count(Likes.recipe_id).label('likes_count')).join(Likes, Likes.recipe_id == Recipe.id,isouter=True).group_by(Recipe.id).all()

    return [
        RecipeWithLikes(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients,
            description=recipe.description,
            image_url=recipe.image_url,
            chef_id=recipe.chef_id,
            likes_count=likes_count
        )
        for recipe, likes_count in recipes
    ]

def get_specific_recipe(recipe_id: int,user_id:int, db: Session):

    recipes = db.query(Recipe, func.count(Likes.recipe_id).label('likes_count')).join(Likes, Likes.recipe_id == Recipe.id,isouter=True).group_by(Recipe.id).filter(Recipe.id == recipe_id).first()

    if recipes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    recipe, likes_count = recipes

    return RecipeWithLikes(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients,
            description=recipe.description,
            image_url=recipe.image_url,
            chef_id=recipe.chef_id,
            likes_count=likes_count
        )



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


