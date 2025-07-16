from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ADMIN_USERNAME: str
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
