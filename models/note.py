# models.py
from datetime import datetime
import enum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base



class NoteCategory(enum.Enum):
    WORK = "Work"
    PERSONAL = "Personal"
    URGENT="Urgent"
    IDEAS = "Ideas"
    STUDY = "Study"
    FITNESS = "Fitness"
    


class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category = Column(Enum(NoteCategory), nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)  

    # Use string reference for relationship
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="notes")