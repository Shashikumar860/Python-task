# ============================================================
# FastAPI TODO App (CRUD) - SQLite Database Version
# ============================================================
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# ------------------------------------------------------------
# Create FastAPI App
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# Database Configuration
# ------------------------------------------------------------
url="sqlite:///./Sms.db"
engine=create_engine(
    url,connect_args={"check_same_thread":False}
)
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()
# ------------------------------------------------------------
# 🧱 Database Model (Table)
# ------------------------------------------------------------
class studentDB(Base):
    __tablename__="Student"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    course = Column(String)
    marks = Column(Integer)
    

# Create table
Base.metadata.create_all(bind=engine)

# ------------------------------------------------------------
# 🧾 Pydantic Schema
# ------------------------------------------------------------
class Student(BaseModel):
    id:int
    name:str
    age:int
    course:str
    marks:int
    model_config = ConfigDict(from_attributes=True)

# ------------------------------------------------------------
# 🔌 Dependency (DB Session)
# ------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------------------------------
# 🏠 Home Route
# ------------------------------------------------------------
@app.get("/")
def home():
    return {"message": "FastAPI Sms with DB 🚀"}
# ------------------------------------------------------------
# ✅ 1. CREATE TODO
# ------------------------------------------------------------
@app.post("/student")
def create_student(stu: Student, db: Session = Depends(get_db)):
    existing = db.query(studentDB).filter(studentDB.id == stu.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="ID already exists")

    new_stu = studentDB(
        id=stu.id,
        name=stu.name,
        age=stu.age,
        course=stu.course,
        marks=stu.marks
    )

    db.add(new_stu)
    db.commit()
    db.refresh(new_stu)

    return {"message": "Student created", "data": new_stu}

# ------------------------------------------------------------
# ✅ 2. READ ALL TODOS
# ------------------------------------------------------------
@app.get("/student")
def get_all_studs(db: Session = Depends(get_db)):
    stud = db.query(studentDB).all()
    return {"count": len(stud), "data": stud}

# ------------------------------------------------------------
# ✅ 3. READ SINGLE TODO
# ------------------------------------------------------------
@app.get("/student/{stu_id}")
def get_todo(stu_id: int, db: Session = Depends(get_db)):
    stud = db.query(studentDB).filter(studentDB.id == stu_id).first()

    if not stud:
        raise HTTPException(status_code=404, detail="Student not found")

    return stud

# ------------------------------------------------------------
# ✅ 4. UPDATE TODO
# ------------------------------------------------------------
@app.put("/student/{stu_id}")
def update_todo(stu_id: int, updated: Student, db: Session = Depends(get_db)):
    stud = db.query(studentDB).filter(studentDB.id == stu_id).first()

    if not stud:
        raise HTTPException(status_code=404, detail="Student not found")

    stud.name = updated.name
    stud.age = updated.age
    stud.course = updated.course
    stud.marks = updated.marks

    db.commit()
    db.refresh(stud)

    return {"message": "Updated successfully", "data": stud}

# ------------------------------------------------------------
# ✅ 5. DELETE TODO
# ------------------------------------------------------------
@app.delete("/student/{stu_id}")
def delete_todo(stu_id: int, db: Session = Depends(get_db)):
    stud = db.query(studentDB).filter(studentDB.id == stu_id).first()

    if not stud:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(stud)
    db.commit()

    return {"message": "Deleted successfully"}