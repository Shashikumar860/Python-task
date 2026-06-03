# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# -----------------------------
# Student Model
# -----------------------------
class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str
    marks: float


# Temporary storage using Python list
students = []


# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "Student Management System API"}


# -----------------------------
# Add New Student
# POST Method
# -----------------------------
@app.post("/students")
def add_student(student: Student):
    # Check if ID already exists
    for s in students:
        if s["id"] == student.id:
            raise HTTPException(status_code=400, detail="Student ID already exists")

    students.append(student.dict())

    return {
        "message": "Student added successfully",
        "student": student
    }


# -----------------------------
# Get All Students
# GET Method
# -----------------------------
@app.get("/students")
def get_students():
    return {
        "students": students
    }


# -----------------------------
# Get Student By ID
# GET Method
# -----------------------------
@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")


# -----------------------------
# Update Student
# PUT Method
# -----------------------------
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    for index, student in enumerate(students):

        if student["id"] == student_id:
            students[index] = updated_student.dict()

            return {
                "message": "Student updated successfully",
                "student": updated_student
            }

    raise HTTPException(status_code=404, detail="Student not found")


# -----------------------------
# Delete Student
# DELETE Method
# -----------------------------
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student["id"] == student_id:
            deleted_student = students.pop(index)

            return {
                "message": "Student deleted successfully",
                "student": deleted_student
            }

    raise HTTPException(status_code=404, detail="Student not found")