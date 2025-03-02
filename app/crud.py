from models.note import NoteCategory
from schemas.note import NoteResponse
from sqlalchemy.orm import Session

from models import Note
from schemas import NoteCreate
from fastapi import Depends, FastAPI, HTTPException
from app.database import get_db
import logging

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

# Create Note
def create_note(note_data: NoteCreate, db: Session):
    try:   
        category_enum = NoteCategory(note_data.category)
        # Create a new Note object using the provided data
        new_note = Note(
            title=note_data.title,
            content=note_data.content,
            category=category_enum
        )
        
        # Add the new note to the session and commit
        db.add(new_note)
        db.commit()
        db.refresh(new_note)  # Refresh the object to get the generated id
        # Return a valid response
        return NoteResponse(id=new_note.id, 
                            title=new_note.title, 
                            content=new_note.content,
                            category=new_note.category, 
                            created_at=new_note.created_at
                        )


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    
# Read All Notes
def get_notes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Note).offset(skip).limit(limit).all()

# Read Single Note
def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()

# Update Note
def update_note(db: Session, note_id: int, note: NoteCreate):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db_note.title = note.title
        db_note.content = note.content
        db_note.category = note.category
        db.commit()
        db.refresh(db_note)
    return db_note

# Delete Note
def delete_note(db: Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note
