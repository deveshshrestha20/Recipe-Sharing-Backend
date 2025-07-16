from fastapi import APIRouter, Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.core.oauth2 import require_role
from app.database.session import get_db
from app.models import User
from app.services.admin_service import dashboard, fetch_users, delete_specific_recipe, delete_specific_user

admin = APIRouter(prefix="/admin", tags=["admin"])

@admin.get("/")
def admin_dashboard(user=Depends(require_role("admin"))):
    return dashboard(user)

# _ = Depends(require_role("admin")) to signal it’s intentionally unused but required.

@admin.get("/users")
def get_all_users(_=Depends(require_role("admin")),db: Session = Depends(get_db),limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)):
    return fetch_users(db, limit = limit,offset = offset)

@admin.delete("/users/{user_id}")
def delete_user(user_id: int,_=Depends(require_role("admin")),db: Session = Depends(get_db)):
    return delete_specific_user(db,user_id)

@admin.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int,_=Depends(require_role("admin")),db: Session = Depends(get_db)):
    return delete_specific_recipe(db,recipe_id)

@admin.delete("/recipes/{recipe_id}/comments/{comment_id}")
def delete_comment(recipe_id: int,comment_id:int, _=Depends(require_role("admin")),db: Session = Depends(get_db)):
    return delete_specific_comment(db,recipe_id,comment_id)