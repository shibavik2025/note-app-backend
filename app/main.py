import json

from typing import List

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from PIL import Image
import io
from fastapi import FastAPI, Form, Depends, File, UploadFile, HTTPException
from app.database import Base, SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware


import models.ProductFeature, models.product
from schemas.product_input import ProductInput
from app.database import get_db
from schemas.product_input import ProductInput
from services.open_ai_integration import generate_seo_content_from_image_and_text, extract_features_from_image, parse_seo_content

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# # Include API routes
# app.include_router(router)


# This ensures models are already imported before calling create_all
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate-product-seo/")
async def generate_product_seo(
    product_input: str = Form(...),
    images: List[UploadFile] = File(...)
):
    try:
        # Convert product_input (JSON string) into a dictionary
        product_input_dict = json.loads(product_input)

        # Validate the JSON using Pydantic
        product_data = ProductInput(**product_input_dict)

        # Extract fields
        product_category = product_data.product_category
        brand = product_data.brand
        features = product_data.features.dict()  # Convert Pydantic model to dict
        usage = product_data.usage

        print(f"Received Product Input: {product_data}")
        print(f"Received {len(images)} images")

        # Validate image count & size
        MAX_IMAGES = 5  # Allow up to 5 images
        MAX_SIZE = 5 * 1024 * 1024  # Max 5 MB per image

        if len(images) > MAX_IMAGES:
            raise HTTPException(status_code=400, detail="Too many images. Max 5 images allowed.")

        image_features_list = []

        for image in images:
            # Validate file type
            if image.content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(status_code=400, detail="Only JPEG and PNG images are allowed.")

            # Read image in-memory (efficiently)
            image.file.seek(0)  # Reset pointer
            img = Image.open(io.BytesIO(image.file.read()))

            # Extract image features (replace with actual feature extraction)
            image_features = extract_features_from_image(img)
            image_features_list.append(image_features)

        # Generate SEO content
        seo_content = generate_seo_content_from_image_and_text(
            product_category, brand, features, usage, image_features_list
        )

        # Parse the response text into structured SEO content
        seo_content = parse_seo_content(seo_content)

        return {"message": "SEO content generated successfully", "seo_content": seo_content}


    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in product_input.")

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
