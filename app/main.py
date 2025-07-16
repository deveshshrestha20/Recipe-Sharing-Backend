from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.recipes import router as recipes_router
from app.api.likes import router as likes_router
from app.api.comments import router as comments_router
from app.api.admin import admin as admin_router
from app.database.session import SessionLocal
from app.services.admin_service import seed_admin_user


@asynccontextmanager
async def lifespan(app: FastAPI ):
    # Seed admin
    print("Created tables...")
    db = SessionLocal()
    try:
        seed_admin_user(db)
    finally:
        db.close()


    # create_tables()
    yield
    print("Shutting down...")


app = FastAPI(title = "Recipe Sharing Platform",lifespan=lifespan)

app.include_router(auth_router)
app.include_router(recipes_router)
app.include_router(likes_router)
app.include_router(comments_router)
app.include_router(admin_router)
@app.get("/")
async def root():
    print("Hello Worlds frre")
    return {"message": "Hello World fsdfd"}



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
