<!-- Project Overview -->
This project generates SEO content for products by combining textual details and image features. It extracts text from images using OCR (Tesseract), uses a pre-trained ResNet model for image features, and generates SEO content using OpenAI’s GPT-3 API. The final output includes SEO title, description, product description, and features, with text extracted from images incorporated into the content.

<!-- Key Features -->
Image Processing: Uses ResNet to extract image features and Tesseract for OCR-based text extraction.
SEO Content Generation: Combines product details, image features, and extracted text to generate SEO-optimized content using OpenAI’s GPT-3.
Structured Output: Returns SEO title, description, product description, and a list of features.


Installation
<!-- Clone the repository and install dependencies: -->
pip install -r requirements.txt

<!-- Set up .env with your OpenAI API key: -->
OPENAI_API_KEY=your-api-key

<!-- Run the FastAPI app: -->
uvicorn main:app --reload
with docker: docker-compose up --build

<!-- API Usage -->
POST /generate-product-seo/
Request: Product details in JSON and image files.
Response: SEO title, SEO description, product description, and features.


<!-- Example cURL request: -->
curl -X 'POST' -F 'product_input={"product_category": "Earbuds", "brand": "Sony"}' -F 'images=@/path/to/image.jpg' http://localhost:8000/generate-product-seo/

<!-- Output Example -->
{
  "seo_title": "Sony Wireless Earbuds with 30 Hours Battery Life - Black",
  "seo_description": "Experience superior sound quality with Sony wireless earbuds...",
  "product_description": "Sony wireless earbuds offer exceptional sound quality...",
  "features": [
    "30 hours battery life",
    "Wireless",
    "Sleek black design"
  ]
}
