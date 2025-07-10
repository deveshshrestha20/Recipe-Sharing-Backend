from fastapi import APIRouter, Depends
from fastapi.params import Path
from sqlalchemy.orm import Session
from starlette import status

from app.database.session import get_db
from app.schemas.like import Like, LikeResponse
from app.core.oauth2 import get_current_user
from app.models import User
from app.services.like_service import like

router = APIRouter(prefix="/recipes/{recipe_id}/like", tags=["Like"])


@router.post("/", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
def like_recipe(like_data: Like,recipe_id: int = Path(...), db : Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return like(recipe_id,like_data,current_user.id,db)


@router.get("/test")
def test():
    return {"message": "Likes router is working"}