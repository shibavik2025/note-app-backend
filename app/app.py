from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import create_note
from schemas import NoteResponse

app = FastAPI()

@app.post("/create_note/", response_model=NoteResponse)
def create_note_route(title: str, content: str,category:str, db: Session = Depends(get_db)):
    # Call the CRUD function to create the note
    note = create_note(title=title, content=content, category=category, db=db)
    return note
