from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load data from CSV
students_data = []
with open("q-fastapi.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        students_data.append({"studentId": int(row["studentId"]), "class": row["class"]})

# API endpoint
@app.get("/api")
def get_students(class_param: list[str] = Query(default=[])):
    if class_param:
        filtered_students = [
            student for student in students_data if student["class"] in class_param
        ]
        return {"students": filtered_students}
    return {"students": students_data}
