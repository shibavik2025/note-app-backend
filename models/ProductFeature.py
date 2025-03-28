import logging
import torch
import numpy as np
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB  # Use JSON instead of binary
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

from app.database import Base, engine, get_db

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create session factory
SessionLocal = sessionmaker(bind=engine)

class ProductFeature(Base):
    __tablename__ = 'product_features'

    id = Column(Integer, primary_key=True)
    feature_name = Column(String, nullable=False)
    feature_vector = Column(JSONB, nullable=True)  # Store as JSON instead of binary

    def set_feature_vector(self, tensor: torch.Tensor):
        """
        Converts a PyTorch tensor into a JSON array and stores it in the database.
        """
        if not isinstance(tensor, torch.Tensor):
            raise TypeError("Input must be a PyTorch tensor")

        self.feature_vector = tensor.detach().cpu().tolist()  # Store as a list

    def get_feature_vector(self):
        """
        Converts stored JSON back to a PyTorch tensor.
        """
        if not self.feature_vector:
            return None
        return torch.tensor(self.feature_vector, dtype=torch.float32)

# ------ Database Interaction ------
def store_feature_vector(db: Session = Depends(get_db)):
    """
    Stores a feature vector in the database.
    """
    try:
        feature = ProductFeature(feature_name="test_feature")
        feature.set_feature_vector(torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float32))
        db.add(feature)
        db.commit()
        db.refresh(feature)
        logger.info(f"Feature stored with ID {feature.id}")
        return {"message": "Feature stored", "id": feature.id}
    except Exception as e:
        db.rollback()
        logger.error(f"Error storing feature: {e}")
        return {"error": str(e)}

def retrieve_feature_vector(db: Session = Depends(get_db)):
    """
    Retrieves a stored feature vector from the database.
    """
    try:
        retrieved_feature = db.query(ProductFeature).filter_by(feature_name="test_feature").first()
        if retrieved_feature:
            tensor = retrieved_feature.get_feature_vector()
            logger.info(f"Recovered tensor: {tensor}")
            return tensor
        else:
            logger.warning("No feature vector found.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving feature vector: {e}")
        return None

# ------ Run Functions Manually ------
if __name__ == "__main__":
    db = SessionLocal()
    store_feature_vector(db)
    retrieve_feature_vector(db)
    db.close()
