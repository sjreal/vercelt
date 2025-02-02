from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
from pathlib import Path
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load data from CSV with error handling
students_data = []
try:
    csv_path = Path(__file__).parent / "data" / "q-fastapi.csv"
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                students_data.append({
                    "studentId": int(row["studentId"]),
                    "class": row["class"]
                })
            except (ValueError, KeyError) as e:
                print(f"Error processing row: {row}, Error: {e}")
except FileNotFoundError:
    print("CSV file not found")

@app.get("/api")
async def get_students(class_param: list[str] = Query(default=[])):
    if not students_data:
        raise HTTPException(status_code=500, detail="Data not available")
    
    if class_param:
        filtered_students = [
            student for student in students_data 
            if student["class"] in class_param
        ]
        return {"students": filtered_students}
    return {"students": students_data}
