from fastapi import FastAPI
from routes import router

app = FastAPI()

# Register Routes
app.include_router(router)

# ================================================================
# App Run: py -m uvicorn main:app --reload
# ================================================================