from fastapi import FastAPI
from app.database import engine, Base

from app.routers import student

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    version="1.0.0"
)

app.include_router(student.router)

@app.get("/")
def root():
    return {"message": "Student API - Go to /docs"}