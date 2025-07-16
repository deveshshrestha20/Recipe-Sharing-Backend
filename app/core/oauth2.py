import os
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from app.database.session import get_db
from app.models import User
from app.schemas.user import TokenData

# the /login endpoint where users submit username/password and get back a JWT access token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

def create_access_token(data: dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc)+ expires_delta
    else:
        expire = datetime.now(timezone.utc)+ timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        # Decoding the JWT Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the ID
        id: str = payload.get('sub')
        if id is None:
            raise credentials_exception
        # Validate with the Schema
        token_data = TokenData(id=id)
    except JWTError as e:
        print(f"JWT Error: {e}")  # Add logging for debugging
        raise credentials_exception

    return token_data

# In a FastAPI app using JWT authentication, get_current_user is a dependency function that:
#
# ✅ Extracts and verifies the JWT access token from the request,
# ✅ Decodes it,
# ✅ Uses the token's data to find the logged-in user from the database,
# ✅ and returns the user object to protected routes.

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    # Convert ID from string to integer
    user = db.query(User).filter(User.id == int(token_data.id)).first()

    if user is None:
        raise credentials_exception
    # print(type(user))

    return user  #  Full User object returned


def get_admin_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    # Convert ID from string to integer
    user = db.query(User).filter(User.id == int(token_data.id)).first()

    if user is None:
        raise credentials_exception
    # print(type(user))

    if user.role == "admin":
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin"
        )


def create_refresh_token(data: dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days = 7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def require_role(required_role: str):
    def checker(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker



