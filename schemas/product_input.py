# schemas/product_input.py
from pydantic import BaseModel
from typing import List, Optional

class ProductFeatures(BaseModel):
    screen_size: Optional[str] = None
    processor: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    color: Optional[str] = None
    battery_life: Optional[str] = None
    special_features: Optional[List[str]] = []

class ProductInput(BaseModel):
    product_category: str
    brand: str
    features: ProductFeatures
    usage: str