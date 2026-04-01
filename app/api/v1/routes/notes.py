from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from starlette import schemas
from starlette.responses import RedirectResponse

from ....schemas.note import NoteCreate, NoteResponse
from ....crud.note import create_note, get_note, get_notes, delete_note
from ....db.session import get_db
from ..dependencies.auth import get_current_user
from ....crud.user import get_user_by_email

router = APIRouter()

@router.post("/", response_model=NoteResponse)
def create_note_route(title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user_by_email(db, email=current_user)
    note_data = NoteCreate(title=title, content=content)
    create_note(note_data, user.id, db)
    return RedirectResponse(url="/", status_code=302)


@router.get("/{note_id}", response_model=NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user_by_email(db, email=current_user)
    return get_note(note_id, db)


@router.get("/", response_model=list[NoteResponse])
def read_notes(notes: NoteCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user_by_email(db, email=current_user)
    return get_notes(user.id, db)

@router.delete("/{note_id}", response_model=NoteResponse)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return delete_note(note_id, db)