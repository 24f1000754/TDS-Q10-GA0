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
    "successful", "fun", "glad", "excited", "nice", "brilliant",
    "pleasant", "pleased", "delighted", "joy", "joyful", "win",
    "won", "winning", "helpful", "impressive", "positive",
    "satisfied", "satisfying", "recommend"
}

negative_words = {
    "hate", "hated", "dislike", "disliked", "sad", "bad", "terrible",
    "horrible", "awful", "worst", "angry", "upset", "disappointed",
    "disappointing", "poor", "fail", "failed", "failure", "pain",
    "painful", "boring", "bored", "worried", "problem", "problems",
    "difficult", "tired", "cry", "crying", "unhappy", "unpleasant",
    "annoyed", "annoying", "frustrated", "frustrating", "regret",
    "regretted", "wrong", "negative", "horrible", "disaster",
    "disastrous", "useless", "rude", "broken", "loss", "lost",
    "losing", "confusing", "confused", "fear", "afraid", "scared",
    "dislike", "disgusting", "disgusted", "mad"
}


def get_sentiment(sentence: str) -> str:
    text = sentence.lower()

    # Handle common negative phrases / negation
    negative_phrases = [
        "not good",
        "not great",
        "not happy",
        "not nice",
        "not enjoyable",
        "not enjoyable",
        "do not like",
        "don't like",
        "did not like",
        "didn't like",
        "do not enjoy",
        "don't enjoy",
        "did not enjoy",
        "didn't enjoy",
        "not satisfied",
        "not pleased",
        "not impressive",
        "not perfect",
        "never good",
        "never great",
        "no good"
    ]

    for phrase in negative_phrases:
        if phrase in text:
            return "sad"

    # Handle common positive phrases
    positive_phrases = [
        "very good",
        "very nice",
        "really good",
        "really great",
        "very happy",
        "really happy",
        "love this",
        "love it",
        "highly recommend"
    ]

    for phrase in positive_phrases:
        if phrase in text:
            return "happy"

    # Remove punctuation and tokenize
    words = re.findall(r"\b[a-z]+\b", text)

    positive_score = 0
    negative_score = 0

    for i, word in enumerate(words):
        # Check whether word is negated
        previous_words = words[max(0, i-3):i]

        negated = any(
            w in {"not", "never", "no", "don't", "didn't", "doesn't",
                  "isn't", "wasn't", "can't", "cannot"}
            for w in previous_words
        )

        if word in positive_words:
            if negated:
                negative_score += 1
            else:
                positive_score += 1

        elif word in negative_words:
            if negated:
                positive_score += 1
            else:
                negative_score += 1

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