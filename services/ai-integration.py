from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load AI models (Hugging Face)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
classifier = pipeline("sentiment-analysis")

class NoteRequest(BaseModel):
    content: str

@app.post("/summarize")
def summarize(note: NoteRequest):
    summary = summarizer(note.content, max_length=50, min_length=10, do_sample=False)
    return {"summary": summary[0]["summary_text"]}

@app.post("/sentiment")
def sentiment(note: NoteRequest):
    result = classifier(note.content)
    return {"sentiment": result[0]["label"]}
