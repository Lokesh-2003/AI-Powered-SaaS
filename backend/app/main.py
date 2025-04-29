from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.dependencies import get_db
from app.db.base import Base
from app.db.session import engine

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_application():
    app = FastAPI(title=settings.app_name)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(api_router, prefix="/api/v1")
    
    return app

app = get_application()

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to Resume Analyzer API"}