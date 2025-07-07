from fastapi import HTTPException,status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.core import oauth2
from app.core.security import hash_password, verify_password
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User

# What this register function should do :
# 1. Check if the user and email already exists.
# 2. Hash the password.
# 3. Create and save the user in the database.

def register_user(user_data: UserCreate, db: Session):
        # Checking if it has an existing username
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

        # Checking if it has an existing email
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        # Hashing the password from the function in core security.py file
        hashed_pw = hash_password(user_data.password)

        # Creating a new user instance to be saved to the DB
        new_user = User(
            username=user_data.username,
            email=str(user_data.email),
            hashed_password=hashed_pw
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user


def login_user(form_data: OAuth2PasswordRequestForm, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'Invalid Credentials')

    if not verify_password(form_data.password,str(user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    #Returning a JWT Token

    access_token = oauth2.create_access_token(data = {"sub": str(user.id)})

    return {'access_token': access_token, "token_type": "bearer"}




