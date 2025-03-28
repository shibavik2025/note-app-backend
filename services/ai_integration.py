import os
import pytesseract
from PIL import Image
import json
import logging
from transformers import pipeline, CLIPProcessor, CLIPModel, GPT2LMHeadModel, GPT2Tokenizer

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load pre-trained models (CLIP model for image classification)
logger.info("Loading CLIP model and processor...")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
logger.info("CLIP model and processor loaded successfully.")

# Load GPT-2 model and tokenizer for text generation (free alternative to OpenAI's GPT)
logger.info("Loading GPT-2 model and tokenizer...")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
logger.info("GPT-2 model and tokenizer loaded successfully.")

# OCR: Extract text from image using Tesseract
def extract_text_from_image(image_path):
    logger.info(f"Extracting text from image: {image_path}")
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    
    if extracted_text:
        logger.info(f"Extracted text: {extracted_text[:100]}...")  # Log first 100 characters for brevity
    else:
        logger.warning("No text extracted from the image.")
    
    return extracted_text.strip() if extracted_text else None

# Function to classify product type based on image and description
def classify_product_type(image_path: str, product_description: str):
    logger.info(f"Classifying product type for image: {image_path} with description: {product_description}")
    
    try:
        image = Image.open(image_path)  # Load image correctly
        inputs = processor(
            text=[product_description],  # Ensure this is formatted correctly
            images=[image], 
            return_tensors="pt"
        )
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)  # Convert to probabilities

        logger.info(f"Product classification probabilities: {probs}")
        return probs
    except Exception as e:
        logger.error(f"Error during classification: {str(e)}")
        raise

# Generate "About this item" section using GPT-2 (free AI alternative to OpenAI)
def generate_about_this_item(features):
    logger.info(f"Generating 'About this item' description for features: {features}")
    prompt = f"Generate an engaging product description for: {features}"

    try:
        inputs = gpt2_tokenizer.encode(prompt, return_tensors="pt")
        outputs = gpt2_model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, temperature=0.7)
        generated_text = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        logger.info(f"Generated 'About this item': {generated_text[:100]}...")  # Log first 100 characters
        return generated_text.strip()
    except Exception as e:
        logger.error(f"Error generating 'About this item': {str(e)}")
        raise

# Generate SEO title
def generate_seo_title(features):
    logger.info(f"Generating SEO title for features: {features}")
    title = f"{features.get('brand', 'Generic')} {features.get('product_type', 'Product')} - {features.get('battery_life', 'Long-lasting')}, {features.get('bluetooth_version', 'Latest Bluetooth')}, {features.get('noise_control', 'Noise Cancellation')}"
    logger.info(f"Generated SEO title: {title}")
    return title

# Generate SEO description using GPT-2 for a free alternative
def generate_seo_description(features):
    logger.info(f"Generating SEO description for features: {features}")
    prompt = f"Generate an SEO-optimized product description for: {json.dumps(features)}"
    
    try:
        inputs = gpt2_tokenizer.encode(prompt, return_tensors="pt")
        outputs = gpt2_model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, temperature=0.7)
        seo_description = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        logger.info(f"Generated SEO description: {seo_description[:100]}...")  # Log first 100 characters
        return seo_description.strip()
    except Exception as e:
        logger.error(f"Error generating SEO description: {str(e)}")
        raise

# Function to dynamically extract features from text and image
def extract_features_from_text_and_image(extracted_text: str, image_features: list):
    logger.info(f"Extracting features from text: {extracted_text[:100]}... and image features: {image_features}")
    features = {}

    # Use Hugging Face's NER pipeline for feature extraction (free alternative to other APIs)
    nlp_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
    
    try:
        ner_results = nlp_pipeline(extracted_text)
        logger.info(f"Named Entity Recognition results: {ner_results}")
        
        # Map the results to relevant product features
        for entity in ner_results:
            if entity['entity'] == 'B-LOC':  # Extract brand information
                features["brand"] = entity['word']
            elif entity['entity'] == 'B-MISC':  # Extract product-specific information like model number
                features["model"] = entity['word']

        # Based on the image (features detected from image, e.g., screen size)
        if 'screen' in image_features:
            features['screen_size'] = "Extracted from Image"

        logger.info(f"Extracted features: {features}")
        return features
    except Exception as e:
        logger.error(f"Error during feature extraction: {str(e)}")
        raise
