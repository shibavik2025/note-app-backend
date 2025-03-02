from fastapi import FastAPI


# Create FastAPI instance
app = FastAPI()


# Define Root Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Notes API"}
