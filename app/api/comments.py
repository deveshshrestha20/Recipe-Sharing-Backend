from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.session import get_db
from app.models import User
from app.schemas import CommentInput
from app.schemas.comment import CommentResponse
from app.core.oauth2 import get_current_user
from app.services.comment_service import creating_comment, deleting_comment

router = APIRouter(prefix="/recipes/{recipe_id}/comment", tags=["Comment"])


@router.post("/",response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(recipe_id: int,comment: CommentInput,db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return creating_comment(recipe_id,user.id,db,comment)

@router.delete("/{comment_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(recipe_id: int,comment_id:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return deleting_comment(recipe_id,user.id,comment_id,db)

@router.get("/test/{comment_id}")
def test_comment(recipe_id: int, comment_id: int, db: Session = Depends(get_db)):
    return {
        "recipe_id": recipe_id,
        "comment_id": comment_id,
        "message": "Router is working!"
    }

