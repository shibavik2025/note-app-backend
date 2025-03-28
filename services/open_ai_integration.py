import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import openai
import re
import pytesseract


openai.api_key = os.getenv("OPENAI_API_KEY")

# Pre-trained ResNet model for feature extraction
resnet = models.resnet50(pretrained=True)
resnet.eval()

# Image transformation pipeline
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features_from_image(image: Image.Image):
    """
    Extracts features from an image using a pre-trained ResNet model and OCR for text.
    """
    # Extract visual features using ResNet (or another model)
    # Optical Character Recognition (OCR) is used to extract text from images.
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        features = resnet(image_tensor)
    
     # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image)

    # Assuming features are just the output of the last layer of ResNet
    return {"image_features": features.tolist(), "extracted_text": extracted_text.strip()}  # Return features and extracted text

def generate_seo_content_from_image_and_text(product_category, brand, features, usage, image_features_list):
    """
    Generates SEO content using both image features and textual product details.
    """
    # Convert the features dictionary into a string format suitable for the AI prompt
    features_str = "\n".join([f"{key}: {value}" for key, value in features.items() if value])

     # Combine image features and extracted text into the prompt
    image_feature_str = "\n".join([f"Image Features: {image_features['image_features']}" for image_features in image_features_list])
    image_text_str = "\n".join([f"Extracted Text from Image: {image_features['extracted_text']}" for image_features in image_features_list])

     # Ensure the extracted text is included even if it's empty or minimal as AI models work better with consistent input formats.
    if not image_text_str.strip():
        image_text_str = "No significant text extracted from image."

    prompt = f"Generate SEO optimized content for the following product:\n\n" \
             f"Product Category: {product_category}\n" \
             f"Brand: {brand}\n" \
             f"Features:\n{features_str}\n" \
             f"Usage: {usage}\n" \
             f"Additional Image Features:\n{image_feature_str}\n\n" \
             f"Extracted Text from Images:\n{image_text_str}\n\n" \
             f"Please generate the following content for SEO:\n" \
             f"1. SEO Title (include product name, key features, and specifications)\n" \
             f"2. SEO Description (detailed description with key selling points)\n" \
             f"3. Product Description (a detailed overview of the product's capabilities)\n" \
             f"4. Features (a bullet list of key features and specifications)\n"

    
    client = openai.OpenAI()  # Create a client instance
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Update to a valid model
        messages=[{"role": "system", "content": "You are an SEO expert."},
                {"role": "user", "content": prompt}],  #  Here, "role": "assistant" is automatically included by OpenAI in the response. useful to maintains context
        max_tokens=500,
        temperature=0.7
    ) 

    return response.choices[0].message.content.strip()

def parse_seo_content(response_text):
    """
    Parses the AI-generated response text into structured SEO content and combines descriptions.
    """
    # Extract SEO Title, Description, and Product Description
    seo_title = re.search(r"SEO Title:(.*)", response_text)
    seo_description = re.search(r"SEO Description:(.*)", response_text)
    product_description = re.search(r"Product Description:(.*)", response_text)
    
    # Extract Features with improved regex to handle lists and multiline text
    features = re.search(r"Features:(.*)", response_text, re.DOTALL)

    # Initialize the result dictionary
    seo_content = {
        "seo_title": seo_title.group(1).strip() if seo_title else "N/A",
        "seo_description": seo_description.group(1).strip() if seo_description else "N/A",
        "product_description": product_description.group(1).strip() if product_description else "N/A",
        "features": []
    }

    if features:
        # This will split by either newlines or commas (based on how AI generates them)
        features_text = features.group(1).strip()
        seo_content["features"] = [feature.strip() for feature in features_text.splitlines() if feature.strip()]
    
    return seo_content
