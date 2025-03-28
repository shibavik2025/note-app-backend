import logging
import torch
import numpy as np
from sqlalchemy import Column, Integer, String, JSON
from app.database import Base, SessionLocal  # Ensure correct database session import

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=True)
    product_type = Column(String, nullable=True)  # Ensure it's JSON serializable
    features = Column(JSON, nullable=True)
    about_this_item = Column(String, nullable=True)
    seo_title = Column(String, nullable=True)
    seo_description = Column(String, nullable=True)

    def __repr__(self):
        return f"<Product(id={self.id}, product_type={self.product_type}, image_url={self.image_url})>"

    @classmethod
    def create(cls, db_session, image_url, product_type, features=None, about_this_item=None, seo_title=None, seo_description=None):
        logger.info(f"Creating new product: {product_type}")

        # Ensure product_type is JSON serializable
        if isinstance(product_type, torch.Tensor):
            product_type = product_type.detach().cpu().numpy().tolist()  # Convert tensor to list
            print(f"product_type", product_type)

        new_product = cls(
            image_url=image_url,
            product_type="product_type",  # JSON-compatible
            features=features,
            about_this_item=about_this_item,
            seo_title=seo_title,
            seo_description=seo_description,
        )

        db_session.add(new_product)
        db_session.commit()
        db_session.refresh(new_product)
        logger.info(f"New product created with ID {new_product.id}")

        return new_product


    @classmethod
    def get_by_id(cls, db_session, product_id):
        """
        Class method to fetch product by ID.
        """
        product = db_session.query(cls).filter(cls.id == product_id).first()
        if product:
            logger.info(f"Product with ID {product_id} found")
        else:
            logger.warning(f"Product with ID {product_id} not found")
        return product

