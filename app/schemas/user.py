from typing import Optional

from pydantic import EmailStr,ConfigDict
from pydantic import BaseModel
import enum


class RoleEnum(str,enum.Enum):
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):

    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_chef: bool
    role: RoleEnum

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None



