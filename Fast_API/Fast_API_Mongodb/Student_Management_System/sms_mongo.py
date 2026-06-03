# ============================================================
# 📝 FastAPI STUDENT MANAGEMENT App - MongoDB Atlas + MongoEngine
# pip install fastapi uvicorn mongoengine pymongo
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongoengine import connect, Document, IntField, StringField, BooleanField

# ------------------------------------------------------------
# 🚀 FastAPI App
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# 🌐 MongoDB Atlas Connection
# ------------------------------------------------------------
MONGO_URL = "mongodb+srv://shashikumarv860_db_user:shashi2113@shashi.p3tis2s.mongodb.net/student_DB?retryWrites=true&w=majority"
'''
mongodb+srv://username:password@clustername.xxxxx.mongodb.net/student_db?retryWrites=true&w=majority
│              │        │        │                              │
│              │        │        │                              └── Database name
│              │        │        └──────────────────────────────── Cluster URL
│              │        └───────────────────────────────────────── Password
│              └────────────────────────────────────────────────── Username
└───────────────────────────────────────────────────────────────── MongoDB protocol
'''
connect(host=MONGO_URL)

# ------------------------------------------------------------
# 🧱 MongoDB Model (Like SQLAlchemy Model)
# ------------------------------------------------------------
class StudentDB(Document):
    id = IntField(primary_key=True)
    name = StringField()
    age = IntField()
    course = StringField()
    marks = IntField()
    completed = BooleanField(default=False)

    meta = {
        "collection": "students"
    }

# ------------------------------------------------------------
# 🧾 Pydantic Schema
# ------------------------------------------------------------
class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str
    marks: int
    completed: bool = False

# ------------------------------------------------------------
# 🏠 Home Route
# ------------------------------------------------------------
@app.get("/")
def home():
    return {"message": "FastAPI + MongoDB Atlas 🚀"}

# ------------------------------------------------------------
# ✅ 1. CREATE STUDENT
# ------------------------------------------------------------
@app.post("/POST/students")
def create_student(student: Student):

    # Check duplicate ID
    existing = StudentDB.objects(id=student.id).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="ID already exists"
        )

    new_student = StudentDB(
        id=student.id,
        name=student.name,
        age=student.age,
        course=student.course,
        marks=student.marks,
        completed=student.completed
    )

    new_student.save()

    return {
        "message": "Student created",
        "data": student
    }

# ------------------------------------------------------------
# ✅ 2. READ ALL STUDENTS
# ------------------------------------------------------------
@app.get("/GET/students")
def get_all_students():

    students = StudentDB.objects()

    data = []

    for student in students:
        data.append({
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "course": student.course,
            "marks": student.marks,
            "completed": student.completed
        })

    return {
        "count": len(data),
        "data": data
    }

# ------------------------------------------------------------
# ✅ 3. READ SINGLE STUDENT
# ------------------------------------------------------------
@app.get("/GET/students/{stdnt_id}")
def get_individual_student(student_id: int):

    student = StudentDB.objects(id=student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "course": student.course,
        "marks": student.marks,
        "completed": student.completed
    }

# ------------------------------------------------------------
# ✅ 4. UPDATE STUDENT
# ------------------------------------------------------------
@app.put("/PUT/students/{student_id}")
def update_individual_student(student_id: int, updated: Student):

    student = StudentDB.objects(id=student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = updated.name
    student.age = updated.age
    student.course = updated.course
    student.marks = updated.marks
    student.completed = updated.completed

    student.save()

    return {
        "message": "Student updated successfully"
    }

# ------------------------------------------------------------
# ✅ 5. DELETE STUDENT
# ------------------------------------------------------------
@app.delete("/DELETE/students/{student_id}")
def delete_individual_student(student_id: int):

    student = StudentDB.objects(id=student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.delete()

    return {
        "message": "Student deleted successfully"
    }