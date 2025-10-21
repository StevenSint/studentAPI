from fastapi import APIRouter ,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.student import Student
from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate


router = APIRouter(prefix = "/students")

#Create - Add new student
@router.post("/", response_model=StudentResponse,status_code = 201)
def create_student(student : StudentCreate, db: Session = Depends(get))

    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail= "Email already exists!")
    

    new_student = Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

