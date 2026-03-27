from fastapi import FastAPI
from app.api.v1.routes import auth
from app.db.session import engine
from app.db.base import Base

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

Base.metadata.create_all(bind=engine)
