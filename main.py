from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_students():
    with open("q-fastapi.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

@app.get("/")
def root():
    return {"message": "FastAPI server is running"}

@app.get("/api")
def get_students(class_: list[str] | None = Query(default=None, alias="class")):
    students = load_students()

    if class_:
        wanted = set(class_)
        students = [s for s in students if s["class"] in wanted]

    return {
        "students": [
            {
                "studentId": int(s["studentId"]),
                "class": s["class"]
            }
            for s in students
        ]
    }




from pydantic import BaseModel
from typing import List

class SentimentRequest(BaseModel):
    sentences: List[str]


positive_words = {
    "love", "loved", "like", "liked", "happy", "great", "good",
    "excellent", "amazing", "wonderful", "fantastic", "awesome",
    "best", "enjoy", "enjoyed", "beautiful", "perfect", "success",
    "successful", "fun", "glad", "excited", "nice", "brilliant"
}

negative_words = {
    "hate", "hated", "sad", "bad", "terrible", "horrible",
    "awful", "worst", "angry", "upset", "disappointed",
    "disappointing", "poor", "fail", "failed", "failure",
    "pain", "painful", "boring", "bored", "worried", "problem",
    "problems", "difficult", "tired", "cry", "crying"
}


def get_sentiment(sentence: str) -> str:
    text = sentence.lower()

    positive_score = sum(
        1 for word in positive_words
        if word in text
    )

    negative_score = sum(
        1 for word in negative_words
        if word in text
    )

    if positive_score > negative_score:
        return "happy"
    elif negative_score > positive_score:
        return "sad"
    else:
        return "neutral"


@app.post("/sentiment")
async def sentiment(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": get_sentiment(sentence)
        })

    return {"results": results}