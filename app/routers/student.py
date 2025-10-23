from fastapi import APIRouter ,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.student import Student
from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate


router = APIRouter(prefix = "/students")

#Create - Add new student
@router.post("/", response_model=StudentResponse,status_code = 201)
def create_student(student : StudentCreate, db: Session = Depends(get_db)):

    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail= "Email already exists!")
    

    new_student = Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

#Get - Get all student
@router.get("/", response_model=List[StudentResponse],status_code=200)
def get_all_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


