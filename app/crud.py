
from models.product import Product
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException
from app.database import get_db
import logging

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
