# Use official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app


# Install system dependencies including Tesseract-OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --timeout=300 --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Wait for PostgreSQL to be ready before running migrations & starting the app
# ENTRYPOINT ["sh", "-c", "until pg_isready -h database -p 5432 -U admin; do echo 'Waiting for database...'; sleep 2; done; alembic upgrade head && exec gunicorn -w $(nproc) -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]