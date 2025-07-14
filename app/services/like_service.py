from fastapi import HTTPException,status
from starlette.responses import Response
from sqlalchemy.orm import Session
from app.models import Likes
from app.schemas.like import Like
from app.models.recipe import Recipe



def like(recipe_id: int,like_data: Like,user_id: int, db: Session):



    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    # like_data is a schema, Likes is a Model
    # Likes.recipe_id is the actual column in the database. recipe_id is the value from the URL path.
    like_query = db.query(Likes).filter(Likes.recipe_id == recipe_id, Likes.user_id == user_id)
    found_liked = like_query.first()

    # For liking Recipes
    if like_data.dir == 1:
        if found_liked:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"The user {user_id} already liked this recipe {recipe_id}")


        like_recipe = Likes(recipe_id = recipe_id, user_id = user_id)


        db.add(like_recipe)
        db.commit()
        db.refresh(like_recipe)
        return {"message": "Recipe Liked Successfully"}
    # For Unliking Recipes
    else:
        if found_liked is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Recipe is not liked")


        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Recipe unliked Successfully"}

