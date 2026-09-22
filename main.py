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
