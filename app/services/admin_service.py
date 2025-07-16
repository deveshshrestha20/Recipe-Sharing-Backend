from starlette import status
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.core.config import settings
from app.core.security import hash_password
from app.models import User, Recipe, Comments
import logging


def dashboard(user):
    return {"msg": f"Welcome Admin {user.username}!"}

def seed_admin_user(db: Session):
    existing_admin = db.query(User).filter(User.role == "admin").first()

    if existing_admin:
        logging.info("Admin user already exists. Skipping creation.")
        return False

    # Avoid raising HTTPException during startup seeding HTTPException is designed for FastAPI request handlers, not for startup logic. Better to raise a standard Exception or just log and return.
    # Raising HTTPException in startup could crash your app unnecessarily.

    admin_username = settings.ADMIN_USERNAME
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD

    if not admin_username or not admin_email or not admin_password:
        logging.error("Admin credentials are missing in settings.")
        return False

    admin_user = User(
        username=admin_username,
        email=admin_email,
        hashed_password=hash_password(admin_password),
        role="admin"
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    logging.info(f"Admin user '{admin_username}' created successfully.")
    return True

def fetch_users(db:Session, limit: int, offset: int):
    users = db.query(User).order_by(User.id).limit(limit).offset(offset).all()
    return users

def delete_specific_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def delete_specific_recipe(db: Session, recipe_id: int):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    db.delete(recipe)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def delete_specific_comment(db: Session, recipe_id: int,comment_id: int):
    delete_recipe = db.query(Comments).filter(Comments.recipe_id == recipe_id).filter(Comments.comment_id == comment_id).first()

    if delete_recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment to the recipe not found")

    db.delete(delete_recipe)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
