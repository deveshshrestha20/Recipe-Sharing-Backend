from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DATABASE_NAME: str
    # DATABASE_USERNAME: str
    # DATABASE_PASSWORD: str
    # DATABASE_HOSTNAME: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
