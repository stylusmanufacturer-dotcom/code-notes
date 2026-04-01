from fastapi import FastAPI
from app.api.v1.routes import auth, notes, pages
from app.db.session import engine
from app.db.base_all import Base
from app.models import user, note
from app.core.templating import templates
from fastapi.staticfiles import StaticFiles



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])
app.include_router(pages.router, prefix="", tags=["pages"])
Base.metadata.create_all(bind=engine)
