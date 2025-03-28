from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from services.ai_integration import extract_text_from_image, classify_product_type, generate_about_this_item, generate_seo_title, generate_seo_description, extract_features_from_text_and_image
import os
from models import Product
from transformers import CLIPProcessor, CLIPModel


model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

router = APIRouter()

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/")
async def upload_product(
    images: list[UploadFile] = File(...),
    product_name: str = Form(None),
    db: Session = Depends(get_db)
):
    os.makedirs("uploads", exist_ok=True)

    product_details = {
        "product_type": None,
        "features": {},
        "image_text": []
    }

    # Process each uploaded image
    for index, image in enumerate(images):
        image_path = f"uploads/{index}_{image.filename}"
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())

        # Extract text from image
        extracted_text = extract_text_from_image(image_path)
        if extracted_text:
            product_details["image_text"].append(extracted_text)

    # Use extracted text to classify the product type and extract features
    product_description = " ".join(product_details["image_text"])
    product_details["product_type"] = classify_product_type(image_path, product_description)

    # Dynamically extract features from text and image
    features = extract_features_from_text_and_image(product_description, ["screen", "battery", "processor"])  # Add image features based on analysis
    product_details["features"].update(features)

    # Generate AI-driven content
    about_this_item = generate_about_this_item(product_details["features"])
    seo_title = generate_seo_title(product_details["features"])
    seo_description = generate_seo_description(product_details["features"])

    # Save to database
    product = Product(
        image_url=", ".join([f"uploads/{image.filename}" for image in images]),
        product_type="",   # product_details["product_type"],
        features=product_details["features"],
        about_this_item=about_this_item,
        seo_title=seo_title,
        seo_description=seo_description
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "product_type": product_details["product_type"],
        "features": product_details["features"],
        "about_this_item": about_this_item,
        "seo_title": seo_title,
        "seo_description": seo_description
    }
