from datetime import datetime, timezone
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.models import Recipe
from app.models.comment import Comments
from app.schemas.comment import CommentInput



def creating_comment(recipe_id: int, user_id: int,db: Session, comment_create = CommentInput):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    new_comment = Comments(
        content = comment_create.content,
        recipe_id=recipe_id,
        user_id=user_id,
        created_at=datetime.now(timezone.utc)

    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


def deleting_comment(recipe_id: int,user_id: int,comment_id: int,db: Session):

    comment = db.query(Comments).filter(Comments.comment_id==comment_id, Comments.recipe_id == recipe_id).first()

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if comment.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to perform this action ")

    db.delete(comment)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

