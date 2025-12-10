from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import engine
from app.db.base import Base
import os

app = FastAPI(title=settings.PROJECT_NAME)

# Ensure static directory exists
STATIC_DIR = "static/images"
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Create tables for new models
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Welcome to Multimodal Chat AI Service"}
