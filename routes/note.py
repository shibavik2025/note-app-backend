from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Note
from app import crud, database
from schemas import NoteCreate, NoteResponse
from app.database import get_db
import traceback

from schemas.note import NoteUpdate

router = APIRouter()

# Create Note
@router.post("/notes/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    try:
        # Attempt to create a note
        created_note = crud.create_note(db=db, note_data=note)
        return created_note
    except Exception as e:
        # Log the error and raise an HTTPException
        print(f"Error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Read All Notes
@router.get("/notes/", response_model=list[NoteResponse])
def read_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()

# Read Single Note
@router.get("/notes/{note_id}", response_model=NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# Update a note
@router.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

# Delete a note
@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}