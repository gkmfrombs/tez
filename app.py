from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change as needed for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data from the CSV file
def load_students_data():
    students = []
    try:
        with open('students.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append({"studentId": int(row["studentId"]), "class": row["class"]})
    except FileNotFoundError:
        print("Error: 'students.csv' not found. Make sure the file exists in the current directory.")
    return students

students_data = load_students_data()

@app.get("/api")
def get_students(class_: list[str] = Query(default=None, alias="class")):
    """
    Get students data.
    If the 'class' query parameter is provided, filter by the specified classes.
    """
    if class_:
        filtered_students = [student for student in students_data if student["class"] in class_]
        return JSONResponse(content={"students": filtered_students})
    return JSONResponse(content={"students": students_data})
