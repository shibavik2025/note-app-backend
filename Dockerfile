# Use official Python image
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Install dependencies first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application (after installing dependencies)
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with hot reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
