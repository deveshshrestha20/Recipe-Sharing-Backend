from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.core.oauth2 import get_current_user
from app.models import User

from app.schemas.recipe import RecipeOut, RecipeCreate, RecipeUpdate

from app.database.session import get_db
from app.services.recipe_service import create_new_recipe, get_all_recipes, delete_specific_recipe, get_specific_recipe, \
    update_recipe

router = APIRouter(prefix="/recipes", tags=["Recipe"])

@router.post("/create",status_code=status.HTTP_201_CREATED, response_model = RecipeOut )
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    print("Received ingredients type:", type(recipe.ingredients))
    return create_new_recipe(recipe,current_user.id,db )


@router.get("/",status_code=status.HTTP_200_OK, response_model = List[RecipeOut])
def fetch_recipe(db: Session = Depends(get_db)):
    return get_all_recipes(db)

@router.get("/{recipe_id}", status_code = status.HTTP_200_OK, response_model = RecipeOut)
def fetch_specific_recipe(recipe_id: int,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_specific_recipe(recipe_id,current_user.id,db)

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id:int ,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return delete_specific_recipe(recipe_id, current_user.id,db)

@router.put("/{recipe_id}", status_code=status.HTTP_200_OK, response_model = RecipeOut)
def update(recipe_id: int, recipe_data: RecipeUpdate , db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_recipe(recipe_id,recipe_data, current_user.id,db)