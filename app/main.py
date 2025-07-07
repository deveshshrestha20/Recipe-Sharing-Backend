from contextlib import asynccontextmanager
from app.database.init_db import create_tables
from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.recipes import router as recipes_router

@asynccontextmanager
async def lifespan(app: FastAPI ):
    print("Creating tables...")
    create_tables()
    yield
    print("Shutting down...")

app = FastAPI(title = "Recipe Sharing Platform",lifespan=lifespan)

app.include_router(auth_router)
app.include_router(recipes_router)

@app.get("/")
async def root():
    print("Hello Worlds frre")
    return {"message": "Hello World fsdfd"}



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
