from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response
from app.schemas.user import UserCreate, UserOut, Token
from app.services.auth_service import register_user, login_user
import traceback
from fastapi.security import OAuth2PasswordRequestForm
from app.database.session import get_db
router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # print("🔥 Received user data:", user)
        return register_user(user, db)
    except Exception as e:
        # print("🔥 Registration error:", e)
        traceback.print_exc()   # <-- This will print full traceback in console
        raise HTTPException(status_code=500, detail="Email already exists")

@router.post("/login", response_model = Token)
def login(response: Response,form_data :OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    return login_user(form_data,response, db)



