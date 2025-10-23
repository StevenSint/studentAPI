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

# READ - Get single student
@router.get("/{student_id}", response_model=StudentResponse,status_code = 200)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

#UPDATE - Update student
@router.put("/{student_id}", response_model=StudentResponse , status_code=200)
def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
     # Convert the Pydantic model to a dictionary.
    update_data = student_update.model_dump()
    
    if update_data.get('name') is not None:
        student.name = update_data['name']
    
    if update_data.get('age') is not None:
        student.age = update_data['age']
        
    if update_data.get('email') is not None:
        student.email = update_data['email']

    if update_data.get('major') is not None:
        student.major = update_data['major']
            
    db.commit()
    db.refresh(student)
    return student

# DELETE - Delete student
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
