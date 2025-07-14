from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from starlette import status
from starlette.responses import Response
from app.models import Likes, Comments
from app.schemas import RecipeCreate
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeUpdate,RecipeWithCounts



def create_new_recipe(recipe_data: RecipeCreate, user_id: int,db: Session ):
    # Convert Pydantic -> SQLAlchemy model
    new_recipe = Recipe(**recipe_data.model_dump(), chef_id=user_id)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

def get_all_recipes(db: Session):

    # recipes = db.query(Recipe).all()
    recipes = (db.query(
        Recipe,
        func.count(Likes.recipe_id).label('likes_count'),
        func.count(Comments.recipe_id).label("comments_count"))
        .join(Likes, Likes.recipe_id == Recipe.id,isouter=True)
        .join(Comments, Comments.recipe_id == Recipe.id,isouter=True)
        .group_by(Recipe.id)
        .all())

    return [
        RecipeWithCounts(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients,
            description=recipe.description,
            image_url=recipe.image_url,
            chef_id=recipe.chef_id,
            likes_count=likes_count,
            comments_count = comments_count
        )
        for recipe, likes_count,comments_count in recipes
    ]

# Use .scalar() when:
#
# Getting aggregate values (COUNT, SUM, AVG, etc.)
# You only need a single value
# Working with functions that return single values
#
# Use .first() when:
#
# Getting model instances
# You need the complete object with all its attributes
# Working with regular SELECT queries

def get_specific_recipe(recipe_id: int, user_id: int, db: Session):
    # Single query to get recipe with counts
    result = (
        db.query(
            Recipe,
            func.count(Likes.recipe_id).label('likes_count'),
            func.count(Comments.recipe_id).label('comments_count')
        )
        .outerjoin(Likes, Likes.recipe_id == Recipe.id)
        .outerjoin(Comments, Comments.recipe_id == Recipe.id)
        .filter(Recipe.id == recipe_id)
        .group_by(Recipe.id)
        .first()
    )

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    recipe, likes_count, comments_count = result

    # Separate query for comments with user info
    comments = (
        db.query(Comments)
        .options(joinedload(Comments.user))
        .filter(Comments.recipe_id == recipe_id)
        .all()
    )

    return {
        "recipe": RecipeWithCounts(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients,
            description=recipe.description,
            image_url=recipe.image_url,
            chef_id=recipe.chef_id,
            likes_count=likes_count ,
            comments_count=comments_count,
        ),
        "comments": [
            {
                "comment_id": comment.comment_id,
                "content": comment.content,
                "created_at": comment.created_at,
                "user_id": comment.user_id,
                "recipe_id": comment.recipe_id,
            }
            for comment in comments
        ]
    }


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


