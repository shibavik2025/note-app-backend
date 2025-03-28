from datetime import datetime

from pydantic import BaseModel

from models.note import NoteCategory

class NoteBase(BaseModel):
    title: str
    content: str
    category:str


class NoteCreate(BaseModel):
    title: str
    content: str
    category:str


class NoteResponse(NoteBase):
    id: int
    title:str
    content:str
    category:NoteCategory
    created_at:datetime

    class Config:
        orm_mode = True



class NoteUpdate(NoteBase):
    id: int
    title:str
    content:str
    category:NoteCategory
    created_at:datetime