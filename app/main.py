# main.py

from fastapi import FastAPI
from routes import note as note_router, user as user_router
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware



import models.note, models.user

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Include API routes
app.include_router(note_router.router)
app.include_router(user_router.router)


# This ensures models are already imported before calling create_all
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}
