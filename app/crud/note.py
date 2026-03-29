from importlib.resources import contents

from ..models.note import Note
from ..schemas.note import NoteCreate
from sqlalchemy.orm import Session


def create_note(note: NoteCreate, user_id: int, db: Session):
    note = Note(title=note.title, content=note.content, owner_id=user_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
def get_notes(user_id: int, db: Session):
    return db.query(Note).filter(Note.user_id == user_id).all()

def get_note(note_id: int, db: Session):
    return db.query(Note).filter(Note.id == note_id).first()

def delete_note(note_id: int, db: Session):
    note = db.query(Note).filter(Note.id == note_id).first()
    db.delete(note)
    db.commit()
    return note

