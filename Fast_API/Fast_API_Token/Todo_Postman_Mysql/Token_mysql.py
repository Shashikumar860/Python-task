# ============================================================
# 🔐 FastAPI TODO App + JWT Authentication + MySQL
# ============================================================

# ============================================================
# 🚀 INSTALL REQUIRED PACKAGES
# ============================================================

'''
pip install fastapi uvicorn sqlalchemy pymysql python-jose
'''

# ============================================================
# 📦 IMPORTS
# ============================================================

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, ConfigDict
from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean
)

from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ============================================================
# 🚀 FASTAPI APP
# ============================================================

app = FastAPI()

# ============================================================
# 🛢️ MYSQL DATABASE CONFIG
# ============================================================

'''
CHANGE THESE VALUES

username = root
password = yourpassword
database = todo_db
'''

DATABASE_URL = "mysql+pymysql://root:root@localhost/todo_token_db"

# ------------------------------------------------------------

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ============================================================
# 🗂️ DATABASE MODEL
# ============================================================

class TodoDB(Base):

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255))

    completed = Column(Boolean, default=False)

# ------------------------------------------------------------

# Create tables
Base.metadata.create_all(bind=engine)

# ============================================================
# 🔐 JWT CONFIGURATION
# ============================================================

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE = timedelta(minutes=5)

# ============================================================
# 🧾 Pydantic Models
# ============================================================

class Todo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool = False

# ------------------------------------------------------------

class Login(BaseModel):

    username: str
    password: str

# ============================================================
# 🛢️ DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ============================================================
# 🔐 CREATE JWT TOKEN
# ============================================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

# ============================================================
# 🔐 TOKEN VALIDATION
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ------------------------------------------------------------

def verify_token(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token expired or invalid"
        )

# ============================================================
# 🏠 HOME API
# ============================================================

@app.get("/")
def home():

    return {
        "message": "FastAPI + JWT + MySQL CRUD 🚀"
    }

# ============================================================
# 🔐 LOGIN API
# ============================================================

@app.post("/login")
def login(user: Login):

    '''
    Username = admin
    Password = admin123
    '''

    if user.username != "admin" or user.password != "admin123":

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": "10 minutes"
    }

# ============================================================
# ✅ CREATE TODO
# ============================================================

@app.post("/todos")
def create_todo(
    todo: Todo,
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):

    # Check duplicate ID
    existing = db.query(TodoDB).filter(
        TodoDB.id == todo.id
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="ID already exists"
        )

    new_todo = TodoDB(
        id=todo.id,
        title=todo.title,
        completed=todo.completed
    )

    db.add(new_todo)

    db.commit()

    db.refresh(new_todo)

    return {
        "message": "Todo created successfully",
        "data": new_todo
    }

# ============================================================
# ✅ GET ALL TODOS
# ============================================================

@app.get("/todos")
def get_all_todos(
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):

    todos = db.query(TodoDB).all()

    return {
        "count": len(todos),
        "data": todos
    }

# ============================================================
# ✅ GET TODO BY ID
# ============================================================

@app.get("/todos/{todo_id}")
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):

    todo = db.query(TodoDB).filter(
        TodoDB.id == todo_id
    ).first()

    if not todo:

        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return todo

# ============================================================
# ✅ UPDATE TODO
# ============================================================

@app.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    updated: Todo,
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):

    todo = db.query(TodoDB).filter(
        TodoDB.id == todo_id
    ).first()

    if not todo:

        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    todo.title = updated.title

    todo.completed = updated.completed

    db.commit()

    db.refresh(todo)

    return {
        "message": "Todo updated successfully",
        "data": todo
    }

# ============================================================
# ✅ DELETE TODO
# ============================================================

@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):

    todo = db.query(TodoDB).filter(
        TodoDB.id == todo_id
    ).first()

    if not todo:

        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    db.delete(todo)

    db.commit()

    return {
        "message": "Todo deleted successfully"
    }

# ============================================================
# 🌐 RUN SERVER
# ============================================================

'''
uvicorn main:app --reload
'''

# ============================================================
# 🌐 MYSQL DATABASE CREATE
# ============================================================

'''
Open MySQL and run:

CREATE DATABASE todo_db;
'''

# ============================================================
# 🌐 SWAGGER DOCS
# ============================================================

'''
http://127.0.0.1:8000/docs
'''

# ============================================================
# 🔥 LOGIN DETAILS
# ============================================================

'''
Username: admin
Password: admin123
'''

# ============================================================
# 🔥 HOW TO USE IN POSTMAN
# ============================================================

'''
1. POST /login

{
    "username": "admin",
    "password": "admin123"
}

2. Copy access_token

3. In Postman:
   Authorization
   -> Bearer Token
   -> Paste token

4. Access protected APIs
'''