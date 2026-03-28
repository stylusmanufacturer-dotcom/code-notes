from fastapi import FastAPI
from app.api.v1.routes import auth, notes

from app.db.session import engine
from app.db.base import Base

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])

Base.metadata.create_all(bind=engine)
